import setuptools


def open_requirements(path):
    with open(path) as f:
        requires = [
            r.split('/')[-1] if r.startswith('git+') else r
            for r in f.read().splitlines()]
    return requires


with open('README.md') as file:
    readme = file.read()

with open('HISTORY.md') as file:
    history = file.read()


requires = open_requirements('requirements.txt')
tests_requires = open_requirements('extra_requirements/requirements-tests.txt')

setuptools.setup(name='thesis_plots',
                 version='0.2.2',
                 description='Collection of plots for dissertation',
                 author='J. R. Angevaare',
                 url='https://github.com/JoranAngevaare/thesis_plots',
                 long_description=readme + '\n\n' + history,
                 long_description_content_type="text/markdown",
                 setup_requires=['pytest-runner'],
                 install_requires=requires,
                 tests_require=requires + tests_requires,
                 python_requires=">=3.10",
                 packages=setuptools.find_packages() + ['data', 'extra_requirements'],
                 package_dir={'thesis_plots': 'thesis_plots',
                              'data': 'data',
                              'extra_requirements': 'extra_requirements',
                              },
                 package_data={'thesis_plots': ['thesis_plots/*'],
                               'extra_requirements': ['requirements-tests.txt'],
                               },
                 classifiers=[
                     'Development Status :: 5 - Production/Stable',
                     'License :: OSI Approved :: BSD License',
                     'Natural Language :: English',
                     'Programming Language :: Python :: 3.8',
                     'Programming Language :: Python :: 3.9',
                     'Programming Language :: Python :: 3.10',
                     'Intended Audience :: Science/Research',
                     'Programming Language :: Python :: Implementation :: CPython',
                     'Topic :: Scientific/Engineering :: Physics',
                 ],
                 zip_safe=False)
