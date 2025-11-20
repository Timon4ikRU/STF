import struct
import os
import datetime
import zlib
import base64
import subprocess
import sys

class Zipper:
    @staticmethod
    def compress(data):
        """Сжатие данных с помощью zlib"""
        compressed = zlib.compress(data, level=9)
        return base64.b85encode(compressed).decode('ascii')
    
    @staticmethod
    def decompress(compressed_data):
        """Распаковка данных"""
        compressed_bytes = base64.b85decode(compressed_data.encode('ascii'))
        return zlib.decompress(compressed_bytes)

class STFEncoder:
    def __init__(self):
        # 8-битная кодировка - 256 возможных символов!
        self.char_to_code = {
            # Русские заглавные (0-31)
            'А': 0, 'Б': 1, 'В': 2, 'Г': 3, 'Д': 4, 'Е': 5, 'Ж': 6, 'З': 7,
            'И': 8, 'Й': 9, 'К': 10, 'Л': 11, 'М': 12, 'Н': 13, 'О': 14, 'П': 15,
            'Р': 16, 'С': 17, 'Т': 18, 'У': 19, 'Ф': 20, 'Х': 21, 'Ц': 22, 'Ч': 23,
            'Ш': 24, 'Щ': 25, 'Ъ': 26, 'Ы': 27, 'Ь': 28, 'Э': 29, 'Ю': 30, 'Я': 31,
            
            # Русские строчные (32-63)
            'а': 32, 'б': 33, 'в': 34, 'г': 35, 'д': 36, 'е': 37, 'ж': 38, 'з': 39,
            'и': 40, 'й': 41, 'к': 42, 'л': 43, 'м': 44, 'н': 45, 'о': 46, 'п': 47,
            'р': 48, 'с': 49, 'т': 50, 'у': 51, 'ф': 52, 'х': 53, 'ц': 54, 'ч': 55,
            'ш': 56, 'щ': 57, 'ъ': 58, 'ы': 59, 'ь': 60, 'э': 61, 'ю': 62, 'я': 63,
            
            # Английские заглавные (64-95)
            'A': 64, 'B': 65, 'C': 66, 'D': 67, 'E': 68, 'F': 69, 'G': 70, 'H': 71,
            'I': 72, 'J': 73, 'K': 74, 'L': 75, 'M': 76, 'N': 77, 'O': 78, 'P': 79,
            'Q': 80, 'R': 81, 'S': 82, 'T': 83, 'U': 84, 'V': 85, 'W': 86, 'X': 87,
            'Y': 88, 'Z': 89,
            
            # Английские строчные (96-127)
            'a': 96, 'b': 97, 'c': 98, 'd': 99, 'e': 100, 'f': 101, 'g': 102, 'h': 103,
            'i': 104, 'j': 105, 'k': 106, 'l': 107, 'm': 108, 'n': 109, 'o': 110, 'p': 111,
            'q': 112, 'r': 113, 's': 114, 't': 115, 'u': 116, 'v': 117, 'w': 118, 'x': 119,
            'y': 120, 'z': 121,
            
            # Цифры (128-137)
            '0': 128, '1': 129, '2': 130, '3': 131, '4': 132, '5': 133, 
            '6': 134, '7': 135, '8': 136, '9': 137,
            
            # Знаки препинания и символы (138-200)
            '!': 138, '"': 139, '#': 140, '$': 141, '%': 142, '&': 143, "'": 144,
            '(': 145, ')': 146, '*': 147, '+': 148, ',': 149, '-': 150, '.': 151,
            '/': 152, ':': 153, ';': 154, '<': 155, '=': 156, '>': 157, '?': 158,
            '@': 159, '[': 160, '\\': 161, ']': 162, '^': 163, '_': 164, '`': 165,
            '{': 166, '|': 167, '}': 168, '~': 169,
            
            # Специальные символы
            ' ': 170, '\n': 171, '\t': 172,
            
            # Дополнительные символы (можно добавить еще)
            '№': 173, '§': 174, '©': 175, '®': 176, '°': 177, '±': 178, '²': 179,
            '³': 180, '´': 181, 'µ': 182, '¶': 183, '·': 184, '¸': 185, '¹': 186,
            'º': 187, '»': 188, '¼': 189, '½': 190, '¾': 191, '¿': 192,
            
            # Кириллические дополнительные
            'Ё': 193, 'ё': 194,
            
            # Остальные коды (195-255) - резерв
        }
        
        self.code_to_char = {v: k for k, v in self.char_to_code.items()}
        
        self.signature = bytes([0x7D, 0x6C, 0x51, 0x99, 0xAF, 0xD9])
        self.zstf_signature = bytes([0x7D, 0x6C, 0x51, 0x99, 0xAF, 0xDA])

    def _get_current_datetime(self):
        now = datetime.datetime.now()
        return (now.day, now.month, now.year % 100, now.hour, now.minute)

    def encode_text(self, text, compressed=False):
        encoded_bytes = bytearray()
        
        if compressed:
            encoded_bytes.extend(self.zstf_signature)
        else:
            encoded_bytes.extend(self.signature)
        
        day, month, year, hour, minute = self._get_current_datetime()
        encoded_bytes.extend(struct.pack('BBBBB', day, month, year, hour, minute))
        
        flags = 0x01 if compressed else 0x00
        encoded_bytes.append(flags)
        encoded_bytes.extend(struct.pack('I', len(text)))
        
        for char in text:
            if char in self.char_to_code:
                encoded_bytes.append(self.char_to_code[char])
            else:
                print(f"Предупреждение: символ '{char}' (код {ord(char)}) не найден, заменен на '?'")
                encoded_bytes.append(158)  # '?'
        
        return bytes(encoded_bytes)

    def decode_text(self, binary_data):
        if binary_data.startswith(self.signature):
            compressed = False
            data = binary_data[6:]
        elif binary_data.startswith(self.zstf_signature):
            compressed = True
            data = binary_data[6:]
        else:
            raise ValueError("Неверный формат STF файла")
        
        day, month, year, hour, minute = struct.unpack('BBBBB', data[:5])
        data = data[5:]
        flags = data[0]
        data = data[1:]
        is_compressed = (flags & 0x01) != 0
        
        if is_compressed:
            compressed_text = data.decode('ascii')
            data = Zipper.decompress(compressed_text)
            data = data[16:]
            text_length = len(data)
        else:
            text_length = struct.unpack('I', data[:4])[0]
            data = data[4:]
        
        decoded_text = []
        for i, byte_val in enumerate(data):
            if i >= text_length and not is_compressed:
                break
            if byte_val in self.code_to_char:
                decoded_text.append(self.code_to_char[byte_val])
            else:
                decoded_text.append('?')
        
        creation_time = f"{day:02d}.{month:02d}.20{year:02d} {hour:02d}:{minute:02d}"
        return ''.join(decoded_text), creation_time, is_compressed

