from fabric.contrib.project import rsync_project
from fabric.api import env, run
from fabric.operations import sudo

PROJECT_EXCLUDES=['*.pyc', '*~', '.*~', '*.db', '*.swp', '*.tmp', '.project',
                  'celeryd.pid', 'backups/***', '_generated_media/***',
                  'media/***', 'locale/***', 'settings_local.py',
                  '.env/***', '.coverage', 'coverage.xml']

env.hosts = ['ubuntu@204.13.50.11']

def deploy_workers():
    rsync_project("/home/ubuntu/app/", local_dir='.', exclude=PROJECT_EXCLUDES, delete=True)
    sudo('supervisorctl restart celery')