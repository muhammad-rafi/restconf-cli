from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()


classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "Intended Audience :: End Users/Desktop",
    "Intended Audience :: System Administrators",
    "Operating System :: OS Independent",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Topic :: Other/Nonlisted Topic"
]

setup(
    name="restconf-cli",
    version="0.1.4",
    description='command line tool for restconf',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Muhammad Rafi',
    author_email='murafi@cisco.com',
    url='https://github.com/muhammad-rafi/restconf-cli',
    license='MIT',
    classifiers=classifiers,
    py_modules=['restconf_cli'],
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=[
        'click==7.1.2',
        'requests==2.26.0',
        'rich==11.2.0'
    ],
    setup_requires=['pytest-runner', 'flake8'],
    tests_require=['pytest'],
    entry_points='''
    [console_scripts]
    restconf-cli=restconf_cli:restconf_cli
    '''
)
