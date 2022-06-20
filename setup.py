import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

with open('requirements.txt') as f:
    requires = f.read().splitlines()

setuptools.setup(
    name='ondewo-nlu-client',
    version='2.8.1',
    author='Ondewo GmbH',
    author_email='office@ondewo.com',
    description='This library facilitates the interaction between a user and his/her CAI server.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ondewo/ondewo-nlu-client-python',
    packages=[
        np
        for np in filter(
            lambda n: n.startswith('ondewo.') or n == 'ondewo',
            setuptools.find_packages()
        )
    ],
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent',
        'Development Status :: 5 - Production/Stable',
        'Topic :: Software Development :: Libraries',
    ],
    python_requires='>=3',
    install_requires=[
        "dataclasses-json==0.5.7",
        "Faker~=13.13.0",
        "google-api-core~=2.8.1",
        "grpcio-reflection~=1.46.3",
        "grpcio-tools~=1.46.3",
        "ondewo-client-utils==0.1.1",
        "ondewo-logging~=3.1.0",
        "polling==0.3.2",
        "protobuf~=3.20.1",
        "pytest==7.1.2",
        "python-dateutil~=2.8.2",
        "regex==2022.6.2",
        "setuptools==62.6.0",
    ],
)
