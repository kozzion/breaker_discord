from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name="breaker_discord",
    version="0.0.2",
    packages=find_packages(),
    package_data={},
    python_requires=">=3.5",
    install_requires=requirements,
    author="Jaap Oosterbroek",
    author_email="jaap.oosterbroek@gmail.com",
    description="stuff for building cool discord bots",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kozzion/breaker_discord",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)