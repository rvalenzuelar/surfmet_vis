
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
import Meteoframes as mf
import os
import numpy as np
import statsmodels.api as sm

from datetime import datetime,timedelta
from glob import glob
from matplotlib.backends.backend_pdf import PdfPages

base_directory='/home/rvalenzuela/SURFACE'
# base_directory='/Users/raulv/Documents/SURFACE'
usr_case=[] # set within get_index_field

def main():

	# global usr_case
	# plot_compare_accum(period=True)


	# fig,ax=plt.subplots(2,1,figsize=(7,11))
	# plot_compare_sum(ax=ax[0],minutes=30, period=True)
	# plot_regression(ax=ax[1],minutes=30, period=True)
	# plt.show(block=False)



	# ppsurf=PdfPages('surf_precipsum_multipage.pdf')
	# ncases=range(1,15)
	# # ncases=[1,2,3]
	# for c in ncases:
	# 	fig,ax=plt.subplots()
	# 	plot_compare_sum(ax=ax,usr_case=str(c), ylim=[0,14], minutes=30, period=True)
	# 	ppsurf.savefig()
	# 	plt.close('all')
	# ppsurf.close()

	# ppsurf=PdfPages('surf_precipreg_multipage.pdf')
	# ncases=range(1,15)
	# # ncases=[1,2,3]
	# for c in ncases:
	# 	fig,ax=plt.subplots()
	# 	plot_regression(ax=ax,usr_case=str(c), minutes=30, period=True)
	# 	ppsurf.savefig()
	# 	plt.close('all')
	# ppsurf.close()


def plot_compare_accum(**kwargs):

	global usr_case

	bby, czd = get_data()
	period=kwargs['period']

	if period:
		period = get_request_dates(usr_case)
		ini = period['ini']
		end = period['end']
		inix = bby.index.get_loc(datetime(ini[0],ini[1],ini[2],ini[3],0))
		endx = bby.index.get_loc(datetime(end[0],end[1],end[2],end[3],0))		
	else:
		inix=0
		endx=-1

	bby_paccum=bby[inix:endx].precip.cumsum()
	czd_paccum=czd[inix:endx].precip.cumsum()

	reg = get_regression(bby_paccum.values,czd_paccum.values)
	print 'm={:3.2f}, Rsq={:3.2f}, n={:d}'.format(reg[0],reg[1],reg[2])

	fig,ax=plt.subplots()
	ax.plot(bby_paccum,label='BBY')
	ax.plot(czd_paccum,label='CZD')
	ax.grid()
	plt.legend()
	plt.suptitle('Accumulated precip case '+usr_case)
	plt.draw()

	fig,ax=plt.subplots()
	ax.scatter(bby_paccum, czd_paccum, color='blue', s=30, edgecolor='None',alpha=0.9)
	ax.plot(range(len(bby_paccum)),color='black',linestyle='--',linewidth=3)
	mmax = np.amax([np.max(bby_paccum), np.max(czd_paccum)])
	ax.set_xlim([0,mmax])
	ax.set_ylim([0,mmax])
	ax.set_xlabel('bby')
	ax.set_ylabel('czd')
	ax.grid()
	plt.suptitle('case '+usr_case)
	plt.draw()


def plot_compare_sum(ax=None,usr_case=None,ylim=None,**kwargs):

	if ax is None:
		ax=plt.gca()

	bby,czd,usr_case = get_data(usr_case)
	minutes=kwargs['minutes']
	period=kwargs['period']
	timeg=pd.TimeGrouper(str(minutes)+'T')
	bbyg = bby.precip.groupby(timeg).sum()
	czdg = czd.precip.groupby(timeg).sum()
	
	'representative time is half the period grouped'
	timed = timedelta(minutes=minutes/2)

	xg=bbyg.index+timed
	ln1=ax.plot(xg, bbyg,'-o')
	ln2=ax.plot(xg, czdg,'-o')
	ax.xaxis.set_major_formatter(mdates.DateFormatter('%d\n%H'))
	labsize=15
	ax.set_xlabel(r'$\Leftarrow$'+'Time (UTC)',fontsize=labsize)
	ax.set_ylabel('Rain rate [mm freq-1]',color='k',fontsize=labsize)	
	ax.grid()
	if period:
		period = get_request_dates(usr_case)
		ini = period['ini']
		end = period['end']
		inix = bbyg.index.get_loc(datetime(ini[0],ini[1],ini[2],ini[3],0))
		endx = bbyg.index.get_loc(datetime(end[0],end[1],end[2],end[3],0))
		ax.set_xlim([xg[inix]-timed, xg[endx]-timed])
		y=bbyg[inix:endx+1].values
		x=czdg[inix:endx+1].values
		reg = get_regression(x,y)
		bbyg=bbyg.ix[inix:endx+1]
		czdg=czdg.ix[inix:endx+1]
	ax.invert_xaxis()
	if ylim is not None:
		ax.set_ylim([ylim[0], ylim[1]])
	datetext=xg[0].strftime('%Y-%b')
	freqtext=' Frequency: '+str(minutes)+' minutes'		
	plt.suptitle('Case '+usr_case+' date: '+datetext+freqtext)
	if usr_case=='1':
		ax.legend(ln1+ln2,['BBY','CZD'],prop={'size':18},loc='best')
	plt.subplots_adjust(bottom=0.15, top=0.95, left=0.1,right=0.95)


