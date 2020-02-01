from setuptools import find_packages, setup

setup(
    name='paperless',
    version='1.0.0-SNAPSHOT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'werkzeug'
    ],
    tests_require=[
        'pytest',
        'coverage',
    ],
)
