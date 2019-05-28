# coding: UTF-8
import glob
import pandas as pd

csvlist = []
csvfiles = glob.glob("./output/*.csv")

for csvfile in csvfiles:
    csvlist.append(pd.read_csv(csvfile))

df = pd.concat(csvlist, sort=False)
df.to_csv("all.csv", encoding="utf_8", index=False)
