
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
import Meteoframes as mf
#import os
import numpy as np
import statsmodels.api as sm

from datetime import datetime, timedelta
from glob import glob
#from matplotlib.backends.backend_pdf import PdfPages


#base_directory = os.path.expanduser('~')
base_directory = '/localdata'


def tta_precip():

    import Windprof2 as wp

    print 'BBY-tta    | BBY-notta | CZD-tta   | CZD-notta | FRS-tta | FRS-notta '
    o = '{:11.1f} {:11.1f} {:11.1f} {:11.1f} {:11.1f} {:11.1f}'
    for case in range(8, 15):
        bby, czd, frs, _ = get_data(str(case))
        tta_times = wp.get_tta_times(case=str(case), continuous=True)
        if len(tta_times) > 0:
            tta_idx_bby = ((bby.index >= tta_times[0]) & (
                bby.index <= tta_times[-1]))
            tta_idx_czd = ((czd.index >= tta_times[0]) & (
                czd.index <= tta_times[-1]))
            tta_idx_frs = ((frs.index >= tta_times[0]) & (
                frs.index <= tta_times[-1]))
            bby_tta = bby.precip[tta_idx_bby].sum()
            bby_notta = bby.precip[~tta_idx_bby].sum()
            czd_tta = czd.precip[tta_idx_czd].sum()
            czd_notta = czd.precip[~tta_idx_czd].sum()
            frs_tta = frs.precip[tta_idx_frs].sum()
            frs_notta = frs.precip[~tta_idx_frs].sum()
        else:
            bby_tta = -999
            bby_notta = bby.precip.sum()
            czd_tta = -999
            czd_notta = czd.precip.sum()
            frs_tta = -999
            frs_notta = frs.precip.sum()
        print o.format(bby_tta, bby_notta, czd_tta, czd_notta, frs_tta,
                       frs_notta)


def plot_compare_sum(ax=None, usr_case=None, ylim=None,
                    minutes=None, period=None,locations=None,
                    xtickfreq=None,legend_line=1,
                    lcolor=['g','r','b'],
                    legend_loc=None):

    if ax is None:
        ax = plt.gca()

    bby, czd, frs, usr_case = get_data(usr_case)
    timeg = pd.TimeGrouper(str(minutes) + 'T')
    bbyg = bby.precip.groupby(timeg).sum()
    czdg = czd.precip.groupby(timeg).sum()


    onehr = timedelta(hours=1)

    bbylab = 'BBY({:2.1f} mm)'
    czdlab = 'CZD({:2.1f} mm)'
    frslab = 'FRS({:2.1f} mm)'

    xg = bbyg.index
    
#    timed = timedelta(minutes=minutes)    
#        xg = bbyg.index + timed
    
    if 'bby' in locations:
        bbysum = bbyg.sum()
        ax.plot(xg, bbyg, '-',lw=2, color=lcolor[0],
                label=bbylab.format(bbysum))
    if 'czd' in locations:
        czdsum = czdg.sum()
        ax.plot(xg, czdg, '-',lw=2, color=lcolor[1],
                label=czdlab.format(czdsum))
    if 'frs' in locations:
        if usr_case in ['8', '9', '10', '11', '12', '13', '14']:
            frsg = frs.precip.groupby(timeg).sum()
            ln3 = ax.plot(xg, frsg, '-',
                          label=frslab.format(frsg.sum()))
    else:
        ln3=[]

    ''' format axes '''
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d\n%H'))
    labsize = 15
#    ax.set_xlabel(r'$\Leftarrow$' + 'Time (UTC)', fontsize=labsize)
    ax.set_xlabel(r'$\leftarrow UTC \left[\stackrel{day}{time}\right]$',
                                          fontsize=12)    
    ax.set_ylabel('Rain rate $[mm h^{-1}]$', color='k', fontsize=labsize)
    
    ''' define period to plot '''
    if period:
        if period == '5h':
            period = request_dates_5h(usr_case)
        elif period == 'significant':
            period = request_dates_significant(usr_case)
        ini = datetime(*(period['ini'] + [0]))
        end = datetime(*(period['end'] + [0]))
#        inix = bbyg.index.get_loc(ini)
#        endx = bbyg.index.get_loc(end)

        if ini.hour not in [0,12]:
            delt=np.mod(12,ini.hour)
            if delt>5:
                delt=np.mod(24,ini.hour)
            inix = ini + onehr*delt
        else:
            inix = ini
        xticks = pd.date_range(inix, end+onehr, freq=xtickfreq)
        ax.set_xticks(xticks)
