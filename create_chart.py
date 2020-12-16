
import matplotlib.pyplot as plt
#import numpy
import sqlite3
import pandas
import matplotlib.dates as md


cmd_sql = r"select  *,datetime(ts,'unixepoch','localtime')  from measurements2 where ts >= (select strftime('%s',(select datetime('now','-24 hour'))))"

db = sqlite3.connect("air_quality.db")
df = pandas.read_sql_query(cmd_sql, db)
df2 = df

df2['m1_0_cf1'] = df2['m1_0_cf1'].clip(upper=500)
df2['m2_5_cf1'] = df2['m2_5_cf1'].clip(upper=500)
df2['m10_0_cf1'] = df2['m10_0_cf1'].clip(upper=500)
df2['ts'] = pandas.to_datetime(df2['ts'], unit='s')

df2.plot(x='ts',y=['m1_0_cf1', 'm2_5_cf1', 'm10_0_cf1'])
date_form = md.DateFormatter("%y/%m/%d %H:%M")
plt.gca().xaxis.set_major_formatter(date_form)
plt.grid()
plt.savefig('ppm.png')

