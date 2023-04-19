"""Setup file for creating the RfPart package."""

from setuptools import setup, find_packages

setup(
    name='RfPart',
    version='0.1',
    description='RF cascade analysis tool',
    author='Ricky Nite',
    author_email='rickynite@gmail.com',
    url='https://github.com/rickynite/RfPart',
    license='LGPL-2.1',
    packages=find_packages(),
    install_requires=['numpy'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v2.1 (LGPLv2.1)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
