from setuptools import setup, find_packages

setup(
    name='eznotes',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'rich',
    ],
    entry_points={
        'console_scripts': [
            'eznotes = eznotes:main',
        ],
    },
)
