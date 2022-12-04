from src.data.dunnhumby import run_preprocess
import hydra
from omegaconf import DictConfig

@hydra.main(version_base=None, config_path="cfg", config_name="env1_cfg")
def preprocess(cfg: DictConfig):
    run_preprocess(cfg)

if __name__ == '__main__':
    preprocess()

