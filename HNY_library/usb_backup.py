import os
import shutil
import time
from datetime import datetime
import schedule

# --- CONFIG ---
FILE_TO_SAVE = "data/student_books_in_out.csv"
USB_MOUNT = "/media/pt"
USB_NAME = "USB321FD"  # replace with your USB drive’s label
BACKUP_FOLDER = "library_backups"  # folder name on the USB to store backups
BACKUP_TIMES = ["09:00", "13:00", "17:00"]

# --- BACKUP FUNCTION ---
def backup_csv_to_usb():
    usb_path = os.path.join(USB_MOUNT, USB_NAME)
    if not os.path.exists(usb_path):
        print(f"[{datetime.now()}] USB not found at {usb_path}")
        return

    dest_dir = os.path.join(usb_path, BACKUP_FOLDER)
    os.makedirs(dest_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    dest_file = os.path.join(dest_dir, f"student_books_in_out_{timestamp}.csv")

    try:
        shutil.copy2(FILE_TO_SAVE, dest_file)
        print(f"[{datetime.now()}] Backup saved to {dest_file}")
    except Exception as e:
        print(f"[{datetime.now()}] Backup failed: {e}")

# --- SCHEDULE JOBS ---
def run_backups():
    for t in BACKUP_TIMES:
        schedule.every().day.at(t).do(backup_csv_to_usb)

    # --- RUN SCHEDULER ---
    while True:
        schedule.run_pending()
        time.sleep(60)
