import struct

from .compatibility import number_type, iter_range
from .core import derive_keys, encode_block


class DesKey(object):
    """Класс для шифрования с использованием ключа"""
    def __init__(self, key):
        self.__encryption_key = guard_key(key)
        self.__decryption_key = self.__encryption_key[::-1]
        self.__key = key

    def encrypt(self, message, initial=None, padding=False):
        """Шифрует сообщение ключевым объектом

        :param message: {bytes} Сообщение, которое нужно зашифровать
        :param initial: {union[bytes, int, long, NoneType]} По умолчанию режим шифрования ECB, можно переключить на CBC передав байтовый объект длины 8 или целое число с прямым порядком байтов
        :param padding: {any} Параметр, который дополнит сообщения до длины кратной 8, при расшифровании откинет лишнии символы
        :return: {bytes} Зашифрованное сообщение
        """
        return handle(message, self.__encryption_key, initial, padding, 1)

    def decrypt(self, message, initial=None, padding=False):
        """Расшифровывает сообщение с помощью ключевого объекта

        :param message: {bytes} Сообщение, которое нужно расшифровать
        :param initial: {union[bytes, int, long, NoneType]} По умолчанию режим шифрования ECB, можно переключить на CBC передав байтовый объект длины 8 или целое число с прямым порядком байтов
        :param padding: {bool} Параметр, который дополнит сообщения до длины кратной 8, при расшифровании откинет лишнии символы
        :return: {bytes} Расшифрованное сообщение
        """
        return handle(message, self.__decryption_key, initial, padding, 0)

    def is_single(self):
        """:return: {bool} Истина, если используется алгоритм DES
        """
        return len(self.__encryption_key) == 1

    def is_triple(self):
        """:return: {bool} Истина, если используется алгоритм 3DES
        """
        return len(self.__encryption_key) == 3

    def __hash__(self):
        return hash((self.__class__, self.__encryption_key))


def encode(block, key, encryption):
    for k in key:
        block = encode_block(block, k, encryption)
        encryption = not encryption

    return block


def guard_key(key):
    if isinstance(key, bytearray):
        key = bytes(key)

    assert isinstance(key, bytes), "Ключ должен быть байтами или массивом байтов"
    assert len(key) in (8, 16, 24), "Длина ключа должны быть 8, 16, или 24"

    k0, k1, k2 = key[:8], key[8:16], key[16:]
    if k1 == k2:
        return tuple(derive_keys(k0)),

    k2 = k2 or k0
    if k1 == k0:
        return tuple(derive_keys(k2)),

    return tuple(tuple(derive_keys(k)) for k in (k0, k1, k2))


def guard_message(message, padding, encryption):
    if isinstance(message, bytearray):
        message = bytes(message)
    assert isinstance(message, bytes), "Сообщение должно быть байтами"
    length = len(message)
    if encryption and padding:
        return message.ljust(length + 8 >> 3 << 3, bytes((8 - (length & 7), )))

    assert length & 7 == 0, (
        "Длина сообщения должна быть кратной 8"
        "(или установите для параметра padding значение True в режиме шифрования)"
    )
    return message


def guard_initial(initial):
    if initial is not None:
        if isinstance(initial, bytearray):
            initial = bytes(initial)
        if isinstance(initial, bytes):
            assert len(initial) & 7 == 0, "Начальное значение должно быть длины 8 (в байтах или массиве байтов)"
            return struct.unpack(">Q", initial)[0]
        assert isinstance(initial, number_type), "Начальное значение должно быть целым или байтовым объектом"
        assert -1 < initial < 1 << 32, "Начальное значение должно быть целым числом от 0 включительно до 2 ** 32"
    return initial


def handle(message, key, initial, padding, encryption):
    message = guard_message(message, padding, encryption)
    initial = guard_initial(initial)

    blocks = (struct.unpack(">Q", message[i: i + 8])[0] for i in iter_range(0, len(message), 8))

    if initial is None:
        # ECB
        encoded_blocks = ecb(blocks, key, encryption)
    else:
        # CBC
        encoded_blocks = cbc(blocks, key, initial, encryption)

    ret = b"".join(struct.pack(">Q", block) for block in encoded_blocks)
    return ret[:-ord(ret[-1:])] if not encryption and padding else ret


def ecb(blocks, key, encryption):
    for block in blocks:
        yield encode(block, key, encryption)


def cbc(blocks, key, initial, encryption):
    if encryption:
        for block in blocks:
            initial = encode(block ^ initial, key, encryption)
            yield initial
    else:
        for block in blocks:
            initial, block = block, initial ^ encode(block, key, encryption)
            yield block
