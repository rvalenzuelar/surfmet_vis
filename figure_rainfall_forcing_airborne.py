# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 15:41:30 2016

@author: raul
"""
import OrographicFor as of
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec



dates = {0:{'t0':'2001-01-23','t1':'2001-01-25','vmax':35},
         1:{'t0':'2001-02-16 22:00','t1':'2001-02-18 09:00','vmax':35},
        }

scale=1
plt.figure(figsize=(6*scale,6.5*scale))

gs0 = gridspec.GridSpec(2, 1,
                        hspace=0.2)

ax0 = plt.subplot(gs0[0],gid='(a) Jan 2001')
ax1 = plt.subplot(gs0[1],gid='(b) Feb 2001')

axes = [ax0, ax1]

source='/localdata/SURFACE/climatology/'
matfs = ['avg60_CZC01_nortype.mat']    


for c in range(2):
    
    if c == 0:
        legend=True
    else:
        legend=False

    matfile=source+matfs[0]

    
    t0=dates[c]['t0']
    t1=dates[c]['t1']
    hax = of.plot(axes[c],matfile,t0,t1,
                  legend=legend,add=['bulk','upslope'],
                  legend_loc=(0.35,0.7,0.2,0.2),
                  ylim=[0,dates[c]['vmax']],xtickfreq='6H',
                  lw=2)

    axes[c].text(0.98,0.95,axes[c].get_gid(),size=14,
                va='top',ha='right',
                weight='bold',transform=axes[c].transAxes,
                backgroundcolor='w',clip_on=True)

#plt.show()

fname='/home/raul/Desktop/rainfall_forcing_airborne.png'
plt.savefig(fname, dpi=300, format='png',papertype='letter',
            bbox_inches='tight')







