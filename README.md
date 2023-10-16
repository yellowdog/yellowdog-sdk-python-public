# YellowDog SDK (Python)

The YellowDog SDK allows you to integrate the YellowDog Platform into your Python applications.

## Usage

Please refer to [the full documentation](https://docs.yellowdog.co/#/sdk/python-sdk).

## Advanced

### Building From Source

If you wish to modify the SDK, you can build it from source. You must have Python 3.7 installed:

```shell
python3 -m venv venv               # Create a new virtual environment
. venv/bin/activate                # Activate the virtual environment
pip install pip -U                 # Upgrade pip
pip install tox                    # Install tox
tox -e dev                         # Create a development environment
```

Pycharm may then be configured by adding .tox/dev/bin/python as the interpreter.

### Testing Against Multiple Python Versions

```shell
# Add the deadsnakes PPA
sudo add-apt-repository ppa:deadsnakes/ppa
# Update package indexes
sudo apt-get update
# Install all supported versions of Python                                              
sudo apt-get install python3.7 python3.7-distutils python3.8 python3.8-distutils python3.9 python3.9-distutils python3.10 python3.10-distutils python3.11 python3.11-distutils 
# Install tox
python3 -m pip install tox  
# Run tests for each Python version                                             
python3 -m tox                                                           
```