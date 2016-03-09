"""
    Module for plotting surface meterology

    Raul Valenzuela
    August, 2015
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import Meteoframes as mf
import os
import sys
import numpy as np
from datetime import datetime

''' set color codes in seaborn '''
sns.set_color_codes()

''' set directory and input files '''
base_directory = '/home/rvalenzuela/SURFACE'
# base_directory='/Users/raulv/Documents/SURFACE'
print base_directory
usr_case = raw_input('\nIndicate case number (i.e. 1): ')
case = 'case'+usr_case.zfill(2)
casedir = base_directory+'/'+case
out = os.listdir(casedir)
out.sort()

files = []
for f in out:
    if f[-3:] == 'met':
        print f
        files.append(f)

name_field = ['press', 'temp', 'rh', 'wspd', 'wdir', 'precip', 'mixr']
name = {'bby': 'BodegaBay', 'czc': 'Cazadero', 'frs': 'Fort Ross'}
elev = {'bby': 15, 'czc': 462, 'frs': 45}

file_met = []
try:
    if sys.argv[1] == 'compare':
        for f in files:
            file_met.append(casedir+'/'+f)
        usr_loc = None
except IndexError:
    usr_loc = raw_input('\nIndicate location (i.e. bby): ')
    for f in files:
        if f[:3] == usr_loc:
            file_met.append(casedir+'/'+f)


def main(option):

    if option == 'compare':
        dfBBY = []
        dfCZD = []
        for f in file_met:
            loc = f[-12:-9]
            if loc == 'bby':
                dfBBY.append(mf.parse_surface(f))
            elif loc == 'czc':
                dfCZD.append(mf.parse_surface(f))

        if len(dfBBY) > 1:
            meteoBBY = pd.concat(dfBBY)
        else:
            meteoBBY = dfBBY[0]

        if len(dfCZD) > 1:
            meteoCZD = pd.concat(dfCZD)
        else:
            meteoCZD = dfCZD[0]

        make_compare(BBY=meteoBBY, CZD=meteoCZD)

    else:

        df = []
        for f in file_met:
            # df.append(mf.parse_surface(f,index_field[usr_loc],name_field,elev[usr_loc]))
            df.append(mf.parse_surface(f))

        if len(df) > 1:
            meteo = pd.concat(df)
        else:
            meteo = df[0]

        make_meteo(meteo)
        make_thermo(meteo)

    plt.show()
    # plt.show(block=False)


def make_meteo(meteo):

    x = meteo.index
    temp = pd.rolling_mean(meteo.temp, 10)
    rh = pd.rolling_mean(meteo.rh, 10)
    wspd = pd.rolling_mean(meteo.wspd, 10)
    wdir = pd.rolling_mean(meteo.wdir, 10)
    press = meteo.press
    precip = meteo.preciph
    slp = meteo.sea_levp/100  # [hPa]

    labsize = 15
    fig, ax = plt.subplots(4, sharex=True, figsize=(8.5, 11))
    ax[0].plot(x, temp)
    ax[0].set_ylabel('Temperature [C]', color='b', fontsize=labsize)
    # ax[0].set_ylim([3,13])
    ax2 = add_second_yaxis(ax[0], x, rh)
    ax2.set_ylabel('RH [%]', color='g', fontsize=labsize)
    ax2.set_ylim([50, 105])
    ax[1].plot(x, wspd)
    ax[1].set_ylabel('WSPD [ms-1]', color='b', fontsize=labsize)
    ax[1].set_ylim([0, 12])
    ax2 = add_second_yaxis(ax[1], x, wdir)
    ax2.set_ylabel('WDIR [deg]', color='g', fontsize=labsize)
    ax2.set_ylim([50, 350])
    ax[2].plot(x, press)
    # ax[2].set_ylim([1015,1025])
    ax[2].set_ylabel('Pressure [hPa]', color='b', fontsize=labsize)
    ax[2].yaxis.set_major_formatter(mticker.ScalarFormatter(useOffset=False))
    ax2 = add_second_yaxis(ax[2], x, slp)
    ax2.set_ylabel('Sea level pressure [hPa]', color='g', fontsize=labsize)
    # ax2.set_ylim([1015,1025])
    ax[3].plot(x+pd.Timedelta('30 minutes'), precip, 'o')
    ax[3].set_ylabel('Rain rate [mm h-1]', color='b', fontsize=labsize)
    ax[3].xaxis.set_major_formatter(mdates.DateFormatter('%d-%H'))
    ax[3].set_xlabel(r'$\Leftarrow$'+' Time (UTC)')
    ax[3].set_ylim([0, 12])

    # print x
    ax[3].set_xlim([x[0], x[-1]])
    ax[3].invert_xaxis()

    l1 = 'Surface meteorology at ' + name[usr_loc]
    l2 = '\nStart time: '+x[0].strftime('%Y-%m-%d %H:%M')+' UTC'
    l3 = '\nEnd time: '+x[-1].strftime('%Y-%m-%d %H:%M')+' UTC'
    fig.suptitle(l1+l2+l3, y=0.98)
    plt.subplots_adjust(hspace=0.08)
    plt.draw()


def make_thermo(meteo):

    x = meteo.index
    theta = pd.rolling_mean(meteo.theta, 10)
    thetaeq = pd.rolling_mean(meteo.thetaeq, 10)
    mixr = pd.rolling_mean(meteo.mixr, 10)

    labsize = 15
    fig, ax = plt.subplots(3, sharex=True, figsize=(8.5, 11))
    ax[0].plot(x, theta)
    ax[0].set_ylabel('Theta [K]', color='b', fontsize=labsize)
    ax[0].set_ylim([276, 286])
    ax[0].invert_xaxis()
    ax[1].plot(x, thetaeq)
    ax[1].set_ylabel('Theta eq. [K]', color='b', fontsize=labsize)
    ax[1].set_ylim([287, 307])
    ax[2].plot(x, mixr)
    ax[2].set_ylabel('Miging ratio [g/kg]', color='b', fontsize=labsize)
    # ax[2].yaxis.set_major_formatter(mticker.ScalarFormatter(useOffset=False))
    # ax[3].plot(x, precip,'o')
    # ax[3].set_ylabel('Rain rate [mm h-1]',color='b',fontsize=labsize)
    ax[2].xaxis.set_major_formatter(mdates.DateFormatter('%d-%H'))
    ax[2].set_xlabel(r'$\Leftarrow$'+' Time (UTC)')
    # ax[2].set_ylim([4.,8.5])

    l1 = 'Surface meteorology at ' + name[usr_loc]
    l2 = '\nStart time: '+x[0].strftime('%Y-%m-%d %H:%M')+' UTC'
    l3 = '\nEnd time: '+x[-1].strftime('%Y-%m-%d %H:%M')+' UTC'
    fig.suptitle(l1+l2+l3, y=0.98)
    plt.subplots_adjust(hspace=0.08)
    plt.draw()


def add_second_yaxis(ax, x, y):

    axt = ax.twinx()
    axt.plot(x, y, 'g')
    axt.grid(False)
    return axt


def make_compare(**kwargs):

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
    ln1 = ax.plot(xbby+dt, bby_precip, '-o')
    ln2 = ax.plot(xczd+dt, czd_precip, '-o')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d\n%H'))
    datetext = xbby[0].strftime('%Y-%b')
    ax.text(0.03, 0.95, 'Date: '+datetext, weight='bold',
            size=18, transform=ax.transAxes)
    ax.set_xlabel(r'$\Leftarrow$'+'Time (UTC)', fontsize=labsize)
    ax.set_ylabel('Rain rate [mm h-1]', color='k', fontsize=labsize)
    ax.set_ylim([0, 22])
    ax.set_xlim([xbby[stidx], xbby[enidx]+pd.Timedelta('1 hour')])
    ax.invert_xaxis()
    plt.legend(ln1+ln2, ['BBY', 'CZD'], prop={'size': 18})
    fig.subplots_adjust(bottom=0.15, top=0.95, left=0.1, right=0.95)

try:
    main(sys.argv[1])
except IndexError:
    main(None)

# main(sys.argv[1])
