from setuptools import setup, find_packages

setup(
    name='Flask-JWT-Login',
    version='0.0.4',
    url='https://github.com/JeongUkJae/Flask-JWT-Login',
    license='MIT',
    author='Jeong Ukjae',
    author_email='jeongukjae@gmail.com',
    description='Flask extension that helps authentication using JWT',
    packages=find_packages(exclude=['tests']),
    zip_safe=False,
    test_suite='nose.collector',
    include_package_data=True,
    install_requires=[
        'Flask==1.0.2',
        'PyJWT==1.6.4',
    ],
    tests_require=['nose'],
)