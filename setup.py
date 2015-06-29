from setuptools import setup

setup(
    name = 'mfp_query_helper',
    version = '0.1',
    packages = ['mfp_query_helper'],
    entry_points = {
        'console_scripts': [
            'mfp_query_helper = mfp_query_helper.__main__:main'
        ]
    },

    install_requires = ['elasticsearch==1.6.0'],

    author = 'IBM',
    description = 'Query helper for MFP Analytics'
)
