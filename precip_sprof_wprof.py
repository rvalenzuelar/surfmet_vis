''' 	Analysis of surface precip and 
	sprof data

	Raul Valenzuela
	December 2015
'''

import matplotlib.pyplot as plt
import statistical_sprof as sprof
import pandas as pd
import plotPrecip as precip
import numpy as np
import statsmodels.api as sm
import read_partition
import plotWindprof2 as wprof

from datetime import timedelta
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import interp1d

def main():

	cprecip=get_dataframe(range(1,15),minutes=60)
	# cprecip=get_dataframe([9],minutes=60)

	# print (np.isnan(cprecip.ratio)) and (cprecip.czdp==0.)
	
	# foo= cprecip[np.isnan(cprecip.ratio)]
	# print foo[(foo.czdp>0.)]
	# print len(foo[(foo.czdp>0.)])

	# print len(cprecip[np.isnan(cprecip.ratio) and cprecip.czdp==0.])

	# fig,ax=plt.subplots(figsize=(8,8))
	# # plot_scatter2D(df=cprecip,ax=ax, target='echotvar', thres=0.04)
	# # plot_scatter2D(df=cprecip,ax=ax, target='dbzvar', thres=2.)
	# plot_scatter2D(df=cprecip,ax=ax, target='vvelvar', thres=0.08)
	# plt.show(block=False)
	
	# fig = plt.figure(figsize=(8,8))
	# ax=fig.add_subplot(111,projection='3d')
	# x=cprecip['echotvar']
	# y=cprecip['vvelvar']
	# z=cprecip['dbzvar']
	# plot_scatter3D(x=x,y=y,z=z,ax=ax)
	# plt.show(block=False)
	return cprecip
	plot_wdir_wspd_23(cprecip=cprecip)


def plot_wdir_wspd_23(cprecip=None):

	txt = ['Sfc', '0.25 km','1.25 km','1.75 km','2.50 km','3.50 km']
	x1 = [	cprecip.wdSfc, cprecip.wd025,	cprecip.wd125,
			cprecip.wd175, cprecip.wd250,	cprecip.wd350]
	x2 = [	cprecip.wsSfc, cprecip.ws025,	cprecip.ws125,
			cprecip.ws175, cprecip.ws250,	cprecip.ws350]

	fig, axg = plt.subplots(3,2,figsize=(10,8),sharex=True,sharey=True)
	ax=np.reshape(axg,(6,1))
	for n,a in enumerate(ax):
		a=a[0]
		a.scatter(x1[n], cprecip.ratioCB,label='BBY')
		a.scatter(x1[n], cprecip.ratioCF,color='r',label='FRS')
		a.text(0.05,0.95,txt[n],weight='bold',transform=a.transAxes)
		if n == 0: a.set_ylabel('CZD/x ratio')
		if n == 5:
			a.set_xlabel('wind direction')
			a.set_xticks(range(0,360,30))
	lg=plt.legend(frameon=True)
	lg.get_frame().set_facecolor('white')
	plt.subplots_adjust(wspace=0.05, hspace=0.05,bottom=0.05,top=0.95)
	plt.suptitle('Hourly precip ratio (surf obs) vs wind direction (windprof)')
	plt.show(block=False)

	fig, axg = plt.subplots(3,2,figsize=(10,8),sharex=True,sharey=True)
	ax=np.reshape(axg,(6,1))
	for n,a in enumerate(ax):
		a=a[0]
		a.scatter(x2[n], cprecip.ratioCB,label='BBY')
		a.scatter(x2[n], cprecip.ratioCF,color='r',label='FRS')
		a.text(0.05,0.95,txt[n],weight='bold',transform=a.transAxes)
		if n == 0: a.set_ylabel('CZD/x ratio')
		if n == 5: a.set_xlabel('wind speed')
	lg=plt.legend(frameon=True)
	lg.get_frame().set_facecolor('white')		
	plt.subplots_adjust(wspace=0.05, hspace=0.05,bottom=0.05,top=0.95)
	plt.suptitle('Hourly precip ratio (surf obs) vs wind speed (windprof)')
	plt.show(block=False)



