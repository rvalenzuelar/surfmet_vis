'''
	Make regression analysis of 
	precipitation time series

	Raul Valenzuela
	2015
'''


import Meteoframes as mf
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm
import numpy as np
from datetime import datetime,timedelta
import sys
import os
import time



''' set directory and input files '''
base_directory='/home/rvalenzuela/SURFACE'
# base_directory='/Users/raulv/Documents/SURFACE'
print base_directory
usr_case = raw_input('\nIndicate case number (i.e. 1): ')
case='case'+usr_case.zfill(2)
casedir=base_directory+'/'+case

''' get all the files in the directory case '''
out=os.listdir(casedir)
out.sort()

''' get only met files '''
files=[]
for f in out:
	if f[-3:]=='met': 
		files.append(f)

''' create file path '''
file_met=[]
for f in files:
	file_met.append(casedir+'/'+f)

''' define some variables '''
name_field=['press','temp','rh','wspd','wdir','precip','mixr']
name={'bby':'BodegaBay','czc':'Cazadero'}
elev={'bby':15,'czc':462}
if usr_case in ['1','2']:
	index_field={'bby':[3,4,10,5,6,11,13],'czc':[3,4,10,5,6,11,13]}
elif usr_case in ['3','4','5','6','7']: 
	index_field={'bby':[3,6,9,10,12,17,26],'czc':[3,4,5,6,8,13,22]}
else:
	index_field={'bby':[3,4,5,6,8,13,15],'czc':[3,4,5,6,8,13,15]}

''' make dataframe for each station '''
dfBBY=[]
dfCZD=[]
for f in file_met:
	loc=f[-12:-9]
	if loc=='bby':
		dfBBY.append(mf.parse_surface(f,index_field[loc],name_field,elev[loc]))
	elif loc=='czc':
		dfCZD.append(mf.parse_surface(f,index_field[loc],name_field,elev[loc]))

''' concatenate dataframes when there is
more than one day of data '''
if len(dfBBY)>1:
	meteoBBY=pd.concat(dfBBY)
else:
	meteoBBY=dfBBY[0]	

if len(dfCZD)>1:
	meteoCZD=pd.concat(dfCZD)
else:
	meteoCZD=dfCZD[0]	

foo=meteoBBY.preciph
bby_precip=foo[~np.isnan(foo)]

foo=meteoCZD.preciph
czd_precip=foo[~np.isnan(foo)]

'''czd has 2 hrs less of obs relative
	to bby in case01'''
if usr_case == '1':
	reversedf = czd_precip.ix[::-1]
	s=pd.Series(np.float64([0,0]),index=[datetime(1998,1,18,1),datetime(1998,1,18,0)])
	s.name='preciph'
	reversedf = reversedf.append(s)
	czd_precip = reversedf.ix[::-1]

case_dt={	'1':[1998,1],'2':[1998,1],'3':[2001,1],
			'4':[2001,1],'5':[2001,2],'6':[2001,2],
			'7':[2001,2],'8':[2003,1],'9':[2003,1],
			'10':[2003,2],'11':[2004,1],'12':[2004,2],
			'13':[2004,2],'14':[2004,2]}

usr_st = raw_input('\nIndicate start date (i.e. DD,HH): ')
usr_dt = map(int, usr_st.split(','))
st_dt = datetime(case_dt[usr_case][0],case_dt[usr_case][1],usr_dt[0],usr_dt[1])
st=bby_precip.index.searchsorted(st_dt)

usr_en = raw_input('\nIndicate first end date (i.e. DD,HH: ')
usr_dt = map(int, usr_en.split(','))
en_dt = datetime(case_dt[usr_case][0],case_dt[usr_case][1],usr_dt[0],usr_dt[1])
en=bby_precip.index.searchsorted(en_dt+timedelta(hours=1))

usr_la = raw_input('\nIndicate last end date (i.e. DD,HH): ')
if usr_la:
	usr_dt = map(int, usr_la.split(','))
	la_dt = datetime(case_dt[usr_case][0],case_dt[usr_case][1],usr_dt[0],usr_dt[1])
	la=bby_precip.index.searchsorted(la_dt+timedelta(hours=1))	
else:
	la=None

bby1=bby_precip.ix[st:en]
czd1=czd_precip.ix[st:en]
model1=sm.OLS(czd1,bby1)
result1=model1.fit()
Rsq1=result1.rsquared
m1=result1.params[0]
obs1=int(result1.nobs)

xr=np.linspace(-2,25,10)
fig,ax=plt.subplots()
ax.plot(range(-1,25),range(-1,25),color=(0.7,0.7,0.7),lw=3)
ax.plot(xr,m1*xr,color='blue',lw=1.5)
ax.scatter(bby1,czd1,marker='o',s=55,color='blue',facecolor='none',zorder=10)
m1txt="{:3.2}".format(m1)
r1txt="{:3.2}".format(Rsq1)
obs1txt="{:d}".format(obs1)
datetxt=st_dt.strftime("%b-%d %H")+"UTC to "+en_dt.strftime("%b-%d %H")+"UTC"
regtext1='Y='+m1txt+'X\nR-sqr='+r1txt+'\nn='+obs1txt
text1=datetxt+'\n'+regtext1
ax.text(0.98,0.20,text1,color='blue',horizontalalignment='right',weight='bold',transform=ax.transAxes)
ax.text(0.1,0.9,st_dt.strftime("Y: %Y"),color='black',weight='bold',transform=ax.transAxes)

if la:
	en_dt2 = en_dt+timedelta(hours=1)
	en=bby_precip.index.searchsorted(en_dt2)
	bby2=bby_precip.ix[en:la]
	czd2=czd_precip.ix[en:la]
	model2=sm.OLS(czd2,bby2)
	result2=model2.fit()
	Rsq2=result2.rsquared
	m2=result2.params[0]
	obs2=int(result2.nobs)

	ax.plot(xr,m2*xr,color='red',lw=1.5)
	ax.scatter(bby2,czd2,marker='+',s=55,color='red',zorder=20)
	m2txt="{:3.2}".format(m2)
	r2txt="{:3.2}".format(Rsq2)
	obs2txt="{:d}".format(obs2)
	regtext2='Y='+m2txt+'X\nR-sqr='+r2txt+'\nn='+obs2txt
	datetxt=en_dt2.strftime("%b-%d %H")+"UTC to "+la_dt.strftime("%b-%d %H")+"UTC"
	text2=datetxt+'\n'+regtext2
	ax.text(0.98,0.04,text2,color='red',horizontalalignment='right',weight='bold',transform=ax.transAxes)

ax.set_xlim([-1,22])
ax.set_ylim([-1,22])
ax.set_aspect('equal')
ax.set_xlabel('Rain rate BBY [mm h-1]')
ax.set_ylabel('Rain rate CZD [mm h-1]')
plt.grid(True)

# plt.show(block=False)
plt.show()






