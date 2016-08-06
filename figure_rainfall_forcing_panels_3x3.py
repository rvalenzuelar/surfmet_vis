# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 15:41:30 2016

@author: raul
"""
import OrographicFor as of
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec



dates = {0:{'t0':'2003-01-12','t1':'2003-01-15','vmax':20},
         1:{'t0':'2003-01-21','t1':'2003-01-24','vmax':25},
         2:{'t0':'2003-02-15','t1':'2003-02-17','vmax':18},
         3:{'t0':'2004-01-09','t1':'2004-01-10','vmax':90},
         4:{'t0':'2004-02-02','t1':'2004-02-03','vmax':40},
         5:{'t0':'2004-02-16','t1':'2004-02-19','vmax':100},
         6:{'t0':'2004-02-25','t1':'2004-02-26','vmax':95}}

scale=1.1
plt.figure(figsize=(11*scale,8.5*scale))

gs0 = gridspec.GridSpec(3, 3,
                        wspace=0.2)

ax = []
ax.append(plt.subplot(gs0[0],gid='(a) Jan 2003'))
ax.append(plt.subplot(gs0[1],gid='(b) Jan 2003'))
ax.append(plt.subplot(gs0[2],gid='(c) Feb 2003'))
ax.append(plt.subplot(gs0[3],gid='(d) Jan 2004'))
ax.append(plt.subplot(gs0[4],gid='(e) Feb 2004'))
ax.append(plt.subplot(gs0[5],gid='(f) Feb 2004'))
ax.append(plt.subplot(gs0[6],gid='(g) Feb 2004'))

source='/localdata/SURFACE/climatology/'
matfs = ['avg60_CZC03_nortype.mat',
         'avg60_CZC04_nortype.mat']    


for c in range(7):
    
    if c == 3:
        legend=True
    else:
        legend=False

    if c in [0,1,2]:
        matfile=source+matfs[0]
    else:
        matfile=source+matfs[1]

    
    t0=dates[c]['t0']
    t1=dates[c]['t1']
    hax = of.plot(ax[c],matfile,t0,t1,
                  legend=legend,add=['bulk','upslope'],
                  legend_loc=(0.7,0.7,0.2,0.2),
                  ylim=[0,dates[c]['vmax']],
                  xtickfreq='12H',
                  lw=2)
    
    if c not in [0]:
        hax.set_ylabel('')
        
    if c not in [5]:
        hax.set_xlabel('')



    ax[c].text(0.05,0.95,ax[c].get_gid(),size=14,va='top',
            weight='bold',transform=ax[c].transAxes,
            backgroundcolor='w',clip_on=True)

plt.show()

#fname='/home/raul/Desktop/rainfall_forcing.png'
#plt.savefig(fname, dpi=300, format='png',papertype='letter',
#            bbox_inches='tight')







