import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

with open("requirements.txt") as f:
    requires = f.read().splitlines()

setuptools.setup(
    name="ondewo-nlu-client-python",
    version="2.4.1",
    author="Ondewo GbmH",
    author_email="info@ondewo.com",
    description="This library facilitates the interaction between a user and his/her CAI server.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/ondewo/ondewo-nlu-client-python",
    packages=setuptools.find_packages(),
    package_data={
        'ondewo.nlu': ['py.typed']
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        'Development Status :: 3 - Alpha',
        'Topic :: Software Development :: Libraries',
    ],
    python_requires='>=3.0.1',
    install_requires=requires,
)
