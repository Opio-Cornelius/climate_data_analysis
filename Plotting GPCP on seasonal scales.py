# Script for plotting GPCP rainfall on seasonal scales
# Importing libraries
import iris
import iris.quickplot as qplt
import iris.plot as iplt
import matplotlib.pyplot as plt
import numpy as np
import iris.coord_categorisation
import cartopy
import cartopy.io.shapereader as shpreader
import cartopy.crs as ccrs
import cartopy.feature as cfeature

#Loading datasets as cubes
cube_gpcp = iris.load('C:/Users/Opio/python_work/data/rectified_data/gpcp_correct.nc')
#print(cube_gpcp)
rain = cube_gpcp[0]
#print(rain)

#Focus on Africa's equatorial belt
min_lon = -70.5; max_lon = 70.5
def lon_range(cell):
    return min_lon <= cell <= max_lon
min_lat = -23; max_lat = 21
def lat_range(cell):
    return min_lat <= cell <= max_lat
Constrain_EqBelt = iris.Constraint(longitude = lon_range, latitude = lat_range)

#Extract Rainfall in the Equatorial Belt of Africa
rain_EB = rain.extract(Constrain_EqBelt)

#Arrange rainfall data by seasons
iris.coord_categorisation.add_season(rain_EB, 'time',name = 'seasons',seasons=('djf','mam','jja','son'))
rain_EB_djf = iris.Constraint(seasons='djf')
rain_EB_djf_sn = rain_EB.extract(rain_EB_djf)

rain_EB_mam = iris.Constraint(seasons='mam')
rain_EB_mam_sn = rain_EB.extract(rain_EB_mam)

rain_EB_jja = iris.Constraint(seasons='jja')
rain_EB_jja_sn = rain_EB.extract(rain_EB_jja)

rain_EB_son = iris.Constraint(seasons='son')
rain_EB_son_sn = rain_EB.extract(rain_EB_son)

# Make a temporal mean so that you can later plot a map out of it
rain_spatial_djf = rain_EB_djf_sn.collapsed(['time'], iris.analysis.MEAN)
rain_spatial_mam = rain_EB_mam_sn.collapsed(['time'], iris.analysis.MEAN)
rain_spatial_jja = rain_EB_jja_sn.collapsed(['time'], iris.analysis.MEAN)
rain_spatial_son = rain_EB_son_sn.collapsed(['time'], iris.analysis.MEAN)

#Plotting
fig = plt.figure(figsize=(8,8))
plt.rcParams["font.family"] = "Times New Roman"
plt.gcf().subplots_adjust(hspace=0, wspace=0.18, top=0.95, bottom=0.3, left=0.08, right=0.88)
ax = plt.subplot(2,2,1, projection=cartopy.crs.PlateCarree())
iplt.contourf(rain_spatial_djf, cmap = plt.cm.Greens, levels=np.arange(0,10,1), extend='max')
plt.gca().set_xticks(np.arange(1,70,5),cartopy.crs.PlateCarree())
plt.gca().set_yticks(np.arange(-20,20,5),cartopy.crs.PlateCarree())
plt.title('December to February')

ax2 = plt.subplot(2,2,2, projection=cartopy.crs.PlateCarree())
iplt.contourf(rain_spatial_mam, cmap = plt.cm.Greens, levels=np.arange(0,10,1), extend='max')
plt.gca().set_xticks(np.arange(1,70,5),cartopy.crs.PlateCarree())
plt.gca().set_yticks(np.arange(-20,20,5),cartopy.crs.PlateCarree())
plt.title('March to May')

ax3 = plt.subplot(2,2,3, projection=cartopy.crs.PlateCarree())
iplt.contourf(rain_spatial_jja, cmap = plt.cm.Greens, levels=np.arange(0,10,1), extend='max')
plt.gca().set_xticks(np.arange(1,70,5),cartopy.crs.PlateCarree())
plt.gca().set_yticks(np.arange(-20,20,5),cartopy.crs.PlateCarree())
plt.title('June to August')

ax4 = plt.subplot(2,2,4, projection=cartopy.crs.PlateCarree())
p4 = iplt.contourf(rain_spatial_son, cmap = plt.cm.Greens, levels=np.arange(0,10,1), extend='max')
plt.gca().set_xticks(np.arange(1,70,5),cartopy.crs.PlateCarree())
plt.gca().set_yticks(np.arange(-20,20,5),cartopy.crs.PlateCarree())
plt.title('September to November')
colorbar_axes = plt.gcf().add_axes([0.92, 0.4, 0.02, 0.45])# [left end, space btn colorbar and plot, right end, thickness]
cb4 = plt.colorbar(p4,colorbar_axes, label='mm/day', orientation='vertical')

#Overlaying Geophysical features
lakes_10m = cfeature.NaturalEarthFeature('physical','lakes','10m',
                                         edgecolor='k',facecolor=cfeature.COLORS['water'])
ax.add_feature(lakes_10m)
ax.add_feature(cartopy.feature.COASTLINE,facecolor='none')
ax.add_feature(cartopy.feature.BORDERS,facecolor='none', linestyle='-', alpha=.9)
ax.add_feature(cartopy.feature.RIVERS)

ax2.add_feature(lakes_10m)
ax2.add_feature(cartopy.feature.COASTLINE,facecolor='none')
ax2.add_feature(cartopy.feature.BORDERS,facecolor='none', linestyle='-', alpha=.9)
ax2.add_feature(cartopy.feature.RIVERS)

ax3.add_feature(lakes_10m)
ax3.add_feature(cartopy.feature.COASTLINE,facecolor='none')
ax3.add_feature(cartopy.feature.BORDERS,facecolor='none', linestyle='-', alpha=.9)
ax3.add_feature(cartopy.feature.RIVERS)

ax4.add_feature(lakes_10m)
ax4.add_feature(cartopy.feature.COASTLINE,facecolor='none')
ax4.add_feature(cartopy.feature.BORDERS,facecolor='none', linestyle='-', alpha=.9)
ax4.add_feature(cartopy.feature.RIVERS)

#Overlaying political features
shpfilename = shpreader.natural_earth(resolution='10m',
                                        category='cultural',name='admin_0_countries')
reader = shpreader.Reader(shpfilename)

#Saving the plot
plt.savefig("GPCP_Equatorial_rain field_seasonal")
