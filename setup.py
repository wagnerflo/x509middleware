from setuptools import setup
from pathlib import Path

setup(
    name='x509middleware',
    description='Python middleware for working with (client) certificates.',
    long_description=(Path(__file__).parent / 'README.md').read_text(),
    long_description_content_type='text/markdown',
    version='1.0',
    author='Florian Wagner',
    author_email='florian@wagner-flo.net',
    url='https://github.com/wagnerflo/x509middleware',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    license_files=['LICENSE'],
    python_requires='>=3.3',
    install_requires=['asn1crypto'],
    packages=['x509middleware'],
)
