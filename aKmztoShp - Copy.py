import os
import zipfile
from osgeo import ogr, osr

def process_layer(layer, outLayer, coordTrans):
    layerDefn = layer.GetLayerDefn()
    for i in range(layerDefn.GetFieldCount()):
        outLayer.CreateField(layerDefn.GetFieldDefn(i))

    for feature in layer:
        geom = feature.GetGeometryRef()
        if geom:
            geom.Transform(coordTrans)
            feature.SetGeometry(geom)
            outLayer.CreateFeature(feature)

def process_kml(kml_file, outDataSource, targetSR):
    driver = ogr.GetDriverByName('KML')
    dataSource = driver.Open(kml_file, 0)

    for layer_idx in range(dataSource.GetLayerCount()):
        layer = dataSource.GetLayerByIndex(layer_idx)
        layerName = os.path.splitext(os.path.basename(kml_file))[0] + "_" + layer.GetName()
        outLayer = outDataSource.CreateLayer(layerName, geom_type=layer.GetGeomType(), srs=targetSR)

        sourceSR = layer.GetSpatialRef()  # Typically, KML uses WGS 84 (EPSG:4326)
        coordTrans = osr.CoordinateTransformation(sourceSR, targetSR)

        process_layer(layer, outLayer, coordTrans)

def kmz_to_shp(kmz_file, output_shp):
    with zipfile.ZipFile(kmz_file, 'r') as zip_ref:
        zip_ref.extractall("/tmp")
        kml_files = [os.path.join("/tmp", f) for f in zip_ref.namelist() if f.endswith('.kml')]

    os.makedirs(os.path.dirname(output_shp), exist_ok=True)

    outDriver = ogr.GetDriverByName('ESRI Shapefile')
    outDataSource = outDriver.CreateDataSource(output_shp)

    # Define the target coordinate system (NAD 1983 StatePlane Louisiana South FIPS 1702 Feet)
    targetSR = osr.SpatialReference()
    wkt = """PROJCS["NAD_1983_StatePlane_Louisiana_South_FIPS_1702_Feet",GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137,298.257222101]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]],PROJECTION["Lambert_Conformal_Conic"],PARAMETER["False_Easting",3280833.333333333],PARAMETER["False_Northing",0],PARAMETER["Central_Meridian",-91.33333333333333],PARAMETER["Standard_Parallel_1",29.3],PARAMETER["Standard_Parallel_2",30.7],PARAMETER["Latitude_Of_Origin",28.5],UNIT["Foot_US",0.30480060960121924]]"""
    targetSR.ImportFromWkt(wkt)

    for kml_file in kml_files:
        process_kml(kml_file, outDataSource, targetSR)

    outDataSource.Destroy()

kmz_file = r"Z:\Greenbelt\Report_Figures\Greenbelt_Report_database\Some_GIS\Preferred Southern Route.kmz"
output_shp = r"Z:\Greenbelt\Report_Figures\Greenbelt_Report_database\Some_GIS\Preferred Southern Route.shp"
kmz_to_shp(kmz_file, output_shp)
