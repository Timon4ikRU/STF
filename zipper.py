# zipper.py
import zlib
import base64

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
