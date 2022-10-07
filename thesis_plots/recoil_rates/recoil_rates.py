import string

import matplotlib as mpl
import matplotlib.pyplot as plt
import numericalunits as nu
import numpy as np

import wimprates
from wimprates import StandardHaloModel

_kms = nu.km / nu.s


def _labeled_line(x,
                  text,
                  ytext,
                  textoffset=0,
                  text_kwargs=None,
                  color='k',
                  alpha=1,
                  text_alpha=None,
                  vh='v',
                  **kwargs):
    if text_kwargs is None:
        text_kwargs = {}
    if text_alpha is None:
        text_alpha = alpha
    getattr(plt, f'ax{vh}line')(x, color=color, alpha=alpha, **kwargs)
    plt.text(x + textoffset, ytext, text, color=color, alpha=text_alpha, rotation='vertical',
             **text_kwargs)


def labeled_hline(x, t, xtext, **kwargs):
    # kwargs.setdefault('va', 'center')
    _labeled_line(x, t, xtext, vh='h', **kwargs)


def labeled_vline(y, t, ytext, **kwargs):
    # kwargs.setdefault('ha', 'center')
    _labeled_line(y, t, ytext, vh='v', **kwargs)


def vel_dist(vs, v_0, v_esc):
    return StandardHaloModel(v_0=v_0 * _kms, v_esc=v_esc * _kms).velocity_dist(vs, None) * _kms


