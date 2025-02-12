import pytest
import os
from backup import detect_os, get_home_directory, create_backup

def test_detect_os():
    os_type = detect_os()
    assert os_type in ["Windows", "Linux", "Darwin"]

def test_get_home_directory():
    home_dir = get_home_directory()
    assert os.path.exists(home_dir)

def test_create_backup():
    backup_path = create_backup()
    assert os.path.exists(backup_path)
    os.remove(backup_path)
