import os
import sys
import pytest

# ✅ Vérifie si le script tourne dans GitHub Actions
print("🔍 Debug: Current working directory:", os.getcwd())
print("🔍 Debug: Files in current directory:", os.listdir(os.getcwd()))

# ✅ Ajoute le dossier parent pour que `backup.py` soit accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backup import detect_os, get_home_directory, get_backup_directory, create_backup

def test_detect_os():
    os_type = detect_os()
    assert os_type in ["Windows", "Linux", "Darwin"]

def test_get_home_directory():
    home_dir = get_home_directory()
    assert os.path.exists(home_dir)
    assert os.path.isdir(home_dir)

def test_get_backup_directory():
    backup_dir = get_backup_directory()

    print(f"📂 Répertoire de sauvegarde sélectionné : {backup_dir}")
    assert backup_dir is not None
    assert os.path.exists(backup_dir), f"Le dossier {backup_dir} n'existe pas !"
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
