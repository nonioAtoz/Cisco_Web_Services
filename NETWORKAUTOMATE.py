from the_app import create_app
from config import Config
print("OUTPUT - PASSING IN FILE NETTWORKAUTOMATE:py")

# RUN OUR APP
app = create_app()

# Remember the two the_app entities? Here you can see both together in the same sentence.
# The Flask application instance is called the_app and is a member of the the_app package. The from the_app import the_app statement
# imports the the_app variable that is a member of the the_app package. If you find this confusing, you can rename either the
# package or the variable to something else.

# Flask needs to be told how to import it, by setting the FLASK_APP environment variable:
# (venv) $ export FLASK_APP=NETWORKAUTOMATE.py
# or
#(venv) $ set FLASK_APP=NETWORKAUTOMATE.py

# TO RUN THE APP
#flask run --host=127.0.0.1 --port=80
#or if we dont want to set up the ENV FOR THE APP WE CAN DO A
#    python NETWORKAUTOMATE.py
#if __name__ == '__main__':
#    app.run(host=app.config["SERVER_NAME"], port=app.config["PORT"], debug=app.config["DEBUG"])