#        ax.set_xlim([ini - timed, end + timed + onehr])
        ax.set_xlim([ini , end + onehr])
    
    ''' invert x axis '''
    ax.invert_xaxis()
    
    ''' set y limit '''
    if ylim is not None:
        ax.set_ylim([ylim[0], ylim[1]])
        
    ''' add suptitle '''
    datetext = xg[0].strftime('%Y-%b')
    freqtext = ' Frequency: ' + str(minutes) + ' minutes'
    plt.suptitle('Case ' + usr_case + ' date: ' + datetext + freqtext)

    ''' add legend '''
    ax.legend(prop={'size': 12},
              numpoints=1,
              handletextpad=0.1,
              framealpha=0,
              handlelength=legend_line,
              bbox_to_anchor=legend_loc)
    if ln3:
        ax.legend(prop={'size': 18}, loc='best')


    return ax, bbysum,czdsum

def plot_compare_accum(ax=None, usr_case=None, **kwargs):

    bby, czd, usr_case = get_data(usr_case)
    period = kwargs['period']

    if period:
#        period = get_request_dates(usr_case)
        ini = datetime(*(period['ini'] + [0]))
        end = datetime(*(period['end'] + [0]))
        inix = bby.index.get_loc(ini)
        endx = bby.index.get_loc(end)
    else:
        inix = 0
        endx = -1

    bby_paccum = bby[inix:endx].precip.cumsum()
    czd_paccum = czd[inix:endx].precip.cumsum()

    reg = get_regression(bby_paccum.values, czd_paccum.values)
    print 'm={:3.2f}, Rsq={:3.2f}, n={:d}'.format(reg[0], reg[1], reg[2])

    ax[0].plot(bby_paccum, label='BBY')
    ax[0].plot(czd_paccum, label='CZD')
    ax[0].grid()
    ax[0].legend(loc=0)
    ax[0].set_title('Accumulated precip case ' + usr_case)

    ax[1].scatter(bby_paccum, czd_paccum, color='blue',
                  s=30, edgecolor='None', alpha=0.9)
    ax[1].plot(range(len(bby_paccum)), color='black',
               linestyle='--', linewidth=3)
    mmax = np.amax([np.max(bby_paccum), np.max(czd_paccum)])
    ax[1].set_xlim([0, mmax])
    ax[1].set_ylim([0, mmax])
    ax[1].set_xlabel('bby')
    ax[1].set_ylabel('czd')
    ax[1].grid()
    ax[1].set_title('Scatter plot precip case ' + usr_case)


def plot_regression(ax=None, usr_case=None, period=None, **kwargs):

    if ax is None:
        ax = plt.gca()

    bby, czd, usr_case = get_data(usr_case)
    minutes = kwargs['minutes']
    timeg = pd.TimeGrouper(str(minutes) + 'T')
    bbyg = bby.precip.groupby(timeg).sum()
    czdg = czd.precip.groupby(timeg).sum()

    'representative time is half the period grouped'
    timed = timedelta(minutes=minutes / 2)

    xg = bbyg.index + timed
    if period:
        if period == '5h':
            period = request_dates_5h(usr_case)
        elif period == 'significant':
            period = request_dates_significant(usr_case)
        ini = datetime(*(period['ini'] + [0]))
        end = datetime(*(period['end'] + [0]))
        inix = bbyg.index.get_loc(ini)
        endx = bbyg.index.get_loc(end)
        y = bbyg[inix:endx].values
        x = czdg[inix:endx].values
        reg = get_regression(x, y)
        bbyg = bbyg.ix[inix:endx]
        czdg = czdg.ix[inix:endx]
        begdate = ini
        enddate = end
    else:
        y = bbyg.values
        x = czdg.values
        reg = get_regression(x, y)
        begdate = bby.index[0]
        enddate = bby.index[-1]

    ax.scatter(bbyg, czdg, color='blue')
    bbyg_max = np.max(bbyg)
    czdg_max = np.max(czdg)
    regtext = 'm={:3.2f}, Rsq={:3.2f}, n={:d}'.format(reg[0], reg[1], reg[2])
    str_beg = begdate.strftime('Beg: %dT%H:%M UTC')
    str_end = enddate.strftime('\nEnd: %dT%H:%M UTC')
    str_freq = '\nFreq: ' + str(minutes) + ' minutes'
    str_times = str_beg + str_end + str_freq
    ax.text(0.1, 0.9, str_times, size=15,
            verticalalignment='top', transform=ax.transAxes)
    ax.text(0.4, 0.1, regtext, weight='bold', size=18, transform=ax.transAxes)
    vmax = int(np.ceil(np.maximum(bbyg_max, czdg_max)))
    ax.plot(range(-1, 15), range(-1, 15), color='black')
    ax.set_xlim([-0.1, vmax])
    ax.set_ylim([-0.1, vmax])
    ax.set_xlabel('BBY')
    ax.set_ylabel('CZD')
    ax.grid()
    ax.set_xlim([-0.5, 14])
    ax.set_ylim([-0.5, 14])
    datetext = xg[0].strftime('%Y-%b')
    freqtext = ' Frequency: ' + str(minutes) + ' minutes'
    plt.suptitle('Case ' + usr_case + ' date: ' + datetext + freqtext)
    plt.subplots_adjust(bottom=0.1, top=0.95, left=0.1, right=0.95)


