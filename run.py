from waitress import serve
from budgetApp.wsgi import application

serve(application, host='127.0.0.1', port='8080')
