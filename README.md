# Cisco_Web_Services
A series of webservices that allow clients to interact with cisco network devices
1.  **Application name:** NETWORKAUTOMATE
2. **Description:**
       A series of webservices that allow clients to interact with cisco network devices.
        We can configure devices or get information of various aspects of device configuration.
        
        All webservices expect a Json data object: A dictionary with some keys and values
        
        - The value for the key 'ip', is the ip address of the network device that the API will try to interact.
        
        - The key 'type' is optional. It represents the type of connection that client wants to force the API to use when connecting with network device.
        'type' value could be 'ssh' or 'telnet'.
        If you omit 'type', The API will try both connections when interacting with the network devices.
        
        - The key 'port' is also optional. Its value represents the network device port that are listening for connections.
        If you omit 'port', the API will use 22 for default ssh connection, and 23 for default telnet.
        
        
        For detailed information on what we are expecting for each service, check webservices definitions, below
        Note: We will return Json data objects
        
        WARNING:
        
        We can't configure or interact with Cisco network devices that have a '#' character present in the hostname. We may try, but it could cause unexpected errors.
        
        ######## Check application documentation for details ##################
        
3. Application deployment: Installation and first-time-setup **(SUMMARY)**
    - We need to have installed on our server, **Python 3.7.6. Version**<br>
    - Have installed python modules listed in the file requirements.txt)
    - Have installed Text-FSM for netmiko 
    - Edit the "config.py" file with Custom settings
    - Set the ENV variables necessary to run the app
      


