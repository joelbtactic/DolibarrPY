# DolibarrPY

Dolibarr PY is a simple Python client for Dolibarr API.

## How to prepare the environment on Linux (Debian)
In this section is described how to get the development environment ready on Debian based systems.

It's recommended to use `virtualenv` and `pip` packages. You can install this two dependencies runnig:
```bash
sudo apt-get update
sudo apt-get install virtualenv python3-pip
```

Once you have `virtualenv` and `pip` tools ready it's time to prepare the virtual environment to run the application.
Following we create a virtual environment and install all Python dependencies:
```bash
cd DolibarrPY
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

## Dolibarr API Configuration
To use DolibarrPY, you need to create a configuration file named `dolibarrpy.ini` with your Dolibarr API credentials:

```ini
[Dolibarr API Credentials]
url = https://dolibarr.example.org/api/index.php/
api_token = your_api_token
application_name = DolibarrPY
verify_ssl = True
```
