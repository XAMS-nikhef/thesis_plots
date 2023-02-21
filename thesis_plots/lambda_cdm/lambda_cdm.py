import matplotlib.pyplot as plt
import pandas as pd
import os
import thesis_plots
from thesis_plots import mathrm


class PlotLambdaCDM:
    def __init__(self, make_rebin=True):
        self.make_rebin = make_rebin

    def plot(self):
        if self.make_rebin:
            df = pd.concat(
                [self.get_df('COM_PowerSpect_CMB-TT-full_R3.01.txt')[:29],
                 self.get_df('COM_PowerSpect_CMB-TT-binned_R3.01.txt')]
            )
        else:
            df = self.get_df('COM_PowerSpect_CMB-TT-full_R3.01.txt')
        data = df.values.T
        data_fit = self.get_df(
            'COM_PowerSpect_CMB-base-plikHM-TTTEEE-lowl-lowE-lensing-minimum-theory_R3.01.txt').values.T

        plt.figure(figsize=(9, 5))
        kw = dict(ls='', capsize=3, marker='.', markersize=7.5)

        plt.plot([], [])
        plt.errorbar(data[0], data[1], yerr=[data[2], data[3]], **kw, label=mathrm('Data'))
        plt.plot(data_fit[0], data_fit[1], zorder=10, marker='', label='$\Lambda$' + mathrm('CDM-fit'))

        plt.xscale('log')
        plt.gca().set_xticks(xs := [2, 5, 10, 30, 100, 1000, 2500], [mathrm(str(i)) for i in xs])
        if self.make_rebin:
            plt.axvline(30, ls='--', c='gray')
        plt.ylabel('$\mathcal{D}_\ell^{TT}\,[\mu \mathrm{K}^2]$')
        plt.xlabel('$\ell$')
        handles, labels = plt.gca().get_legend_handles_labels()
        plt.legend(handles[::-1], labels[::-1], **thesis_plots.legend_kw(ncol=3))
        plt.ylim(0, 6000)
        plt.gca().set_yticks(range(0, 6000, 500), minor=True)

    @staticmethod
    def get_df(name):
        base = os.path.join(thesis_plots.root_folder, 'data', 'planck')
        if not os.path.exists(file := os.path.join(base, name)):
            raise FileNotFoundError(f'{file} not in {base}, chose from {os.listdir(base)}')

        data = []
        with open(file, 'r') as file:
            for line in file:
                if line.startswith('#'):
                    headers = line.split()[1:]
                    continue
                data.append([float(f) for f in line.split()])
        return pd.DataFrame(data, columns=headers)
