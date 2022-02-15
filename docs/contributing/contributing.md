# Contributing

If you would like to contribute to `xkcd-pass`, then your contributions are definitely
welcome and will be very appreciated. Below is some guidance to help contribute to this
project.

## Development Environment Setup

The first thing you need to do is fork this project and then clone that project to your
local machine. I recommend either developing on Ubuntu or WSL 2.0 if using Windows.

Once you have cloned the project, navigate to that directory with:

```
cd xkcd-password-gen
```

To get your development environment ready and install any required dependencies run:

```
tools/setup/prep-dev-environment
```

and

```
tools/setup-git-repo
```

and
```
source xkcd-password-gen/bin/activate
```

The middle command will setup some commit hooks to run our linters on any changed files before
the commit and then run the linters on your commit message to ensure it meets our
commit message guidelines. You can read our guidelines [here](https://github.com/adambirds/xkcd-password-gen/blob/master/docs/contributing/commit-guidelines.md).

## Linters and Tests

The linters that will be ran when you try and commit, will only run on changed files. To
run these manually on the entire project you can run:

```
tools/lint
```

We also have 100% test coverage on this project so you should ensure to write tests for all
the code you write and you can run these with:

```
pytest -v
```

## Git

We use a **[rebase][gitbook-rebase]-oriented workflow.** We do not use merge
commits. This means you should use `git fetch` followed by `git rebase`
rather than `git pull` (or you can use `git pull --rebase`). Also, to prevent
pull requests from becoming out of date with the main line of development,
you should rebase your feature branch prior to submitting a pull request, and
as needed thereafter. If you're unfamiliar with how to rebase a pull request,
[read this excellent guide][github-rebase-pr].

[gitbook-rebase]: https://git-scm.com/book/en/v2/Git-Branching-Rebasing
[github-rebase-pr]: https://github.com/edx/edx-platform/wiki/How-to-Rebase-a-Pull-Request

## Building Package and Testing Locally

To build the package run:

```
python3 -m build
```

You can then install this locally with the following command replacing the version number
with the current one:

```
pip install dist/xkcd_pass-1.0.9-py3-none-any.whl --force-reinstall
```
