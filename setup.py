from setuptools import setup, find_packages


setup(
    name='uds-sdk',
    version='2.0.0',
    url='http://github.com/nict-isp/uds-sdk',
    author='NICT',
    description='A Crawling tool for sensing event data.',
    packages=find_packages(exclude=('tests', 'tests.*')),
    include_package_data=True,
    entry_points={
        'console_scripts': ['uds = uds.tools.cli:main']
    },
    install_requires=[
        'beautifulsoup',
        'bunch',
        'lxml',
        'MySQL-python',
        'python-dateutil',
        'pytz',
        'simplejson',
        'suds',
        'tweepy',
    ],
)
