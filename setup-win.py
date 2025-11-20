# setup-win.py
import winreg
import sys
import os

def setup_windows():
    """Установка ассоциаций файлов для Windows"""
    
    try:
        # Создаем ассоциацию для .stf
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, ".stf") as key:
            winreg.SetValue(key, "", winreg.REG_SZ, "STFFile")
        
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, "STFFile") as key:
            winreg.SetValue(key, "", winreg.REG_SZ, "STF Text Document")
        
        # Создаем ассоциацию для .zstf
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, ".zstf") as key:
            winreg.SetValue(key, "", winreg.REG_SZ, "ZSTFFile")
        
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, "ZSTFFile") as key:
            winreg.SetValue(key, "", winreg.REG_SZ, "ZSTF Compressed Text Document")
        
        print("✅ Ассоциации файлов для Windows установлены!")
        print("📁 .stf файлы теперь определяются как 'STF Text Document'")
        print("📁 .zstf файлы теперь определяются как 'ZSTF Compressed Text Document'")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        print("Запусти от имени администратора")

if __name__ == "__main__":
    setup_windows()
