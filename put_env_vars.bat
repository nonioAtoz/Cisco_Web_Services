REM path to ntc templates - see netmiko TEXTFM
REM set NET_TEXTFSM=C:\Users\nuno\PycharmProjects\NETWORKAUTOMATE_FINAL\ntc-templates\templates\

REM set the env type for our application: could be one or another
REM set FLASK_ENV=development
set set FLASK_ENV=production

REM DEFINE WHERE FLASK WILL LOOK FOR THE APP SO THAT WE CAN DO COMMANDS LIKE flask run --host 127.0.0.1 --port 80
set FLASK_APP=NETWORKAUTOMATE.py

REM Configure mail So that flask could send emails on production environment, when errors occur.
REM EXAMPLE FOR THIS GOOGLE EMAIL ACCOUNT: nm.10000.testes@gmail.com
set MAIL_SERVER=smtp.googlemail.com
set MAIL_PORT=587
set MAIL_USE_TLS=1
set MAIL_USERNAME=your_username_here
set MAIL_PASSWORD=yout_password_here
REM flask run --host 127.0.0.1 --port 80