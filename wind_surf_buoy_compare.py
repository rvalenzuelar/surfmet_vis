import Meteoframes as mf
import numpy as np
import pandas as pd


def plot(case=None):

    if case == 11:
        print('No buoy data for case 11\n')
        return 0

    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates

    f1, f2 = get_files(case)

    surf = get_surf(f1)
    buoy = get_buoy(f2, surf.index)

    fig, ax = plt.subplots(2, 1, sharex=True)
    ax0, ax1 = ax
    ax0.plot(surf.U, label='surf')
    ax0.plot(buoy.U, label='buoy')
    ax0.text(0.05, 0.9, 'U-comp', weight='bold', transform=ax0.transAxes)
    ctxt = 'Case '+str(case)
    ax0.text(0.8, 0.9, ctxt, transform=ax0.transAxes)
    ax1.plot(surf.V, label='surf')
    ax1.plot(buoy.V, label='buoy')
    ax1.text(0.05, 0.9, 'V-comp', weight='bold', transform=ax1.transAxes)
    ax1.invert_xaxis()
    fmt = mdates.DateFormatter('%d\n%H')
    ax1.xaxis.set_major_formatter(fmt)
    plt.legend(loc=0)
    plt.show(block=False)


def scatter(case=None):

    if case == 11:
        print('No buoy data for case 11\n')
        return 0

    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from scipy.stats import linregress

    f1, f2 = get_files(case)

    surf = get_surf(f1)
    buoy = get_buoy(f2, surf.index)

    res1 = linregress(surf.U.values, buoy.U.values)
    res2 = linregress(surf.V.values, buoy.V.values)
    stxt1 = 'Rsq: {:3.2f}\np-value: {:4.3f}'.format(
        np.round(res1[2]**2, 2), res1[3])
    stxt2 = 'Rsq: {:3.2f}\np-value: {:4.3f}'.format(
        np.round(res2[2]**2, 2), res2[3])

    print('interpU: {}, coefU: {}'.format(
        np.round(res1[1], 2), np.round(res1[0], 2)))
    print('interpV: {}, coefV: {}'.format(
        np.round(res2[1], 2), np.round(res2[0], 2)))

    fig, ax = plt.subplots(1, 2, figsize=(10, 5))
    ax0, ax1 = ax

    ax0.scatter(surf.U, buoy.U)
    ax0.plot([-10, 11], [-10, 11], color=(0.5, 0.5, 0.5), ls='--')
    x = np.arange(-10, 11)
    ax0.plot(x, res1[1]+(res1[0]*x), color=(1, 0, 0), ls='-')
    ax0.text(0.05, 0.9, 'U-comp', weight='bold', transform=ax0.transAxes)
    ax0.text(0.05, 0.8, stxt1, weight='bold', transform=ax0.transAxes)
    ax0.set_xlim([-10, 10])
    ax0.set_ylim([-10, 10])
    ax0.set_xlabel('surface wind [ms-1]')
    ax0.set_ylabel('buoy wind [ms-1]')
    ax0.set(aspect='equal')

    ax1.scatter(surf.V, buoy.V)
    ax1.plot([-1, 16], [-1, 16], color=(0.5, 0.5, 0.5), ls='--')
    x = np.arange(-1, 16)
    ax1.plot(x, res2[1]+(res2[0]*x), color=(1, 0, 0), ls='-')
    ax1.text(0.05, 0.9, 'V-comp', weight='bold', transform=ax1.transAxes)
    ax1.text(0.05, 0.8, stxt2, weight='bold', transform=ax1.transAxes)
    ax1.set_xlim([-1, 15])
    ax1.set_ylim([-1, 15])
    ax1.set_xlabel('surface wind [ms-1]')
    ax1.set_ylabel('buoy wind [ms-1]')
    ax1.set(aspect='equal')

    ctxt = 'Case {}\nBeg: {}\nEnd: {}'
    tbeg = surf.iloc[0].name
    tend = surf.iloc[-1].name
    plt.suptitle(ctxt.format(str(case), tbeg, tend))
    plt.show(block=False)


def get_surf(f=None):
    surf = mf.parse_surface(f)
    sucomp = -surf.wspd * np.sin(np.radians(surf.wdir))
    svcomp = -surf.wspd * np.cos(np.radians(surf.wdir))
    surf['U'] = sucomp
    surf['V'] = svcomp
    surf.drop(surf.columns[[0, 1, 2, 5, 6, 7, 8, 9, 10]], axis=1, inplace=True)
    g = pd.TimeGrouper('10T')
    surfU = surf.U.groupby(g).mean()
    surfV = surf.V.groupby(g).mean()
    surf10 = pd.DataFrame(data={'U': surfU, 'V': surfV})

    return surf10


def get_buoy(f=None, target_index=None):
    buoy = mf.parse_buoy(f)
    bucomp = -buoy.SPD * np.sin(np.radians(buoy.DIR))
    bvcomp = -buoy.SPD * np.cos(np.radians(buoy.DIR))
    buoy['U'] = bucomp
    buoy['V'] = bvcomp
    buoy.drop(buoy.columns[[0, 1, 2, 3, 4]], axis=1, inplace=True)
    buoy = buoy.loc[target_index]

    return buoy


def get_files(case=None):
    import os
    homed = os.path.expanduser('~')

    string1 = homed + '/SURFACE/case{}/{}'
    string2 = homed + '/BUOY/case{}/{}'

    fname1 = {
        8: 'bby03012.met',
        9: 'bby03022.met',
        10: 'bby03046.met',
        11: 'bby04009.met',
        12: 'bby04033.met',
        13: 'bby04047.met',
        14: 'bby04056.met'
    }

    fname2 = {
        8: '46013c2003.txt',
        9: '46013c2003.txt',
        10: '46013c2003.txt',
        11: '46013c2004.txt',
        12: '46013c2004.txt',
        13: '46013c2004.txt',
        14: '46013c2004.txt'
    }

    f1 = string1.format(str(case).zfill(2), fname1[case])
    f2 = string2.format(str(case).zfill(2), fname2[case])

    return f1, f2
