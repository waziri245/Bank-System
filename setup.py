from setuptools import setup, find_packages

setup(
    name="bank-system",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "tkinter",
    ],
    python_requires=">=3.6",
)