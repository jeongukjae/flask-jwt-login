from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='Flask-JWT-Login',
    version='0.0.1',
    url='https://github.com/JeongUkJae/Flask-JWT-Login',
    license='MIT',
    author='Jeong Ukjae',
    author_email='jeongukjae@gmail.com',
    description='Flask extension that helps authentication using JWT',
    packages=find_packages(exclude=['tests']),
    long_description=open('README.md').read(),
    zip_safe=False,
    test_suite='nose.collector',
    include_package_data=True,
    install_requires=requirements,
    tests_require=['nose'],
)