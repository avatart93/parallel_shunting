from setuptools import setup

setup(
    name='parallel_shunting',
    version='1.0',
    description='Shunting yard algorithm ran over multiple processes.',
    url='https://github.com/avatart93/parallel_shunting',
    author='Dexter',
    author_email='gilmuher93@gmail.com',
    license='GPLv3',
    packages=['parallel_shunting'],
    scripts=['scripts/launch_server.py', 'scripts/launch_client.py', 'scripts/launch_client.py'],
    long_description=open('README.txt').read()
)