def plot_compare_hourly(**kwargs):

    bby = kwargs['BBY']
    czd = kwargs['CZD']

    ''' remove rows with nan '''
    bby = bby[np.isfinite(bby['preciph'])]
    czd = czd[np.isfinite(czd['preciph'])]

    bby_precip = bby.preciph
    czd_precip = czd.preciph

    xbby = bby.index
    xczd = czd.index

    sptime = raw_input('\nSpecific time? (y/n): ')
    if sptime == 'y':
        st = raw_input('Start time? (dd,hh): ').split(',')
        en = raw_input('End time? (dd,hh): ').split(',')
        stD = int(st[0])
        stH = int(st[1])
        enD = int(en[0])
        enH = int(en[1])
        Y = xbby[0].year
        m = xbby[0].month
        stidx = np.where(xbby == pd.Timestamp(datetime(Y, m, stD, stH)))
        enidx = np.where(xbby == pd.Timestamp(datetime(Y, m, enD, enH)))
    else:
        stidx = 0
        enidx = -1

    labsize = 15
    fig, ax = plt.subplots()
    dt = pd.Timedelta('30 minutes')
    ln1 = ax.plot(xbby + dt, bby_precip, '-o')
    ln2 = ax.plot(xczd + dt, czd_precip, '-o')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d\n%H'))
    datetext = xbby[0].strftime('%Y-%b')
    ax.text(0.03, 0.95, 'Date: ' + datetext,
            weight='bold', size=18, transform=ax.transAxes)
    ax.set_xlabel(r'$\Leftarrow$' + 'Time (UTC)', fontsize=labsize)
    ax.set_ylabel('Rain rate [mm h-1]', color='k', fontsize=labsize)
    ax.set_ylim([0, 22])
    ax.set_xlim([xbby[stidx], xbby[enidx] + pd.Timedelta('1 hour')])
    ax.invert_xaxis()
    plt.legend(ln1 + ln2, ['BBY', 'CZD'], prop={'size': 18})
    fig.subplots_adjust(bottom=0.15, top=0.95, left=0.1, right=0.95)


def get_files(usr_case=None):

    if usr_case is None:
        print base_directory
        usr_case = raw_input('\nIndicate case number (i.e. 1): ')

    case = 'case' + usr_case.zfill(2)
    casedir = base_directory + '/SURFACE/' + case
    out = glob(casedir + '/*.met')
    out.sort()
    return out, usr_case


def get_index_field(usr_case):

    if usr_case in ['1', '2']:
        index_field = {'bby': [3, 4, 10, 5, 6, 11, 13],
                       'czc': [3, 4, 10, 5, 6, 11, 13]}
    elif usr_case in ['3', '4', '5', '6', '7']:
        index_field = {'bby': [3, 5, 8, 10, 12, 17, 26],
                       'czc': [3, 4, 5, 6, 8, 13, 22]}
    else:
        index_field = {'bby': [3, 4, 5, 6, 8, 13, 15],
                       'czc': [3, 4, 5, 6, 8, 13, 15],
                       'frs': [3, 4, 5, 6, 8, 13, 15]}

    name_field = ['press', 'temp', 'rh', 'wspd', 'wdir', 'precip', 'mixr']

    return index_field, name_field


def get_data(usr_case=None):

    file_met, usr_case = get_files(usr_case)
    index_field, name_field = get_index_field(usr_case)
    dfBBY = []
    dfCZD = []
    dfFRS = []
    # period = get_request_dates(usr_case)

    for f in file_met:
        loc = f[-12:-9]
        if loc == 'bby':
#            elev = 15
#            dfBBY.append(mf.parse_surface(
#                f, index_field[loc], name_field, elev))
            dfBBY.append(mf.parse_surface(f))
        elif loc == 'czc':
