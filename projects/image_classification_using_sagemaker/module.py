import os
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.models as models
import torchvision.transforms as transforms
import smdebug.pytorch as smd

from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True


class DogClassification:
    IMG_SIZE = (224, 224)
    MEAN = [0.485, 0.456, 0.406]
    STD = [0.229, 0.224, 0.225]

    def __init__(self, args):
        self.train_dataset_directory = args.train_dataset_directory
        self.test_dataset_directory = args.test_dataset_directory
        self.batch_size = args.batch_size
        self.lr = args.lr
        self.target_class_count = args.target_class_count

    def create_data_loader(self):
        '''
            Transform images into data loaders
        '''
        train_data_transform = transforms.Compose([
            transforms.Resize(size=self.IMG_SIZE),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=self.MEAN,
                std=self.STD
            )
        ])

        train_image_datasets = torchvision.datasets.ImageFolder(
            root=self.train_dataset_directory,
            transform=train_data_transform
        )

        train_data_loader = torch.utils.data.DataLoader(
            train_image_datasets,
            batch_size=self.batch_size,
            shuffle=True
        )

        test_data_transform = transforms.Compose([
            transforms.Resize(size=self.IMG_SIZE),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=self.MEAN,
                std=self.STD
            )
        ])

        test_image_datasets = torchvision.datasets.ImageFolder(
            root=self.test_dataset_directory,
            transform=test_data_transform
        )

        test_data_loader = torch.utils.data.DataLoader(
            test_image_datasets,
            batch_size=self.batch_size,
            shuffle=False
        )
        return train_data_loader, test_data_loader

    def setup_training(self):
        '''
            Setup training
        '''
        device = torch.device(
            'cuda:0' if torch.cuda.is_available() else 'cpu'
        )

        model = self.get_model()
        model = model.to(device)

        loss_criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(model.parameters(), lr=self.lr)
        return model, loss_criterion, optimizer, device

    def get_model(self):
        '''
            Using a VGG16 pretrained model
        '''
        model = models.vgg16(pretrained=True)
        for param in model.parameters():
            param.requires_grad = False

        num_features = model.classifier[-1].in_features
        features = list(model.classifier.children())[:-1]
        features.extend([nn.Linear(num_features, self.target_class_count)])
        model.classifier = nn.Sequential(*features)

        return model

    def train(
            self,
            train_loader,
            criterion,
            optimizer,
            epoch,
            device,
            hook=None):
        '''
            Script training
        '''
        self.model = self.get_model()
        self.model.train()
        if hook is not None:
            hook.set_mode(smd.modes.TRAIN)

        for batch_idx, (data, target) in enumerate(train_loader):
            data = data.to(device)
            target = target.to(device)
            optimizer.zero_grad()
            output = self.model(data)
            loss = criterion(output, target)
            loss.backward()
            optimizer.step()
            print(
                "Train epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.5f}".format(
                    epoch,
                    batch_idx * len(data),
                    len(train_loader.dataset),
                    100.0 * batch_idx / len(train_loader),
                    loss.item(),
                )
            )

    def test(self, test_loader, criterion, device, hook=None):
        '''
            Script testing
        '''
        self.model = self.get_model()
        self.model.eval()
        if hook is not None:
            hook.set_mode(smd.modes.EVAL)
        test_loss = 0
        correct = 0
        with torch.no_grad():
            for data, target in test_loader:
                data = data.to(device)
                target = target.to(device)
                output = self.model(data)
                test_loss += criterion(output, target).item()
                pred = output.max(1, keepdim=True)[1]
                correct += pred.eq(target.view_as(pred)).sum().item()

        test_loss /= len(test_loader.dataset)
        print(
            "Test set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n".format(
                test_loss, correct,
                len(test_loader.dataset),
                100.0 * correct / len(test_loader.dataset)
            )
        )

    def save_model(self):
        '''
            Save model
        '''
        model_path = os.path.join(
            self.model_output_dir,
            "model.pth"
        )
        torch.save(self.model.state_dict(), model_path)
