from setuptools import setup, find_packages
from pathlib import Path

this_dir = Path(__file__).parent
long_description = (this_dir / "README.md").read_text(encoding="utf-8")

setup(
    name="8bit-music-lib",   # pip install 時に使う名前
    version="0.2.1",
    description="A simple 8bit-style music library",
    long_description=long_description,
    long_description_content_type="text/markdown",  # PyPIでREADMEをMarkdown表示
    author="neutrino-dot",
    license="MIT",
    url="https://github.com/neutrino-dot/8bit-music-lib",  # GitHub リポジトリ
    project_urls={
        "Bug Tracker": "https://github.com/neutrino-dot/8bit-music-lib/issues",
        "Documentation": "https://github.com/neutrino-dot/8bit-music-lib#readme",
        "Source Code": "https://github.com/neutrino-dot/8bit-music-lib",
        "Release Notes": "https://github.com/neutrino-dot/8bit-music-lib/releases"
    },
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
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Sound/Audio :: Sound Synthesis",
    ],
)
