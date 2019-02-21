# Developing
You need the following things installed:
- python 3.5.3
- pip for python 3
- pipenv

Everything else is installed by the virtual environment:
```bash
$ pipenv install
```

To activate the virtenv, simply run:
```bash
$ pipenv shell
```
Now you can do things like:
```bash
$ python
»> import spheroboros
```

## Building Docs
Simply navigate to the docs/ directory and run`make` with the output style of your choice:
```bash
$ cd docs
$ make html
```

## Warning
Do NOT push to PyPI repos directly, using `setuptools` or `twine`.  Instead, use gitlab ci/cd!


