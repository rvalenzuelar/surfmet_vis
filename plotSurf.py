"""
	Module for plotting surface meterology

	Raul Valenzuela
	August, 2015
"""

from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import Thermodyn as thermo
import os

''' set color codes in seaborn '''
sns.set_color_codes()

''' set directory and input files '''
base_directory='/home/rvalenzuela/SURFACE'
print base_directory
usr_case = raw_input('\nIndicate case number (i.e. 1): ')
case='case'+usr_case.zfill(2)
casedir=base_directory+'/'+case
out=os.listdir(casedir)
out.sort()
files=[]
for f in out:
	if f[-3:]=='met': 
		print f
		files.append(f)
usr_location = raw_input('\nIndicate location (i.e. bby): ')
file_met=[]
for f in files:
	if f[:3]==usr_location:
		file_met.append(casedir+'/'+f)
name_field=['press','temp','rh','wspd','wdir','precip','mixr']
if usr_location=='bby':
	index_field=[3,6,9,10,12,17,26]
	locname='Bodega Bay'
	locelevation = 15 # [m]
elif usr_location=='czc':
	index_field=[3,4,5,6,8,13,22]
	locname='Cazadero'
	locelevation = 462 # [m]

def main():

	df=[]
	for f in file_met:
		df.append(parse_dataframe(f))

	if len(df)>1:
		meteo=pd.concat(df)
	else:
		meteo=df[0]

	make_meteo(meteo)
	make_thermo(meteo)

def parse_dataframe(file_met):

	dates_col=[0,1,2]
	dates_fmt='%Y %j %H%M'

	''' read the csv file '''
	dframe = pd.read_csv(file_met,header=None)

	''' parse date columns into a single date col '''
	raw_dates=dframe.ix[:,dates_col]
	raw_dates.columns=['Y','j','HHMM']
	raw_dates['HHMM'] = raw_dates['HHMM'].apply(lambda x:'{0:0>4}'.format(x))
	raw_dates=raw_dates.apply(lambda x: '%s %s %s' % (x['Y'],x['j'],x['HHMM']), axis=1)
	dates=raw_dates.apply(lambda x: datetime.strptime(x, dates_fmt))

	''' make meteo df, assign datetime index, and name columns '''
	meteo=dframe.ix[:,index_field]
	meteo.index=dates
	meteo.columns=name_field

	''' make field with hourly acum precip '''
	hour=pd.TimeGrouper('H')
	preciph = meteo.precip.groupby(hour).sum()
	meteo = meteo.join(preciph, how='outer', rsuffix='h')

	''' add thermodynamics '''
	theta = thermo.theta(C=meteo.temp,hPa=meteo.press)
	thetaeq = thermo.theta_equiv(C=meteo.temp,hPa=meteo.press)
	meteo.loc[:,'theta'] = pd.Series(theta,index=meteo.index)	
	meteo.loc[:,'thetaeq'] = pd.Series(thetaeq,index=meteo.index)	

	''' add sea level pressure '''
	Tv = thermo.virtual_temperature(C=meteo.temp,mixing_ratio=meteo.mixr/1000.)
	slp = thermo.sea_level_press(K=Tv+273.15, Pa=meteo.press*100, m=locelevation)
	meteo.loc[:,'sea_levp']=slp

	''' assign metadata (prototype, not really used) '''
	units = {'press':'mb', 'temp':'C', 'rh':'%', 'wspd':'m s-1', 'wdir':'deg', 'precip':'mm', 'mixr': 'g kg-1'}
	agl = {'press':'NaN', 'temp':'10 m', 'rh':'10 m', 'wspd':'NaN', 'wdir':'NaN', 'precip':'NaN', 'mixr': 'NaN'}
	for n in name_field:
		meteo[n].units=units[n]
		meteo[n].agl=agl[n]
		meteo[n].nan=-9999.999
		meteo[n].sampling_freq='1 minute'	

	return meteo

