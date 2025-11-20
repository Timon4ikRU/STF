# stf_opener.py
import sys
import os
from stf_encoder import STFFile

def main():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        if filename.endswith(('.stf', '.zstf')):
            stf = STFFile()
            try:
                text, creation_time, compressed = stf.load(filename)
                print(f"=== STF Viewer ===")
                print(f"Файл: {os.path.basename(filename)}")
                print(f"Создан: {creation_time}")
                print(f"Формат: {'ZSTF (сжатый)' if compressed else 'STF'}")
                print(f"Размер: {os.path.getsize(filename)} байт")
                print(f"\nСодержимое:")
                print("-" * 50)
                print(text)
                print("-" * 50)
                
                # Сохраняем как TXT для удобства
                txt_filename = os.path.splitext(filename)[0] + '.txt'
                with open(txt_filename, 'w', encoding='utf-8') as f:
                    f.write(text)
                print(f"\nТекст также сохранен в: {txt_filename}")
                
            except Exception as e:
                print(f"Ошибка открытия файла: {e}")
        
        # ЖДЕМ НАЖАТИЯ КЛАВИШИ В ЛЮБОМ СЛУЧАЕ
        input("\nНажмите Enter для выхода...")
        
    else:
        print("Перетащите STF файл на этот исполняемый файл или укажите путь к файлу.")
        input("Нажмите Enter для выхода...")

if __name__ == "__main__":
    main()
