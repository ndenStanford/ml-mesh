# 3rd party libraries
import pandas as pd


d = {"col1": ["a", "b"], "col2": ["c", "d"]}
df = pd.DataFrame(data=d)
x3 = df["col2"].astype(pd.StringDtype())
df["col3"] = x3
x4 = pd.Series([x for x in df["col2"].values]).astype(pd.StringDtype())
df["col4"] = x4
df
