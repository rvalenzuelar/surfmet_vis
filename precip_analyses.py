

# fig,ax=plt.subplots(2,1,figsize=(6, 8))
# plot_compare_accum(ax=ax, period=False)
# plt.show(block=False)

# fig,ax=plt.subplots(2,1,figsize=(7,9))
import Precip as precip
import matplotlib.pyplot as plt 

# plot_compare_sum(ax=ax[0],minutes=30, period=None)
# plot_regression(ax=ax[1],minutes=30, period=None)
# plt.show(block=False)

# fig,ax=plt.subplots(2,1,figsize=(7,9))
# plot_compare_sum(ax=ax[0],minutes=30, period='significant')
# plot_regression(ax=ax[1],minutes=30, period='significant')				
# plt.show(block=False)

# ppsurf=PdfPages('surf_precip_ground_cases_60min.pdf')
# ncases=range(8,15)
# # ncases=[1,2,3]
# for c in ncases:
# 	fig,ax=plt.subplots()
# 	plot_compare_sum(ax=ax,usr_case=str(c), ylim=[0,22], minutes=60, period='significant')
# 	ppsurf.savefig()
# 	plt.close('all')
# ppsurf.close()

# ppsurf=PdfPages('surf_precipreg_multipage.pdf')
# ncases=range(1,15)
# # ncases=[1,2,3]
# for c in ncases:
# 	fig,ax=plt.subplots()
# 	plot_regression(ax=ax,usr_case=str(c), minutes=30, period=True)
# 	ppsurf.savefig()
# 	plt.close('all')
# ppsurf.close()

# ncases=range(8,15)
# for c in ncases:
# 	fig,ax=plt.subplots()
# 	precip.plot_compare_sum(ax=ax,usr_case=str(c), ylim=[0,22], minutes=60, period='significant')
# plt.show(block=False)


