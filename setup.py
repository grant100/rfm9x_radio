import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rfm9x",
    version="1.0.0",
    author="Grant Sowards",
    description="RFM9x LoRa Radio",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/grant100/rfm9x_radio.git",
    packages=setuptools.find_packages(),
    install_requires=['Flask', 'Flask-Cors', 'setproctitle', 'adafruit-circuitpython-ssd1306', 'adafruit-circuitpython-framebuf', 'adafruit-circuitpython-rfm9x'],

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Home Automation",
        ""
    ],
    python_requires='>=3.6',
)
