
**Title**

Climate driven hydrologic nonstationarity patterns across the Continental United States

**Authors**

Jonathan Frame<sup>*,1,2</sup>

* Corresponding author: jonathan.frame@noaa.gov

1. National Oceanic and Atmospheric Administration, Office of Water Prediction, National Water Center.

2. University of Alabama. 

**Abstract**

We calculated metrics of climate change, land use-land cover change, and hydrologic nonstationarity in 671 catchments across the Continental United States (CONUS) that are known not to have relatively little urbanization and anthropogenic land cover. Climate change is correlated with hydrologic nonstationarity in these basins. Land use-land cover change has no correlation with hydrologic nonstationarity in these basins. We present kriging maps over CONUS showing climate change, land use-land cover change, and hydrologic nonstationarity.

**Introduction**

Hydrologic nonstationarity has a few distinct, but not necessarily contradicting, meanings. In general, nonstationarity refers to a condition in which the statistical representation of a system is not constant. As an example, although the flow of a river fluctuates with the seasons and individual precipitation events, average annual flows are often used as a representative hydrologic characteristic. If the average annual flow has some trend (not just year to year fluctuations about a constant value), then it could be described as non stationary. Anthropogenic land use/land cover changes can also cause non stationary conditions. For example, if a watershed has increasing urbanization that increases the impervious surfaces, this can cause higher and quicker peak flows. Changing flow responses to similar precipitation events could be described as hydrologic non stationarity. 

Hydrologic nonstationarity has been identified as a serious limitation of hydrologic modeling, specifically for the purposes of water resources management (Milly et al. 2008). Nonstationarity refers to the assumption that watershed properties that control water flow are considered to be time invariant (Sadegh et al. 2014, Lui et al. 2020). Climatological conditions have been identified as drivers of nonstationarity (Deb et al. 2019a). Surface water - groundwater interactions have also been linked as highly influential to non-stationary hydrologic responses (Deb et al. 2019b).

A study of the Mann-Kendall statistic on flow only across CONUS was done by Tamaddun et al. 2016. We expand on this study by including precipitation, annual land surface conditions and land cover.

We attempted to distinguish between climatological and land use/land cover (LULC) drivers of hydrologic nonstationarity in CONUS. We first revised the assumption that hydrologic nonstationarity exists across CONUS, and compared our analysis to Tamaddun et al. 2016. We then compared the relationship between changes in a hydrologic rainfall - runoff characteristic with changes in yearly climatological indexes and changing land cover. 

We address the following research question: Can we distinguish between climate driven and land use / land cover driven hydrologic nonstationarity?

H0: Hydrologic nonstationarity is identifiable by geographic location 

H1: Hydrologic nonstationarity is correlated with a changing climate

H2: Hydrologic nonstationarity is correlated with a changing land surface 

**Methods and data**

We analyze hydrologic nonstationarity at the CAMELS basins. Nonstationarity is calculated using a Mann-Kendall statistic (Mann 1945, Kendall 1975) for monotonic change during the years from 1980 to 2014. The Mann-Kendall statistic is a common test for hydrologic nonstationarity (Lui et al. 2019). The test was done for the ratio of annual volumetric runoff and annual volumetric precipitation across the basins. These data came from the USGS stream gauge network, and precipitation was from the NLDAS reanalysis from 1980 - 2014.

We analyze the monotonic change of yearly averaged climatological surface variables from the ERA5-Land monthly averaged - ECMWF climate reanalysis. We summarize changes in the land cover from forest (Sexton et al. 2016) and impervious surface (NLCD 3026). 


