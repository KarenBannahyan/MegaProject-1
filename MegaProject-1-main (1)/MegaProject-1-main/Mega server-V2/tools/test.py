from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os
from base64 import b64encode, b64decode

# Функция для генерации случайного ключа и инициализирующего вектора (IV)
def generate_key_and_iv():
    key = os.urandom(32)  # 32 байта для AES-256
    iv = os.urandom(16)   # 16 байт для AES в режиме CBC
    return key, iv

# Функция для шифрования данных
def encrypt_file(file_path, key, iv):
    # Открытие исходного файла
    with open(file_path, 'rb') as file:
        data = file.read()

    # Паддинг данных для соответствия блокам AES
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()

    # Шифрование данных
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    # Сохранение зашифрованных данных в новый файл
    with open('passwords_encrypted.txt', 'wb') as enc_file:
        enc_file.write(b64encode(encrypted_data))  # Сохраняем зашифрованные данные в base64

    # Сохраняем ключ и IV (для расшифровки)
    with open('key_and_iv.txt', 'wb') as key_file:
        key_file.write(b64encode(key))  # Ключ
        key_file.write(b'\n')  # Разделитель между ключом и IV
        key_file.write(b64encode(iv))  # IV

    print("Файл успешно зашифрован и сохранен!")

# Функция для расшифровки данных
def decrypt_file(encrypted_file_path, key, iv):
    # Открытие зашифрованного файла
    with open(encrypted_file_path, 'rb') as enc_file:
        encrypted_data = b64decode(enc_file.read())

    # Расшифровка данных
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

    # Удаление паддинга
    unpadder = padding.PKCS7(128).unpadder()
    unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()

    # Сохранение расшифрованных данных в новый файл
    with open('passwords_decrypted.txt', 'wb') as dec_file:
        dec_file.write(unpadded_data)

    print("Файл успешно расшифрован и сохранен!")

# Основная функция
def main():
    key = 'j3qmGB5whzBhuCWAzCNH/PW8j9SxK2BdoLJF29TijA4='
    iv = 'cjAOwQReDuc0v+Ce9KStJw=='
    # Генерация ключа и IV
    # key, iv = generate_key_and_iv()
    #
    # # Шифрование файла
    # encrypt_file('passwords.txt', key, iv)
    #
    # # Для расшифровки, предполагаем, что у нас есть правильный ключ и IV:
    # with open('key_and_iv.txt', 'rb') as key_file:
    #     key_data = key_file.read().split(b'\n')
    #     key = b64decode(key_data[0])
    #     iv = b64decode(key_data[1])

    # Расшифровка файла
    decrypt_file('passwords_encrypted.txt', key, iv)

if __name__ == '__main__':
    main()
