from setuptools import setup, find_packages

setup(
    name="dataset_processing_lib",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "requests",
        "earthengine-api"
    ],
)
