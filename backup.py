import os
import platform
import tarfile
import zipfile
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from datetime import datetime
from colorama import Fore, Style

load_dotenv()

def detect_os():
    return platform.system()


def get_home_directory():
    return os.path.expanduser("~")


def get_backup_directory():
    os_type = detect_os()
    home_dir = get_home_directory()

    if os_type == "Windows":
        backup_dir = os.path.join(home_dir, "Documents")
    else:  # Linux et MacOS
        backup_dir = os.path.join(home_dir, "backup")

    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir, exist_ok=True)

    return backup_dir


def create_backup():
    os_type = detect_os()
    backup_dir = get_backup_directory()

    if not backup_dir or not os.path.exists(backup_dir):
        print(Fore.RED + f"❌ Erreur : Le dossier {backup_dir} n'existe pas." + Style.RESET_ALL)
        return None

    backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    home_dir = get_home_directory()

    ignored_files = [f"backup_{datetime.now().strftime('%Y%m%d')}"]

    if os_type == "Windows":
        archive_path = os.path.join(home_dir, f"{backup_name}.zip")
        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as archive:
            for foldername, _, filenames in os.walk(backup_dir):
                for filename in filenames:
                    file_path = os.path.join(foldername, filename)

                    if filename.startswith('.') or any(ignored in file_path for ignored in ignored_files):
                        print(f"⏩ Fichier ignoré : {file_path}")
                        continue

                    try:
                        print(f"📂 Ajout de {file_path} à l'archive...")
                        archive.write(file_path, os.path.relpath(file_path, home_dir))
                    except PermissionError:
                        print(f"⚠️ Permission refusée : {file_path}")

    else:
        archive_path = os.path.join(home_dir, f"{backup_name}.tar.gz")
        with tarfile.open(archive_path, "w:gz") as archive:
            try:
                archive.add(backup_dir, arcname=os.path.basename(backup_dir))
            except PermissionError:
                print(f"⚠️ Permission refusée : {backup_dir}")

    print(Fore.GREEN + f"✅ Sauvegarde créée avec succès : {archive_path}" + Style.RESET_ALL)
    return archive_path


def send_email_notification(backup_path):
    sender_email = os.getenv("EMAIL_SENDER")
    receiver_email = os.getenv("EMAIL_RECEIVER")
    email_password = os.getenv("EMAIL_PASSWORD")

    subject = "Notification: Sauvegarde Terminée"
    message = f"La sauvegarde du dossier sélectionné a été effectuée avec succès : {backup_path}"

    msg = EmailMessage()
    msg.set_content(message)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, email_password)
            server.send_message(msg)
        print(Fore.GREEN + "📧 Email de notification envoyé avec succès !" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"❌ Erreur lors de l'envoi de l'email : {e}" + Style.RESET_ALL)


def main():
    print("📂 Détection de l'OS et création de la sauvegarde...")
    backup_path = create_backup()
    if backup_path:
        send_email_notification(backup_path)


if __name__ == "__main__":
    main()