def make_meteo(meteo):

	x =meteo.index
	temp = pd.rolling_mean(meteo.temp,10)
	rh = pd.rolling_mean(meteo.rh,10)
	wspd = pd.rolling_mean(meteo.wspd,10)
	wdir = pd.rolling_mean(meteo.wdir,10)
	press = meteo.press
	precip = meteo.preciph
	slp = meteo.sea_levp/100 # [hPa]

	labsize=15
	fig, ax = plt.subplots(4,sharex=True,figsize=(8.5,11))
	ax[0].plot(x , temp)	
	ax[0].set_ylabel('Temperature [C]',color='b',fontsize=labsize)
	ax[0].invert_xaxis()
	ax[0].set_ylim([3,13])
	ax2=add_second_yaxis(ax[0], x, rh)
	ax2.set_ylabel('RH [%]',color='g',fontsize=labsize)
	ax2.set_ylim([50,105])
	ax[1].plot(x ,wspd)
	ax[1].set_ylabel('WSPD [ms-1]',color='b',fontsize=labsize)
	ax[1].set_ylim([0,12])
	ax2=add_second_yaxis(ax[1], x , wdir)
	ax2.set_ylabel('WDIR [deg]',color='g',fontsize=labsize)	
	ax2.set_ylim([50,350])	
	ax[2].plot(x, press)
	ax[2].set_ylabel('Pressure [hPa]',color='b',fontsize=labsize)		
	ax[2].yaxis.set_major_formatter(mticker.ScalarFormatter(useOffset=False))
	ax2=add_second_yaxis(ax[2], x , slp)
	ax2.set_ylabel('Sea level pressure [hPa]',color='g',fontsize=labsize)	
	ax2.set_ylim([1010,1022])
	ax[3].plot(x, precip,'o')
	ax[3].set_ylabel('Rain rate [mm h-1]',color='b',fontsize=labsize)	
	ax[3].xaxis.set_major_formatter(mdates.DateFormatter('%d-%H'))
	ax[3].set_xlabel(r'$\Leftarrow$'+' Time (UTC)')
	ax[3].set_ylim([0,12])	

	l1='Surface meteorology at '+ locname
	l2='\nStart time: '+x[0].strftime('%Y-%m-%d %H:%M')+' UTC'
	l3='\nEnd time: '+x[-1].strftime('%Y-%m-%d %H:%M')+' UTC'
	fig.suptitle(l1+l2+l3,y=0.98)

	plt.draw()

def make_thermo(meteo):

	x =meteo.index
	theta = pd.rolling_mean(meteo.theta,10)
	thetaeq = pd.rolling_mean(meteo.thetaeq,10)
	mixr = pd.rolling_mean(meteo.mixr,10)


	labsize=15
	fig, ax = plt.subplots(3,sharex=True,figsize=(8.5,11))
	ax[0].plot(x , theta)	
	ax[0].set_ylabel('Theta [K]',color='b',fontsize=labsize)
	ax[0].set_ylim([276,286])
	ax[0].invert_xaxis()
	ax[1].plot(x ,thetaeq)
	ax[1].set_ylabel('Theta eq. [K]',color='b',fontsize=labsize)	
	ax[1].set_ylim([287,307])
	ax[2].plot(x, mixr)
	ax[2].set_ylabel('Miging ratio [g/kg]',color='b',fontsize=labsize)		
	# ax[2].yaxis.set_major_formatter(mticker.ScalarFormatter(useOffset=False))
	# ax[3].plot(x, precip,'o')
	# ax[3].set_ylabel('Rain rate [mm h-1]',color='b',fontsize=labsize)	
	ax[2].xaxis.set_major_formatter(mdates.DateFormatter('%d-%H'))
	ax[2].set_xlabel(r'$\Leftarrow$'+' Time (UTC)')
	ax[2].set_ylim([4.,8.5])

	
	l1='Surface meteorology at '+ locname
	l2='\nStart time: '+x[0].strftime('%Y-%m-%d %H:%M')+' UTC'
	l3='\nEnd time: '+x[-1].strftime('%Y-%m-%d %H:%M')+' UTC'
	fig.suptitle(l1+l2+l3,y=0.98)

	plt.draw()

def add_second_yaxis(ax,x,y):
	axt=ax.twinx()
	axt.plot(x,y,'g')
	axt.grid(False)	
	return axt



main()
# plt.show()
plt.show(block=False)