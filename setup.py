from setuptools import setup, find_packages

setup(
    name="8bit-music-lib",   # pip install 時に使う名前
    version="0.1.0",
    description="A simple 8bit-style music library",
    author="neutrino-dot",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "scipy",
    ],
    extras_require={
        "sounddevice": ["sounddevice"],
        "simpleaudio": ["simpleaudio"],
        "jupyter": ["ipython"],
    },
    python_requires=">=3.8",
)