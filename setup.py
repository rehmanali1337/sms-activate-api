from setuptools import setup, find_packages
from cryptapi._metadata import __version__

required_packages = ["aiohttp", "aiofiles"]


setup(
    name="crypt-api-wrapper",
    version=__version__,
    author="Rehman Ali",
    author_email="",
    description="An async python wrapper for official cryptapi API",
    url="",
    packages=find_packages(),
    install_requires=required_packages,
)
