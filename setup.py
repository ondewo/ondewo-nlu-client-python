import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

with open("requirements.txt") as f:
    requires = []
    for line in f:
        req = line.strip()
        if "#egg=" in req:
            req_url, req_name = req.split("#egg=")
            req_str = f"{req_name} @ {req_url}"
        else:
            req_str = req
        print(req_str)
        requires.append(req_str)

setuptools.setup(
    name="ondewo-nlu-client",
    version="1.1.3",
    author="Ondewo GbmH",
    author_email="info@ondewo.com",
    description="This library facilitates the interaction between a user and his/her CAI server.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ondewo/ondewo-nlu-client-python",
    packages=[
        np for np in filter(lambda n: n.startswith("ondewo.") or n == "ondewo", setuptools.find_packages())
    ],
    package_data={"ondewo.nlu": ["py.typed"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Topic :: Software Development :: Libraries",
    ],
    python_requires=">=2.6,!=3.0.*",
    install_requires=requires,
)
