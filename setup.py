from distutils.core import setup
import sys
import py2exe
sys.path.append("C:\\WINDOWS\\WinSxS\\x86_Microsoft.VC90.CRT_1fc8b3b9a1e18e3b_9.0.21022.8_x-ww_d08d0375")
setup(
    windows = ['noctopus'],
    options = {
        'py2exe' : {
            'includes' :['sys']
        }
    }
)
