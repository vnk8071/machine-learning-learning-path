import torch


class CFG:
    DATA_DIR = './data'
    MEAN = (0.5, 0.5, 0.5)
    STD = (0.225, 0.225, 0.225)
    BATCH_SIZE = 32
    NUM_WORKERS = 2
    LEARNING_RATE = 0.05
    CLASSES = (
        'plane',
        'car',
        'bird',
        'cat',
        'deer',
        'dog',
        'frog',
        'horse',
        'ship',
        'truck')
    DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    EPOCHS = 20
