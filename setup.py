from setuptools import setup, find_packages

setup(
    name="flexi-nlp-tools",
    version="0.3.3",
    description="NLP toolkit based on the flexi-dict data structure, designed for efficient fuzzy search, with a focus on simplicity, performance, and flexibility.",
    author="Tetiana Lytvynenko",
    author_email="lytvynenkotv@gmail.com",
    license="MIT",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    keywords=["fuzzy search", "nlp tools", "flexi search", "numeral converter"],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "dill>=0.3.9,<0.4",
        "pandas>=2.2.3,<2.3",
        "g2p_en>=2.1.0, <2.2",
        "transliterate>=1.10.2, <1.11",
        "nltk>=3.9.1, <3.10",
        "certifi"
    ],
    python_requires=">=3.11",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    zip_safe=False,
    package_data={
        "numeral_converter.resource": ["*.csv"],
    },
)
