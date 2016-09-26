from setuptools import setup, find_packages

setup(
    name='FLOG',
    version='0.79',
    description='FLOG: Flask Blog',
    url='https://github.com/optrv/flog',
    author='optrv',
    author_email='petr.ov@icloud.com',
    install_requires=['Flask>=0.11', 'flask-paginate>=0.4.5', 'Pillow>=3.3.1', 'pydub>=0.16.5'],
    packages=find_packages()
)