def plot_wdir_wspd_22(cprecip):

	fig,((ax0,ax1), (ax2,ax3))=plt.subplots(2,2,sharex=True,sharey=True)
	ax0.scatter(cprecip.wdSfc, cprecip.ratio)
	ax1.scatter(cprecip.wd025, cprecip.ratio)
	ax2.scatter(cprecip.wd125, cprecip.ratio)
	ax3.scatter(cprecip.wd175, cprecip.ratio)
	ax0.text(0.05,0.95,'Sfc',weight='bold',transform=ax0.transAxes)
	ax1.text(0.05,0.95,'0.25 km',weight='bold',transform=ax1.transAxes)
	ax2.text(0.05,0.95,'1.25 km',weight='bold',transform=ax2.transAxes)
	ax3.text(0.05,0.95,'1.75 km',weight='bold',transform=ax3.transAxes)
	ax0.set_ylabel('CZD/BBY ratio')
	ax2.set_xlabel('wind direction')
	ax2.set_xticks(range(0,360,30))
	ax3.set_xticks(range(0,360,30))
	plt.subplots_adjust(wspace=0.05, hspace=0.05)
	plt.show(block=False)


	fig,((ax0,ax1), (ax2,ax3))=plt.subplots(2,2,sharex=True,sharey=True)
	ax0.scatter(cprecip.wsSfc, cprecip.ratio)
	ax1.scatter(cprecip.ws025, cprecip.ratio)
	ax2.scatter(cprecip.ws125, cprecip.ratio)
	ax3.scatter(cprecip.ws175, cprecip.ratio)
	ax0.text(0.05,0.95,'Sfc',weight='bold',transform=ax0.transAxes)
	ax1.text(0.05,0.95,'0.25 km',weight='bold',transform=ax1.transAxes)
	ax2.text(0.05,0.95,'1.25 km',weight='bold',transform=ax2.transAxes)
	ax3.text(0.05,0.95,'1.75 km',weight='bold',transform=ax3.transAxes)
	ax0.set_ylabel('CZD/BBY ratio')
	ax2.set_xlabel('wind speed')
	plt.subplots_adjust(wspace=0.05, hspace=0.05)
	plt.show(block=False)


def plot_scatter3D(x=None,y=None,z=None,ax=None):

	ax.scatter(x.values,y.values,z.values,c='r', marker='o')
	ax.set_xlim([0,5])
	ax.set_ylim([0,1])
	ax.set_zlim([0,50])
	ax.set_xlabel(x.name)
	ax.set_ylabel(y.name)
	ax.set_zlabel(z.name)
	plt.draw()


def plot_scatter2D(df=None,ax=None, target=None, thres=None):


	target=df[target]	
	strat = df.ix[ np.where(target.values<thres)[0]]
	conv = df.ix[ np.where(target.values>=thres)[0]]
	xs=strat.bbyp
	ys=strat.czdp
	regStrat=get_regression(ys,xs)
	xc=conv.bbyp
	yc=conv.czdp
	regConv=get_regression(yc,xc)	

	labelStrat='Strat m={:3.2f} Rsq={:3.2f} n={:g}'.format(*regStrat)
	labelConv='Conv m={:3.2f} Rsq={:3.2f} n={:g}'.format(*regConv)

	''' scatter plot '''
	ax.scatter(xs, ys,c='blue',edgecolors='None', s=150,linewidths=4,alpha=0.5,label=labelStrat)
	ax.scatter(xc, yc,c='red',edgecolors='None', s=150,linewidths=4,alpha=0.5,label=labelConv)
	xx=np.arange(-1,20)
	yy=xx
	ax.plot(xx,yy,color='black')
	ax.plot(xx,yy*regStrat[0],color='blue')
	ax.plot(xx,yy*regConv[0],color='red')
	ax.set_xlabel('BBY precip')
	ax.set_ylabel('CZD precip')
	ax.set_xlim([-0.5,19.5])
	ax.set_ylim([-0.5,19.5])
	ax.text(0.05,0.95,target.name + ' thres = {:3.2f}'.format(thres),transform=ax.transAxes)
	ax.grid()
	ax.set(aspect='equal')
	plt.subplots_adjust(top=0.98, bottom=0.04,left=0.07, right=0.96)
	plt.legend(scatterpoints=1,loc='lower right')
	plt.draw()

