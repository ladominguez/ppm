
import matplotlib.pyplot as plt
#import numpy
import sqlite3
import pandas
import matplotlib.dates as md

db = sqlite3.connect("air_quality.db")
df = pandas.read_sql_query("select ts, m1_0_cf1, m2_5_cf1, m10_0_cf1 from measurements2 order by ts", db)
df2 = df

df2['m1_0_cf1'] = df2['m1_0_cf1'].clip(lower=10)
df2['m2_5_cf1'] = df2['m2_5_cf1'].clip(lower=10)
df2['m10_0_cf1'] = df2['m10_0_cf1'].clip(lower=10)
df2['ts'] = pandas.to_datetime(df2['ts'], unit='s')

df2.plot(x='ts')
plt.savefig('ppm.png')

