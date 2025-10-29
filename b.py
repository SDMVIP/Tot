import os
import zipfile
import requests

# إعدادات تليجرام
bot_token = "7341619247:AAEM4oHze0sEZOmSBEVTi_tgvIwWKjJS9qM"
chat_id = "7677247170"

# اسم ملف النسخة
backup_name = f"backup_{__import__('datetime').datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.zip"

# 1️⃣ ضغط الملفات
def zip_all_files(zip_filename):
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as backup_zip:
        for root, dirs, files in os.walk('.'):
            for file in files:
                if file != zip_filename:  # لا تضيف ملف الباك اب نفسه
                    file_path = os.path.join(root, file)
                    backup_zip.write(file_path, os.path.relpath(file_path, '.'))

zip_all_files(backup_name)
print(f"✅ تم إنشاء النسخة: {backup_name}")

# 2️⃣ إرسال النسخة لتليجرام
with open(backup_name, 'rb') as file_data:
    response = requests.post(
        f"https://api.telegram.org/bot{bot_token}/sendDocument",
        data={'chat_id': chat_id, 'caption': f"📦 نسخة احتياطية: {backup_name}"},
        files={'document': file_data}
    )

if response.status_code == 200:
    print("✅ تم إرسال النسخة إلى تيليجرام")
    os.remove(backup_name)
    print("🗑️ تم حذف النسخة من السيرفر")
else:
    print(f"❌ فشل الإرسال: {response.status_code}\n{response.text}")
