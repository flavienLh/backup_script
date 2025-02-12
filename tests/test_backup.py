import os
import sys
import pytest
from backup import detect_os, get_home_directory, get_backup_directory, create_backup

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_detect_os():
    os_type = detect_os()
    assert os_type in ["Windows", "Linux", "Darwin"]

def test_get_home_directory():
    home_dir = get_home_directory()
    assert os.path.exists(home_dir)
    assert os.path.isdir(home_dir)

def test_get_backup_directory():
    backup_dir = get_backup_directory()
    assert backup_dir is not None
    assert os.path.exists(backup_dir)
    assert os.path.isdir(backup_dir)

@pytest.fixture
def temporary_backup():
    backup_path = create_backup()
    yield backup_path
    if backup_path and os.path.exists(backup_path):
        os.remove(backup_path)

def test_create_backup(temporary_backup):
    backup_path = temporary_backup
    assert os.path.exists(backup_path)
    assert os.path.isfile(backup_path)

