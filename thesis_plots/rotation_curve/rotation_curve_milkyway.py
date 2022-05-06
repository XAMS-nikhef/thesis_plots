"""
Code to make a plot of the velocity distribution, we use two very nice repos to make our live easy:
 - https://github.com/henrysky/milkyway_plot
 - https://github.com/MariusCautun/Milky_Way_mass_profile
"""

import os
import matplotlib.pyplot as plt
import numpy as np


def combined_milkiway_plot():
    # nested imports to decrease import time
    from mw_plot import MWPlot
    from astropy import units as u
    from galpy.potential import vcirc
    from mw_mass_profile import Cautun20_galpy_potential
    from mw_mass_profile.Cautun20_galpy_potential import Cautun20
    Cautun_halo, Cautun_Discs, Cautun_Bulge, Cautun_cgm = Cautun20

    abs_path = os.path.dirname(os.path.realpath(Cautun20_galpy_potential.__file__))
    # setup a mw-plot instance of bird's eyes view of the disc
    solar_position = 8.122  # Solar position in kpc

    mw1 = MWPlot(radius=30 * u.kpc,
                 center=(0, 0) * u.kpc,
                 unit=u.kpc,
                 coord='galactocentric',
                 rot90=0,
                 grayscale=False,
                 annotation=True)

    fig, (ax1, ax2) = plt.subplots(2, 1,
                                   figsize=(7.5, 7.5 * 1.25),
                                   sharex=True,
                                   gridspec_kw={"height_ratios": {0.25, 1}

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
    plt.yticks(plt.yticks()[0][:-1])
    plt.sca(ax1)

    # read the Eilers et al (2019) rotation curve data
    MW_Vrot_data = np.loadtxt(os.path.join(abs_path, '..', 'data', 'MW_rotation_Eilers_2019.txt'))
    vdata_r = MW_Vrot_data[:, 0]
    vdata_vc = MW_Vrot_data[:, 1]
    vdata_vc_u = MW_Vrot_data[:, 2]
    vdata_vc_l = MW_Vrot_data[:, 3]

    # compare the various rotation curves with the data
    rvals = np.linspace(0., 50., 101)  # kpc

    plt.errorbar(vdata_r * u.kpc,
                 vdata_vc,
                 yerr=[vdata_vc_l, vdata_vc_u],
                 c='k',
                 label='Eilers 19',
                 ls='',
                 zorder=-1,
                 marker='.',
                 capsize=3,
                 )
    # TODO, why /solar_position??
    plt.plot(rvals * u.kpc, vcirc(Cautun20, rvals / solar_position, 0), label='Total')
    plt.plot(rvals * u.kpc, vcirc(Cautun_halo, rvals / solar_position, 0), label='DM Halo')
    plt.plot(rvals * u.kpc, vcirc(Cautun_Discs, rvals / solar_position, 0), label='Discs')
    plt.plot(rvals * u.kpc, vcirc(Cautun_Bulge, rvals / solar_position, 0), label='Bulge')
    plt.plot(rvals * u.kpc, vcirc(Cautun_cgm, rvals / solar_position, 0), label='CGM')
    plt.axvline(solar_position, ls='--', c='r', label='Sun')
    ax1.set_ylabel('$V_c$ $[\mathrm{km/s}]$', fontsize=mw1.fontsize)
    plt.axvline(0, ls='-', c='k')
    plt.xlim(-30, 30)
    plt.legend(ncol=2, fontsize=13)
    ax1.tick_params(labelsize=mw1.fontsize * 0.8, width=mw1.fontsize / 10, length=mw1.fontsize / 2)
    # ax1.set_yticks(ax1.get_yticks()[1:])
    # plt.yticks(plt.yticks()[0][1:])
    plt.ylim(bottom=50, top=250)
    _ = [i.set_linewidth(mw1.fontsize / 10) for i in ax1.spines.values()]
