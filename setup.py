from setuptools import setup

setup(
    name='trepl',
    version='0.1',
    packages=['trepl'],
    author="Wes Chow",
    author_email="wes@chartbeat.com",
    description=("Generic Tiered Replication implementation."),
    license="Apache",
    keywords="tiered replication copysets",
    url="https://github.com/chartbeat-labs/trepl",
    long_description="""
Generic Tiered Replication implementation.

Trepl generates copysets using the Tiered Replication
algorithm. Copysets are useful for picking nodes for replicating data
in a distributed system, among other use cases. See
https://github.com/chartbeat-labs/trepl for more details.
"""
    ,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        "Programming Language :: Python",
        "License :: OSI Approved :: Apache Software License",
    ],
)
