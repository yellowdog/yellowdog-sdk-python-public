# YellowDog SDK (Python)

The YellowDog SDK allows you to integrate the YellowDog Platform into your Python applications.

## Usage

Please refer to [the full documentation](https://docs.yellowdog.co/#/sdk/python-sdk).

## Advanced

### Building From Source

If you wish to modify the SDK, you can build it from source. You must have Python 3.8 installed:

```shell
./scripts/setup
```

Pycharm may then be configured by adding .tox/dev/bin/python as the interpreter.

### Debugging

When debugging the SDK via Pycharm, Pycharm will offer to install the CPython extensions to speed up debugging.

In order for this to work on Ubuntu, you need to first have the dev package for the version of Python you are debugging against.

For example:

```shell
sudo apt-get install python3.8-dev
```

### Testing Against Multiple Python Versions

```shell
# Add the deadsnakes PPA
sudo add-apt-repository ppa:deadsnakes/ppa
# Update package indexes
sudo apt-get update
# Install all supported versions of Python                                              
sudo apt-get install python3.8 python3.8-distutils python3.9 python3.9-distutils python3.10 python3.10-distutils python3.11 python3.11-distutils python3.12 python3.12-distutils  
# Install tox
python3 -m pip install tox  
# Run tests for each Python version                                             
python3 -m tox                                                           
```
