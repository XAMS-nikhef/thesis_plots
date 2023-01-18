import thesis_plots
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from functools import partial


class PlotRotationCurveRichards:
    fit_result = None

    def read_data(self):
        data = pd.read_csv(
            os.path.join(thesis_plots.root_folder, 'data', 'rotation_curve_richards', 'data.csv')).values.T

        # Parse the different data sets, each being X, Y and starting with a header (hence the 1:)
        total = data[:2][:, 1:]
        d_total = data[2:4][:, 1:]
        bary = data[4:6][:, 1:]
        disc = data[6:8][:, 1:]
        halo = data[8:10][:, 1:]
        bulge = data[10:12][:, 1:]
        gas = data[12:14][:, 1:]

        order = list(range(len(d_total[0])))
        ii = 30
        order[ii] = ii + 1
        order[ii + 1] = ii

        ii = 32
        order[ii] = ii + 1
        order[ii + 1] = ii
        d_total = d_total.astype(float)
        down = np.concatenate([[0], d_total[1][order][::2]])
        up = np.concatenate([[0], d_total[1][order][1::2]])

        return (
            total.astype(float),
            down,
            up,
            bary.astype(float),
            disc.astype(float),
            halo.astype(float),
            bulge.astype(float),
            gas.astype(float),
        )

    @staticmethod
    def _function(x, a, b, c):
        x = np.clip(x, 0, 10000)
        return a * (x) ** b + x * c

    def _do_fit(self, f, x, y):
        ff = curve_fit(f, x, y, p0=[1, 0.5, 0], maxfev=int(1e5))
        self.fit_result = ff
        return ff[0]

    def get_fit(self, halo, check=False):
        # Make it less squiqly

        halo_data = halo[:, ~np.isnan(halo[0])]
        halo_fit = self._do_fit(self._function, *halo_data)
        if check:
            plt.figure(figsize=(6, 4))
            plt.plot(*halo_data)
            plt.plot(x := halo_data[0], self._function(x, *halo_fit))

        return partial(self._function, **dict(zip('abc', halo_fit)))

    def plot(self):
        mathrm = thesis_plots.mathrm
        fit = pd.read_csv(os.path.join(thesis_plots.root_folder, 'data', 'rotation_curve_richards', 'fit.csv')).values.T
        total, down, up, bary, disc, halo, bulge, gas = self.read_data()
        fitted_model = self.get_fit(halo)

        kw = dict(capsize=3, ls='')

        mask = ~np.isnan(total[0])
        mask2 = ~np.isnan(up)
        mask3 = total[0][mask] < 3
        _ = plt.errorbar(*total[:, mask][:, mask3], yerr=[total[1][mask][mask3] - down[mask2][mask3],
                                                          -total[1][mask][mask3] + up[mask2][mask3]],
                         mfc='none',
                         **kw,
                         label=mathrm('Ionized gas data')
                         )
        plt.errorbar(*total[:, mask][:, ~mask3], yerr=[total[1][mask][~mask3] - down[mask2][~mask3],
                                                       -total[1][mask][~mask3] + up[mask2][~mask3]],
                     **kw,
                     c=_[0]._color,
                     marker=_[0]._marker,
                     label=mathrm('Neutral hydrogen data'))
        plt.plot(*bary, label=mathrm('Baryonic'))
        plt.plot(*disc, label=mathrm('Disc'))
        plt.plot(*bulge, label=mathrm('Bulge'))
        plt.plot(*gas, label=mathrm('Gas'))

        plt.plot(x := np.linspace(0, max(bary[0]), 100), fitted_model(x), label=mathrm('Halo'), marker='', ls='--')
        plt.plot(*fit, ls='-', marker='', label=mathrm('Total'))
        plt.legend(**thesis_plots.legend_kw(ncol=3))
        plt.xlim(left=0)
        plt.ylim(bottom=0)
        plt.xlabel(mathrm('Radius [kpc]'))
        plt.ylabel(mathrm('Velocity [km s^{-1}]'))
        plt.gca().set_yticks(range(0, 301, 25), minor=True)
        plt.gca().set_xticks(range(12), minor=True)
