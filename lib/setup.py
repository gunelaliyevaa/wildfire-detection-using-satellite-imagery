from setuptools import setup, find_packages

setup(
    name='lib',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'requests',
        'matplotlib',
        'os',
        'tensorflow',
        'google-cloud-storage',
        'earthengine-api',
        'numpy'
    ])