def plot_regression(ax=None,usr_case=None,**kwargs):

	if ax is None:
		ax=plt.gca()

	bby,czd,usr_case = get_data(usr_case)
	minutes=kwargs['minutes']
	period=kwargs['period']
	timeg=pd.TimeGrouper(str(minutes)+'T')
	bbyg = bby.precip.groupby(timeg).sum()
	czdg = czd.precip.groupby(timeg).sum()

	'representative time is half the period grouped'
	timed = timedelta(minutes=minutes/2)

	xg=bbyg.index+timed
	if period:
		period = get_request_dates(usr_case)
		ini = period['ini']
		end = period['end']
		inix = bbyg.index.get_loc(datetime(ini[0],ini[1],ini[2],ini[3],0))
		endx = bbyg.index.get_loc(datetime(end[0],end[1],end[2],end[3],0))
		y=bbyg[inix:endx].values
		x=czdg[inix:endx].values
		reg = get_regression(x,y)
		bbyg=bbyg.ix[inix:endx]
		czdg=czdg.ix[inix:endx]

	ax.scatter(bbyg,czdg,color='blue')
	bbyg_max=np.max(bbyg)
	czdg_max=np.max(czdg)
	regtext='m={:3.2f}, Rsq={:3.2f}, n={:d}'.format(reg[0],reg[1],reg[2])
	str_times=xg[inix].strftime('%dT%H:00 - ')+xg[endx].strftime('%dT%H:00 UTC')
	ax.text(0.3,0.95,str_times, size=15, transform=ax.transAxes)
	ax.text(0.4,0.1,regtext,weight='bold', size=18, transform=ax.transAxes)
	vmax=int(np.ceil(np.maximum(bbyg_max,czdg_max)))
	ax.plot(range(-1,15),range(-1,15),color='black')
	ax.set_xlim([-0.1,vmax])
	ax.set_ylim([-0.1,vmax])
	ax.set_xlabel('BBY')
	ax.set_ylabel('CZD')
	ax.grid()
	ax.set_xlim([-0.5,14])
	ax.set_ylim([-0.5,14])
	datetext=xg[0].strftime('%Y-%b')
	freqtext=' Frequency: '+str(minutes)+' minutes'		
	plt.suptitle('Case '+usr_case+' date: '+datetext+freqtext)	
	plt.subplots_adjust(bottom=0.1, top=0.95, left=0.1,right=0.95)

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

def get_files(usr_case=None):

	if usr_case is None:
		print base_directory
		usr_case = raw_input('\nIndicate case number (i.e. 1): ')

	case='case'+usr_case.zfill(2)
	casedir=base_directory+'/'+case
	out=glob(casedir+'/*.met')
	out.sort()
	return out,usr_case

def get_index_field(usr_case):
	
	if usr_case in ['1','2']:
		index_field={'bby':[3,4,10,5,6,11,13],'czc':[3,4,10,5,6,11,13]}
	elif usr_case in ['3','4','5','6','7']: 
		index_field={'bby':[3,5,8,10,12,17,26],'czc':[3,4,5,6,8,13,22]}
	else:
		index_field={'bby':[3,4,5,6,8,13,15],'czc':[3,4,5,6,8,13,15]}

	name_field=['press','temp','rh','wspd','wdir','precip','mixr']

	return index_field, name_field

def get_data(usr_case=None):

	file_met,usr_case=get_files(usr_case)
	index_field, name_field = get_index_field(usr_case)
	dfBBY=[]
	dfCZD=[]
	period = get_request_dates(usr_case)
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

	return meteoBBY, meteoCZD, usr_case

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

def get_regression(x,y):

	model=sm.OLS(x, y)
	result=model.fit()
	m=result.params[0]
	Rsq=result.rsquared
	Nobs=int(result.nobs)	

	return [m,Rsq,Nobs]

main()