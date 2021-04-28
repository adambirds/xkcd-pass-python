# xkcd_pass
![build status](https://github.com/adambirds/xkcd_password-gen/actions/workflows/build.yml/badge.svg)
[![PyPI version](https://badge.fury.io/py/xkcd_pass.svg)](https://badge.fury.io/py/xkcd_pass)
[![codecov](https://codecov.io/gh/adambirds/xkcd_password-gen/branch/master/graph/badge.svg?token=4RKK2ABREH)](https://codecov.io/gh/adambirds/xkcd_password-gen)
![PyPI - Downloads](https://img.shields.io/pypi/dm/xkcd_pass)

A flexible and scriptable password generator which generates strong passphrases, inspired by XKCD 936

```
$ xkcd_pass
> HeadscarfSuddenDumping93
```

![](https://imgs.xkcd.com/comics/password_strength.png)

## Install
`xkcd_pass` can easily be installed with the following command:

```
pip install xkcd_pass
```

or manually by:

```
python setup.py install
```

## Source
The source code can be found [here](https://github.com/adambirds/xkcd_password-gen).

Contributions welcome and gratefully appreciated!

## Requirements
Python 3 (Version 3.6 or later).

## Running `xkcd_pass`
`xkcd_pass` can be called with no arguments with an output using the default wordfile and settings.
```
$ xkcd_pass
> HeadscarfSuddenDumping93
```
The default settings return a single password made up of 3 words each having its first letter capitalized with two random digits afterwards.

It can also be called with a mixture of multiple arguments for example:

```
$ xkcd_pass -d _ -c 5 --min 5 --max 7 --padding-digits-num 4
> Mundane_Music_Spleen1837
> Reuse_Acclaim_Clarify2492
> Wildly_Contest_Anchor1798
> Imprint_Luster_Happy4339
> Scarf_Strobe_Footer5579
```

This will return:
* `-d _` words joined by `_`.
* `-c 5` 5 passwords to choose from.
* `--min 5 --max 7` words between 5 and 7 characters long.
* `--padding-digits-num 4` 4 digits on the end of the password.

A full overview of the available options can be accessed by running following command:

```
xkcd_pass --help
```

## Word Lists

Several word lists are provided with the package. The default, eff-long, was specifically designed by the EFF for [passphrase generation](https://www.eff.org/deeplinks/2016/07/new-wordlists-random-passphrases) and is licensed under [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/us/). As it was originally intended for use with Diceware ensure that the number of words in your passphrase is at least six when using it. Two shorter variants of that list, eff-short and eff-special, are also included. Please refer to the EFF documentation linked above for more information.

Note that `xkcd_pass` can be used with any word file of the correct format: a file containing one word per line.

## Changelog

* **Version 1.0.0**
    * Initial Release
* **Version 1.0.1**
    * Fixed license display on PyPI.
    * Fixed links to license files on PyPI.
* **Version 1.0.2**
    * Fix interactive usage.
    * Fix issue where wrong wordfile wasn't being recognised.
    * Add 100% test coverage.
* **Version 1.0.5**
    * Fix typo in static import causing wordfile error.
* **Version 1.0.6**
    * Change package name to `xkcd_pass`.

## License

This project is released under the [GNU GENERAL PUBLIC LICENSE v3](https://github.com/adambirds/xkcd_password-gen/blob/master/LICENSE). However the original code from [redacted/xkcd_password-generator](https://github.com/redacted/xkcd_password-generator) is licensed under the [BSD 3-Clause license](https://github.com/adambirds/xkcd_password-gen/blob/master/LICENSE.BSD).