import math

a = 'abcdefghijklmnop'

# TODO
class NondetAlg(object):
    """Класс для шифрования с использованием недетерменированного алгоритма"""
    def __init__(self, key):
        self.key = key
    
    def f1(text):
        q = ''
        for key, i in enumerate(text):
            q += str(math.exp(key + math.cos(key) + math.sqrt(key))).replace('.', i).replace(' ', 'sdvcx').lower()

        return q

    def f2():
        pass

    def f3():
        pass

    def f4():
        pass

    def f5():
        pass

example = NondetAlg('qwerty')
enctypt = NondetAlg.f1('HI')
print(encrypt)