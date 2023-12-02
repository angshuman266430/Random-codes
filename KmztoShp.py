import os
import zipfile
from osgeo import ogr, osr

def kmz_to_shp(kmz_file, output_shp):
    # Step 1: Unzip KMZ to KML
    with zipfile.ZipFile(kmz_file, 'r') as zip_ref:
        zip_ref.extractall("/tmp")
        kml_file = [os.path.join("/tmp", f) for f in zip_ref.namelist() if f.endswith('.kml')][0]

    # Step 2: Convert KML to temporary Shapefile
    driver = ogr.GetDriverByName('KML')
    dataSource = driver.Open(kml_file, 0)
    layer = dataSource.GetLayer()

    outDriver = ogr.GetDriverByName('ESRI Shapefile')
    outDataSource = outDriver.CreateDataSource(output_shp)
    outLayer = outDataSource.CreateLayer(output_shp, geom_type=layer.GetGeomType())

    # Define source and target spatial references
    sourceSR = layer.GetSpatialRef()
    targetSR = osr.SpatialReference()
    targetSR.ImportFromWkt("""PROJCS["NAD_1983_StatePlane_Louisiana_South_FIPS_1702_Feet",GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137,298.257222101]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]],PROJECTION["Lambert_Conformal_Conic"],PARAMETER["False_Easting",3280833.333333333],PARAMETER["False_Northing",0],PARAMETER["Central_Meridian",-91.33333333333333],PARAMETER["Standard_Parallel_1",29.3],PARAMETER["Standard_Parallel_2",30.7],PARAMETER["Latitude_Of_Origin",28.5],UNIT["Foot_US",0.30480060960121924]]""")

    # Coordinate transformation
    coordTrans = osr.CoordinateTransformation(sourceSR, targetSR)

    # Add fields from KML to Shapefile
    layerDefn = layer.GetLayerDefn()
    for i in range(layerDefn.GetFieldCount()):
        outLayer.CreateField(layerDefn.GetFieldDefn(i))

    # Add features to Shapefile with geometries reprojected
    for feature in layer:
        geom = feature.GetGeometryRef()
        geom.Transform(coordTrans)
        feature.SetGeometry(geom)
        outLayer.CreateFeature(feature)

    outDataSource.Destroy()

    # Step 3: Set Projection
    with open(output_shp.replace('.shp', '.prj'), 'w') as prj_file:
        prj_file.write(targetSR.ExportToWkt())

def convert_all_kmz_in_folder(source_folder, target_folder):
    for file in os.listdir(source_folder):
        if file.endswith('.kmz'):
            kmz_file_path = os.path.join(source_folder, file)
            shp_file_path = os.path.join(target_folder, os.path.splitext(file)[0] + '.shp')
            kmz_to_shp(kmz_file_path, shp_file_path)

# Example usage
source_folder = r"Z:\Greenbelt\Report_Figures\Some_GIS\GoogleEarth"
target_folder = r"Z:\Greenbelt\Report_Figures\KMZtoShp"
convert_all_kmz_in_folder(source_folder, target_folder)
