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
        'click==6.7',
        'Flask==0.12.2',
        'itsdangerous==0.24',
        'Jinja2==2.9.6',
        'MarkupSafe==1.0',
        'PyJWT==1.5.3',
        'Werkzeug==0.12.2'
    ],
    tests_require=['nose'],
)