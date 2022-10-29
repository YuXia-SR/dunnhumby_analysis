# Open source retail dataset


### Downloading the dataset
The data has been uploaded to Git Large File Storage. Install git-lfs [here](https://git-lfs.github.com/).


### Context

Data in this repository was extracted from the open source dataset ["The Complete Journey"](https://www.dunnhumby.com/source-files). This dataset contains household level transactions over two years from a group of 2,500 households who are frequent shoppers at a retailer. It contains all of each household’s purchases, not just those from a limited number of categories. For certain households, demographic information as well as direct marketing contact history are included.

This dataset provides a starting point for feature engineering, customer segmentation, and simulator design.


### Data Glossary

This dataset contains more tables, as well as transaction information, than we may need at this stage to construct the first version of the simulator. You may find the following tables useful to start with.

**transaction_data.csv**

| Column Name               | Column Description                                           |
| ------------------------- | ------------------------------------------------------------ |
| household_key           | Uniquely identifies each household |
| BASKET_ID               | Uniquely identifies a purchase occasion                                           |
| DAY          | Day when transaction occurred |
| PRODUCT_ID                    | Uniquely identifies each product |
| QUANTITY                 | Number of the products purchased during the trip |
| SALES_VALUE               | Amount of dollars retailer receives from sale |
| STORE_ID              | Uniquely identifies each store|
| RETAIL_DISC          | Discount applied due to retailer's loyalty card program  |
| TRANS_TIME     | Time of day when the transaction occurred |
| WEEK_NO | Week of the transaction. Ranges 1-102 |
| COUPON_DISC           | Discount applied due to manufacturer coupon  |
| COUPON_MATCH_DISC      | Discount applied due to retailer's match of manufacturer coupon  |


**product.csv**

| Column Name               | Column Description                                           |
| ------------------------- | ------------------------------------------------------------ |
| PRODUCT_ID                    | Uniquely identifies each product |
| DEPARTMENT                 | Groups similar products together |
| COMMODITY_DESC               | Groups similar products together at a lower level |
| SUB_COMMODITY_DESC              | Groups similar products together at the lowest level|
| MANUFACTURER          | Code that links products with same manufacturer together  |
| BRAND     | Indicate Private or National label brand |
| CURR_SIZE_OF_PRODUCT           | Indicates package size  |


We will keep track on the features used in the current simulator on this [wiki page](https://github.com/Bain/twinning/wiki/Marketing-Tables). For more detailed description about all tables, please refer to the pdf manual in the zip folder. Here's a diagram overview on all available tables:
<img width="1036" alt="image" src="https://user-images.githubusercontent.com/61883895/196764432-e446c28a-d63e-48fe-a37e-f73eca534e83.png">
