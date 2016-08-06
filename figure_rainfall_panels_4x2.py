


import Precip as precip
import matplotlib.pyplot as plt 
import matplotlib.gridspec as gridspec
from matplotlib import rcParams
rcParams['mathtext.default'] = 'sf'
rcParams['xtick.labelsize'] = 15
rcParams['ytick.labelsize'] = 15
rcParams['legend.fontsize'] = 15
#rcParams['axes.labelsize'] = 15
#rcParams['xtick.labelsize'] = 20

ncases = range(8,15)

scale=1.1
plt.figure(figsize=(11*scale,11*scale))

gs0 = gridspec.GridSpec(4, 2,
                        wspace=0.1,
                        hspace=0.3)

ax0 = plt.subplot(gs0[0],gid='(a) 12-14Jan03')
ax1 = plt.subplot(gs0[1],gid='(b) 21-23Jan03')
ax2 = plt.subplot(gs0[2],gid='(c) 15-16Feb03')
ax3 = plt.subplot(gs0[3],gid='(d) 09Jan04')
ax4 = plt.subplot(gs0[4],gid='(e) 02Feb04')
ax5 = plt.subplot(gs0[5],gid='(f) 16-18Feb04')
ax6 = plt.subplot(gs0[6],gid='(g) 25-26Feb04')


axes = [ax0, ax1, ax2, ax3, ax4, ax5, ax6]

for c,ax in zip(ncases,axes):
    
    if c ==8:
        legend_line=1
        legend_loc=(0.04, 0.7, 0.4, 0.2)
    else:
        legend_line=0
        legend_loc=(0.02, 0.7, 0.4, 0.2)
        
    hax,bbysum,czdsum = precip.plot_compare_sum(ax=ax,
                            usr_case=str(c), ylim=[0,25],
                            minutes=60, period='significant',
                            locations=['bby','czd'],xtickfreq='12H',
                            legend_line=legend_line,
                            legend_loc=legend_loc)
    if c > 8:
    	hax.set_ylabel('')

    if c in range(9,15,2):
        hax.set_yticklabels('')
        
    if c == 13:
        txt = r'$\leftarrow UTC \left[\stackrel{day}{time}\right]$'
        hax.set_xlabel(txt,fontsize=20)
        txt='ratio:{:2.1f}'.format(czdsum/bbysum)
        hax.text(0.06,0.48,txt,transform=hax.transAxes,
                 fontsize=13)
    else:
        hax.set_xlabel('')
    
        txt='ratio:{:2.1f}'.format(czdsum/bbysum)
        hax.text(0.08,0.48,txt,transform=hax.transAxes,
                 fontsize=13)
    
for ax in axes:
    ax.text(0.05,0.9,ax.get_gid(),size=14,
            weight='bold',transform=ax.transAxes)
    
plt.suptitle('')

plt.show()

#fname='/home/raul/Desktop/rainfall_singlestorm.png'
#plt.savefig(fname, dpi=300, format='png',papertype='letter',
#            bbox_inches='tight')
