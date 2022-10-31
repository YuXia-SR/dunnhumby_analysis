#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import seaborn as sns
from collections import Counter
from collections import Counter
import matplotlib.pyplot as plt
import os
import math
import sys
sns.set_style("darkgrid")

import warnings
warnings.filterwarnings("ignore")

import zipfile

 # unzip file
# zy = zipfile.ZipFile('/content/sample_data/dunnhumby - The Complete Journey CSV-20221028T212450Z-001.zip')
# ret = zy.extractall()


# ![Screenshot%202022-10-27%20212543.png](attachment:Screenshot%202022-10-27%20212543.png)

# In[172]:


path = '/Users/yingyingliu/Documents/Data Folder/'

product = pd.read_csv(path + 'product.csv')
transaction = pd.read_csv(path + 'transaction_data.csv')
campaign_desc = pd.read_csv(path + 'transaction_data.csv')
hh_demo = pd.read_csv(path + 'hh_demographic.csv')

##According to the  methodology of Wan, Mengting[1], I selected these three datasets.
# [1]Wan, Mengting, et al. "Modeling consumer preferences and price sensitivities from large-scale grocery shopping 
#    transaction logs." Proceedings of the 26th International Conference on World Wide Web. 2017.


# In[173]:


campaign_desc.head()


# In[174]:


campaign_desc.nunique()


# In[175]:


trans_key_list = list(transaction.household_key.unique())

hh_demo_key_list = list(hh_demo.household_key.unique())


# In[176]:


def common_member(a, b): 
    """A function to find the common items in two lists."""
    a_set = set(a) 
    b_set = set(b) 
    if (a_set & b_set): 
        return list((a_set & b_set))
    else: 
        print("No common elements")


# #### 这一步删除无效transaction，看不懂问我

# In[177]:


trans_and_hh_demo_keys_list = common_member(trans_key_list, hh_demo_key_list)

print("transaction inner join demongraphic data" + str(len(trans_and_hh_demo_keys_list)) + " households.")


# 这两个table的key是：house_hold_key, 下一步我要merge这两个表by key 
# In the transction dataset, each row represents a single product that has an accompanying basket_id

# ![image.png](attachment:image.png)

# 这一步首先把你说的无效的交易砍掉了

# In[234]:


trans_baskets_hh_key = pd.DataFrame(transaction.groupby(['household_key', 'BASKET_ID']).sum()).drop(['DAY', 'PRODUCT_ID','QUANTITY', 'STORE_ID', 'RETAIL_DISC', 'TRANS_TIME', 'WEEK_NO', 'COUPON_DISC', 'COUPON_MATCH_DISC'], axis=1)
trans_baskets_hh_key = trans_baskets_hh_key.merge(transaction.drop(['SALES_VALUE', 'RETAIL_DISC', 'COUPON_DISC', 'COUPON_MATCH_DISC'], axis=1), on="BASKET_ID").drop_duplicates(subset=['BASKET_ID'])
trans_baskets_hh_key.head()


# In[236]:


trans_demo = trans_baskets_hh_key.merge(hh_demo, on='household_key')

trans_demo.head(20)
# trans_demo.shape   (140339, 14)


# In[223]:


product.head()      


# In[224]:


product['COMMODITY_DESC'].nunique()


# Actually I'm so confused with product_id which is so unique 😂

# In[225]:


product.shape


# In[226]:


product = product[['COMMODITY_DESC', 'PRODUCT_ID']] 


# ![image.png](attachment:image.png)
# Transactional data contains purchase history of each household. 

# ### Delete unique product

# In[189]:


transaction=transaction[transaction['QUANTITY']>0]
transaction=transaction[transaction['SALES_VALUE']>0]


# #### key: product_id
# 
# ![image.png](attachment:image.png)

# In[190]:


av_uniq_prod = round(len(transaction.groupby(['household_key',"PRODUCT_ID"]).sum()["QUANTITY"])/len(grouped_sum),1)
av_uniq_prod


# In[191]:


grouped_sum = transaction.groupby("household_key").sum()
grouped_sum.head()


# In[196]:


product.head()


# In[201]:


product['COMMODITY_DESC'].nunique()     #### len(SUB_COMMODITY_DESC) = 2383


# In[229]:


prod_key_list = list(product['PRODUCT_ID'].unique())
trans_demo_key_list = list(product['PRODUCT_ID'].unique())


# In[230]:


prod_key_and_trans_demo_key_list = common_member(prod_key_list, trans_demo_key_list)

print("transaction inner join product " + str(len(prod_key_and_trans_demo_key_list)) + " products")


# In[233]:


trans_demo.head()


# In[240]:


sample = pd.merge(trans_demo, product, on=['PRODUCT_ID'], how='left')

sample.head()


# In[241]:


len(sample)


# In[243]:


sample.to_csv('/Users/yingyingliu/Desktop/sample.csv')


# In[54]:


fig_store = plt.figure(figsize=(14,8))
sns.barplot(y="Store ID",x="Total Sales (USD)",data = sales[:20],order=sales[:30]["Store ID"],orient="h")
plt.title('Top 30 Stores based on Sale Amount', fontsize=17)
plt.xlabel('Total Sales (USD)', fontsize=14)
plt.ylabel('Store ID', fontsize=14)
plt.show()

customer analysis
# In[57]:


purc_per_cust = transaction.groupby("household_key").sum()["SALES_VALUE"].sort_values(ascending=False)
purc_per_cust = pd.DataFrame(list(zip(purc_per_cust.index,purc_per_cust)),columns=["household_key","Total Purchase (USD)"])


# In[59]:


purc_per_cust.describe()


# In[58]:


fig_store = plt.figure(figsize=(14,8))
sns.barplot(y="household_key",x="Total Purchase (USD)",data = purc_per_cust[:30],order=purc_per_cust[:30]["household_key"],orient="h")
plt.title('Top 30 Customers based on Purchase Number', fontsize=17)
plt.xlabel('Total Purchases (USD)', fontsize=14)
plt.ylabel('Household Key', fontsize=14)
plt.show()


# In[64]:


hh_demo.head()


# In[65]:


def pie_categorical(data):
    #function to plot the histogram of categorical variables in pie graph
    features = data.columns
    #plot pie charts of categorical variables
    fig_pie_cat = plt.figure(figsize=(15,15))
    count = 1
    #calculate dynamic numbers of subplot rows and columns
    cols = int(np.ceil(np.sqrt(len(features))))
    rows = int(np.ceil(len(features)/cols))
    for i in features:
        ax = fig_pie_cat.add_subplot(rows,cols,count)
        data[i].value_counts().plot(kind="pie",autopct="%.1f%%",ax=ax)
        plt.ylabel("")
        plt.title(i,fontweight="bold",fontsize=8)
        count += 1

def hist_numeric(data):
    #function to plot the histogram of numeric variables
    features = data.columns
    fig_hists = plt.figure(figsize=(15,15))
    fig_hists.subplots_adjust(hspace=0.5,wspace=0.5)
    count = 1
    #calculate dynamic numbers of subplot rows and columns
    cols = int(np.ceil(np.sqrt(len(features))))
    rows = int(np.ceil(len(features)/cols))
    for i in features:
        ax = fig_hists.add_subplot(rows,cols,count)
        data[i].plot(kind="hist",alpha=.5,bins=25,edgecolor="navy",legend=False,ax=ax)
        ax.set_xlabel("")
        ax.set_title(i,fontweight="bold",fontsize=10)
        count += 1


# In[70]:


pie_categorical(hh_demo.drop("household_key",axis=1))


# In[ ]:




