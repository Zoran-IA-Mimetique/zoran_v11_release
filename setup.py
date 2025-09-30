from setuptools import setup, find_packages

setup(
    name="zoran-mimetic",
    version="1.0.0a1",
    description="Zoran — Injecteurs GlyphNet & Architecture Polymorphique",
    author="Institut IA Zoran",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.23",
        "matplotlib>=3.7",
        "cryptography>=41.0",
    ],
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "zoran-demo=zoran.__main__:main",
        ],
    },
)
