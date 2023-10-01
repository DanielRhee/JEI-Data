import pandas as pd
import datetime
import csv
import numpy
import math

geyserRaw = pd.read_csv('Old_Faithful_eruptions.tsv', sep='\t')

# Extract data into 2D array
geyserData = geyserRaw.to_numpy()

# Geyser Duration/Height plotted against wait
allWaits = []
allLengths = []
allHeights = []
waitVsLength = []
waitVsHeight = []
for i in range(1, len(geyserData)-1):
    # Get difference in seconds and see if it's less than 110 minutes (To make sure the erruptions are in succession), make sure the geyser length is within reason, also make sure the geyser is post 2009
    if (int(geyserData[i+1][2])-int(geyserData[i][2]))/60 <= 115 and (int(geyserData[i+1][2])-int(geyserData[i][2]))/60 >= 34 and datetime.datetime.fromtimestamp(int(geyserData[i][2])) > datetime.datetime(2010, 1, 1):
        # Check if the data was measured in hours:
        if geyserData[i][16] != 'h' and not math.isnan(float(geyserData[i][15])):
            waitVsLength.append([(int(geyserData[i+1][2])-int(geyserData[i][2]))/60,int(geyserData[i][15])])
            allWaits.append((int(geyserData[i+1][2])-int(geyserData[i][2]))/60)
            allLengths.append(int(geyserData[i][15]))

#Write to csv file
with open('OldFaithfulProcessedLengthData.csv', 'w') as output:
    writer = csv.writer(output)
    for dataPoint in waitVsLength:
        writer.writerow(dataPoint)

with open('OldFaithfulProcessedHeightData.csv', 'w') as output:
    writer = csv.writer(output)
    for dataPoint in waitVsHeight:
        writer.writerow(dataPoint)
