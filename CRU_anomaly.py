#Script for plotting CRU annual temperature anomaly
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

cube_cru = iris.load('C:/Users/Opio/python_work/data/cru/cru_1901_2016.nc')
cru_orig = cube_cru[0]
cube_2010 = iris.load('C:/Users/Opio/python_work/data/cru/cru_2010.nc')
temp_2010 = cube_2010[0]
cube_2011 = iris.load('C:/Users/Opio/python_work/data/cru/cru_2011.nc')
temp_2011 = cube_2011[0]

#Focus on East Africa
min_lon = 7.5; max_lon = 52.5
def lon_range(cell):
    return min_lon <= cell <= max_lon
min_lat = -23; max_lat = 21
def lat_range(cell):
    return min_lat <= cell <= max_lat
Constrain_EA = iris.Constraint(longitude = lon_range, latitude = lat_range)

#Extreact out East Africa
cru_orig_EA = cru_orig.extract(Constrain_EA)
temp_2010_EA = temp_2010.extract(Constrain_EA)
temp_2011_EA = temp_2011.extract(Constrain_EA)

#Calculate temporal mean for CRU original dataset 1901 to 2016
cru_long_term = cru_orig_EA.collapsed(['time'], iris.analysis.MEAN)
temp_2010_EA_2D = temp_2010_EA.collapsed(['time'], iris.analysis.MEAN)
temp_2011_EA_2D = temp_2010_EA.collapsed(['time'], iris.analysis.MEAN)

#Calculate standard deviation for CRU original dataset 1901 to 2016
cru_sd = cru_orig_EA.collapsed(['time'], iris.analysis.STD_DEV)

#Calculate Anomaly
cru_2010_anom = (temp_2010_EA_2D - cru_long_term)/cru_sd
cru_2011_anom = (temp_2011_EA_2D - cru_long_term)/cru_sd

#Plotting
fig = plt.figure(figsize=(8,8), dpi=200)
plt.rcParams["font.family"] = "Times New Roman"
plt.gcf().subplots_adjust(hspace=0.3, wspace=0.18, top=0.95, bottom=0.42, left=0.08, right=0.88)
ax1 = plt.subplot(1,2,1, projection=cartopy.crs.PlateCarree())
iplt.contourf(cru_2010_anom, cmap = plt.cm.YlOrRd, levels=np.arange(0,1.6,0.2), extend='max')
plt.gca().set_xticks(np.arange(8,50,10),cartopy.crs.PlateCarree())
plt.gca().set_yticks(np.arange(-22,20,10),cartopy.crs.PlateCarree())
plt.title('2010')

ax2 = plt.subplot(1,2,2, projection=cartopy.crs.PlateCarree())
p2 = iplt.contourf(cru_2011_anom, cmap = plt.cm.YlOrRd, levels=np.arange(0,1.6,0.2), extend='max')
plt.gca().set_xticks(np.arange(8,50,10),cartopy.crs.PlateCarree())
plt.gca().set_yticks(np.arange(-22,20,10),cartopy.crs.PlateCarree())
plt.title('2011')
colorbar_axes = plt.gcf().add_axes([0.15, 0.42, 0.65, 0.02])# [left end, space btn colorbar and plot, right end, thickness]
cb2 = plt.colorbar(p2,colorbar_axes, label='Degrees Celsius', orientation='horizontal')

#Overlaying Geophysical features
lakes_10m = cfeature.NaturalEarthFeature('physical','lakes','10m',
                                         edgecolor='k', facecolor='none')
ax1.add_feature(lakes_10m)
ax1.add_feature(cartopy.feature.COASTLINE,facecolor='none')
ax1.add_feature(cartopy.feature.BORDERS,facecolor='none', linestyle='-', alpha=.5)
#ax1.add_feature(cartopy.feature.RIVERS)

ax2.add_feature(lakes_10m)
ax2.add_feature(cartopy.feature.COASTLINE,facecolor='none')
ax2.add_feature(cartopy.feature.BORDERS,facecolor='none', linestyle='-', alpha=.5)

#Overlaying political features
shpfilename = shpreader.natural_earth(resolution='10m',
                                        category='cultural',name='admin_0_countries')
reader = shpreader.Reader(shpfilename)

#Saving the plot
plt.savefig("2010_&_2011_CRU tempearure anomalies")