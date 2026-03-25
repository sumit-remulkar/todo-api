from setuptools import setup

setup(
    name='Todo API',
    version='1.0',
    packages=['backend'],
    install_requires=['fastapi', 'uvicorn'],
    include_package_data=True,
    package_data={'backend': ['models.py']},
    author='Your Name',
    author_email='your.email@example.com'
)