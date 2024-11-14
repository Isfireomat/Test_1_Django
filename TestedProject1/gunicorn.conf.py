import os
bind = "0.0.0.0:8000"
workers = os.cpu_count()
timeout = 30
loglevel = "info"
preload_app = True