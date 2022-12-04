# This script includes preprocessing + cleaning up of the Dunnhumby data for training of demand model and customer model

import pandas as pd
import os
from omegaconf import DictConfig


def run_preprocess(cfg: DictConfig):
    colnames = cfg.colnames
    raw_data_path = cfg.paths.dunnhumby_data_path
    infrequent_customers_threshold = cfg.preprocess.infrequent_customers_threshold
    infrequent_products_threshold = cfg.preprocess.infrequent_products_threshold
    small_sale_threshold = cfg.preprocess.small_sale_threshold
    process_data_folder = cfg.paths.processed_data

    if not os.path.exists(raw_data_path):
        os.makedirs(raw_data_path)

    if not os.path.exists(process_data_folder):
        os.makedirs(process_data_folder)

    # transaction_data, product, hh_demographic are tables we will focus to understand in this script
    trx = pd.read_csv(raw_data_path + 'transaction_data.csv')
    product_table = pd.read_csv(raw_data_path + 'product.csv')
    customer_table = pd.read_csv(raw_data_path + 'hh_demographic.csv')

    # filter out the transactions made by customers who visit less than 3 times (0.5% quantiles) -> defined by infrequent_customers_threshold
    temp = trx.groupby(colnames.customer_key).nunique()[colnames.day]
    quantiles = temp.quantile(infrequent_customers_threshold)
    customer_list = temp[temp > quantiles].index

    # filter out the transactions made on products that only have transaction records less than 4 days (60% quantiles) -> defined by infrequent_products_threshold
    temp = trx.groupby(colnames.product_nbr).nunique()[colnames.day]
    quantiles = temp.quantile(infrequent_products_threshold)
    frequent_product_list = temp[temp > quantiles].index

    # filter out the transactions made on products that only have daily sales less than 5 units (99.5% quantiles) -> small_sale_threshold
    temp = trx.groupby([colnames.product_nbr, colnames.day]).sum()[
        colnames.item_qty].reset_index()
    temp = temp.groupby(colnames.product_nbr).mean()[colnames.item_qty]
    quantiles = temp.quantile(small_sale_threshold)
    big_product_list = temp[temp > quantiles].index
    product_list = set(frequent_product_list) & set(big_product_list)

    # putting all filters together
    trx_filtered = trx[(trx[colnames.product_nbr].isin(product_list)) & (
        trx[colnames.customer_key].isin(customer_list))]
    customer = customer_table[customer_table[colnames.customer_key].isin(
        customer_list)]
    product = product_table[product_table[colnames.product_nbr].isin(
        product_list)]

    trx_filtered = trx_filtered[trx_filtered[colnames.item_qty] > 0]

    # saving the trx csv
    trx_filtered.to_csv(process_data_folder + 'trx_filtered.csv', index=False)
    customer.to_csv(process_data_folder + 'customer_filtered.csv', index=False)
    product.to_csv(process_data_folder + 'product_filtered.csv', index=False)
