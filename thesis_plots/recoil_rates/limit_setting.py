import os
from functools import lru_cache

import numericalunits as nu
import numpy as np
import pandas as pd
import scipy
from thesis_plots import root_folder
from tqdm.notebook import tqdm

import wimprates


class LZ:
    """Mimic the LZ experiment, use data from https://arxiv.org/pdf/2207.03764.pdf"""
    exposure = 0.9  # t*yr
    efficiency = 1
    e_roi = [0, 70]  # keVnr
    material = 'Xe'
    _itp = None

    @staticmethod
    @lru_cache(None)
    def get_eff():
        """Read the efficiency from the /data folder"""
        return pd.read_table(os.path.join(root_folder, 'data', 'lz_limit', 'Fig2_NRefficiency.txt', ), delimiter='\t')

    @property
    def _itp_eff(self):
        if self._itp is None:
            eff = self.get_eff()
            self._itp = scipy.interpolate.interp1d(*eff.values.T[:2], fill_value=0, bounds_error=False, )
        return self._itp

    def combined_efficiency(self, e_nr):
        """Calculate the energy threshold"""
        interpolator = self._itp_eff
        return interpolator(e_nr)


class LimitSetter:
    """Set a poisson limit for no background"""
    no_background_possion = 2.3  # number of events for 90% confidence interval: scipy.stats.poisson.cdf(0, 2.3)==0.1

    tqdm_active = True

    def __init__(self,
                 detector=None,
                 halo_model: wimprates.StandardHaloModel = None):
        if detector is None:
            detector = LZ()
        if halo_model is None:
            halo_model = wimprates.StandardHaloModel()
        self.detector = detector
        self.halo_model = halo_model

    def set_limits(self,
                   mass_range=np.linspace(1, 1000, 10),
                   log_sigma_range=(-49, -42),
                   n_sigma_bins=10,
                   ):
        """
        Get limits for the given masses, expressed as
        :param mass_range: list of masses [GeV] to compute a limit for
        :param log_sigma_range: boundaries where to interpolate between to solve for the log-cross-section to get a limit at
        :param n_sigma_bins: number of bins for the interpolation to get the limit at
        :return: list of length <mass_range> to get the 90% confidence level limit at.
        """
        sigmas = np.linspace(*log_sigma_range, int(n_sigma_bins))

        results = []
        for mw in tqdm(mass_range, disable=not self.tqdm_active, desc='Getting limit for masses'):
            # For each log-cross-section, calculate the total number of observed events
            n_observed = []
            for s in sigmas:
                n_i = self.integrate_rate(mw, s)
                n_observed.append(n_i)
                if n_i > self.no_background_possion:
                    break

            itp = scipy.interpolate.interp1d(n_observed, sigmas[:len(n_observed)], bounds_error=False)
            results.append(itp(self.no_background_possion))
        # Convert back to non-log10 numbers:
        return 10 ** np.array(results)

    def integrate_rate(self, mw, log_cross_section):
        """
        Get the number of expected wimp events for wimps evaluated at e_nr.
        We assume infinite energy resolution and energy threshold as by `detector.e_threshold_nr`

        :param mw: wimp mass ~O(1-100), unit GeV/c2
        :param log_cross_section: log10(sigma_nucleon/cm2)
        :return: Integrated rate
        """

        def d_rate(e_nr):
            eff = self.detector.combined_efficiency(e_nr)
            if eff < 1e-6:
                return 0
            rate = wimprates.rate_wimp(
                es=e_nr * 1000 * nu.eV,
                mw=mw * nu.GeV / nu.c0 ** 2,
                sigma_nucleon=10 ** log_cross_section * nu.cm ** 2,
                interaction='SI',
                material=self.detector.material,
                halo_model=self.halo_model,
            ) * (nu.keV * (1000 * nu.kg) * nu.year)
            return rate * eff

        total_rate, _ = scipy.integrate.quad(d_rate, *self.detector.e_roi, epsrel=1e-2)
        total_rate *= self.detector.exposure * self.detector.efficiency
        return total_rate
