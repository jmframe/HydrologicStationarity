var usa = ee.FeatureCollection("USDOS/LSIB_SIMPLE/2017")
           .filter(ee.Filter.eq('country_na', 'United States'));
var mk = ee.FeatureCollection('users/jmframe/mk-results');
Map.addLayer(mk);
print(mk);

var int1 = mk.kriging({
  propertyName: 'Q/P',
  shape: 'exponential',
  range: 400000,
  sill: 1.0,
  nugget: 0.1,
  maxDistance: 400000,
  reducer: 'mean',
});
var qp = int1.clip(usa);
var style1 = {
  min:-3,
  max:3,
  palette:['red','white','blue']
};
Map.addLayer(qp, style1, 'Q/P');

var int2 = mk.kriging({
  propertyName: 'tree_canopy_cover',
  shape: 'exponential',
  range: 400000,
  sill: 1.0,
  nugget: 0.1,
  maxDistance: 400000,
  reducer: 'mean',
});
var tree = int2.clip(usa);
var style2 = {
  min:-3,
  max:3,
  palette:['brown','white','green']
};
Map.addLayer(tree, style2, 'forest_cover');

var int2 = mk.kriging({
  propertyName: 'impervious',
  shape: 'exponential',
  range: 400000,
  sill: 1.0,
  nugget: 0.1,
  maxDistance: 400000,
  reducer: 'mean',
});
var tree = int2.clip(usa);
var style2 = {
  min:-3,
  max:3,
  palette:['green','white','grey']
};
Map.addLayer(tree, style2, 'impervious');

var int2 = mk.kriging({
  propertyName: 'skin_temperature',
  shape: 'exponential',
  range: 400000,
  sill: 1.0,
  nugget: 0.1,
  maxDistance: 400000,
  reducer: 'mean',
});
var tree = int2.clip(usa);
var style2 = {
  min:-3,
  max:3,
  palette:['#20B2AA','white','#800000']
};
Map.addLayer(tree, style2, 'skin_temperature');
