from setuptools import setup, find_packages 

setup(
    name='redpitaya_resonators',
    packages=find_packages(where=("src")),
    package_dir={"":"src"}
)