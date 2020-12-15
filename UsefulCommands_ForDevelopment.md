# RUN THE APP
   ```
    flask run --host 127.0.0.1 --port 80
    
    - host and port will be where the app will receive th requests
   ```
# Useful commands for development in python
```
set FLASK_ENV=production
set FLASK_ENV=development
flask run --host=127.0.0.23 --port=5001
flask run --host=127.0.0.1 --port=80
python -m json.tool os_environ.json | findstr "LOG_TYPE"
python -m json.tool os_environ.json --sorted-keys
ptyhon -m --help

curl 127.0.0.1/index
curl -help file_name

# Believe it or not, this first version of the application is now complete! Before running it,
# though, Flask needs to be told how to import it, by setting the FLASK_APP environment variable:
# (venv) $ export FLASK_APP=name_of_the_app.py
# or
# (venv) $ set FLASK_APP=name_of_the_app.py
```
- More on Useful commands
```
## python version
python -m --version
# or
python -V

CHECK VERSION 
if not sys.version_info.major == 3 and sys.version_info.minor >= 6:

    print("Python 3.6 or higher is required.")

    print("You are using Python {}.{}.".format(sys.version_info.major, sys.version_info.minor))

    sys.exit(1)
===========================================================================
##  PIP COMMANDS
# SEACRH FOR PACKAGES
    pip search <name_package>
# INSTALL PACKAGE
    pip install package
# LIST PACKAGES INSTALED
     pip list
# LIST PACKAGES OUTDATED 
    pip list -o
    or
    pip list --outdated
# to list out all the packages that are up to date
    pip list -u
    or
    pip list --uptodate
#  get details about a package that is currently installed
    pip show Flask
    pip show jinja2
# UNISTALL package
    pip unistall <name_package>

# freeze the packages and their current version
    pip freeze > requirements.txt	

# install packages from requirements.txt
    pip install -r requirements.txt
=============================================================================
## Python command-line tools
https://opensource.com/article/18/5/3-python-command-line-tools

1. import click
2. from docopt import docopt
3. import fire 
4.from setuptools import setup

#install package using setup:
pip install . 

## SETUP A PATH TO PYTHON MODULE
set PYTHONPATH=C:\Users\nuno\PycharmProjects\NextApprouchfinalNetworkAutomate\the_app
set PYTHONPATH=PATH/TO/THE/MODULE

## run unittest
python -m unittest <name_of_the_file.py>

## read a json - we can use a pipe with grep
    python -mjson.tool netwrok.json
    #
    curl http://api.joind.in | python -mjson.tool

## ON IMPORTS 
# Absolute imports - import something available on sys.path
# Relative imports - import something relative to the current module, must be a part of a packag
import sys
# WE HAVE TO USE SETUP TOOLS FOR PACKAGING OUR APP 
#for line in sys.path:
#    print(line)
#sys.path.append('C:\\Users\\nuno\\PycharmProjects\\NextApprouchfinalNetworkAutomate\\the_app')
#for line in sys.path:
#    print(line)
#try:
#    import the_app

#    the_app.app.logger.info("This is a message writen on our tests.py")
#except ImportError:
#    sys.exit("We could not find our_package." )
# set PYTHONPATH=C:\Users\nuno\PycharmProjects\NextApprouchfinalNetworkAutomate\the_app

============================================================================0
## VIRTUAL ENVIRNMENTS
we need to run
. venv/bin/activate
or
source venv/bin/activate

## instaLL on linux ??
yum -y install python-virtualenv
virtualenv env
source env/bin/activate

pip install ipython
```


(TEST THIS) 
- Setup for Gunicorn with Nginx. #Deploy App on Production. Alternatives to Gunicorn?
  - https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04-pt
  - [x] Check online miguel Grinberg great tutorial on how deploy a flask application.  

RESOURCES: 
 - Grinberg, michael, O'reilly, 2018, link: https://books.google.pt/books?id=cVlPDwAAQBAJ&pg=PT32&lpg=PT32&dq=how+to+create+a+request+object+accessible+form+flask+app&source=bl&ots=xNKSho5jfY&sig=ACfU3U23LVwpm3njMUuv_5T9qqk7zw6w5A&hl=pt-PT&sa=X&ved=2ahUKEwjrjfrNvNnpAhU57uAKHZZ6BDoQ6AEwCnoECAoQAQ#v=onepage&q=how%20to%20create%20a%20request%20object%20accessible%20form%20flask%20app&f=false
 - logging _issues, link: https://stackoverflow.com/questions/15727420/using-logging-in-multiple-modules
 - logging _issues, link: https://www.scalyr.com/blog/getting-started-quickly-with-flask-logging/
 - Error AND Exceptions, link: https://docs.python.org/3/tutorial/errors.html
 - idea for after request, link: https://medium.com/tenable-techblog/the-boring-stuff-flask-logging-21c3a5dd0392
 - Deploy SWAGGER FAST: use blueprints, link https://pypi.org/project/flask-swagger-ui/
 - verify this link: # https://stackoverflow.com/questions/17740089/register-function-for-all-urls-in-flask
 - GIT: https://git-scm.com/download/win
 - INSTALL TEXTFSM :https://pynet.twb-tech.com/blog/automation/netmiko-textfsm.html
 - gunicorn: https://gunicorn.org/#docs
 - CISCO COMMANDS MODE :https://www.cisco.com/E-Learning/bulk/public/tac/cim/cib/using_cisco_ios_software/02_cisco_ios_hierarchy.htm