import os
import platform
import tarfile
import zipfile
import smtplib
from email.message import EmailMessage
from datetime import datetime
from colorama import Fore, Style


def detect_os():
    return platform.system()


def get_home_directory():
    return os.path.expanduser("~")


def create_backup():
    os_type = detect_os()
    home_dir = get_home_directory()
    backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    if os_type == "Windows":
        archive_path = os.path.join(home_dir, f"{backup_name}.zip")
        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as archive:
            for foldername, _, filenames in os.walk(home_dir):
                for filename in filenames:
                    file_path = os.path.join(foldername, filename)
                    archive.write(file_path, os.path.relpath(file_path, home_dir))
    else:
        archive_path = os.path.join(home_dir, f"{backup_name}.tar.gz")
        with tarfile.open(archive_path, "w:gz") as archive:
            archive.add(home_dir, arcname=os.path.basename(home_dir))

    print(Fore.GREEN + f"Sauvegarde créée avec succès : {archive_path}" + Style.RESET_ALL)
    return archive_path


def send_email_notification(backup_path):
    sender_email = "votre_email@gmail.com"
    receiver_email = "votre_email@gmail.com"
    subject = "Notification: Sauvegarde Terminée"
    message = f"La sauvegarde a été effectuée avec succès : {backup_path}"

    msg = EmailMessage()
    msg.set_content(message)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, "votre_mot_de_passe")
            server.send_message(msg)
        print(Fore.GREEN + "Email de notification envoyé avec succès !" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"Erreur lors de l'envoi de l'email : {e}" + Style.RESET_ALL)


def main():
    print("Détection de l'OS et création de la sauvegarde...")
    backup_path = create_backup()
    send_email_notification(backup_path)


if __name__ == "__main__":
    main()
