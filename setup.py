from setuptools import setup, find_packages

setup(
    name='Servo',
    version='1.0',
    description='An IRC Bot made with Twisted.',
    url='https://github.com/AWilliams17',
    author='Austin Williams',
    author_email='awilliams17411@gmail.com',
    keywords='IRC Bot',
    packages=find_packages(exclude=['tests']),
    install_requires=['twisted', 'requests', 'beautifulsoup'],
    entry_points={
        'console_scripts': [
            'Servo=Servo.bin.servo:main',  # I think that's how it works?
        ],
    },
)
