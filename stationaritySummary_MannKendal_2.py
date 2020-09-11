#!/home/jmframe/programs/anaconda3/bin/python3
"""
Created on Thu May 9 2019
@author: Jonathan Frame
"""
import numpy as np
import pandas as pd
import os
import statistics as sts
import time
import sys
import collections
# Need to set print options to max for generating the results files.
np.set_printoptions(threshold=sys.maxsize)
#import matplotlib.pyplot as plt

# time the program
startProgramTime = time.time()

#Store all attributes. Really just need basin area, but the rest might come in handy.
att_path = "/home/NearingLab/data/camels_attributes_v2.0/camels_all.txt"
attributes = pd.read_csv(att_path, sep=";")
attributes.set_index('gauge_id', inplace=True)

#data directory path
dq_path = "/home/NearingLab/projects/jmframe/CAMELS_stationarity/usgs_streamflow/"
dp_path = "/home/NearingLab/projects/jmframe/CAMELS_stationarity/nldas_precipitation/"

# Setting nGauges to be one above the known number of gauges in CAMELS
nGauges = 673
count_id = 0
metrics = 5 #i.e., P, Q, P-Q, Q/P, (P-Q)/P

#Mann-Kendall Statistic
mk = np.zeros([nGauges,metrics+1])

# Loop through all the files in the discharge directory first.
for filename in os.listdir(dq_path):
    startCatchmentTime = time.time()
    q_path = dq_path + filename
    
    # the known location of the gauge ids in the files
    gauge_id = filename[0:8]
    print("gauge_id: " + gauge_id)

    # Now set a path to the corresponding precipitation gauge.
    p_path = dp_path + gauge_id + "_lump_nldas_forcing_leap.txt"
    
    # Confirm that there is a corresponding precipitation gauge to the discharge.
    if int(gauge_id) in attributes.index:
        catch_area = attributes.loc[int(gauge_id),'area_geospa_fabric'] # km^2
        print("the catchment area is: ", catch_area, " km^2")
        mk[count_id][0] = int(gauge_id)
    else:
        print("WARNING::this catchment is not in the CAMELS attributes: ")
        print("Moving on to the next one...")
        continue

    # Load in the data. Note: Precipitation has headers.
    dataQ = np.loadtxt(q_path, dtype={'names': ('id', 'year', 'month', 'day', \
        'Q','status'), 'formats': ('i4', 'i4', 'i4', 'i4', 'f4', 'U10')})
    # open the precipitation file and read line by line.
    with open(p_path) as f:
        lines = (line for line in f if not line.startswith('#'))
        dataP = np.loadtxt(lines, dtype={'names': ('year', 'month', 'day', 'hour', \
            'dayls', 'P','SRAD', 'SWE', 'Tmax', 'Tmin', 'Vp'), 'formats': ('i4', 'i4', \
            'i4', 'i4', 'f4', 'f4', 'f4', 'f4', 'f4', 'f4', 'f4')}, skiprows=4)

    #Total number of records
    nQ = dataQ.shape[0]
    nP = dataP.shape[0]

    # Set start and end data information for the streamflow record forcing data.
    yearStart  = dataQ[1][1]
    yearEnd = dataQ[nQ-1][1]
    nYears = (yearEnd - yearStart) + 1
    yearEnd = yearStart + 1 #switch from the whole record, to the individual year
    #Indexes to get annual record for statistics
    startQ = -1 #the beginning index of the annual record
    endQ = -1 #the end index of the annual record
    holdP = 0 #hold the index of the annual record

    # don't give a good value if the record is not long enough.
    if nYears < 10:
        print("gauge_id: " + gauge_id)
        print("not enough years in this record to generate stats")
        for z in range(1, nMetrics):
            mk[count_id][z] = -999
        continue

    print("number of years in the record: ", nYears)

    # year, days on record, P, Q, P-Q, P/Q, (P-Q)/P, 
    yearStats = np.zeros([nYears, 7])
    
    # Now loop through and calculate some stuff for individual years
    # First go through the whole record, and figure out where the years are.
    for y in range(0, nYears-1):
        # print("Looping year: ", yearStart)
        startYearTime = time.time() #time this loop for efficiency.
    
        #These two loops get the index of the first and last record in the sample.
        #keep track of where the previous years are in the loop with startQ and endQ
        for i in range(endQ+1, nQ):
            if dataQ[i][1] == yearStart:
                startQ = i
                yearStart = yearStart + 1 #advance the year for the next iteration
                break #once the index is found, immediately end the loop.
        # print('startQ: ', startQ) 
        for i in range(startQ, nQ):
            if dataQ[i][1] == yearEnd: 
                endQ = i
                yearEnd = yearEnd + 1
                break 
        #print('endQ: ', endQ)

        j = 0 #need a counter from zero for each year
        m = (endQ - startQ) + 1 #number of valurd in the discharge range.
        listQ = np.zeros(m) # list each record in sample for doing these statistics.
        listP = np.zeros(m) # corresponding precipitation list.
       
        # Now that we know where the year starts and ends, go through it day by day.
        for i in range(startQ, endQ):
            iYear = dataQ[i][1]
            yearStats[y][0] = iYear
            iMonth = dataQ[i][2]
            iDay = dataQ[i][3]
            Q = dataQ[i][4]
    
            #Match the precipitation day, and save the data.
            for iP in range(holdP, nP):
                if dataP[i][0] == iYear and dataP[i][1] == iMonth and dataP[i][2] == iDay:
                    P = dataP[i][5]
                    holdP = iP #Hold this spot, to start looking from here next time
                    break
                if iP == nP:
                    print("date: ", iYear, '-', iMonth,"-", iDay)
                    print("There is no corresponding precipitation for the Discharge")
                    P = 0

            if Q > -1:
                # convert discharge from cfs to mm
                # mm/day=(ft3/sec)(m3/ft3)(sec/min)(min/hr)(hr/day)(1/km2)(1/m2)(mm/m) 
                Q = Q*(1/(3.28084**3))*60*60*24*(1/catch_area)*(1/1000**2)*1000
                yearStats[y][1] = yearStats[y][1] + 1
                listQ[j] = Q
                listP[j] = P # I don't know if I should include precip if no discharge.
                j = j + 1
            else:
                listQ = np.delete(listQ, [j])
                listP = np.delete(listP, [j])
                # print("date: ", iYear, '-', iMonth,"-", iDay, \
                #    "The Discharge record is bad and will not be used")
 
        # if too many records are bad, then don't do any statistics
        if yearStats[y][1] > 300:
            yearStats[y][2] = sum(listP)
            yearStats[y][3] = sum(listQ)
            yearStats[y][4] = sum(listP) - sum(listQ) 
            yearStats[y][5] = sum(listQ) / max(1,sum(listP))
            yearStats[y][6] = (sum(listP) - sum(listQ)) / max(1,sum(listP))

        #print("total time for this year: ", time.time() - startYearTime)

    # Printing the precipitation and discharge to individual files
    orig_stdout = sys.stdout
    f = open('pq/' + gauge_id + '.txt', 'w+')
    sys.stdout = f
    with np.printoptions(precision=2, suppress=True):
        print('year  nDays  P  Q  P-Q   Q/P  (P-Q)/p')
        for y in range(0, nYears-1):
            print(yearStats[y][0],yearStats[y][1], yearStats[y][2], yearStats[y][3], \
                yearStats[y][4], yearStats[y][5], yearStats[y][6])
    sys.stdout = orig_stdout
    f.close()

    #print("total time for this catchment: ", time.time() - startCatchmentTime)