class STFFile:
    def __init__(self):
        self.encoder = STFEncoder()
    
    def save(self, filename, text, compressed=False):
        if compressed:
            encoded_normal = self.encoder.encode_text(text, compressed=False)
            compressed_data = Zipper.compress(encoded_normal)
            
            encoded_bytes = bytearray()
            encoded_bytes.extend(self.encoder.zstf_signature)
            day, month, year, hour, minute = self.encoder._get_current_datetime()
            encoded_bytes.extend(struct.pack('BBBBB', day, month, year, hour, minute))
            encoded_bytes.append(0x01)
            encoded_bytes.extend(compressed_data.encode('ascii'))
        else:
            encoded_bytes = self.encoder.encode_text(text, compressed=False)
        
        with open(filename, 'wb') as f:
            f.write(encoded_bytes)
        
        mode = "ZSTF" if compressed else "STF"
        print(f"Файл {filename} сохранен в формате {mode}! Размер: {len(encoded_bytes)} байт")
    
    def load(self, filename):
        with open(filename, 'rb') as f:
            encoded_data = f.read()
        
        return self.encoder.decode_text(encoded_data)

# Тестирование
def test_encoding():
    encoder = STFEncoder()
    test_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ абвгдежзийклмнопрстуфхцчшщъыьэюя 0123456789 !@#$%^&*()"
    
    print("=== ТЕСТ 8-БИТНОЙ КОДИРОВКИ ===")
    for char in test_chars:
        if char in encoder.char_to_code:
            code = encoder.char_to_code[char]
            decoded = encoder.code_to_char.get(code, '?')
            status = "✓" if decoded == char else "✗"
            print(f"{status} '{char}' -> {code:03d} -> '{decoded}'")
        else:
            print(f"✗ '{char}' не найден в кодировке")

if __name__ == "__main__":
    test_encoding()
    
    print("\n=== СОЗДАНИЕ ФАЙЛОВ ===")
    stf = STFFile()
    
    text = "ПРИВЕТ МИР! Hello World 123 Привет мир! hello world"
    stf.save("test_8bit.stf", text, compressed=False)
    stf.save("test_8bit.zstf", text, compressed=True)
    
    print("\n--- STF файл ---")
    loaded_text, time, compressed = stf.load("test_8bit.stf")
    print(f"Текст: {loaded_text}")
    print(f"Создан: {time}, Сжатие: {compressed}")
    
    print("\n--- ZSTF файл ---")
    loaded_text, time, compressed = stf.load("test_8bit.zstf")
    print(f"Текст: {loaded_text}")
    print(f"Создан: {time}, Сжатие: {compressed}")
