from distutils.core import setup

setup(
    name='tkorder',
    version='1.0',
    author='Sebastien Serre',
    author_email='sserre.bx@gmail.com',
    url='www.github.com/ssbx/tkorder',
    package_dir = {'': 'src'},
    scripts = ['bin/tkorder'],
    py_modules=[
        'ModTracker',
        'ModTrackerCube',
        'ModTrackerGraphite',
        'ModTrackerTargetView',
        'ModTrackerTree',
        'Supercast',
        'SupercastPDU',
        'TkorderIcons',
        'TkorderMain'
    ],
)