<table>
  <tr>
   <td><strong>Data product</strong>
   </td>
   <td><strong>Source</strong>
   </td>
   <td><strong>Spatial resolution</strong>
   </td>
   <td><strong>Temporal resolution</strong>
   </td>
   <td><strong>Temporal range</strong>
   </td>
  </tr>
  <tr>
   <td>ERA5-Land monthly averaged - ECMWF climate reanalysis
   </td>
   <td> ECMWF
   </td>
   <td> 0.1 degrees
   </td>
   <td> Monthly
   </td>
   <td> 1981 - present
   </td>
  </tr>
  <tr>
   <td>Global Forest Cover Change (GFCC) Tree Cover Multi-Year
   </td>
   <td> GFCC
   </td>
   <td> 30 m
   </td>
   <td> Semi annual
   </td>
   <td> 2000 - 2015
   </td>
  </tr>
  <tr>
   <td>NLCD: USGS National Land Cover Database
   </td>
   <td> NLCD
   </td>
   <td> 30 m
   </td>
   <td> Semi-annual
   </td>
   <td> 1992 - 2015
   </td>
  </tr>
</table>


We aggregated and extracted data for each of the 671 CAMELS basins using Google Earth Engine. A feature collection containing polygons of the CAMELS basins was imported into Google Earth Engine. A function was developed to aggregate, reduce and clip raster data from image collections for any given polygon, then export those data to CSV files. That function was then mapped over the full CAMELS basin feature collection.

Process workflow:



1. Upload camels basins as feature collection.
2. Load in image collection for target variable.
3. Clip image collection to basin shape.
4. Filter image collection by years.
5. Reduce images down to one image.
6. Reduce image down to representative statistic.
7. Export data.
8. Load data into python.
9. Calculate metrics for change
    1. Climate - Mann Kendall
    2. Land cover - basin area normalized mean annual change
10. Set up regression model
11. Let it rip
12. Load basin change values into GEE
13. Interpolate across CONUS and plot.

To test our hypotheses we used random forest regression to correlate geographic location, changes in climate and land cover to changes in hydrologic conditions. We reject/fail to reject our hypotheses by subjectively looking at a scatter plot of these regressions.

H0: dH = f(latitude, longitude)
H1: dH = f(dC)
H2: dH = f(dLC)

**Results**


![alt_text](maps/fig1.png "image_tooltip")


Figure 1. Locations of USGS stream gauges on the 671 basins used in this study.

![alt_text](maps/fig2.png "image_tooltip")


Figure 2. Hydrologic nonstationarity in terms of annual runoff ratio (Q / P). This map uses Kriging to interpolate between the catchments. 

![alt_text](maps/fig3.png "image_tooltip")


I did not include figures for Soil Temperature, Transportation and Evaporation for the sake of brevity. The maps look somewhat similar anyways.

![alt_text](maps/fig4.png "image_tooltip")


Figure 4. Change in impervious surfaces interpolated across CONUS from 1992 - 2015. Note that the basins sampled are supposed to be relatively undeveloped. So this interpolation is not supposed to include ‘urban’ areas. 

![alt_text](maps/fig5.png "image_tooltip")


Figure 5. Forest cover changes interpolated across CONUS. This map is actually kind of silly, because instead of interpolating at the samples, I could have just done the calculations on each pixel in the image. It would have been relatively easy to do, but it wouldn’t have been useful for my correlations with average basin hydrologic characteristics. 


![alt_text](maps/fig6.png "image_tooltip")


Figure 6. Correlation between geographic location and hydrologic nonstationarity. We fail to reject hypothesis 0. Also shown is the Gini importance factor showing that latitude and longitude are equally weighted when predicting hydrologic nonstationarity.

![alt_text](maps/fig7.png "image_tooltip")


Figure 7. Correlation between annual climate variables and hydro. Nonstationarity. We fail to reject hypothesis 1. Also shown is the Gini importance factor showing that evaporation is the most weighted and transpiration is least weighted.

![alt_text](maps/fig8.png "image_tooltip")


Figure 8. We reject hypothesis 2 and show that hydrologic nonstationarity does not correspond to changes in land cover. The weights on the right are meaningless, since there is no correlation.

**Conclusions**

Hydrologic nonstationarity at these 671 basins across CONUS is driven by climate, not land cover change. We conclude that Figure 2 shows the impact of climate change on general hydrologic conditions. Surface water runoff is increasing in the Northwest, Northern Plains, Northeast and Southern Florida. Surface water runoff is decreasing in most of the Southern United States, Michigan and Wisconsin.

