from setuptools import setup

VERSION = '1.0.0b1'

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
    python_requires='>=3.4',
    install_requires=[
        'Django>=1.11',
        'django-modeltranslation>=0.13b1',
        'nltk',
        'lxml',
    ],
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Text Processing :: Linguistic'
    ]
)
