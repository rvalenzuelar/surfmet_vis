# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 16:12:18 2016

@author: raul
"""

def plot(ax,matfile,t0,t1,legend=True,add=None,legend_line=1,
         lw=2,legend_loc=None,ylim=None,xtickfreq=None):
    
    import matplotlib.dates as mdates
    import parse_data as par
    import pandas as pd
    import numpy as np
    from matplotlib import rcParams
    from datetime import timedelta
    
    rcParams['mathtext.default'] = 'sf'
    
    df=par.oroforcing(matfile=matfile)
    
    ''' retireve data '''
    ts = pd.date_range(t0, t1, freq='1H')
    bulk = df.loc[ts].bulk.values
    iwv  = df.loc[ts].iwv.values
    upslp = df.loc[ts].upslp.values
    time = df.loc[ts].index


    for n in add:
        if n == 'bulk':
            target=bulk
            label='Bulk flux (0.85-1.15 km)'
        elif n=='iwv':
            target=iwv
            label='IWV'
        elif n=='upslope':
            target=upslp
            label='Upslope wind (230$^\circ$)'
        ax.plot(time,target,label=label,lw=lw)


    ''' format axes '''
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d\n%H'))
    labsize = 15
    ax.set_xlabel(r'$\leftarrow UTC \left[\stackrel{day}{time}\right]$',
                  fontsize=labsize)
    ax.set_ylabel('Bulk flux [cm m s-1]\nUpslope wind [m s-1]', 
                  color='k', fontsize=labsize)

    ''' add legend '''
    if legend is True:
        ax.legend(prop={'size': 12},
                  numpoints=1,
                  handletextpad=0.1,
                  framealpha=0,
                  handlelength=legend_line,
                  bbox_to_anchor=legend_loc)

    ''' adjust ylim '''
    if ylim is not None:
        ax.set_ylim(ylim)

    'representative time is half the period grouped'
    timed = timedelta(minutes=60 / 2)

#    ''' adjust xlim '''
#    xticks = pd.date_range(time[0], time[-1], freq='12H')
#    ax.set_xticks(xticks)
#    ax.set_xlim([time[0] - timed, time[-1] + timed])

    onehr = timedelta(hours=1)
    ini = ts[0]
    end = ts[-1]
    if ini.hour not in [0,12]:
        delt=np.mod(12,ini.hour)
        if delt>5:
            delt=np.mod(24,ini.hour)
        inix = ini + onehr*delt
    else:
        inix = ini
    xticks = pd.date_range(inix, end+onehr, freq=xtickfreq)
    ax.set_xticks(xticks)
    ax.set_xlim([ini - timed, end + timed])


    ''' invert x axis '''
    ax.invert_xaxis()

    return ax
    