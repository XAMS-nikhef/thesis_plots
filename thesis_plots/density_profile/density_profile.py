import numpy as np
import matplotlib.pyplot as plt


def nfw_profile(r, rho_0, r_s):
    # Equation 1.2
    return rho_0 * r_s ** 3 / (r * (r + r_s) ** 2)


def plot_nfw(rho_0=1, r_s=1):
    r = np.linspace(0, 4, 101)
    y = nfw_profile(r, rho_0=rho_0, r_s=r_s)
    plt.plot(r, y)
    plt.xlabel('Radius [a.u.]')
    plt.ylabel('$\\rho/\\rho_0$')
