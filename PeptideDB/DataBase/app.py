from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from django.core.wsgi import get_wsgi_application
import os
from importlib.util import find_spec
from fastapi.staticfiles import StaticFiles
from django.conf import settings
# from 
# Export Django settings env variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PeptideDB.settings')

# Get Django WSGI app
django_app = get_wsgi_application()

# Import a model
# And always import your models after you export settings
# and you get Django WSGI app
from accounts.models import Account

# Create FasatAPI instance
app = FastAPI()

# Serve Django static files
app.mount('/static',
    StaticFiles(
         directory=os.path.normpath(
              os.path.join(find_spec('django.contrib.admin').origin, '..', 'static')
         )
   ),
   name='static',
)

# Define a FastAPI route
@app.get('/fastapi-test')
def read_main():
    return {
        'total_accounts': Account.objects.count(),
        'is_debug': settings.DEBUG 
    }

# Mount Django app
app.mount('/django-test', WSGIMiddleware(django_app))