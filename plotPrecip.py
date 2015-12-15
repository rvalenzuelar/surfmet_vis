
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
import Meteoframes as mf
import os
import numpy as np

from datetime import datetime
from glob import glob

base_directory='/home/rvalenzuela/SURFACE'
# base_directory='/Users/raulv/Documents/SURFACE'
usr_case=[]

def main():

	file_met=get_files()
	dfBBY=[]
	dfCZD=[]
	index_field, name_field = get_index_field(usr_case)
	for f in file_met:
		loc=f[-12:-9]
		if loc=='bby':
			dfBBY.append(mf.parse_surface(f,index_field[loc],name_field,15))
		elif loc=='czc':
			dfCZD.append(mf.parse_surface(f,index_field[loc],name_field,462))

	if len(dfBBY)>1:
		meteoBBY=pd.concat(dfBBY)
	else:
		meteoBBY=dfBBY[0]	

	if len(dfCZD)>1:
		meteoCZD=pd.concat(dfCZD)
	else:
		meteoCZD=dfCZD[0]	

	# plot_compare_hourly(BBY=meteoBBY,CZD=meteoCZD)
	plot_compare_accum(BBY=meteoBBY,CZD=meteoCZD)

	plt.show(block=False)

def plot_compare_hourly(**kwargs):

	bby=kwargs['BBY']
	czd=kwargs['CZD']
	
	''' remove rows with nan '''
	bby = bby[np.isfinite(bby['preciph'])]
	czd = czd[np.isfinite(czd['preciph'])]

	bby_precip = bby.preciph
	czd_precip = czd.preciph

	xbby = bby.index
	xczd = czd.index
	
	sptime = raw_input('\nSpecific time? (y/n): ')	
	if sptime=='y':
		st = raw_input('Start time? (dd,hh): ').split(',')
		en = raw_input('End time? (dd,hh): ').split(',')
		stD=int(st[0])
		stH=int(st[1])
		enD=int(en[0])
		enH=int(en[1])
		Y=xbby[0].year
		m=xbby[0].month
		stidx=np.where(xbby == pd.Timestamp(datetime(Y,m,stD,stH)))
		enidx=np.where(xbby == pd.Timestamp(datetime(Y,m,enD,enH)))
	else:
		stidx=0
		enidx=-1

	labsize=15
	fig,ax = plt.subplots()
	dt=pd.Timedelta('30 minutes')
	ln1=ax.plot(xbby+dt, bby_precip,'-o')
	ln2=ax.plot(xczd+dt, czd_precip,'-o')
	ax.xaxis.set_major_formatter(mdates.DateFormatter('%d\n%H'))
	datetext=xbby[0].strftime('%Y-%b')
	ax.text(0.03,0.95,'Date: '+datetext,weight='bold',size=18,transform=ax.transAxes)
	ax.set_xlabel(r'$\Leftarrow$'+'Time (UTC)',fontsize=labsize)
	ax.set_ylabel('Rain rate [mm h-1]',color='k',fontsize=labsize)	
	ax.set_ylim([0,22])	
	ax.set_xlim([xbby[stidx],xbby[enidx]+pd.Timedelta('1 hour')])	
	ax.invert_xaxis()
	plt.legend(ln1+ln2,['BBY','CZD'],prop={'size':18})
	fig.subplots_adjust(bottom=0.15, top=0.95, left=0.1,right=0.95)

def plot_compare_accum(**kwargs):

	global usr_case

	bby=kwargs['BBY']
	czd=kwargs['CZD']

	bby_paccum=bby.precip.cumsum()
	czd_paccum=czd.precip.cumsum()

	# print np.max(np.diff(bby_paccum.index))
	# print np.where(np.diff(bby_paccum.index)>np.min(np.diff(bby_paccum.index)))

	# print np.max(np.diff(czd_paccum.index))
	# print np.where(np.diff(czd_paccum.index)>np.min(np.diff(czd_paccum.index)))

	fig,ax=plt.subplots()
	ax.plot(bby_paccum,label='bby')
	ax.plot(czd_paccum,label='czd')
	ax.grid()
	plt.legend()
	plt.suptitle('case '+usr_case)
	plt.draw()

	fig,ax=plt.subplots()
	ax.plot(bby.precip,marker='o', linestyle='None', label='bby')
	ax.plot(czd.precip,marker='o', linestyle='None', label='czd')
	ax.grid()
	plt.legend()
	plt.suptitle('case '+usr_case)
	plt.draw()

	fig,ax=plt.subplots()
	ax.scatter(bby_paccum, czd_paccum, color='blue', s=30, edgecolor='None',alpha=0.9)
	mmax = np.amax([np.max(bby_paccum), np.max(czd_paccum)])
	ax.set_xlim([0,mmax])
	ax.set_ylim([0,mmax])
	ax.set_xlabel('bby')
	ax.set_ylabel('czd')
	ax.grid()
	plt.suptitle('case '+usr_case)
	plt.draw()

def get_files():

	global usr_case
	print base_directory
	usr_case = raw_input('\nIndicate case number (i.e. 1): ')
	case='case'+usr_case.zfill(2)
	casedir=base_directory+'/'+case
	out=glob(casedir+'/*.met')
	out.sort()
	return out

def get_index_field(usr_case):
	
	if usr_case in ['1','2']:
		index_field={'bby':[3,4,10,5,6,11,13],'czc':[3,4,10,5,6,11,13]}
	elif usr_case in ['3','4','5','6','7']: 
		index_field={'bby':[3,5,8,10,12,17,26],'czc':[3,4,5,6,8,13,22]}
	else:
		index_field={'bby':[3,4,5,6,8,13,15],'czc':[3,4,5,6,8,13,15]}

	name_field=['press','temp','rh','wspd','wdir','precip','mixr']

	return index_field, name_field

def get_request_dates(usr_case):

	reqdates={ '1': {'ini':[1998,1,18,15],'end':[1998,1,18,20]},
				'2': {'ini':[1998,1,26,4],'end':[1998,1,26,9]},
				'3': {'ini':[2001,1,23,21],'end':[2001,1,24,2]},
				'4': {'ini':[2001,1,25,15],'end':[2001,1,25,20]},
				'5': {'ini':[2001,2,9,10],'end':[2001,2,9,15]},
				'6': {'ini':[2001,2,11,3],'end':[2001,2,11,8]},
				'7': {'ini':[2001,2,17,17],'end':[2001,2,17,22]},
				'8': {'ini':[2003,1,12,15],'end':[2003,1,12,20]},
				'9': {'ini':[2003,1,22,18],'end':[2003,1,22,23]},
				'10': {'ini':[2003,2,16,0],'end':[2003,2,16,5]},
				'11': {'ini':[2004,1,9,17],'end':[2004,1,9,22]},
				'12': {'ini':[2004,2,2,12],'end':[2004,2,2,17]},
				'13': {'ini':[2004,2,17,14],'end':[2004,2,17,19]},
				'14': {'ini':[2004,2,25,8],'end':[2004,2,25,13]}
				}	

	return reqdates[usr_case]

main()