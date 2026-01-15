from setuptools import find_packages, setup

setup(
    name="myworkflow",
    version="1.0.0",
    description="CLI tools for development workflows",
    author="Helio Fernandes 404",
    author_email="heliodevhub@gmail.com",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "myworkflow=main:main",
        ],
    },
    python_requires=">=3.10",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
