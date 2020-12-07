#!/home/jmframe/programs/anaconda3/bin/python3
"""
    Add land cover changes to the Mann Kendall result
"""
import numpy as np
import pandas as pd
from glob import glob
from tqdm import tqdm

att_path = "/home/NearingLab/data/camels_attributes_v2.0/camels_all.txt"
attributes = pd.read_csv(att_path, sep=";")
attributes = attributes.set_index('gauge_id')
mean_area = np.mean(np.mean(attributes.loc[:,['area_gages2', 'area_geospa_fabric']]))

df = pd.read_csv('results-mk.txt').drop(columns=['empty'])
sites = df['site']
df = df.set_index('site')
land_change_catagories = ['tree_canopy_cover', 'impervious']
end_lc_col = {'tree_canopy_cover':2, 'impervious':3}
for land_cat in land_change_catagories:
    df[land_cat] = np.empty(df.shape[0])
    df.loc[:, land_cat] = np.nan
    print('working on '+land_cat)
    files = glob('lulc/'+land_cat+'/*')
    for site in tqdm(sites):
        area = np.mean(attributes.loc[site,['area_gages2', 'area_geospa_fabric']])
        _file = 'lulc/'+land_cat+'/basin_'+str(int(site))+'.csv'
        if _file not in files:
            print(str(site)+'has no '+land_cat+' data')
            continue
        with open(_file, 'r') as f:
            d = pd.read_csv(f)
        d = np.array(d[land_cat])
        if d[0] > 0:
            lc_change = mean_area*(np.mean(d[1:end_lc_col[land_cat]])-d[0])/d[0]/area
        else:
            lc_change = mean_area*(np.mean(d[1:end_lc_col[land_cat]])-d[0])/area
        df.loc[site, land_cat] = lc_change

df.to_csv('results-mk-lc.txt')
print(df)
print('I cant believe it worked')
