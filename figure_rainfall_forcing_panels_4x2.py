# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 15:41:30 2016

@author: raul
"""
import OrographicFor as of
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib import rcParams

rcParams['mathtext.default'] = 'sf'
rcParams['xtick.labelsize'] = 15
rcParams['ytick.labelsize'] = 15
rcParams['legend.fontsize'] = 15

dates = {0:{'t0':'2003-01-12','t1':'2003-01-15','vmax':20},
         1:{'t0':'2003-01-21','t1':'2003-01-24','vmax':25},
         2:{'t0':'2003-02-15','t1':'2003-02-17','vmax':18},
         3:{'t0':'2004-01-09','t1':'2004-01-10','vmax':90},
         4:{'t0':'2004-02-02','t1':'2004-02-03','vmax':40},
         5:{'t0':'2004-02-16','t1':'2004-02-19','vmax':100},
         6:{'t0':'2004-02-25','t1':'2004-02-26','vmax':95}}

scale=1.1
plt.figure(figsize=(11*scale,11*scale))

gs0 = gridspec.GridSpec(4, 2,
                        wspace=0.2,
                        hspace=0.3)

ax = []
ax.append(plt.subplot(gs0[0],gid='(a) 12-14Jan03'))
ax.append(plt.subplot(gs0[1],gid='(b) 21-23Jan03'))
ax.append(plt.subplot(gs0[2],gid='(c) 15-16Feb03'))
ax.append(plt.subplot(gs0[3],gid='(d) 09Jan04'))
ax.append(plt.subplot(gs0[4],gid='(e) 02Feb04'))
ax.append(plt.subplot(gs0[5],gid='(f) 16-18Feb04'))
ax.append(plt.subplot(gs0[6],gid='(g) 25-26Feb04'))

source='/localdata/SURFACE/climatology/'
matfs = ['avg60_CZC03_nortype.mat',
         'avg60_CZC04_nortype.mat']    


for c in range(7):
    
    if c == 3:
        leg_bool=True
    else:
        leg_bool=False

    if c in [0,1,2]:
        matfile=source+matfs[0]
    else:
        matfile=source+matfs[1]

    
    t0=dates[c]['t0']
    t1=dates[c]['t1']
    hax = of.plot(ax[c],
                  matfile,t0,t1,
                  legend      = leg_bool,
                  add         = ('bulk','upslope'),
                  lcolors     = ('b','g'),
                  ylims       = ([0,100], [0,35]),
                  second_axis = 'bulk',
                  lw          = 2,
                  legend_loc  = (0.75,0.7,0.2,0.2),
                  ylim        = [0, dates[c]['vmax']],
                  xtickfreq   = '12H',
                  )

    if c == 5:
        txt = r'$\leftarrow UTC \left[\stackrel{day}{time}\right]$'
        hax[0].set_xlabel(txt,fontsize=20)
    
    if c not in [0]:
        hax[0].set_ylabel('')

    if c not in [3]:
        hax[1].set_ylabel('')
        
    if c not in [5]:
        hax[0].set_xlabel('')

    if c in [0,1,2]:
        hax[1].set_yticks([])

    ax[c].text(0.05,0.95,ax[c].get_gid(),size=14,va='top',
            weight='bold',transform=ax[c].transAxes,
            backgroundcolor='w',clip_on=True)

#plt.show()

fname='/home/raul/Desktop/rainfall_forcing.png'
plt.savefig(fname, dpi=300, format='png',papertype='letter',
            bbox_inches='tight')







