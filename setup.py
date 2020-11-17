import os

from setuptools import setup


this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md')) as f:
    long_description = f.read()


setup(
    name='tox-poetry',
    description='Tox poetry plugin',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='0.1.2',
    author='Timofey Kukushkin',
    author_email='tima@kukushkin.me',
    url='https://github.com/tkukushkin/tox-poetry',
    py_modules=['tox_poetry'],
    package_dir={'': 'src'},
    install_requires=[
        'pluggy',
        'tox>=3.7.0;python_version>="3"',
        'tox==3.15.1;python_version<"3"',
        'toml',
    ],
    extras_require={
        'test': [
            'coverage',
            'pycodestyle;python_version>="3.9"',
            'pylint;python_version>="3.9"',
            'pytest',
        ],
    },
    entry_points={
        'tox': ['poetry = tox_poetry'],
    },
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: tox',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    project_urls={
        'Source': 'https://github.com/tkukushkin/tox-poetry',
    },
)
