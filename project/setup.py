"""Setup configuration for the CollabLearn project."""

from setuptools import setup, find_packages

setup(
    name="collablearn",
    version="0.1.0",
    description=(
        "Human-Computer Collaborative Learning System Prototype — "
        "Research on Intelligent Education and Industry Development"
    ),
    author="Research Group",
    python_requires=">=3.10",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "networkx>=3.3",
        "numpy>=1.26",
        "scipy>=1.13",
        "openai>=1.30",
        "tiktoken>=0.7",
        "pandas>=2.2",
        "pydantic>=2.7",
        "sqlalchemy>=2.0",
        "click>=8.1",
        "pyyaml>=6.0",
        "rich>=13.7",
        "python-dateutil>=2.9",
        "tqdm>=4.66",
    ],
    extras_require={
        "dev": [
            "pytest>=8.2",
            "pytest-cov>=5.0",
            "mypy>=1.10",
            "ruff>=0.4",
        ],
    },
    entry_points={
        "console_scripts": [
            "collablearn=src.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Education",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
