import os
import pandas as pd


def test():
    files = os.listdir('./data/raw/')
    assert 'transaction_data.csv' in files

if __name__ == '__main__':
    test()