Even though land use / land cover change has not been shown to be correlated with hydrologic nonstationarity, and thus not a driver, we still see some interesting results when interpolating the changes within ‘natural’ basin boundaries. Many hotspots appear to be undergoing significant increases in permeability land cover. Some of these include the Northeast, Houston TX and what looks like Reno NV. Interestingly the Pacific Northwest is not increasing in impermeability, and they are also seeing an increase in runoff. There also happens to be a hotspot of deforestation around the Seattle metropolitan area.

**References**

Sexton et al. 2016. [https://lpdaac.usgs.gov/documents/145/GFCC_User_Guide_V1.pdf](https://lpdaac.usgs.gov/documents/145/GFCC_User_Guide_V1.pdf)

NLCD. 2016 [https://www.mrlc.gov/national-land-cover-database-nlcd-2016](https://www.mrlc.gov/national-land-cover-database-nlcd-2016)

Deb, Proloy, Anthony S. Kiem, and Garry Willgoose. “Mechanisms Influencing Non-Stationarity in Rainfall-Runoff Relationships in Southeast Australia.” _Journal of Hydrology_ 571, no. February (2019): 749–64. [https://doi.org/10.1016/j.jhydrol.2019.02.025](https://doi.org/10.1016/j.jhydrol.2019.02.025).

Kendall, M.G. 1975. Rank Correlation Methods, 4th edition, Charles Griffin, London.

Liu, Saiyan, Shengzhi Huang, Yangyang Xie, Qiang Huang, Hao Wang, and Guoyong Leng. “Assessing the Non-Stationarity of Low Flows and Their Scale-Dependent Relationships with Climate and Human Forcing.” _Science of the Total Environment_ 687 (2019): 244–56. https://doi.org/10.1016/j.scitotenv.2019.06.025.

Liu, Ziwei, Hanbo Yang, and Taihua Wang. “A Simple Framework for Estimating the Annual Runoff Frequency Distribution under a Non-Stationarity Condition.” _Journal of Hydrology_, no. July (2020): 125550. [https://doi.org/10.1016/j.jhydrol.2020.125550](https://doi.org/10.1016/j.jhydrol.2020.125550).

Mann, H.B. 1945. Non-parametric tests against trend, Econometrica 13:163-171.

Milly, Author P C D, Julio Betancourt, Malin Falkenmark, Robert M Hirsch, W Zbigniew, Dennis P Lettenmaier, Ronald J Stouffer, and P C D Milly. “Stationarity Is Dead : Stationarity Whither Water Management ?” _Science_ 319, no. 5863 (2008): 573–74. https://doi.org/10.1126/science.1151915.

Sadegh, Majtaba, Jasper A. Vrugt, Xu Xhonggang, and Elena Volpi. “The Stationarity Paradigm Revisited.” _Water Resources Research_, no. 51 (2014): 9207–31. https://doi.org/10.1002/2015WR017408.Received.

Tamaddun, Kazi, Ajay Kalra, and Sajjad Ahmad. “Identification of Streamflow Changes across the Continental United States Using Variable Record Lengths.” _Hydrology_ 3, no. 2 (2016). [https://doi.org/10.3390/hydrology3020024](https://doi.org/10.3390/hydrology3020024).

Zhang, Ke, Gebdang B. Ruben, Xin Li, Zhijia Li, Zhongbo Yu, Jun Xia, and Zengchuan Dong. “A Comprehensive Assessment Framework for Quantifying Climatic and Anthropogenic Contributions to Streamflow Changes: A Case Study in a Typical Semi-Arid North China Basin.” _Environmental Modelling and Software_ 128, no. April (2020): 104704. https://doi.org/10.1016/j.envsoft.2020.104704.

**Data availability**

[https://github.com/jmframe/HydrologicStationarity](https://github.com/jmframe/HydrologicStationarity)



