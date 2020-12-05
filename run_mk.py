#!/home/jmframe/programs/anaconda3/bin/python3
import mannkendal as mk
"""
    Run Mann Kendall test a lot of sites...
"""
import numpy as np
import pandas as pd
from glob import glob
from tqdm import tqdm

files = glob('ecmwf/potential_evaporation/*')

sites = []
mk_list = []
for i in tqdm(files):
    site = i.split('_')[2].split('.')[0]
    sites.append(site)
    with open(i, 'r') as f:
        d = pd.read_csv(f)
    d = np.array(d['potential_evaporation'])
    mk_list.append(mk.mannkedizl(d))
mk_df = pd.DataFrame(sites, mk_list)
print(mk_df)
print('I cant believe it worked')