#            elev = 462
#            dfCZD.append(mf.parse_surface(
#                f, index_field[loc], name_field, elev))
            dfCZD.append(mf.parse_surface(f))            
        elif loc == 'frs':
#            elev = 462
#            dfFRS.append(mf.parse_surface(
#                f, index_field[loc], name_field, elev))
            dfFRS.append(mf.parse_surface(f))

    if len(dfBBY) > 1:
        meteoBBY = pd.concat(dfBBY)
    else:
        meteoBBY = dfBBY[0]

    if len(dfCZD) > 1:
        meteoCZD = pd.concat(dfCZD)
    else:
        meteoCZD = dfCZD[0]

    if len(dfFRS) > 1:
        meteoFRS = pd.concat(dfFRS)
    else:
        try:
            meteoFRS = dfFRS[0]
        except IndexError:
            index = meteoBBY.index
            columns = meteoBBY.columns
            meteoFRS = pd.DataFrame(index=index, columns=columns)

    return meteoBBY, meteoCZD, meteoFRS, usr_case


def request_dates_5h(usr_case):
    '''     these dates select continuos periods of precip
        in 5 hour
    '''
    reqdates = {'1': {'ini': [1998, 1, 18, 15], 'end': [1998, 1, 18, 20]},
                '2': {'ini': [1998, 1, 26, 4], 'end': [1998, 1, 26, 9]},
                '3': {'ini': [2001, 1, 23, 21], 'end': [2001, 1, 24, 2]},
                '4': {'ini': [2001, 1, 25, 15], 'end': [2001, 1, 25, 20]},
                '5': {'ini': [2001, 2, 9, 10], 'end': [2001, 2, 9, 15]},
                '6': {'ini': [2001, 2, 11, 3], 'end': [2001, 2, 11, 8]},
                '7': {'ini': [2001, 2, 17, 17], 'end': [2001, 2, 17, 22]},
                '8': {'ini': [2003, 1, 12, 15], 'end': [2003, 1, 12, 20]},
                '9': {'ini': [2003, 1, 22, 18], 'end': [2003, 1, 22, 23]},
                '10': {'ini': [2003, 2, 16, 0], 'end': [2003, 2, 16, 5]},
                '11': {'ini': [2004, 1, 9, 17], 'end': [2004, 1, 9, 22]},
                '12': {'ini': [2004, 2, 2, 12], 'end': [2004, 2, 2, 17]},
                '13': {'ini': [2004, 2, 17, 14], 'end': [2004, 2, 17, 19]},
                '14': {'ini': [2004, 2, 25, 8], 'end': [2004, 2, 25, 13]}
                }

    return reqdates[usr_case]


def request_dates_significant(usr_case):
    ''' these dates try to avoid discontinuity when possible
        and periods of no rain at the beginning and end
        of the time series
    '''
    reqdates = {'1': {'ini': [1998, 1, 18, 15], 'end': [1998, 1, 19, 0]},
                '2': {'ini': [1998, 1, 26, 0], 'end': [1998, 1, 27, 5]},
                '3': {'ini': [2001, 1, 23, 0], 'end': [2001, 1, 25, 0]},
                '4': {'ini': [2001, 1, 25, 9], 'end': [2001, 1, 26, 23]},
                '5': {'ini': [2001, 2, 9, 8], 'end': [2001, 2, 10, 14]},
                '6': {'ini': [2001, 2, 11, 2], 'end': [2001, 2, 11, 13]},
                '7': {'ini': [2001, 2, 16, 22], 'end': [2001, 2, 18, 8]},
                '8': {'ini': [2003, 1, 12, 0], 'end': [2003, 1, 14, 23]},
                '9': {'ini': [2003, 1, 21, 0], 'end': [2003, 1, 23, 23]},
                '10': {'ini': [2003, 2, 15, 0], 'end': [2003, 2, 16, 23]},
                '11': {'ini': [2004, 1, 9, 0], 'end': [2004, 1, 9, 23]},# end is last in obs
                '12': {'ini': [2004, 2, 2, 0], 'end': [2004, 2, 2, 23]}, # end is last in obs
                '13': {'ini': [2004, 2, 16, 0], 'end': [2004, 2, 18, 23]},
                '14': {'ini': [2004, 2, 25, 0], 'end': [2004, 2, 25, 23]} # end is last in obs
                }

    return reqdates[usr_case]


def get_regression(x, y):

    model = sm.OLS(x, y)
    result = model.fit()
    m = result.params[0]
    Rsq = result.rsquared
    Nobs = int(result.nobs)

    return [m, Rsq, Nobs]
