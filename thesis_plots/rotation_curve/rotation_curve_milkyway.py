"""
Code to make a plot of the velocity distribution, we use two very nice repos to make our live easy:
 - https://github.com/henrysky/milkyway_plot
 - https://github.com/MariusCautun/Milky_Way_mass_profile
"""

import os

import matplotlib.pyplot as plt
import numpy as np
from thesis_plots import string_to_mathrm as mathrm
import thesis_plots


def combined_milkiway_plot(r_max=26, h_frac=0.33):
    from mw_plot import MWPlot
    from astropy import units as u
    from galpy.potential import vcirc
    from mw_mass_profile import Cautun20_galpy_potential
    from mw_mass_profile.Cautun20_galpy_potential import Cautun20
    Cautun_halo, Cautun_Discs, Cautun_Bulge, Cautun_cgm = Cautun20

    abs_path = os.path.dirname(os.path.realpath(Cautun20_galpy_potential.__file__))
    # setup a mw-plot instance of bird's eyes view of the disc
    solar_position = 8.122  # Solar position in kpc
    ax2_ylim = 21
    ax2_frac = ax2_ylim / r_max
    mw1 = MWPlot(radius=r_max * u.kpc,
                 center=(0, 0) * u.kpc,
                 unit=u.kpc,
                 coord='galactocentric',
                 rot90=0,
                 grayscale=False,
                 annotation=True)

    fig, (ax1, ax2) = plt.subplots(2, 1,
                                   figsize=(9, ax2_frac * 9 * (h_frac + 1)),
                                   sharex=True,
                                   gridspec_kw={"height_ratios": {h_frac, 1}
                                                })
    plt.subplots_adjust(
        left=0.05,  # the left side of the subplots of the figure
        right=0.95,  # the right side of the subplots of the figure
        bottom=0.05,  # the bottom of the subplots of the figure
        top=0.95,  # the top of the subplots of the figure
        wspace=1.0,  # the amount of width reserved for blank space between subplots
        hspace=0.0,  # the amount of height reserved for white space between subplots
    )
    mw1.transform([ax2])
    ax2.scatter(solar_position, 0, c='r', s=100)
    plt.sca(ax2)
    plt.xlim(-r_max, r_max)

    plt.yticks(plt.yticks()[0][:-1])
    plt.sca(ax1)

    # read the Eilers et al (2019) rotation curve data
    MW_Vrot_data = np.loadtxt(os.path.join(abs_path, '..', 'data', 'MW_rotation_Eilers_2019.txt'))
    vdata_r = MW_Vrot_data[:, 0]
    vdata_vc = MW_Vrot_data[:, 1]
    vdata_vc_u = MW_Vrot_data[:, 2]
    vdata_vc_l = MW_Vrot_data[:, 3]

    # compare the various rotation curves with the data
    rvals = np.linspace(0.5, r_max, 101)  # kpc

    plt.errorbar(vdata_r * u.kpc,
                 vdata_vc,
                 yerr=[vdata_vc_l, vdata_vc_u],
                 c='k',
                 label=mathrm('Eilers 19'),
                 ls='',
                 zorder=-1,
                 marker='.',
                 capsize=3,
                 )
    mw1.fontsize = plt.rcParams['axes.labelsize']
    # TODO, why /solar_position??
    plt.plot(rvals * u.kpc, vcirc(Cautun20, rvals / solar_position, 0), label=mathrm('Total'), marker='')
    plt.plot(rvals * u.kpc, vcirc(Cautun_halo, rvals / solar_position, 0), label=mathrm('Halo'), marker='')
    plt.plot(rvals * u.kpc, vcirc(Cautun_Discs, rvals / solar_position, 0), label=mathrm('Disc'), marker='')
    plt.plot(rvals * u.kpc, vcirc(Cautun_Bulge, rvals / solar_position, 0), label=mathrm('Bulge'), marker='')
    plt.plot(rvals * u.kpc, vcirc(Cautun_cgm, rvals / solar_position, 0), label=mathrm('CGM'), marker='')
    plt.axvline(solar_position, ls='--', c='r', label=mathrm('Sun'))
    ax1.set_ylabel('$V_c$ $[\mathrm{km/s}]$', fontsize=mw1.fontsize)
    plt.axvline(0, ls='-', c='k')

    plt.legend(**thesis_plots.legend_kw(bbox_to_anchor=(0.02, 0.1, 0.46, 0.32), ncol=2))
    plt.ylim(bottom=0, top=250)

    ax2.set_ylim(-ax2_ylim, ax2_ylim)
    ax2.set_yticks(t := np.arange(-20, 21, 10), [mathrm(str(tt)) for tt in t], size=mw1.fontsize)
    ax2.set_xticks(t := np.arange(-20, 21, 10), [mathrm(str(tt)) for tt in t], size=mw1.fontsize)
    plt.sca(ax2)
    ax2.tick_params(axis='both', direction='out')
    for xy_label in [plt.ylabel, plt.xlabel]:
        xy_label('$\mathrm{Galactrocentric\ coordinates\ [kpc]}$')
