    virtualenv venv
    # on Windows run next 
    venv\Scripts\activate
        
    pip install -r requirements.txt
    
    set FLASK_APP run.py
    set FLASK_DEBUG=1
    
    flask run
