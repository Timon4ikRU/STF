# test_compression.py
import os
from stf_encoder import STFFile

def test_compression():
    stf = STFFile()
    
    # Создаем большой текст для теста сжатия
    big_text = """
    Это большой текст для тестирования сжатия в формате ZSTF.
    Мы напишем здесь много повторяющихся слов и фраз чтобы 
    алгоритм сжатия мог показать свою эффективность.
    
    Повторение повторение повторение повторение повторение.
    Очень много повторяющихся слов слов слов слов слов.
    Текст текст текст текст текст текст текст текст.
    Сжатие сжатие сжатие сжатие сжатие сжатие сжатие.
    
    """ * 10  # Умножаем текст в 10 раз
    
    print(f"Исходный текст: {len(big_text)} символов")
    
    # Сохраняем в обоих форматах
    stf.save("big_test.stf", big_text, compressed=False)
    stf.save("big_test.zstf", big_text, compressed=True)
    
    # Сравниваем размеры
    stf_size = os.path.getsize("big_test.stf")
    zstf_size = os.path.getsize("big_test.zstf")
    
    print(f"\n--- РЕЗУЛЬТАТЫ СЖАТИЯ ---")
    print(f"STF размер: {stf_size} байт")
    print(f"ZSTF размер: {zstf_size} байт")
    print(f"Экономия: {stf_size - zstf_size} байт")
    print(f"Коэффициент сжатия: {zstf_size/stf_size:.2%}")

if __name__ == "__main__":
    test_compression()
