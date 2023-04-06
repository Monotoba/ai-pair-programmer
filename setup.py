import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(f"{here}/docs/USERGUIDE.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="AIPairProgrammer",
    version="0.0.1",
    author="SensorNet.Us (Randall Morgan)",
    author_email="<rmorgan@sensornet.us>",
    description="Pair Programming with AI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="package URL",
    project_urls={
        "Bug Tracker": "package issues URL",
    },
    classifiers=[
        "Programming Language :: Python :: 3.7+",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    dependencies=[

    ],
    package_dir={"aipairprogrammer": ""},
    packages=find_packages(where="./aipairprogrammer"),
    python_requires=">=3.7"
)
