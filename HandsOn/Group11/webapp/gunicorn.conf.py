# Config file
wsgi_app = 'museum_api.api.app:app'

# Server socket
bind = ['0.0.0.0:8080']

# Worker Options
workers = 4
worker_class = 'uvicorn.workers.UvicornWorker'

# Logging
loglevel = 'info'
