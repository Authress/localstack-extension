# Contributing to this LocalStack Extension

## Setup
```sh

pip install flake8 pytest
pip3 install -r requirements.txt -r test-requirements.txt
```

### Install local development version

To install the Authentication & Authorization extension into LocalStack in developer mode, you will need Python 3.10, and create a virtual environment in the extensions project.

In the newly generated project, run:

<!--
Support (Beta) version of localstack auth command
```bash
mkdir -p ~/.localstack
echo '{"token":true}' > ~/.localstack/auth.json
```

-->

```bash
cd localstack-extensions/authress
python -m pip install --upgrade pip
python3 -m pip install --upgrade localstack==2.2.0
make install
localstack extensions dev enable .
EXTENSION_DEV_MODE=1 localstack start
```
