from setuptools import setup

setup(
    name='parallel_shunting',
    version='1.0',
    description='Shunting yard algorithm ran over multiple processes.',
    url='https://github.com/avatart93/parallel_shunting',
    author='Dexter',
    author_email='gilmuher93@gmail.com',
    license='GPLv3',
    packages=['parallel_shunting', 'data'],
    package_data={'data': ['scripts/*.txt']},
    entry_points={
        'console_scripts': [
            'psy_tests = parallel_shunting.tests:main',
            'psy_server = parallel_shunting.server:main',
            'psy_client = parallel_shunting.client:main'
        ]
    }
)
