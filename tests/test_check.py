import os
from hydra import initialize, compose

def test_unzip_raw_data():
    # verify if the output files are present in the desired path
    with initialize(version_base=None, config_path="../cfg"):
        cfg = compose(config_name="env1_cfg")

    raw_data_path = cfg.paths.dunnhumby_data_path
    files = os.listdir(raw_data_path)
    # check file presence
    assert "transaction_data.csv" in files
    assert "hh_demographic.csv" in files
    assert "product.csv" in files

if __name__ == "__main__":
    test_unzip_raw_data()
