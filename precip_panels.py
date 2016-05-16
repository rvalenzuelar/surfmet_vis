import Precip as precip
import matplotlib.pyplot as plt 
import numpy as np

ncases = range(8,15)
fig,axes = plt.subplots(3,3,figsize=(11,8.5))
axes = axes.flatten()
axes[-1].set_visible(False)
axes[-2].set_visible(False)
axes = axes[:7]

for c,ax in zip(ncases,axes):
    hax = precip.plot_compare_sum(ax=ax, usr_case=str(c), ylim=[0,28],
    						minutes=60, period='significant',
    						locations=['bby','czd'],xtickfreq='12H')
    if c > 8:
    	hax.set_ylabel('')

    if c not in [8,11,14]:
        hax.set_yticklabels('')

    hax.set_xlabel('')
plt.suptitle('')
plt.subplots_adjust(left=0.1,right=0.9,
                    bottom=0.1,top=0.9,
                    hspace=0.25,wspace=0.1)
plt.show(block=False)