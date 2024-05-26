# mineral_resource_detection
mineral_resource_classifier


Broad instructions were to bring a machine learning worfklow from Google Earth Engine (GEE) into DEP. In November through trial and error, we found that this requires having pre-generated input training images. The approach would be more complicated than the GEE approach and the approaches used in the Tonga workshop which both did not work in the analytics hub. As a result, there were three potential ways to prepare the input datasets (cloudless mosaics):

1. depal functions (same methods for Tonga workshop to download using depal functions) 
- a. First - tried to define using boundary for all of Fiji but this had a dateline issue.
- b. Next tried a bounding box that ignored the Eastern Islands. The first aoi included rotuma (2 training data points), the second aoi excluded rotuma (too much ocean).
- c. There is greater capacity to incorporate this training data into GEE than DEP. So we will need to make some adjustments to allow DEP to do this. 
`training_image_2022 = dep.get_landcover_mosaic(aoi, year="2022", resolution=10, coastal_clip=False)`  
- d. When using a dask cluster to try and run this and generate a mosaic the analytics hub still times out. 

2. Method for downloading mangroves from STAC items
- a. After checking on blob storage it looks like the STAC items for Sentinel Mosaics only covers one year (2022 or 2023?) for Fiji. So this approach doesn’t seem useful yet. 

3. Method for GeoMads from tiles
- a. Geomedians should be more statistically robust than cloudless mosaics. 
- b. Looking into the GeoMAD approach but this is only available for Landsat at the moment. 
- c. Will be retrofitted with Sentinel at a later date pending work from Alex.


Work in this repo is based on some of the work from November-December 2023. Many of the notebooks were lost due to unexpected clearing of all disk data on the staging platform. New notebooks have been copied onto this from nmetherall's own repository. 

