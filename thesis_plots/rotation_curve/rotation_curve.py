"""
Pie-chart galaxy rotation curves based on work from Erik Hogenbirk

Erik Hogenbirk. (2018). ErikHogenbirk/DMPlots: More code and update (v1.1.0). Zenodo. https://doi.org/10.5281/zenodo.1479669

t the rotation curve of M33, as measured in https://academic.oup.com/mnras/article/311/2/441/965167.
"""


import numpy as np
import matplotlib.pyplot as plt
import os
import thesis_plots

# # %matplotlib inline
# plt.rc('font', size=22)
# plt.rcParams['figure.figsize'] = (10.0, 7.0)
# plt.rc('text', usetex=True)


class RotationCurve:
    def __init__(self):
        base = os.path.dirname(os.path.realpath(thesis_plots.__file__))
        data = {}
        fns = ['fit', 'pts', 'pts+', 'pts-', 'halo', 'gas', 'stellar_disk', 'luminous+', 'luminous-']
        for fn in fns:
            data[fn + '_x'], data[fn] = _read_curve(os.path.join(base, '..', 'data', 'rotation_curve', f'{fn}.txt'))

        data['dpts'] = (data['pts+'] - data['pts-']) * 0.5

        for fn in ['gas', 'stellar_disk', 'halo', 'fit', 'luminous+', 'luminous-']:
            data[fn + '_x'] = np.concatenate([[0], data[fn + '_x']])
            data[fn] = np.concatenate([[0], data[fn]])

        xp = np.linspace(0, 16, 200)
        data['x'] = xp
        data['baryons'] = np.sqrt(np.interp(xp, data['gas_x'], data['gas'])**2 + np.interp(xp, data['stellar_disk_x'], data['stellar_disk'])**2)
        data['all'] = np.sqrt(
            np.interp(xp, data['gas_x'], data['gas'])**2 +
            np.interp(xp, data['stellar_disk_x'], data['stellar_disk'])**2 +
            np.interp(xp, data['halo_x'], data['halo'])**2)

        for pol in ('+', '-'):
            data['lum%s' % pol] = np.interp(xp, data['luminous%s_x' % pol], data['luminous%s' % pol])

        self.data = data

    def plot_rotation_curve(self):
        data = self.data
        plt.errorbar(data['pts_x'], data['pts'], data['dpts'], marker='.', capsize=5, ls='None', label='Measured')
        plt.plot(data['stellar_disk_x'], data['stellar_disk'], label='Stars')
        plt.plot(data['x'], data['baryons'], label='Stars and gas')
        plt.plot(data['fit_x'], data['fit'], label='Stars, gas and dark matter')

        # plt.plot(d['x'], d['all'], label='All')
        # plt.plot(d['gas_x'], d['gas'], label='Gas')
        plt.xlabel('Radius (kpc)')
        plt.ylim(0, 160)
        plt.xlim(0, 15)
        plt.legend()

    def plot_rotation_curve_fancy(self):
        data = self.data
        plt.errorbar(data['pts_x'], data['pts'], data['dpts'], marker='.', capsize=5, ls='None', label='Measured')
        plt.plot(data['stellar_disk_x'], data['stellar_disk'], label='Stars', ls='--', lw=2.5)
        plt.plot(data['x'], data['baryons'], label='Stars and gas', ls='-.', lw=2.5)
        plt.plot(data['fit_x'], data['fit'], label='Stars, gas and dark matter', lw=2.5)

        plt.xlabel(r'Radius (kpc)')
        plt.ylabel(r'v$_c$ (km/s)')
        plt.ylim(0, 140)
        plt.xlim(0, 15)
        plt.text(9, 32, 'Expected from stars', color='C1', rotation = -6)
        plt.text(8.3, 62.5, 'Expected from stars and gas', color='C2', rotation = -8)
        plt.text(8.75, 112, 'Including dark matter halo', color='C3', rotation = 8)

        plt.fill_between(data['x'], data['lum-'], data['lum+'], color='C2', alpha=0.2)

        xp = np.linspace(0.001, 15, 200)
        for start in np.arange(20, 701, 20):
            plt.plot(xp, start * np.sqrt(1/xp), color='k', alpha=0.2, lw=1.5)


def _string_fmt(s):
    s = str(s)
    s = s.replace(';', '')
    s = s.replace(',', '.')
    s = s.replace("b'", '')
    s = s.replace("'", '')
    return s

def _read_curve(fn):
    d = np.loadtxt(fn, converters={i: _string_fmt for i in (0, 1)})
    return d[:, 0], d[:, 1]