import pandas as pd
import datetime
import csv
import numpy
import math
import re

geyserBeehiveRaw = pd.read_csv('Beehive_eruptions.tsv', sep='\t')
geyserIndicatorRaw = pd.read_csv('Beehives_Indicator_eruptions.tsv', sep='\t')
# Extract data into 2D array
geyserBeehiveData = geyserBeehiveRaw.to_numpy()
geyserIndicatorData = geyserIndicatorRaw.to_numpy()

#Get all indicator times from post 2010
filteredData = []
for i in range(len(geyserIndicatorData)-1):
    # Make sure the geyser is post 2009
    #if (datetime.datetime.fromtimestamp(int(geyserIndicatorData[i][2])) > datetime.datetime(2010, 1, 1)):
    filteredData.append(int(geyserIndicatorData[i][2]))

fullFilteredData = []
seen = set()
# Add behive eruptions
for i in range(1,len(geyserBeehiveData)-2):#591, 592):#1,len(geyserBeehiveData)-2):#591, 592): #len(geyserBeehiveData)-2): #7200, 7300): #2, len(geyserBeehiveData)-2):
    # Make sure the geyser is post 2009
    #if (datetime.datetime.fromtimestamp(int(geyserBeehiveData[i][2])) > datetime.datetime(2010, 1, 1)):
    currIndex = 0
    # Identify the closest indicator eruption
    #print(currIndex, filteredData[currIndex], int(geyserBeehiveData[i][2]), filteredData[currIndex] < int(geyserBeehiveData[i][2]), currIndex < len(filteredData)-2)
    while filteredData[currIndex] < int(geyserBeehiveData[i][2]) and currIndex < len(filteredData)-2:
        #print( filteredData[currIndex], int(geyserBeehiveData[i][2]))
        currIndex += 1
    #print(currIndex)
    #print(currIndex)
    if abs(int(geyserBeehiveData[i][2])-filteredData[currIndex-1]) <= 45*60:
        #print("checkers")
        #print (geyserBeehiveData[i][2], filteredData[currIndex],currIndex, int(geyserBeehiveData[i][2])-filteredData[currIndex])
        fullFilteredData.append([filteredData[currIndex-1], int(geyserBeehiveData[i][2])])
        seen.add(filteredData[currIndex-1])

falsePositiveData = [["Duration", "Time since last eruption", "Followed by eruption?"]]
for i in range(1, len(geyserIndicatorData)-1):
    if not (geyserIndicatorData[i][2] in seen): 
        if "to" in str(geyserIndicatorData[i][14]) or str(geyserIndicatorData[i][14])[len(str(geyserIndicatorData[i][14]))-1] == "m":
            falsePositiveData.append([int(re.sub('[^0-9]','', geyserIndicatorData[i][14]))/60, geyserIndicatorData[i][2]-geyserIndicatorData[i-1][2], "y"])
    else:
        if "to" in str(geyserIndicatorData[i][14]) or str(geyserIndicatorData[i][14])[len(str(geyserIndicatorData[i][14]))-1] == "m":
            falsePositiveData.append([int(re.sub('[^0-9]','', geyserIndicatorData[i][14]))/60, geyserIndicatorData[i][2]-geyserIndicatorData[i-1][2], "n"])

#Write to csv file
with open('BeehiveProcessedData-TEST.csv', 'w') as output:
    writer = csv.writer(output)
    for dataPoint in fullFilteredData:
        writer.writerow(dataPoint)

with open('BeehiveProcessedData-FP.csv', 'w') as output:
    writer = csv.writer(output)
    for dataPoint in falsePositiveData:
        writer.writerow(dataPoint)
