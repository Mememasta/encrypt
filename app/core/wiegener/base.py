import re

from itertools import cycle


alp = 'abcdefghijklmnopqrstuvwxyz'


class Wiegener(object):
    """Класс для шифрования с использованием ключа"""
    def __init__(self, key):
        assert bool(re.search('[a-zA-Z]', key)), "Введите ключ латинскими символами"
        self.__key = key.lower()


    def encode_wiegener(self, message):
        """Шифрует сообщение ключевым объектом
        
        :param message: {string} Сообщение, которое нужно зашифровать
        :return: {string} Зашифрованное сообщение
        """
        assert bool(re.search('[a-zA-Z]', message)), "Введите сообщение латинскими символами"
        message = message.lower()
        f = lambda arg: alp[(alp.index(arg[0])+alp.index(arg[1])%26)%26]
        return ''.join(map(f, zip(message, cycle(self.__key))))


    def decode_wiegener(self, encrypted_message):
        """Расшифровывает сообщение ключевым объектом
        
        :param encrypted_message: {string} Сообщение, которое нужно расшифровать
        :return: {string} Расшифрованное сообщение
        """
        f = lambda arg: alp[alp.index(arg[0])-alp.index(arg[1])%26]
        return ''.join(map(f, zip(encrypted_message, cycle(self.__key))))