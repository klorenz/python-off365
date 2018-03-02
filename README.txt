https://stackoverflow.com/questions/288546/connect-to-exchange-mailbox-with-python
https://pypi.python.org/pypi/exchangelib/

# Usage

This is work in progress and right now you should run this as:

PYTHONPATH=. python -m off365 --help

and other commands.

For running this tool you have to register your app first on https://apps.dev.microsoft.com/.  
See https://developer.microsoft.com/en-us/graph/docs/concepts/auth_register_app_v2 for documentation.

Having registered your app there you can run:

  PYTHONPATH=. python -m off365 --client-id CLIENT_GUID --client-secret THE_SECRET --redirect-uri REDIRECT_URI --tenant YOUR_TENANT --username USERNAME

You will be asked for the password to username.  Data is stored for now in

~/.config/off365/config




