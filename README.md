# xkcd-pass
![build status](https://github.com/adambirds/xkcd-password-gen/actions/workflows/build.yml/badge.svg)
[![PyPI version](https://badge.fury.io/py/xkcd-pass.svg)](https://badge.fury.io/py/xkcd_pass)
[![codecov](https://codecov.io/gh/adambirds/xkcd-password-gen/branch/master/graph/badge.svg?token=Ia2ppYjdkw)](https://codecov.io/gh/adambirds/xkcd-password-gen)
![PyPI - Downloads](https://img.shields.io/pypi/dm/xkcd-pass)
[![GitHub release](https://img.shields.io/github/release/adambirds/xkcd-password-gen.svg)](https://github.com/adambirds/xkcd-password-gen/releases/latest)
[![code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![mypy coverage](https://img.shields.io/badge/mypy-100%25-green.svg)](https://github.com/python/mypy)

A flexible and scriptable password generator which generates strong passphrases, inspired by [XKCD 936][xkcd].

```
$ xkcd-pass
> DenotePetroleumMournfulStoreroom47
```

Whilst this password generator is inspired by [XKCD 936][xkcd], its defaults have been configured in a way which gives this tool the most compatibility out of the box with the majority of services we use passwords for today. The faults that we have set are:
* Phrase containing 4 words between 5 and 9 characters (The default wordfile `eff-long` only contains words between 5 and 9 characters).
* The first letter of each word is capitalized.
* The passphrase is ended with two random digits.

This allows the password generator to provide passwords by default which will be strong, easy to remember, difficult to brute-force and still pass the usual requirements of at least one upper-case letter, one lower-case letter and at least 1 digit.

Some of the base code that I started with for this project come from [redacted/xkcd-password-generator](https://github.com/redacted/XKCD-password-generator). Whilst that package was great, the reason for taking this project separately and adapting it is for the below reasons:
* To neaten up the codebase to make it easier for other contributors to help develop it further.
* To provide the project with an active maintainer meaning bugs and potential new features can be released more promptly.
* To neaten up the output so it is much easier to use with our scripts and programs.
* To provide it with more compatibility for more services by adding the random digit generator to the end of the password.
* To have a thoroughly tested codebase giving users the ability to trust that the package will work as expected.

[xkcd]: https://xkcd.com/936/
![](https://imgs.xkcd.com/comics/password_strength.png)

## Support
For support using this bot, please join our [official support server](https://discord.gg/f5veJaa4ZX) on [Discord](https://discord.com).

[![discord](https://img.shields.io/discord/941885906443468880?color=%237289DA&label=Coding%20With%20Adam&logo=discord&logoColor=white)](https://discord.gg/f5veJaa4ZX)

## Install
`xkcd-pass` can easily be installed with the following command:

```
pip install xkcd-pass
```

or manually by:

```
python setup.py install
```

## Source
The source code can be found [here](https://github.com/adambirds/xkcd-password-gen).

Contributions welcome and gratefully appreciated!

## Requirements
Python 3 (Version 3.6 or later).

## Running `xkcd_pass`
`xkcd-pass` can be called with no arguments with an output using the default wordfile and settings.
```
$ xkcd-pass
> HeadscarfSuddenDumping93
```
The default settings return a single password made up of 4 words each having its first letter capitalized with two random digits afterwards.

It can also be called with a mixture of multiple arguments for example:

```
$ xkcd-pass -d _ -c 5 --min 5 --max 7 --padding-digits-num 4
> Crisped_Harsh_Relearn_Chemist9839
> Brittle_Deacon_Banker_Amigo4544
> Ambush_Emptier_Antsy_Walrus2442
> Donated_Either_Stardom_Duress8549
> Ether_Prevail_Virtual_Tiger3393
```

This will return:
* `-d _` words joined by `_`.
* `-c 5` 5 passwords to choose from.
* `--min 5 --max 7` words between 5 and 7 characters long.
* `--padding-digits-num 4` 4 digits on the end of the password.

A full overview of the available options can be accessed by running following command:

```
xkcd-pass --help
```

## Bash-Completion
`xkcd-pass` also supports bash-completion. To set this up you need to add the below to your `.bashrc` file:

```
eval "$(register-python-argcomplete xkcd-pass)"
```

This will then take effect the next time you login. To enable bash-completion immediately, you can run:

```
source .bashrc
```

## Word Lists

Several word lists are provided with the package. The default, eff-long, was specifically designed by the EFF for [passphrase generation](https://www.eff.org/deeplinks/2016/07/new-wordlists-random-passphrases) and is licensed under [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/us/). As it was originally intended for use with Diceware ensure that the number of words in your passphrase is at least six when using it. Two shorter variants of that list, eff-short and eff-special, are also included. Please refer to the EFF documentation linked above for more information.

Note that `xkcd-pass` can be used with any word file of the correct format: a file containing one word per line.

## Changelog

* **Version 1.0.0**
    * Initial Release
* **Version 1.0.1**
    * Fixed license display on PyPI.
    * Fixed links to license files on PyPI.
* **Version 1.0.2**
    * Fix interactive usage.
    * Fix issue where wrong wordfile wasn't being recognized.
    * Add 100% test coverage.
* **Version 1.0.5**
    * Fix typo in static import causing wordfile error.
* **Version 1.0.6**
    * Change package name to `xkcd_pass`.
* **Version 1.0.7**
    * Change command-line package to `xkcd-pass`.
* **Version 1.0.9**
    * Fix issues with README.md badges after rename.
    * Update `--help` for `MIN_LENGTH` and `MAX_LENGTH`.
    * Update number of words in password to 4 by default.
    * Restructured tests into individual files to neaten up codebase.
    * Added static type annotations to the codebase.
    * Added support for `zulint` to run various code linters easily.
* **Version 1.1.0**
    * Add support for bash-completion for `xkcd-pass`.
    * Update github links to correct names in PyPi metadata.
    * Add tool to prep dev environment.
    * Add documentation for contributing and development.
    * Add support for correct entropy for padded digits.
* **Version 1.1.1**
    * Add docs for official discord support server.
    * Update link to source code in docs to correct typo.
    * Fix an issue in contributing logs to add an extra step needed.
    * Fixed issue with codecov badge in docs.
    * Update example docs to use correct defaults.
    * Fixed issue with prep-dev-environment script.

## License

This project is released under the [GNU GENERAL PUBLIC LICENSE v3](https://github.com/adambirds/xkcd-password-gen/blob/master/LICENSE). However the original code from [redacted/xkcd-password-generator](https://github.com/redacted/XKCD-password-generator) is licensed under the [BSD 3-Clause license](https://github.com/adambirds/xkcd-password-gen/blob/master/LICENSE.BSD).

## Contributing

Anybody is welcome to contribute to this project. I just ask that you check out our contributing guidelines
[here](https://github.com/adambirds/xkcd-password-gen/blob/master/docs/contributing/contributing.md) first.
