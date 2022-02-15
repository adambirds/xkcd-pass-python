import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

install_requires = ["argcomplete"]
setuptools.setup(
    name="xkcd-pass",
    version="1.1.1",
    author="Adam Birds",
    author_email="adam.birds@adbwebdesigns.co.uk",
    description="Generate secure multiword passwords/passphrases, inspired by XKCD",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/adambirds/xkcd-password-gen",
    project_urls={
        "Bug Tracker": "https://github.com/adambirds/xkcd-password-gen/issues",
    },
    license="LGPLv3",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    entry_points={"console_scripts": ["xkcd-pass=xkcd_pass.xkcd_pass:main"]},
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=install_requires,
)
