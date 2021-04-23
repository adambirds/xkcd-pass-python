import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xkpassgen",  # Replace with your own username
    version="1.0.0",
    author="Adam Birds",
    author_email="adam.birds@adbwebdesigns.co.uk",
    description="Generate secure multiword passwords/passphrases, inspired by XKCD",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/adambirds/xkcd-password-gen",
    project_urls={
        "Bug Tracker": "https://github.com/adambirds/xkcd-password-gen/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={"console_scripts": ["xkpassgen=xkpassgen.xkpassgen:main"]},
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    include_package_data=True,
    python_requires=">=3.6",
)
