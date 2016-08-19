


import Precip as precip
import matplotlib.pyplot as plt 
import matplotlib.gridspec as gridspec
import pandas as pd
from matplotlib import rcParams
from rv_utilities import discrete_cmap

rcParams['mathtext.default'] = 'sf'

ncases = [3,7]

scale=1
plt.figure(figsize=(6*scale,6.5*scale))

gs0 = gridspec.GridSpec(2, 1,
                        hspace=0.25)

ax0 = plt.subplot(gs0[0],gid='(a) 23-24Jan01')
ax1 = plt.subplot(gs0[1],gid='(b) 17Feb01')

axes = [ax0, ax1]

sound_dates={3:['2001-01-23 16:19',
                '2001-01-23 18:05',
                '2001-01-23 19:57',
                '2001-01-23 22:00',
                '2001-01-24 00:01',
                '2001-01-24 01:45',
                '2001-01-24 04:00'],
             7:['2001-02-17 12:34',
                '2001-02-17 19:43',
                '2001-02-17 18:58',
                '2001-02-17 20:50',
                '2001-02-17 13:52',
                '2001-02-17 22:58',
                '2001-02-17 14:50',
                '2001-02-17 18:06',
                '2001-02-17 15:47',
                '2001-02-17 21:51',
                '2001-02-17 16:59',]}

cmap = discrete_cmap(7, base_cmap='Set1')


for c,ax in zip(ncases,axes):
    
    if c == 3:
        legend_line=1
        legend_loc=(0, 0.7, 0.4, 0.2)
        freq = '6H'
    else:
        legend_line=0
        legend_loc=(0, 0.7, 0.4, 0.2)
        freq = '6H'
        
    hax,bbysum,czdsum = precip.plot_compare_sum(ax=ax,
                            usr_case=str(c),
                            ylim=[0,12],
                            minutes=60,
                            period='significant',
                            locations=['bby','czd'],
                            xtickfreq=freq,
                            legend_line=legend_line,
                            legend_loc=legend_loc,
                            lcolor=[cmap(0),cmap(1)],)
    
    for t in sound_dates[c]:
        x = pd.date_range(start=t,end=t)
        y = 0
        hax.scatter(x,y,s=40,c='k',marker='o',lw=0.5,
                    clip_on=False, zorder=10000)

    ''' add rainfall ratio '''        
    txt='ratio:{:2.1f}'.format(czdsum/bbysum)
    hax.text(0.11,0.55,txt,transform=hax.transAxes,
             fontsize=13)

    ''' add marker sounding '''
    txt = 'Sounding\nlaunch'
    if c == 3:
        t = '2001-01-24 21:00'
        x,y = [pd.date_range(start=t,end=t),5.5]
        hax.scatter(x,y,s=40,c='k',marker='o',lw=1,
                    clip_on=False, zorder=10000)
        hax.text(0.11,0.35,txt,
                 fontsize=13,
                 transform=hax.transAxes,
                 )
    
    ''' add panel ID '''
    hax.text(0.05,0.9,ax.get_gid(),size=14,
            weight='bold',transform=hax.transAxes)
    

plt.suptitle('')

#plt.show()

fname='/home/raul/Desktop/fig_rainfall_airborne.png'
plt.savefig(fname, dpi=300, format='png',papertype='letter',
            bbox_inches='tight')
