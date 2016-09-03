# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 16:12:18 2016

@author: raul
"""

def plot(ax,matfile,t0,t1,legend=True, add=None, second_axis=None,
         legend_line=1, lw=2, lcolors=None, legend_loc=None,
         ylim=None,xtickfreq=None,labsize = 15, ylims=None):
    
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
    time  = df.loc[ts].index
    bulk  = df.loc[ts].bulk.values
    iwv   = df.loc[ts].iwv.values
    upslp = df.loc[ts].upslp.values
    
    targets = {'bulk':bulk,'iwv':iwv,'upslope':upslp}
    
    leg_labels  = {'bulk':'Bulk flux',
                   'iwv': 'IWV',
                   'upslope':'Upslope wind'}
                   
    y_labels  = {'bulk':'Bulk flux $[cm\ m\ s^{-1}]$',
                   'iwv': 'IWV',
                   'upslope':'Upslope wind $[m\ s^{-1}]$'}
               
    if second_axis is None:
        for a in add:
            ax.plot(time,targets[a],
                    label=leg_labels[a],
                    lw=lw)
            txt  = 'Bulk flux $[cm\ m\ s^{-1}]$\n'
            txt += 'Upslope wind $[m\ s^{-1}]$'
            ax.set_ylabel(txt, color='k', fontsize=labsize) 
            
    else:
        ax2 = ax.twinx()
        lns = list()
        for a,color,ylim in zip(add,lcolors,ylims):
            if a == second_axis:
               cax   = ax2
            else:
               cax   = ax
            ln = cax.plot(time,targets[a],
                          label=leg_labels[a],
                          lw=lw,
                          color=color)
            lns.append(ln)
            cax.set_ylim(ylim)
            cax.set_ylabel(y_labels[a], color=color, fontsize=labsize)            
            cax.tick_params(axis='y', colors=color)


    ''' format axes '''
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d\n%H'))
    ax.set_xlabel(r'$\leftarrow UTC \left[\stackrel{day}{time}\right]$',
                  fontsize=labsize)


    ''' add legend '''
    if legend is True:
        if second_axis is None:
            ax.legend(prop={'size': 12},
                      numpoints=1,
                      handletextpad=0.1,
                      framealpha=0,
                      handlelength=legend_line,
                      bbox_to_anchor=legend_loc)
        else:
            lns = lns[0]+lns[1]
            labs = [l.get_label() for l in lns]
            ax.legend(lns,labs,
                      prop={'size': 12},
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

    ''' adjust xlim '''
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

    if second_axis is None:
        return ax
    else:
        return [ax,ax2]
    