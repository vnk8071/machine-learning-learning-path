from module.train_model import training
import hydra
from omegaconf import DictConfig


@hydra.main(config_path=".", config_name="config", version_base="1.2")
def main(config: DictConfig):
    training(config)


if __name__ == "__main__":
    main()
