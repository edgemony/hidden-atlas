from setuptools import setup, find_packages

setup(
    name='hidden-atlas',
    version='0.1',
    description='A game based on city maps and geography',
    author='PortlandGames',
    packages=find_packages(),
    install_requires=[
        'osmnx>=1.9.0',
        'matplotlib>=3.8.0',
        'geopandas>=0.14.0',
        'adjustText>=1.0.0'
    ],
    python_requires='>=3.6',
    include_package_data=True,
    package_data={
        'hidden_atlas': ['data/*.txt'],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'Programming Language :: Python :: 3',
        'Topic :: Games/Entertainment',
    ],
)
