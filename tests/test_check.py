import os
import pandas as pd
import sys
sys.path.append('../')
from hydra import initialize, compose
from src.data.dunnhumby import run_preprocess

def test():
    with initialize(version_base=None, config_path="../cfg"):
        cfg = compose(config_name="env1_cfg")
    # check raw data
    raw_data = cfg.paths.dunnhumby_data_path
    trx = pd.read_csv(raw_data + 'transaction_data.csv')
    print(trx.columns)
    assert cfg.colnames.customer_key in trx.columns

def test_preprocess_completed():
    # verify if the output files are present in the desired path
    with initialize(version_base=None, config_path="../cfg"):
        cfg = compose(config_name="env1_cfg")
    run_preprocess(cfg)
    processed_data = cfg.paths.processed_data
    files = os.listdir(processed_data)
    # check file presence
    assert 'customer_filtered.csv' in files
    assert 'product_filtered.csv' in files
    assert 'trx_filtered.csv' in files


if __name__ == '__main__':
    test()
    test_preprocess_completed()