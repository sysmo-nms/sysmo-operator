from distutils.core import setup

setup(
    name='noctopus-client',
    version='1.0',
    author='Sebastien Serre',
    author_email='sserre.bx@gmail.com',
    url='www.github.com/ssbx/noctopus-client',
    package_dir = {'': 'src'},
    scripts = ['bin/noctopus-client'],
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
