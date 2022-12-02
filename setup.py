from setuptools import find_packages, setup

from eznotes import VERSION

setup(
    name="eznotes",
    version=VERSION,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Click",
        "rich",
    ],
    entry_points={
        "console_scripts": [
            "eznotes = eznotes.entrypoints:main",
            "eznotes-getfull = eznotes.entrypoints.getfull:cli_main",
        ],
    },
)
