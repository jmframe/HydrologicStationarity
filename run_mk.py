#!/home/jmframe/programs/anaconda3/bin/python3
import mannkendal as mk
"""
    Run Mann Kendall test a lot of sites...
"""
import numpy as np
import pandas as pd

d = np.array([1, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7, 8, 8, 9])
site = '1234'
mk.mannkedizl(site, d)
print('I cant believe it worked')
