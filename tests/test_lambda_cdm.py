import thesis_plots


def test_make_rebin_false():
    thesis_plots.setup_plt()
    thesis_plots.PlotLambdaCDM(make_rebin=False).plot()
    thesis_plots.save_fig('planck_cdm')
