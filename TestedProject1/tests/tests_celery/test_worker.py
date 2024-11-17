import subprocess

def test_worker():
    processes = subprocess.check_output(['ps', 'aux']).decode()
    assert 'celery' in processes