# %%
import pandas as pd

# %%
# load excel file into dataframe
df = pd.read_excel('data/Data_clean.xlsx', sheet_name='Sheet 1')
# remove second row
df.drop(0, inplace=True)
# add integer index as column
df.reset_index(inplace=True)
# display first 5 rows
df.head()
# %%
cols = df.columns
cols
answer_cols = ['Short1', 'Short2', 'Short3', 'Short4', 'Short5', 'Long1', 'Long2', 'Long3', 'Long4', 'Long5']
id_cols = ["index"]
# melt dataframe
df_melt = pd.melt(df, id_vars=id_cols, value_vars=answer_cols, var_name='Question', value_name='Answer')
# sort by index
df_melt.sort_values(by=['index', "Question"], inplace=True)
# all columns that start with 'Short1'
short1_cols = [col for col in df.columns if col.startswith('Short1')]
# remove 'Short1' from list
short1_cols.remove('Short1')
#short2_cols = [col for col in df.columns if col.startswith('Short2')]

#df_melt[["Question", "Answer", "index"] + short1_cols].head(21)
df_melt.head(21)
# %%
# split original dataframe into sub dataframes along the column axis by prefix short1, short2, etc.
prefixes = answer_cols
dfs = {prefix: df.filter(like=prefix).rename(columns={prefix: 'Answer'}) for prefix in prefixes}
for prefix, df_sub in dfs.items():
    df_sub["Question"] = prefix
    df_sub.columns = df_sub.columns.str.replace(prefix, '').str.lstrip('_')
    df_sub.reset_index(inplace=True)
    df_sub.drop(columns=['Answer'], inplace=True)

dfs['Short1'].head(21)
# %%
df_list = []
for prefix, df_sub in dfs.items():
    df_temp = pd.merge(df_sub, df_melt, on=['index', 'Question'], how='left')
    df_list.append(df_temp)
#df_list[0].head(21)
df_final = pd.concat(df_list, axis=0)
# Get a list of all column names, sorted
all_columns = sorted(df_final.columns.tolist())

# Move the specified columns to the front of the list
for col in reversed(['index', 'Question', 'Answer']):
    all_columns.remove(col)
    all_columns.insert(0, col)

# Reindex the dataframe with the new column order
df_final = df_final.reindex(columns=all_columns)
# sort by index and question
df_final.sort_values(by=['index', "Question"], inplace=True)
df_final.head(21)
df_final.to_excel('data/Data_clean_transformed.xlsx', index=False)
