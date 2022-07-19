from setuptools import setup, find_packages


setup(
    name="restconf-cli",
    version="0.1.1",
    description='command line tool for restconf',
    author='Muhammad Rafi',
    author_email='murafi@cisco.com',
    url='https://example.com/setup-py',
    py_modules=['restconf-cli'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click==7.1.2',
        'requests==2.26.0',
        'rich==11.2.0',
        'flake8==4.0.1',
        'pytest==7.0.1'
    ],
    setup_requires=['pytest-runner', 'flake8'],
    tests_require=['pytest'],
    entry_points='''
    [console_scripts]
    restconf-cli=restconf_cli:restconf_cli
    '''
)
