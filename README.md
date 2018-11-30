# Check Yo' Text
UPDATED: 11/21/18
App security class project. A Flask Python spell-checking application that reviews text files.

Features:
    Highlights text that produces spell-checking errors.
    Provides suggestions for spell-errors. (in progress)
    Can log in and save your text files.

Security Features:
    Secure connection via HTTPS
    Protected against CSRF and XSS
    Non-permanent sessions that logout when browser is closed
    Checks appropriate extensions
    Error logging, user interaction logging (click and scroll)

How to Use:

    WINDOWS: (***NOTE: Very janky. Preferably use Linux instead.***)
        pip install pyopenssl pynput flask requests pymysql flask_login
        python init.py
    
    LINUX:
        virtualenv venv
        . venv/bin/activate
        pip install pyopenssl pynput flask requests pymysql flask_login 
        python init.py  
        deactivate
