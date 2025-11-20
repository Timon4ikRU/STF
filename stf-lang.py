#!/usr/bin/env python3
# stf-lang.py
import argparse
import sys
import os
from stf_encoder import STFFile

def main():
    parser = argparse.ArgumentParser(
        description='STF Language Tool - Работа с STF/ZSTF файлами',
        prog='stf-lang'
    )
    
    # Основные аргументы
    parser.add_argument('input', help='Входной файл')
    
    # Режимы работы
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-s', '--stf', action='store_true', 
                      help='Конвертировать в STF формат')
    group.add_argument('-z', '--zstf', action='store_true',
                      help='Конвертировать в ZSTF формат (сжатый)')
    group.add_argument('-d', '--decode', action='store_true',
                      help='Декодировать STF/ZSTF файл')
    group.add_argument('-i', '--info', action='store_true',
                      help='Информация о STF/ZSTF файле')
    
    args = parser.parse_args()
    
    stf = STFFile()
    
    try:
        # Режим информации
        if args.info:
            if not args.input.endswith(('.stf', '.zstf')):
                print("Ошибка: для --info укажите .stf или .zstf файл")
                return 1
            
            text, creation_time, compressed = stf.load(args.input)
            
            print(f"=== STF File Info ===")
            print(f"File: {os.path.basename(args.input)}")
            print(f"Created: {creation_time}")
            print(f"Format: {'ZSTF (compressed)' if compressed else 'STF'}")
            print(f"Size: {os.path.getsize(args.input)} bytes")
            print(f"Characters: {len(text)}")
            print(f"Compression ratio: {os.path.getsize(args.input)/len(text):.2f} bytes/char")
            return 0
        
        # Режим декодирования
        if args.decode:
            if not args.input.endswith(('.stf', '.zstf')):
                print("Ошибка: для --decode укажите .stf или .zstf файл")
                return 1
            
            text, creation_time, compressed = stf.load(args.input)
            
            # Автоматически определяем выходной файл
            output_file = os.path.splitext(args.input)[0] + '.txt'
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(text)
            
            print(f"Декодировано: {args.input} -> {output_file}")
            print(f"Символов: {len(text)}")
            return 0
        
        # Режимы кодирования (STF/ZSTF)
        if not args.input.endswith('.txt'):
            print("Ошибка: для кодирования укажите .txt файл")
            return 1
        
        # Читаем входной файл
        with open(args.input, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # Автоматически определяем выходной файл
        base_name = os.path.splitext(args.input)[0]
        
        # STF кодирование
        if args.stf:
            output_file = base_name + '.stf'
            stf.save(output_file, text, compressed=False)
            print(f"Закодировано: {args.input} -> {output_file}")
            print(f"Размер: {os.path.getsize(output_file)} байт")
        
        # ZSTF кодирование
        elif args.zstf:
            output_file = base_name + '.zstf'
            stf.save(output_file, text, compressed=True)
            print(f"Закодировано: {args.input} -> {output_file}")
            print(f"Размер: {os.path.getsize(output_file)} байт")
        
        return 0
        
    except FileNotFoundError:
        print(f"Ошибка: файл '{args.input}' не найден")
        return 1
    except Exception as e:
        print(f"Ошибка: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
