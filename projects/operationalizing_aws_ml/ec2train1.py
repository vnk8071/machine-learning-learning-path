import os
import argparse

import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.models as models
import torchvision.transforms as transforms

from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True


class DogClassification:
    IMG_SIZE = (224, 224)
    MEAN = [0.485, 0.456, 0.406]
    STD = [0.229, 0.224, 0.225]

    def __init__(self, args):
        self.dataset_directory = args.data
        self.train_data_path = os.path.join(self.dataset_directory, 'train')
        self.validation_data_path = os.path.join(self.dataset_directory, 'valid')
        self.test_data_path = os.path.join(self.dataset_directory, 'test')
        self.batch_size = args.batch_size
        self.lr = args.lr
        self.model_output_dir = args.model_output_dir

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

        test_data_transform = transforms.Compose([
            transforms.Resize(size=self.IMG_SIZE),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=self.MEAN,
                std=self.STD
            )
        ])

        train_image_datasets = torchvision.datasets.ImageFolder(
            root=self.train_data_path,
            transform=train_data_transform
        )
        train_data_loader = torch.utils.data.DataLoader(
            train_image_datasets,
            batch_size=self.batch_size,
            shuffle=True
        )

        validation_image_datasets = torchvision.datasets.ImageFolder(
            root=self.validation_data_path,
            transform=test_data_transform,
        )
        validation_data_loader = torch.utils.data.DataLoader(
            validation_image_datasets,
            batch_size=self.batch_size,
            shuffle=False
        )

        test_image_datasets = torchvision.datasets.ImageFolder(
            root=self.test_data_path,
            transform=test_data_transform
        )
        test_data_loader = torch.utils.data.DataLoader(
            test_image_datasets,
            batch_size=self.batch_size,
            shuffle=False
        )
        return train_data_loader, validation_data_loader, test_data_loader

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
            Using a Resnet18 pretrained model
        '''
        model = models.resnet18(pretrained=True)

        for param in model.parameters():
            param.requires_grad = False

        model.fc = nn.Sequential(
            nn.Linear(in_features=512, out_features=128),
            nn.ReLU(inplace=True),
            nn.Linear(in_features=128, out_features=133)
        )
        return model

    def train(
        self,
        model,
        train_loader,
        validation_loader,
        criterion,
        optimizer,
        device,
        epochs=50,
    ):
        '''
            Script training
        '''
        best_loss = 1e6
        image_dataset = {'train': train_loader, 'valid': validation_loader}
        loss_counter = 0

        for epoch in range(epochs):
            print(f"Epoch: {epoch}")
            for phase in ['train', 'valid']:
                if phase == 'train':
                    model.train()
                else:
                    model.eval()
                running_loss = 0.0
                running_corrects = 0

                for inputs, labels in image_dataset[phase]:
                    inputs = inputs.to(device)
                    labels = labels.to(device)
                    outputs = model(inputs)
                    loss = criterion(outputs, labels)

                    if phase == 'train':
                        optimizer.zero_grad()
                        loss.backward()
                        optimizer.step()

                    _, preds = torch.max(outputs, 1)
                    running_loss += loss.item() * inputs.size(0)
                    running_corrects += torch.sum(preds == labels.data)

                epoch_loss = running_loss // len(image_dataset[phase])
                epoch_acc = running_corrects // len(image_dataset[phase])

                if phase == 'valid':
                    if epoch_loss < best_loss:
                        best_loss = epoch_loss
                    else:
                        loss_counter += 1

                print('{} loss: {:.4f}, acc: {:.4f}, best loss: {:.4f}'.format(
                    phase,
                    epoch_loss,
                    epoch_acc,
                    best_loss)
                )
            if loss_counter == 1:
                break
            if epoch == 0:
                break
        return model

    def test(self, model, test_loader, criterion, device):
        '''
            Script testing
        '''
        model.eval()
        running_loss = 0
        running_corrects = 0

        for inputs, labels in test_loader:
            inputs = inputs.to(device)
            labels = labels.to(device)
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            _, preds = torch.max(outputs, 1)
            running_loss += loss.item() * inputs.size(0)
            running_corrects += torch.sum(preds == labels.data)

        total_loss = running_loss // len(test_loader)
        total_acc = running_corrects.double() // len(test_loader)

        print(f"Testing Loss: {total_loss}")
        print(f"Testing Accuracy: {total_acc}")

    def save_model(self, model):
        '''
            Save model
        '''
        model_path = os.path.join(
            self.model_output_dir,
            "model.pth"
        )
        torch.save(model.cpu().state_dict(), model_path)


def main(args):
    '''
        Main script
    '''
    classifier = DogClassification(args)
    train_loader, validation_loader, test_loader = classifier.create_data_loader()
    model, loss_criterion, optimizer, device = classifier.setup_training()

    model = classifier.train(
        model=model,
        train_loader=train_loader,
        validation_loader=validation_loader,
        criterion=loss_criterion,
        optimizer=optimizer,
        device=device,
        epochs=args.epochs
    )
    classifier.test(model, test_loader, loss_criterion, device)

    classifier.save_model(model)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--batch-size",
        type=int,
        default=2,
        help="input batch size for training",
    )
    parser.add_argument(
        "--lr", type=float, default=1e-4, help="learning rate"
    )
    parser.add_argument(
        "--epochs", type=int, default=5, help="number of epochs to train",
    )
    parser.add_argument(
        "--model-output-dir",
        type=str,
        default="TrainedModels"
    )
    parser.add_argument(
        "--data",
        type=str,
        default="dogImages"
    )
    args = parser.parse_args()

    main(args)
