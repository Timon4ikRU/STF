#!/usr/bin/env python3
# setup-linux.py
import os
import subprocess
import sys

def setup_linux():
    """Установка MIME type для STF файлов в Linux"""
    
    # Создаем MIME type
    mime_content = """<?xml version="1.0" encoding="UTF-8"?>
<mime-info xmlns="http://www.freedesktop.org/standards/shared-mime-info">
    <mime-type type="application/x-stf">
        <comment>STF text file</comment>
        <magic>
            <match type="string" value="\\x7D\\x6C\\x51\\x99\\xAF\\xDA" offset="0"/>
            <match type="string" value="\\x7D\\x6C\\x51\\x99\\xAF\\xD9" offset="0"/>
        </magic>
        <glob pattern="*.stf"/>
        <glob pattern="*.zstf"/>
        <sub-class-of type="text/plain"/>
    </mime-type>
</mime-info>"""
    
    try:
        # Создаем директорию MIME
        mime_dir = os.path.expanduser("~/.local/share/mime/packages")
        os.makedirs(mime_dir, exist_ok=True)
        
        # Сохраняем MIME type
        mime_path = os.path.join(mime_dir, "application-x-stf.xml")
        with open(mime_path, 'w') as f:
            f.write(mime_content)
        
        # Обновляем MIME базу
        subprocess.run(["update-mime-database", os.path.expanduser("~/.local/share/mime")])
        
        print("✅ MIME type для STF файлов установлен!")
        print("📁 .stf и .zstf файлы теперь определяются как 'STF text file'")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        print("Запусти с sudo для системной установки")

if __name__ == "__main__":
    setup_linux()