---  
 ### HOW TO INSTALL:
 1. Install the required  packages **(We could check requirements.txt)**
    #### Here, a list of the most important modules used: 
      - **Flask** -  A framework based on Werkzeug and Jinja 2 template system, that allows web development
      - **Netmiko** – A open-source python module that simplifies SSH management to network devices 
      - **Flask_swagger_ui** - allows us to add openApi for documentation on our running APP

      **Note:** We have used Python 3.7.6. but probably the app can run on python 3.5.
    ####1.1 Manual install of Python Packages     
      - [x] pip install flask
      - [x] pip install flask-swagger-ui
      - [x] pip install netmiko
     ####1.2 We can install via pip using the requirements.txt file instead of manual installment
      - [x] pip install -r requirements.txt
      
 2. Install NTC-templates for netmiko. It uses TEXT-FSM for parsing the output of the Network devices CLI
     - [x] We dont need to install/download the ntc templates folder. The folder is already in place. We just need
        to five to the O.S. a path to the folder. 
        ```
            export NET_TEXTFSM=/path/to/ntc-templates/templates/** 
        ```
        NOTE: If for any reason, we need to install the folder (NTC-templates), please check below.
     - [x] help link on how to install:
        https://pynet.twb-tech.com/blog/automation/netmiko-textfsm.html
        
     - [ ]  Git web page for NTC-Templates: 
     https://github.com/networktocode/ntc-templates
     
    2.1. GET the NTC-Templates from git
     - [x] git clone https://github.com/networktocode/ntc-templates.git
    
     2.2. Configure a environment variable for TEXT-FSM in the  O.System
       - [x] Create ENV VARIABLE: **"NET_TEXTFSM"** and assign a value for the path to NTC TEMPLATES folder         
            ```
            # on Linux: 
                export NET_TEXTFSM=/path/to/ntc-templates/templates/ 
          
            # on Windows: (Maybe going to control panel,system, advanced settings, and add enviroment var)
                or  set NET_TEXTFSM=/path/to/ntc-templates/templates/ 
            ```
         - **TIP on windows install:** 
           If the local user don´t have administator rights, run the command listed below.
           Reboot the system after configuring the env variable.<br>
         
             ```
              rundll32 sysdm.cpl,EditEnvironmentVariables
             ```
 3. Choose between environments
    - **We could run our application in 3 different modes:**
        - [x] "production" # the default (used for production)
        
        - [ ] "development" # for debugging e development
        
        - [ ] "testing" # environment for testing (unittesting)
     
     For changing the environment we have to configure FLASK_ENV env variable:
      ```
      set FLASK_ENV=production
      ```
    
    - <b>We have 2 levels of config:</b> 
      
      - **(1)**: Is  O.System ENV variables:
        ######(the above variable  FLASK_ENV is an example)
        - email settings (e.g. MAIL_PORT=587)
        - path to the app  (e.g. FLASK_APP=NETWORKAUTOMATE.py)
        - app Environment  (e.g FLASK_ENV=production)
          -  We have 2 files, for referencing Operating System ENV  variables that can be configured:
              
              -  "put_env_vars.bat"  # for windows platform
          
              - put_env_vars.sh  # for linux platform
      
      - **(2):** Are application variables:
        - They exist in the file: "config.py"
        
        - Other application settings like log file path or log file size can be encountered in the file "config.py".<br>
        **NOTE: We want to check this file before running the app.**
    
        - The **'config.py'** file have all the settings for different environments
        
    ####On Production:
    - [x] This is the default environment for our app if "FLASK_ENV" variable is not set. (default is: FLASK_ENV=production) 
    
    - [x] When on production environment, if server mail variables are not configured, emails with application errors will be not sent
     to administrators. Check (put_env_vars.bat for details. Also keep in mind that these emails settings  are configured on OS ENV VARIABLES level, not "config.py file")
       - [x] The administrator list can be populated with custom emails. this variable is in config.py file 
    -[x] The 'config.py' file have all the settings for different environments
            <br> - We can run the scripts listed below: 
   
 4. **One Example on how to run the application:**
    
    ```
    ## For different scenario it can be 'development' or 'testing'
    ## configure the environment for the app (production) 
        set FLASK_ENV=production
    ##  set the path to our application
    ## DEFINE WHERE FLASK WILL LOOK FOR THE APP SO THAT WE CAN DO COMMANDS LIKE flask run --host 127.0.0.1 --port 80
        set FLASK_APP=NETWORKAUTOMATE.py
    ## Run the app
    ## - host and port will be where the app will receive th requests
        flask run --host 127.0.0.1 --port 80
    ```
 5. **API Documentation URL:**

    <p>We have documented our API using OpenAPI specification</p>   

    - **Swagger/OpenApi specification**:
        - For accessing to the API documentation just run the app and go to:
         http://your_server_ip_address:80/documentation<br>
         **( We can also use these tool to consume our Webservices)**
        
         **Postman API** is another useful tool **for consuming and testing our API**: https://www.getpostman.com/downloads/
        <br>
         - WE have a file called **'NEXT_APPROUCH.postman_collection.json'** stored in project folder **/postman_Collection**
        
           - It's a json file: 
             - With a collection of requests to the API.
             - Can be imported to a postman application used for testing 
             - Good point to start 
        
        - Online  OpenAPI editor: https://editor.swagger.io/ , (useful for editing yaml/json files) <br>
         Network_Automate API Documentation files are stored in the /static folder.<br>
         **Note**: We can encounter 2 files the in /static folder, One YAML and other JSON:
          -  We only need one of them. (for precaution on future needs we downloaded both YAML and JSON file) <br>
               - YAML is more human-readable than JSON.<br> 
          - In the development phase, we create the files using  the online swagger editor. <br>
            - This editor as a real time preview of the html page generated by the openAPI from the source YAML or JSON files.<br>
          - Also, there is a folder /swagger-editor-or-master; **in these folder is the swagger-editor**; good for off-line YAML edits.  
             
        </p>

 6. **Application Structure: files and folders**
       #### Files and Folders rapid guide(check each file for details):
       ##### /PythonClients
          some files with python clients (to consume our webservices) 
       #### /ntc-templates
         these folder is for TEXTFSM template system (used by netmiko for parsing output commands) . It was created automatically( it could be in different place on the computer. see how to install text_fsm)
       ##### /postman_Collection
          In These folder exists a json file called 'NEXT_APPROUCH.postman_collection.json', that we can import to Postman aplication,
          to test and consume our webservices. 
          Postman is a powerfull apllication to document and test REST APIS.
        #### /POSTMAN_Collection
          folder to store unitary tests. We develop just one for learning purposes
       #####the_app/static
         The folder contain one yaml file that documents our api using (SWAGGER/OpenAPi specification)
         The file name:  documentation20200620.yaml 
       ##### requirements.txt
         These file contains all the python packages necessary to run the APP.
       ##### NETWORKAUTOMATE.py
          A pointer to our flask application
       ##### routes.py
          the view functions
       ##### connect.py
          There is a class in these file to network device managment
          We can add more functionalities here
       ##### operations.py
          A bunch of function that provides functionalities to our application. 
          Ex. a function that request FLASK envirnment or a function that validate client data
       ##### request_data.py
          A bunch of function that provides functionalities to our application. 
       ##### manage_logs.py
          Contains a class that simplify the use of logs
       ##### config.py
          Our application consfiguration file. (Edit this file)
       ##### put_en_vars.bat
        file with env variables (for referencing in setup)   
       ##### put_en_vars.sh
        file with env variables (for referencing in setup)   
       ##### /LOGS 
        LOGS FOLDER WILL BE THE DEFAULT FOLDER FOR LOGS if not changed in config.py
       
 7. **Application Errors and corresponding HTTP Response codes**
  
     - These is the structure of our message to send to client and for logging when ERRORS:
        ``` 
        - error_dict = {"STATUS": "Failure",
                  "ERROR": {},
                  "TYPE": {},
                  "MESSAGE": {}
                  }
        ```  
    - HTTP Status codes are made of up 3 digits that fall into  5 categories.<br> Each catogory representing a certain class of code.<br> 
    The first digit is the category and the 5 categories correspond to the following class:
  
        ```  
        - 1XX - INFORMATIONAL
        - 2XX - SUCESS
        - 3XX - REDIRECTION
        - 4XX - CLIENT ERRORS
        - 5XX - SERVER ERRORS
        ```  
      =======================================================

    - These table presents Application error and corresponding HTTP RESPONSE TO CLIENT
        ``` 
        - APLICATION SERVER ERROR 1 - HTTP ERROR 400
        - APLICATION SERVER ERROR 2 - HTTP ERROR 400
        - APLICATION SERVER ERROR 3 - HTTP ERROR 400
        - APLICATION SERVER ERROR 4 - HTTP ERROR 512
        - APLICATION SERVER ERROR 5 - HTTP ERROR 513
        - APLICATION SERVER ERROR 400 - HTTP ERROR 400
        - APLICATION SERVER ERROR 500 - HTTP ERROR 500
        - APLICATION SERVER ERROR 404 - HTTP ERROR 404
       
        ########## - Check documentation for details. ################################
        ``` 

 8. **Resources used in development process**
      #####   - Useful Links:
     - MVC (model view controler):<br>
        https://www.guru99.com/mvc-tutorial.html<br>
     - REST API: <br>
     https://pt.wikipedia.org/wiki/REST <br>
     https://www.guru99.com/comparison-between-web-services.html<br>
    
      ##### - Some Python Resources
      - Flask
        - https://flask.palletsprojects.com/en/1.1.x
        - https://blog.miguelgrinberg.com/index
        - https://www.packtpub.com
        - https://udemy.com - DAVID BOMABAL - 
       - CISCO
         - https://www.cisco.com
         - https://developer.cisco.com
         - CISCO COMMANDS MODE :https://www.cisco.com/E-Learning/bulk/public/tac/cim/cib/using_cisco_ios_software/02_cisco_ios_hierarchy.htm
    
      - Netmiko 
        - https://github.com/ktbyers/netmiko
        - https://pynet.twb-tech.com/blog/automation/netmiko.html 
      
      - Various
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
     
 9. **DEPLOY ON PRODUCTION WITH A WSGI PRODUCTION SERVER:**
    ##### **Gunicorn WSGI SERVER**
    - Setup for Gunicorn, Nginx, docker, ubuntu ... 
      
      - [x] Check online miguel Grinberg great tutorial on how deploy a flask application.
           - **Examples on using docker, Heroku, Gunnicorn, or traditional way**
           - Source: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xvii-deployment-on-linux
      - [x] Tutorial on Digital Ocean
          - https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04-pt
            
    ##### **Waitress WSGI SERVER**
      - Deploy app with Waitress: 
        - Source: https://flask.palletsprojects.com/en/1.1.x/tutorial/deploy/
        - Source: https://docs.pylonsproject.org/projects/waitress/en/stable/
  
  
  
  ## A big thank you to all those who helped me in the development process:
    - Alexandre Santos - (Especialista de informática, SGSIIC – Serviço de Gestão de Sistemas e Infraestruturas de Informação e Comunicação da Universidade de Coimbra)
    - Pedro Vapi - (Chefe de divisão, SGSIIC – Serviço de Gestão de Sistemas e Infraestruturas de Informação e Comunicação da Universidade de Coimbra)
    - Anthony Herbert - programer https://prettyprinted.com/
    - Python/Networking community:
      - https://www.python.org/
      - https://realpython.com/
      - https://www.geeksforgeeks.org/
      - https://www.udemy.com/user/davidbombal/
      - https://www.youtube.com/c/HankPreston/playlists
      - https://developer.cisco.com/
      - https://www.tutorialspoint.com/python/index.htm
      - https://www.w3schools.com/python/
      - https://www.freecodecamp.org/
      - https://www.youtube.com/user/thenewboston
      - https://pythonprogramming.net/
      - https://www.thepythoncode.com/
      - https://www.youtube.com/user/schafer5
         
      
   

