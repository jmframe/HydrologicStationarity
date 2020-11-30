#!/home/jmframe/programs/anaconda3/bin/python3
"""
Function for Mann-Kendall Test For Monotonic Trend
"""
import numpy as np
import pandas as pd
import os
import statistics as sts
import sys
import collections

#Mann-Kendall Statistic
mk = np.zeros([nGauges,metrics+1])

def mannkedizl(gauge_id,d):

    #Total number of records
    n = d.shape[0]

    # don't give a good value if the record is not long enough.
    if n < 10:
        print("gauge_id: " + gauge_id)
        print("not enough years in this record to generate stats")
        return -999
    
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
    S = 0
    var_s = 0
    t = 0
    for s in range(0, nYears-2):
        for i in range(s+1, nYears-1):
            diff = d[i] - d[s]
            if diff > 0:
                S = S + 1
            if diff < 0:
                S = S - 1

    # Calculate the tie score
    statList = np.ndarray.tolist(d)
    statDict = {i:statList.count(i) for i in statList}
    var_sum_t = np.zeros(n)
    for i in statDict:
        tp = statDict[i]
        t = t+tp*(tp-1)*(2*tp-5)

    if sum(t) > 0:
        print("tie in gauge: " + gauge_id)
        print("tie score: ", t)

    var_s = (1/18)*((n*(n-1)*(2*n+5))-t)
    if S > 0:
        mk = (S-1)/np.sqrt(var_s)  
    if S < 0:
        mk = (S+1)/np.sqrt(var_s)  
    print("Mann-Kendall Statistic")
    with np.printoptions(precision=2, suppress=True):
        print(mk)

    return mk
