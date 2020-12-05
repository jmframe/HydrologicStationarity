#!/home/jmframe/programs/anaconda3/bin/python3
"""
Function for Mann-Kendall Test For Monotonic Trend
    https://vsp.pnnl.gov/help/Vsample/Design_Trend_Mann_Kendall.htm
    1. List the data in the order in which they were collected over time
    Done above
    2. Determine the sign of all n(n−1)/2 possible differences xj−xk, where j>k. 
      These differences are: x2−x1,x3−x1,...,xn−x1,x3−x2,x4−x2,...,xn−xn−2,xn−xn−1
    3 3. Let sgn(xj−xk) be an indicator function that takes on the values:
      1, 0, or -1 according to the sign of xj−xk, that is,
        sgn(xj−xk) = 1 if xj−xk> 0
        sgn(xj−xk) = 0 if xj−xk = 0, or if the sign of xj−xk cannot be determined
        sgn(xj−xk) = -1 if xj−xk< 0
    4. Compute S = sum(sum(sgn(xj-xK)))
    5. n should be greater than 10
    6. Compute the variance of S as follows:
      VAR(S) = (1/18)[n(n-1)(2n+5) - sum(t(t-1)(2t+5)]
"""
import numpy as np
import pandas as pd
import os
import statistics as sts
import sys
import collections

def mannkedizl(gauge_id,d):

    #Total number of records
    n = d.shape[0]

    # don't give a good value if the record is not long enough.
    if n < 10:
        print("gauge_id: " + gauge_id)
        print("not enough years in this record to generate stats")
        return -999

    mk = 0 
    s = 0
    S = 0
    var_s = 0
    var_sum_t = 0 # tie variance sum
    g = 0 # Number of tied groups

    for s in range(0, n-2):
        for i in range(s+1, n-1):
            diff = d[i] - d[s]
            if diff > 0:
                S = S + 1
            if diff < 0:
                S = S - 1

    # Calculate the tie score
    statList = np.ndarray.tolist(d)
    statDict = {i:statList.count(i) for i in statList}
    for i in statDict:
        tp = statDict[i]
        if tp > 1:
            g += 1
            var_sum_t += tp*(tp-1)*(2*tp-5)

    if var_sum_t > 0:
        print("tie in gauge: " + gauge_id)
        print(statDict)
        print("tie score: ", var_sum_t)

    var_s = (1/18)*((n*(n-1)*(2*n+5))-var_sum_t)
    if S > 0:
        mk = (S-1)/np.sqrt(var_s)  
    if S < 0:
        mk = (S+1)/np.sqrt(var_s)  
    print("Mann-Kendall Statistic")
    with np.printoptions(precision=2, suppress=True):
        print(mk)

    return mk
