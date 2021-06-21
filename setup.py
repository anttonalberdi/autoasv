from setuptools import setup

setup(name='autoasv',
    version='1.0',
    description='The funniest joke in the world',
    url='https://github.com/anttonalberdi/autoasv',
    author="Antton Alberdi",
    author_email="anttonalberdi@gmail.com",
    license='MIT',
    packages=['autoasv'],
    entry_points = {
        'console_scripts': ['autoasv=autoasv.autoasv:main'],
    },
    zip_safe=False)
