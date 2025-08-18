"""
Setup script for the multi-agent scientific investigation system
"""

from setuptools import setup, find_packages
import os

# Read README for long description
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="scientific-agents",
    version="1.0.0",
    author="Scientific AI Research Team",
    author_email="research@example.com",
    description="Multi-agent AI system for automated scientific investigations",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/scientific-agents",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=8.3.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "viz": [
            "matplotlib>=3.7.0",
            "plotly>=5.17.0",
            "seaborn>=0.12.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "scientific-agents=src.main:main",
            "sci-cli=src.cli_interface:main",
        ],
    },
    include_package_data=True,
    package_data={
        "src": ["*.json", "*.yaml", "*.txt"],
    },
)