from setuptools import setup, find_packages

setup(
    name = 'FLOG',
    version = '0.79',
    description = 'FLOG: Flask Blog',
    url = 'https://github.com/optrv/flog',
    author = 'optrv',
    author_email = 'petr.ov@icloud.com',
    install_requires = ['Flask', 'Pillow', 'pydub'],
    packages = find_packages()
)

