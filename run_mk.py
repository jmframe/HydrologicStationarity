#!/home/jmframe/programs/anaconda3/bin/python3
import mannkendal as mk
"""
    Run Mann Kendall test a lot of sites...
"""
import numpy as np
import pandas as pd
from glob import glob
from tqdm import tqdm

att_path = "/home/NearingLab/data/camels_attributes_v2.0/camels_all.txt"
attributes = pd.read_csv(att_path, sep=";")
qp = pd.read_csv('results-mk-runoff-ratio.txt', sep=" ");
qp_site = qp['site'].to_list()
qp_site = [int(i) for i in qp_site]
qp['site'] = qp_site
qp = qp.set_index('site')
sites = attributes['gauge_id'].to_list()
#latitude = attributes['gauge_lat'].to_list()
#longitude = attributes['gauge_lon'].to_list()
attributes.set_index('gauge_id', inplace=True)

ecmwf_data = ['potential_evaporation',
              'skin_temperature', 
              'soil_temperature_level_1', 
              'evaporation_from_vegetation_transpiration'] 
df = pd.DataFrame(index=sites, columns = ecmwf_data)

for i in df.index.values:
    if i not in list(qp.index.values):
        print(str(i)+' is an index of df, but not qp')

#df['lat'] = latitude
#df['lon'] = longitude
for ecmwf in ecmwf_data:
    print('calculating Mann Kendall trends for '+ecmwf)
    files = glob('ecmwf/'+ecmwf+'/*')
    for site in tqdm(sites):
        _file = 'ecmwf/'+ecmwf+'/basin_'+str(int(site))+'.csv'
        if _file not in files:
            print(str(site)+'has no '+ecmwf+' data')
            continue
        with open(_file, 'r') as f:
            d = pd.read_csv(f)
        d = np.array(d[ecmwf])
        df.loc[site, ecmwf] = mk.mannkedizl(d)
df = df.join(qp)
df.to_csv('results-mk.txt')
print(df)
print('I cant believe it worked')
