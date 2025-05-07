from setuptools import setup, find_packages

setup(
    name="debuginator",
    version="0.0.1",
    description="AI-powered error analysis tool",
    packages=find_packages(),
    install_requires=open("requirements.txt").read().splitlines(),
    entry_points={
        "console_scripts": [
            "debuginator=debuginator.cli:main",
        ],
    },
)