#https://vsp.pnnl.gov/help/Vsample/Design_Trend_Mann_Kendall.htm
# 1. List the data in the order in which they were collected over time
# Done above
# 2. Determine the sign of all n(n−1)/2 possible differences xj−xk, where j>k. 
  # These differences are: x2−x1,x3−x1,...,xn−x1,x3−x2,x4−x2,...,xn−xn−2,xn−xn−1
# 3 3. Let sgn(xj−xk) be an indicator function that takes on the values:
  # 1, 0, or -1 according to the sign of xj−xk, that is,
    # sgn(xj−xk) = 1 if xj−xk> 0
    # sgn(xj−xk) = 0 if xj−xk = 0, or if the sign of xj−xk cannot be determined
    # sgn(xj−xk) = -1 if xj−xk< 0
# 4. Compute S = sum(sum(sgn(xj-xK)))
# 5. n should be greater than 10
# 6. Compute the variance of S as follows:
  # VAR(S) = (1/18)[n(n-1)(2n+5) - sum(t(t-1)(2t+5)]
    s = 0
    S = np.zeros(metrics)
    var_s = np.zeros(metrics)
    t = np.zeros(metrics)
    for s in range(0, nYears-2):
        for i in range(s+1, nYears-1):
            for stat in range(0, metrics):
                d = yearStats[i][stat+2] - yearStats[s][stat+2]
                if d > 0:
                    S[stat] = S[stat] + 1
                if d < 0:
                    S[stat] = S[stat] - 1
    # Calculate the tie score
    for stat in range(0, metrics):
        statList = np.ndarray.tolist(yearStats[:,stat+2])
        #print(statList)
        statDict = {i:statList.count(i) for i in statList}
        #print(statDict)
        for i in statDict:
            tp = statDict[i]
            t[stat] = tp*(tp-1)*(2*tp-5)
        if sum(t) > 0:
            print("tie in gauge: " + gauge_id)
            print("tie score: ", t)

    for stat in range(0, metrics):
        var_s[stat] = (1/18)*((nYears*(nYears-1)*(2*nYears+5))-t[stat])
        if S[stat] > 0:
            mk[count_id][stat+1] = (S[stat]-1)/np.sqrt(var_s[stat])  
        if S[stat] < 0:
            mk[count_id][stat+1] = (S[stat]+1)/np.sqrt(var_s[stat])  
    print("Mann-Kendall Statistic")
    with np.printoptions(precision=2, suppress=True):
        print(mk[count_id])

    # move the counter for the next gauge
    count_id = count_id + 1

# Create an array with the Camels latitudes and longitudes, for the output.
camels_ll = np.genfromtxt('/home/NearingLab/data/camels_attributes_v2.0/gauge_id_lat_lon_name.txt', delimiter=';')
G = camels_ll.shape[0]

# Printing the results out to file.            
# copying the sys.stdout
orig_stdout = sys.stdout
f = open('mann-kendal.txt', 'w+')
sys.stdout = f
with np.printoptions(precision=2, suppress=True):
    for i in range(0, nGauges-1):
        # Brute force method to line up the latitudes and longitudes with the mann-kendal results.
        for iLL in range(0,G):
            if mk[i][0] == camels_ll[iLL][0]:
                lat = camels_ll[iLL][1]
                lon = camels_ll[iLL][2]
                break
            if iLL == G:
                lat = -9999
                lon = -9999
        print(mk[i][0], lat, lon,  mk[i][1], mk[i][2], mk[i][3], mk[i][4], mk[i][5])
sys.stdout = orig_stdout
f.close()

print("total time for this program: ", time.time() - startProgramTime)



