# %%
import pandas as pd

# %%
# load excel file into dataframe
df = pd.read_excel('data/Data_clean.xlsx', sheet_name='Sheet 1')
# display first 5 rows
df.head()
# %%
