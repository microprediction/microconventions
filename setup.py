import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="microconventions",
    version="0.3.4",
    description="Conventions used at MicroPrediction.Org",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/microprediction/microconventions",
    author="microprediction",
    author_email="info@microprediction.org",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["microconventions"],
    test_suite='pytest',
    tests_require=['pytest'],
    include_package_data=True,
    install_requires=["muid>=0.5.0", "getjson", "pymorton", "numpy", "scipy", "requests", "deepdiff","schema","tdigest"],
    entry_points={
        "console_scripts": [
            "microconventions=microconventions.__main__:main",
        ]
    },
)
