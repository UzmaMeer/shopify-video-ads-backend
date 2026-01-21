import sys
from tasks import celery_app

# This allows you to run "python worker.py" directly!
if __name__ == '__main__':
    print("👷 Starting Windows Celery Worker...")
    
    argv = [
        'worker',
        '--pool=solo',
        '--loglevel=info'
    ]
    
    celery_app.worker_main(argv)