def get_dataframe(cases=None,minutes=None):

	data={'case':[], 'bbyp':[], 'czdp': [], 'echotvar':[]}
	cprecip=pd.DataFrame(data=data)

	for c in cases:

		' sprof data'
		'*****************************************************'
		dbz,vvel,ht,ts,ts2,dayt = sprof.get_arrays(str(c))
		
		' echo top variance'
		echotm = sprof.timeserie_echotop(dbz,ht,plot=False,retrieve='km')

		' layer-averaged variance'
		partition=read_partition.partition(dayt[0].year)
		bbht,bbtimeidx=partition.get_bbht(time=dayt)
		# center = np.nanmax(bbht)+1.0
		# bottom = np.nanmax(bbht)
		bottom = np.asarray(0.)
		vvel_mean,_=sprof.layer_mean(vvel=vvel,height=ht,bottom=bottom)
		_,dbz_mean=sprof.layer_mean(dbz=dbz,height=ht,bottom=bottom)

		' compute variance '
		a={'echotm':echotm, 'vvel_mean':vvel_mean, 'dbz_mean':dbz_mean}
		df = pd.DataFrame(data=a,index=dayt)
		timeg=pd.TimeGrouper(str(minutes)+'T')
		dfg = df.groupby(timeg).var()
		dfg2=dfg.ix[:]
		dr_sprof=pd.date_range(dfg2.index[0],periods=len(dfg2),freq=str(minutes)+'T')

		' sum precip in minutes interval '
		'*****************************************************'		
		bby,czd,frs,_ = precip.get_data(str(c))
		bbyp = bby.precip.groupby(timeg).sum()
		czdp = czd.precip.groupby(timeg).sum()
		frsp = frs.precip.groupby(timeg).sum()
		' use time from sprof to select'
		inix = bbyp.index.get_loc(dr_sprof[0])
		endx = bbyp.index.get_loc(dr_sprof[-1])
		bbyp2=bbyp.ix[inix:endx]
		czdp2=czdp.ix[inix:endx]
		frsp2=frsp.ix[inix:endx]
		ratioCB = np.round(czdp2/bbyp2,2)
		ratioCB[np.isinf(ratioCB.values)]=np.nan
		ratioCF = np.round(czdp2/frsp2,2)
		ratioCF[np.isinf(ratioCF.values)]=np.nan

		' windprof data '
		'*****************************************************'
		wspd,wdir,timestamp,hgt = wprof.make_arrays(case=str(c),surface=True)
		dr_wprof = pd.date_range(timestamp[0],timestamp[-1], freq='60T')
		idx_time = np.where((dr_wprof>=dr_sprof[0]) & (dr_wprof<dr_sprof[-1]))[0]

		' select altitudes '
		ws00=np.round(wspd[0,idx_time],1)
		wd00=np.round(wdir[0,idx_time],0)
		f = interp1d(hgt,range(0,len(hgt)))
		idx = int(np.round(f(0.25), 0))
		ws025=np.round(wspd[idx, idx_time],1)
		wd025=np.round(wdir[idx, idx_time],0)
		idx = int(np.round(f(1.25), 0))
		ws125=np.round(wspd[idx, idx_time],1)
		wd125=np.round(wdir[idx, idx_time],0)
		idx = int(np.round(f(1.75), 0))
		ws175=np.round(wspd[idx, idx_time],1)
		wd175=np.round(wdir[idx, idx_time],0)
		idx = int(np.round(f(2.5), 0))
		ws250=np.round(wspd[idx, idx_time],1)
		wd250=np.round(wdir[idx, idx_time],0)
		idx = int(np.round(f(3.5), 0))
		ws350=np.round(wspd[idx, idx_time],1)
		wd350=np.round(wdir[idx, idx_time],0)

		d={'case':np.repeat(c, len(bbyp.ix[inix:endx])), 
			'bbyp':bbyp2, 
			'czdp': czdp2, 
			'frsp': frsp2,
			'echotvar':dfg2['echotm'][:-1],
			'vvelvar':dfg2['vvel_mean'][:-1],
			'dbzvar':dfg2['dbz_mean'][:-1],
			'wsSfc': ws00,	'wdSfc': wd00,
			'ws025': ws025, 'wd025': wd025,
			'ws125': ws125, 'wd125': wd125,
			'ws175': ws175, 'wd175': wd175,						
			'ws250': ws250, 'wd250': wd250,	
			'ws350': ws350, 'wd350': wd350,	
			'ratioCB': ratioCB,
			'ratioCF':ratioCF}
		df=pd.DataFrame(data=d, index=dfg2[:-1].index,)
		cprecip=cprecip.append(df)

	''' reorder columns '''
	cprecip=cprecip[['case', 
						'bbyp', 'czdp','frsp',
						'ratioCB', 'ratioCF',
						'wsSfc', 'wdSfc', 
						'ws025','wd025',  
						'ws125','wd125',  
						'ws175','wd175', 
						'ws250','wd250', 
						'ws350','wd350', 
						'echotvar','vvelvar','dbzvar']]

	return cprecip	

def plot1():

	fig,ax=plt.subplots()
	ax.plot(dayt,echotm)
	ax2=ax.twinx()
	ax2.plot(ts+timedelta(minutes=15),dfg2.values,marker='o',color='green')
	ax.set_xticks(ts)
	ts_lab=[x.strftime('%H%M') for x in ts]
	ax.set_xticklabels(ts_lab)
	ax.grid(True)
	ax.invert_xaxis()
	plt.show(block=False)

def get_regression(x,y):

	model=sm.OLS(x, y)
	result=model.fit()
	m=result.params[0]
	Rsq=result.rsquared
	Nobs=int(result.nobs)	

	return [m,Rsq,Nobs]


cprecip=main()


