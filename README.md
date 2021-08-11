# YellowDog SDK (Python)

The YellowDog SDK allows you to integrate the YellowDog Platform into your Python applications.

## Usage

Please refer to [the full documentation](https://docs.yellowdog.co/api/python/index.html).

## Advanced: Building from Source

If you wish to modify the SDK, you can build it from source. You must have Python 3.7 installed:

    python3 -m venv venv               # Create a new virtual environment
    . venv/bin/                        # Activate the virtual environment
    pip install pip -U                 # Upgrade pip
    pip install -r requirements.txt    # Install all development and production dependencies
    pytest tests                       # Execute the unit tests
