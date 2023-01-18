import matplotlib.pyplot as plt

import thesis_plots


def test_rotation_curve():
    rotation_curve = thesis_plots.RotationCurve()
    rotation_curve.plot_rotation_curve()
    plt.clf()

    rotation_curve.plot_rotation_curve_fancy()
    plt.clf()


def test_combined_curves():
    thesis_plots.combined_milkiway_plot()
    plt.clf()


def test_richards():
    plot = thesis_plots.PlotRotationCurveRichards()
    total, down, up, bary, disc, halo, bulge, gas = plot.read_data()
    plot.get_fit(halo, check=True)
