from setuptools import setup

VERSION = '0.0.1'

with open('README.rst', 'r', encoding='utf-8') as fo:
    long_descr = fo.read()

setup(
    name='django-modeltranslation-xliff',
    version=VERSION,
    packages=['modeltranslation_xliff'],
    url='',
    license='MIT',
    author='Roman Miroshnychenko',
    author_email='roman1972@gmail.com',
    description='XLIFF exchange for django-modeltranslation',
    long_description=long_descr,
    install_requires=[
        'Django>=1.11',
        'django-modeltranslation>=0.13b1',
        'nltk',
        'lxml',
    ],
    setup_requires=['pytest-runner'],
    test_require=['pytest', 'pytest-django'],
    zip_safe=False
)
