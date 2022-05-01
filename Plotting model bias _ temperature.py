# Script for plotting model bias in temperature (HadCM3 against CRU)
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

cube_HadCM3 = iris.load_cube('C:/Users/Opio/python_work/data/rectified_data/HadCM3_temp_correct.nc')

#Changing units from Kelvins to degrees celcius
cube_HadCM3.data = cube_HadCM3.data - 273.15
cube_HadCM3.units = "degrees Celsius"
cube_cru = iris.load('C:/Users/Opio/python_work/data/rectified_data/cru_temp_time.nc')
obs_temp = cube_cru[0]

#Focus on Africa's equatorial belt
min_lon = -20.5; max_lon = 60.5
def lon_range(cell):
    return min_lon <= cell <= max_lon
min_lat = -23; max_lat = 21
def lat_range(cell):
    return min_lat <= cell <= max_lat
Constrain_EqBelt = iris.Constraint(longitude = lon_range, latitude = lat_range)
# Extract by Equatorial Belt Constraint
model_temp_EB = cube_HadCM3.extract(Constrain_EqBelt)
obs_temp_EB = obs_temp.extract(Constrain_EqBelt)

#Arrange data by seasons
iris.coord_categorisation.add_season(model_temp_EB, 'time', name = 'seasons', seasons=('djf','mam','jja','son'))
model_temp_EB_djf = iris.Constraint(seasons='djf')
model_temp_EB_djf_sn = model_temp_EB.extract(model_temp_EB_djf)
model_temp_EB_mam = iris.Constraint(seasons='mam')
model_temp_EB_mam_sn = model_temp_EB.extract(model_temp_EB_mam)
model_temp_EB_jja = iris.Constraint(seasons='jja')
model_temp_EB_jja_sn = model_temp_EB.extract(model_temp_EB_jja)
model_temp_EB_son = iris.Constraint(seasons='son')
model_temp_EB_son_sn = model_temp_EB.extract(model_temp_EB_son)

iris.coord_categorisation.add_season(obs_temp_EB, 'time', name = 'seasons')
obs_temp_EB_djf = iris.Constraint(seasons='djf')
obs_temp_EB_djf_sn = obs_temp_EB.extract(obs_temp_EB_djf)
obs_temp_EB_mam = iris.Constraint(seasons='mam')
obs_temp_EB_mam_sn = obs_temp_EB.extract(obs_temp_EB_mam)
obs_temp_EB_jja = iris.Constraint(seasons='jja')
obs_temp_EB_jja_sn = obs_temp_EB.extract(obs_temp_EB_jja)
obs_temp_EB_son = iris.Constraint(seasons='son')
obs_temp_EB_son_sn = obs_temp_EB.extract(obs_temp_EB_son)

#Make a temporal mean so that you can later do a spatial map
model_temp_2D_djf = model_temp_EB_djf_sn.collapsed(['time'], iris.analysis.MEAN)
model_temp_2D_mam = model_temp_EB_mam_sn.collapsed(['time'], iris.analysis.MEAN)
model_temp_2D_jja = model_temp_EB_jja_sn.collapsed(['time'], iris.analysis.MEAN)
model_temp_2D_son = model_temp_EB_son_sn.collapsed(['time'], iris.analysis.MEAN)

obs_temp_2D_djf = obs_temp_EB_djf_sn.collapsed(['time'], iris.analysis.MEAN)
obs_temp_2D_mam = obs_temp_EB_mam_sn.collapsed(['time'], iris.analysis.MEAN)
obs_temp_2D_jja = obs_temp_EB_jja_sn.collapsed(['time'], iris.analysis.MEAN)
obs_temp_2D_son = obs_temp_EB_son_sn.collapsed(['time'], iris.analysis.MEAN)

# Calculate Bias
bias_djf = model_temp_2D_djf - obs_temp_2D_djf
bias_mam = model_temp_2D_mam - obs_temp_2D_mam
bias_jja = model_temp_2D_jja - obs_temp_2D_jja
bias_son = model_temp_2D_son - obs_temp_2D_son

#Typeset the units
bias_djf.units = "Degrees Celsius"
bias_mam.units = "Degrees Celsius"
bias_jja.units = "Degrees Celsius"
bias_son.units = "Degrees Celsius"

#Plotting
fig = plt.figure(figsize=(8,8), dpi=200)
plt.rcParams["font.family"] = "Times New Roman"
plt.gcf().subplots_adjust(hspace=0.3, wspace=0.18, top=0.95, bottom=0.42, left=0.08, right=0.88)
ax1 = plt.subplot(2,2,1, projection=cartopy.crs.PlateCarree())
iplt.contourf(bias_djf, cmap = plt.cm.seismic, levels=np.arange(-10,10,1), extend='max')
plt.gca().set_xticks(np.arange(-20,60,10),cartopy.crs.PlateCarree())
plt.gca().set_yticks(np.arange(-22,20,5),cartopy.crs.PlateCarree())
plt.title('December to February')

ax2 = plt.subplot(2,2,2, projection=cartopy.crs.PlateCarree())
iplt.contourf(bias_mam, cmap = plt.cm.seismic, levels=np.arange(-10,10,1), extend='max')
plt.gca().set_xticks(np.arange(-20,60,10),cartopy.crs.PlateCarree())
plt.gca().set_yticks(np.arange(-22,20,5),cartopy.crs.PlateCarree())
plt.title('March to May')

ax3 = plt.subplot(2,2,3, projection=cartopy.crs.PlateCarree())
iplt.contourf(bias_jja, cmap = plt.cm.seismic, levels=np.arange(-10,10,1), extend='max')
plt.gca().set_xticks(np.arange(-20,60,10),cartopy.crs.PlateCarree())
plt.gca().set_yticks(np.arange(-22,20,5),cartopy.crs.PlateCarree())
plt.title('June to August')

ax4 = plt.subplot(2,2,4, projection=cartopy.crs.PlateCarree())
p4 = iplt.contourf(bias_son, cmap = plt.cm.seismic, levels=np.arange(-10,10,1), extend='both')
plt.gca().set_xticks(np.arange(-20,60,10),cartopy.crs.PlateCarree())
plt.gca().set_yticks(np.arange(-22,20,5),cartopy.crs.PlateCarree())
plt.title('September to November')
colorbar_axes = plt.gcf().add_axes([0.15, 0.35, 0.65, 0.02])# [left end, space btn colorbar and plot, right end, thickness]
cb4 = plt.colorbar(p4,colorbar_axes, label='Degrees Celsius', orientation='horizontal')

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
#ax2.add_feature(cartopy.feature.RIVERS)

ax3.add_feature(lakes_10m)
ax3.add_feature(cartopy.feature.COASTLINE,facecolor='none')
ax3.add_feature(cartopy.feature.BORDERS,facecolor='none', linestyle='-', alpha=.5)
#ax3.add_feature(cartopy.feature.RIVERS)

ax4.add_feature(lakes_10m)
ax4.add_feature(cartopy.feature.COASTLINE,facecolor='none')
ax4.add_feature(cartopy.feature.BORDERS,facecolor='none', linestyle='-', alpha=.5)
#ax4.add_feature(cartopy.feature.RIVERS)

#Overlaying political features
shpfilename = shpreader.natural_earth(resolution='10m',
                                        category='cultural',name='admin_0_countries')
reader = shpreader.Reader(shpfilename)

#Saving the plot
plt.savefig("Temperature_Bias_HadCM3_against_CRU")




