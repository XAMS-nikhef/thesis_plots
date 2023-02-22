# ThesisPlots

Collection of plots of dissertation thesis, simplified version of the [original repository](https://github.com/JoranAngevaare/thesis_plots)

[![Coverage Status](https://coveralls.io/repos/github/XAMS-nikhef/thesis_plots/badge.svg?branch=master)](https://coveralls.io/github/XAMS-nikhef/thesis_plots?branch=master)
[![CodeFactor](https://www.codefactor.io/repository/github/XAMS-nikhef/thesis_plots/badge)](https://www.codefactor.io/repository/github/XAMS-nikhef/thesis_plots)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.6527303.svg)](https://doi.org/10.5281/zenodo.6527303)


## Use case
If you want to organize your thesis plots in an easily reproducible manner, this might be a nice example for you.

**Getting started**
```
# Fork the repository to your own github account, and copy it locally (or on a cluster)

# clone the repository
git clone git@github.com:<YOUR_GITHUB_ACCOUNT>/thesis_plots.git

# install the repository and it's dependencies. You can either do this in your own or  
pip install -e thesis_plots
```

Additionally, you want to setup latex such that you can use it to rended axis labels etc.
There is an example in the [pytest](https://github.com/XAMS-nikhef/thesis_plots/blob/master/.github/workflows/pytest.yml) script for `linux` and
`macos` (I'm sorry Windows users maybe you want to install a [WSL](https://learn.microsoft.com/en-us/windows/wsl/install) anyway 😉).
The latex rendering on `macos` is still untested at the time of writing.


Now you can add new notebooks in the notebooks folder.
If you are happy with a new plot you made, you can upload it using the normal git commands:
```
cd thesis_plots

# Check which changes you made
git status
git diff

# Make a new branch
git checkout -b <NEW_PROJECT>

# Now add and commit to the repository
git add <THE FILES YOU WANT TO ADD>
git commit -m "<SOME DISCRIPTION>"
git push --set-upstream origin <NEW_PROJECT>
```
This will crate a new branch on your repository which you can now view on you page `https://github.com/<YOUR_GITHUB_ACCOUNT>/thesis_plots`

## Changing the setup
In the file ``main.py`` you can customize the default style of plots that are set by the function `setup_plt`.
The documentation on this is on [Matplotlib](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.rc.html).

## Example usage
Imagine that you made a new notebook with the following code in the notebook `notebooks/normal_distribution.ipynb`:
```python
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LogNorm
import thesis_plots
distribution = np.random.normal(loc = 1, scale = 2, size = (2, 100_000))

# Load your plotting style
thesis_plots.setup_plt()

# Make the plot
plt.hist2d(*distribution, 
           norm=LogNorm(), 
           bins=25,
           cmap='custom_map');
plt.colorbar(label=thesis_plots.mathrm('Counts/bin'))
plt.xlabel(thesis_plots.mathrm('X (some unit)'))
plt.ylabel(thesis_plots.mathrm('Y (some unit)'))
plt.title(thesis_plots.mathrm('Normal distribution'))
```

You can upload this notebook directly (following the commands above) or you can create a new module:
```
mkdir thesis_plots/normal_distribution
touch thesis_plots/normal_distribution/normal_distribution_plot.py
touch thesis_plots/normal_distribution/__init__.py
```
In `thesis_plots/__init__.py` you would add a line `from .normal_distribution import *`.
In `touch thesis_plots/normal_distribution/__init__.py` you will import the `normal_distribution_plot.py` file similar to
```python
from . import normal_distribution_plot
from .normal_distribution_plot import *
```

And in `thesis_plots/normal_distribution/normal_distribution_plot.py` you would make a function/class for the code you just wrote
```python
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LogNorm
import thesis_plots

def plot_normal_distribution():
    distribution = np.random.normal(loc = 1, scale = 2, size = (2, 100_000))
    
    # Make the plot
    plt.hist2d(*distribution, 
               norm=LogNorm(), 
               bins=25,
               cmap='custom_map');
    plt.colorbar(label=thesis_plots.mathrm('Counts/bin'))
    plt.xlabel(thesis_plots.mathrm('X (some unit)'))
    plt.ylabel(thesis_plots.mathrm('Y (some unit)'))
    plt.title(thesis_plots.mathrm('Normal distribution'))
```

This greatly simplifies your notebook, where you can now reduce the code to:

```python
import thesis_plots
# Load your plotting style
thesis_plots.setup_plt()
thesis_plots.normal_distribution.plot_normal_distribution()
```

## Advanced features
 - Every time you make (or merge) a pull request, you will test making the plots on github actions. This prevents you 
   from writing buggy code or forgetting to upload a data file.
 - If you want to add data files, you can for instance do that in `data`, see the Lambda CDM example.
 - You can setup a coverage report on `https://coveralls.io/github/<YOUR_GITHUB_USER>/thesis_plots` this allows you to view if all your code is actually used (and therefore useful)
 - You can add tests in the `tests` folder, these are run as well when you commit to github.