class RecoilRatesPlot:
    sigma_nucleon = 1e-47
    mws = np.array([5, 10, 20, 50, 100, 200])
    targets = ('Si', 'Ar', 'Ge', 'Xe')
    color_map = 'viridis_r'
    _subplot_opts = dict(
        left=0.05,  # the left side of the subplots of the figure
        right=0.95,  # the right side of the subplots of the figure
        bottom=0.05,  # the bottom of the subplots of the figure
        top=0.95,  # the top of the subplots of the figure
        wspace=0.05,  # the amount of width reserved for blank space between subplots
        hspace=0.,  # the amount of height reserved for white space between subplots
    )

    figure_settings = dict(facecolor='white', )
    text_kwargs = dict(x=1 - 0.025,
                       y=0.9,
                       bbox=dict(boxstyle="round",
                                 alpha=0.5,
                                 facecolor='gainsboro', ))

    @staticmethod
    def join_x_axes(ax_dict, merge):
        """Merge axes that are in merge to share the same x-axis"""
        ax_dict[merge[0]].get_shared_x_axes().join(*[ax_dict[k] for k in merge])

    @staticmethod
    def estimate_bounds(mw_array):
        bounds = (
                [np.log10(mw_array[0] / (np.log10(mw_array[1]) / np.log10(mw_array[0])))] +
                list((np.log10(mw_array[:-1]) + np.log10(mw_array[1:])) / 2) +
                [np.log10(1.9 * mw_array[-1] - mw_array[-2])]
        )
        return 10 ** np.array(bounds)

    def plot_recoil_rates(self, targets=None):
        if targets is None:
            targets = self.targets
        fig = plt.figure(**self.figure_settings)
        plt.subplots_adjust(**self._subplot_opts)
        shm = StandardHaloModel(v_0=220 * _kms)
        layout = """"""
        legend_key = 'l'
        assert len(targets) >= 1, f"should have at least one target, got {targets}"
        for i, target in enumerate(targets):
            le = string.ascii_uppercase[i]
            layout += f"""
            {le}{legend_key}
            {le}{legend_key}
            {le}{legend_key}"""
        axes = fig.subplot_mosaic(layout,
                                  gridspec_kw={'height_ratios': [0.1, 1, 0.1] * len(targets),
                                               'width_ratios': [1, 0.03]})
        n_target = len(targets)
        target_keys = string.ascii_uppercase[:n_target]
        self.join_x_axes(axes, target_keys)
        y_max = 0
        y_min = np.inf
        es = np.logspace(-1, np.log10(200), 1000)
        norm = mpl.colors.LogNorm(vmin=self.mws[0], vmax=self.mws[-1])
        for ax, label in zip(target_keys, targets):
            plt.sca(axes[ax])
            for mw in self.mws:
                xs = wimprates.rate_wimp(es=es * 1000 * nu.eV,
                                         mw=mw * nu.GeV / nu.c0 ** 2,
                                         sigma_nucleon=self.sigma_nucleon * nu.cm ** 2,
                                         interaction='SI',
                                         material=label,
                                         halo_model=shm,
                                         ) * (nu.keV * (1000 * nu.kg) * nu.year)
                plt.plot(es, xs, c=getattr(plt.cm, self.color_map)(norm(mw)), )
                y_max = max(y_max, np.max(xs))
                y_min = min(y_min, np.max(xs))
            axes[ax].text(s=f'$\mathrm{{{label}}}$',
                          **self.text_kwargs,
                          transform=axes[ax].transAxes,
                          ha='right',
                          va='top',
                          )

        mpl.colorbar.ColorbarBase(ax=axes[legend_key], norm=norm,
                                  orientation='vertical',
                                  cmap=self.color_map,
                                  boundaries=self.estimate_bounds(self.mws),
                                  ticks=self.mws,
                                  label='$\mathrm{M}_{\chi}$')

        for k in target_keys[:-1]:
            axes[k].set_xticks([])
        y_max = np.ceil(y_max / (10 ** np.floor(np.log10(y_max)))) * 10 ** (np.floor(np.log10(y_max)))
        y_min = 10 ** np.floor(np.log10(y_min))
        for k in target_keys:
            axes[k].set_ylabel('$\mathrm{Rate}$\\\\$\mathrm{[c/(keV\,t\,yr)]}$')

            plt.sca(axes[k])
            plt.xscale('log')
            plt.yscale('log')
            plt.ylim(y_min, y_max)
        axes[target_keys[-1]].set_xlabel('$\mathrm{E_{nr}}$ $\mathrm{[keV]}$')

    def plot_velocities(self,
                        targets=None,
                        vs=np.linspace(0, 800 * _kms, 1_000)
                        ):
        if targets is None:
            targets = self.targets

        fig = plt.figure(**{**self.figure_settings, **{'figsize': (10, 10)}})
        plt.subplots_adjust(**self._subplot_opts)
        plt.subplots_adjust(hspace=0.15)
        legend_key = 'l'
        layout = """
                 A.
                 .."""
        for le, target in zip(string.ascii_uppercase[1:len(targets) + 1], targets):
            layout += f"""
                 {le}{legend_key}"""
        axes = fig.subplot_mosaic(layout,
                                  gridspec_kw={
                                      'height_ratios': [2, 0.2] + [1] * len(targets),
                                      'width_ratios': [1, 0.03]})
        n_target = len(targets)
        target_keys = string.ascii_uppercase[1:n_target + 1]
        self.join_x_axes(axes, string.ascii_uppercase[:n_target + 1])
        es = np.linspace(0, 5, 100)

        new = vel_dist(vs, v_0=238, v_esc=544)
        plt.sca(axes['A'])
        axes['A'].xaxis.set_ticks_position('both')

        plt.plot(vs / _kms,
                 vel_dist(vs, v_0=220, v_esc=544),
                 label='$\mathrm{Old}$', color='b')
        labeled_vline(544, '$v_\mathrm{esc}$', 0.0001, color='b', ls='--', textoffset=5)
        plt.plot(vs / _kms,
                 new,
                 label='$\mathrm{New}$', color='g')

        plt.fill_between(
            vs / _kms,
            vel_dist(vs, v_0=238 - 1.5, v_esc=528),
            vel_dist(vs, v_0=238 + 1.5, v_esc=528),
            color='g',
            alpha=0.5,
        )
        labeled_vline(528, '$v_\mathrm{esc}$', 0.0001, color='g', ls='--', text_kwargs=dict(ha='left'),
                      textoffset=-25)
        plt.axvspan(528 - 25, 528 + 24, alpha=0.1)
        plt.fill_between(
            vs / _kms,
            vel_dist(vs, v_0=238, v_esc=528 - 25),
            vel_dist(vs, v_0=238, v_esc=528 + 24),
            color='g',
            alpha=0.5,
        )
        axes['A'].set_ylim(bottom=0, top=None)
        plt.xlabel("$\mathrm{Speed}$ $\mathrm{[km/s]}$")
        plt.ylabel("$\mathrm{Density}$ $\mathrm{[km/s]^{-1}}$")
        axes['A'].legend(loc='upper right', ncol=1)
        for ax, label in zip(target_keys, targets):
            plt.sca(axes[ax])
            norm = mpl.colors.LogNorm(vmin=self.mws[0], vmax=self.mws[-1])
            for mw in self.mws:
                xs = wimprates.vmin_elastic(es * 1000 * nu.eV, mw * nu.GeV / nu.c0 ** 2, label) / _kms
                plt.plot(xs, es, c=getattr(plt.cm, self.color_map)(norm(mw)), )

            axes[ax].text(s=f'$\mathrm{{{label}}}$',
                          **{**self.text_kwargs, **{'x': 0.95}},
                          transform=axes[ax].transAxes,
                          ha='left',
                          va='top',
                          )
        mpl.colorbar.ColorbarBase(ax=axes[legend_key],
                                  norm=norm,
                                  orientation='vertical',
                                  cmap=self.color_map,
                                  boundaries=self.estimate_bounds(self.mws),
                                  ticks=self.mws,
                                  label='$\mathrm{M}_\chi$')
        for k in target_keys[:-1]:
            axes[k].set_xticks([])
        for k in target_keys:
            axes[k].set_ylabel('$\mathrm{E}_\mathrm{nr}$ $\mathrm{[keV]}$')
            axes[k].set_ylim(es[0], es[-1])
        axes[target_keys[-1]].set_xlim(0, 800)
        axes[target_keys[-1]].set_xlabel('${v}_\mathrm{min}$ $\mathrm{[km/s]}$')