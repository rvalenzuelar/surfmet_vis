


import Precip as precip
import matplotlib.pyplot as plt 
import matplotlib.gridspec as gridspec
import pandas as pd
from matplotlib import rcParams
rcParams['mathtext.default'] = 'sf'

ncases = [3,7]

scale=1
plt.figure(figsize=(6*scale,6.5*scale))

gs0 = gridspec.GridSpec(2, 1,
                        hspace=0.22)

ax0 = plt.subplot(gs0[0],gid='(a) Jan 2001')
ax1 = plt.subplot(gs0[1],gid='(b) Feb 2001')

axes = [ax0, ax1]

sound_dates={3:['2001-01-23 16:19',
                '2001-01-23 18:05',
                '2001-01-23 22:00',
                '2001-01-24 01:45',
                '2001-01-24 00:01',
                '2001-01-23 19:57',
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
                            usr_case=str(c), ylim=[0,12],
                            minutes=60, period='significant',
                            locations=['bby','czd'],xtickfreq=freq,
                            legend_line=legend_line,
                            legend_loc=legend_loc)
    
    for t in sound_dates[c]:
        x = pd.date_range(start=t,end=t)
        y = 0
        hax.scatter(x,y,s=80,c='k',marker='x',lw=1,
                    clip_on=False, zorder=10000)

    ''' add marker legend '''
    if c == 3:
        hax.text(0.035,0.55,'X Sounding launch',transform=hax.transAxes,
                 fontsize=13)

    ''' add rainfall ratio '''        
    txt='ratio:{:2.1f}'.format(czdsum/bbysum)
    hax.text(0.07,0.45,txt,transform=hax.transAxes,
             fontsize=13)
    
    ''' add panel ID '''
    hax.text(0.05,0.9,ax.get_gid(),size=14,
            weight='bold',transform=hax.transAxes)
    

plt.suptitle('')

#plt.show()

fname='/home/raul/Desktop/rainfall_airborne.png'
plt.savefig(fname, dpi=300, format='png',papertype='letter',
            bbox_inches='tight')
