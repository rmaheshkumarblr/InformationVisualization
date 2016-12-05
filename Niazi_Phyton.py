# Sorayya Niazi


import csv
import numpy
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

mydataX = list()
mydataY = list()
id = 0
Numdata = 540
with open('Work_1.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        mydataX.append(row['Date'])
        mydataY.append(row['Fatalities'])
        # print(row['Date'], row['Fatalities'])
        id = id + 1
        if ( id > Numdata ):
            break;
        
mydataX_new = [dt.datetime.strptime(d,'%m/%d/%Y').date() for d in mydataX]

plt.xlabel('Year')
plt.ylabel('Fatalities')
plt.ylim((0,300))

#plt.plot(mydataX_new,mydataY,'r-')
#plt.savefig('Year_Fatalities_Line.png')
    
plt.scatter(mydataX_new,mydataY)
plt.savefig('Year_Fatalities_Scatter.png')



