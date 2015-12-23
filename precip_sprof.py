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

from datetime import timedelta

def main():

	data={'case':[], 'bbyp':[], 'czdp': [], 'echotvar':[]}
	cprecip=pd.DataFrame(data=data)

	for c in range(1,15):

		' sprof data'
		dbz,vvel,ht,ts,ts2,dayt = sprof.get_arrays(str(c))
		
		' echo top variance'
		echotm = sprof.timeserie_echotop(dbz,ht,plot=False,retrieve='km')

		' layer-averaged variance'
		partition=read_partition.partition(dayt[0].year)
		bbht,bbtimeidx=partition.get_bbht(time=dayt)
		# center = np.nanmax(bbht)+1.0
		bottom = np.nanmax(bbht)
		vvel_mean,_=sprof.layer_mean(vvel=vvel,height=ht,bottom=bottom)
		_,dbz_mean=sprof.layer_mean(dbz=dbz,height=ht,bottom=bottom)

		' compute variance '
		a={'echotm':echotm, 'vvel_mean':vvel_mean, 'dbz_mean':dbz_mean}
		df = pd.DataFrame(data=a,index=dayt)
		minutes=60
		timeg=pd.TimeGrouper(str(minutes)+'T')
		dfg = df.groupby(timeg).var()
		dfg2=dfg.ix[:]
		ts=pd.date_range(dfg2.index[0],periods=len(dfg2),freq=str(minutes)+'T')

		' sum precip in minutes interval '
		bby,czd,_ = precip.get_data(str(c))
		bbyp = bby.precip.groupby(timeg).sum()
		czdp = czd.precip.groupby(timeg).sum()
		inix = bbyp.index.get_loc(ts[0])
		endx = bbyp.index.get_loc(ts[-1])

		d={'case':np.repeat(c, len(bbyp.ix[inix:endx])), 
			'bbyp':bbyp.ix[inix:endx], 
			'czdp': czdp.ix[inix:endx], 
			'echotvar':dfg2['echotm'][:-1],
			'vvelvar':dfg2['vvel_mean'][:-1],
			'dbzvar':dfg2['dbz_mean'][:-1]}
		df=pd.DataFrame(data=d, index=dfg2[:-1].index,)
		cprecip=cprecip.append(df)

	''' reorder columns '''
	cprecip=cprecip[['case', 'bbyp', 'czdp', 'echotvar','vvelvar','dbzvar']]
	# print cprecip
	# return 0

	''' regression '''
	thres_target=0.32 # [echot]
	target=cprecip.echotvar
	
	# thres_target=10.0 # [logvar dbz]
	# target=cprecip.dbzvar
	
	# thres_target=0.08 # [linvar vvel]
	# target=cprecip.vvelvar

	strat = cprecip.ix[ np.where(target.values<thres_target)[0]]
	conv = cprecip.ix[ np.where(target.values>=thres_target)[0]]
	xs=strat.bbyp
	ys=strat.czdp
	regStrat=get_regression(ys,xs)
	xc=conv.bbyp
	yc=conv.czdp
	regConv=get_regression(yc,xc)	

	labelStrat='Strat m={:3.2f} Rsq={:3.2f} n={:g}'.format(*regStrat)
	labelConv='Conv m={:3.2f} Rsq={:3.2f} n={:g}'.format(*regConv)

	print strat


	''' scatter plot '''
	fig,ax=plt.subplots(figsize=(8,8))
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
	ax.text(0.05,0.95,target.name + ' thres = {:3.2f}'.format(thres_target),transform=ax.transAxes)
	ax.grid()
	ax.set(aspect='equal')
	plt.subplots_adjust(top=0.98, bottom=0.04,left=0.07, right=0.96)
	plt.legend(scatterpoints=1,loc='lower right')
	plt.show(block=False)


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


main()


