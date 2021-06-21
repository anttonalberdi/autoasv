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
        'console_scripts': ['mybinary=autoasv.autoasv:cli'],
    },
    zip_safe=False)
