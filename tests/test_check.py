import os
def test():
    files = os.listdir('./data/raw/')
    assert 'transaction_data.csv' in files

if __name__ == '__main__':
    test()