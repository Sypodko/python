import hashlib

class MyDict:
    def __init__(self):
        self.__data = []
        self.__sootvetstvie = {}

    def __repr__(self):
        return str(self.__sootvetstvie)

    def my_hash_function(self, key):
        key_str = str(key)
        sha = hashlib.sha384()
        sha.update(key_str.encode('utf-8'))
        return sha.hexdigest()

    def __getitem__(self, key):
        hash_value = self.my_hash_function(key)
        if hash_value in self.__sootvetstvie:
            index = self.__sootvetstvie[hash_value]
            return self.__data[index]
        raise KeyError(f"Key {key} not found")

    def __setitem__(self, key, value):
        hash_value = self.my_hash_function(key)
        if hash_value in self.__sootvetstvie:
            index = self.__sootvetstvie[hash_value]
            self.__data[index] = value
        else:
            self.__sootvetstvie[hash_value] = len(self.__data)
            self.__data.append(value)

    def __delitem__(self, key):
        hash_value = self.my_hash_function(key)
        if hash_value in self.__sootvetstvie:
            index = self.__sootvetstvie.pop(hash_value)
            self.__data.pop(index)
            for i in range(index, len(self.__data)):
                key = self.__data[i]
                self.__sootvetstvie[self.my_hash_function(key)] = i
        else:
            raise KeyError(f"Key {key} not found")

    def __contains__(self, key):
        hash_value = self.my_hash_function(key)
        return hash_value in self.__sootvetstvie

    def clear(self):
        self.__data.clear()
        self.__sootvetstvie.clear()

    def copy(self):
        new_dict = MyDict()
        new_dict.__data = self.__data.copy()
        new_dict.__sootvetstvie = self.__sootvetstvie.copy()
        return new_dict

    @classmethod
    def fromkeys(cls, seq, value=None):
        new_dict = cls()
        for key in seq:
            new_dict[key] = value
        return new_dict

    def get(self, key, default=None):
        hash_value = self.my_hash_function(key)
        if hash_value in self.__sootvetstvie:
            index = self.__sootvetstvie[hash_value]
            return self.__data[index]
        return default

    def items(self):
        return list(zip(self.__sootvetstvie.keys(), self.__data))

    def keys(self):
        return list(self.__sootvetstvie.keys())

    def pop(self, key, default=None):
        hash_value = self.my_hash_function(key)
        if hash_value in self.__sootvetstvie:
            index = self.__sootvetstvie.pop(hash_value)
            value = self.__data.pop(index)
            for i in range(index, len(self.__data)):
                key = self.__data[i]
                self.__sootvetstvie[self.my_hash_function(key)] = i
            return value
        if default is not None:
            return default
        raise KeyError(f"Key {key} not found")

    def popitem(self):
        if not self.__sootvetstvie:
            raise KeyError("popitem(): dictionary is empty")
        key, index = self.__sootvetstvie.popitem()
        value = self.__data.pop(index)
        for i in range(len(self.__data)):
            self.__sootvetstvie[self.my_hash_function(self.__data[i])] = i
        return key, value

    def setdefault(self, key, default=None):
        if key not in self:
            self[key] = default
        return self[key]

    def update(self, other):
        if isinstance(other, dict):
            for key, value in other.items():
                self[key] = value
        elif hasattr(other, 'items'):
            for key, value in other.items():
                self[key] = value

    def values(self):
        return self.__data

# Создание экземпляра
my_dict = MyDict()

# __setitem__ и __getitem__
my_dict["apple"] = 10
my_dict["banana"] = 20
print(my_dict["apple"])    # 10
print(my_dict["banana"])   # 20

# __contains__
print("apple" in my_dict)     # True
print("cherry" in my_dict)    # False

# get
print(my_dict.get("apple"))         # 10
print(my_dict.get("cherry"))        # None
print(my_dict.get("cherry", 0))     # 0

# setdefault
print(my_dict.setdefault("banana", 50))  # 20 (не меняется, уже есть)
print(my_dict.setdefault("cherry", 50))  # 50 (создана новая)
print(my_dict["cherry"])                 # 50

# pop
print(my_dict.pop("banana"))       # 20
print(my_dict.pop("banana", 999))  # 999 (уже удалён)

# popitem
my_dict["x"] = 1
my_dict["y"] = 2
k, v = my_dict.popitem()
print(f"Popped: {k} -> {v}")       # Что-то из словаря

# keys
print("Keys:", my_dict.keys())     # Список всех хэшей (ключей)

# values
print("Values:", my_dict.values())  # Список всех значений

# items
print("Items:", my_dict.items())    # Список пар (хэш, значение)

# clear
my_dict.clear()
print("After clear:", my_dict.items())  # []

# fromkeys
md2 = MyDict.fromkeys(["one", "two", "three"], 42)
print("fromkeys:", md2.items())   # Все значения — 42

# copy
md3 = md2.copy()
print("copy:", md3.items())       # Должны быть те же, что и в md2

# update
md3.update({"one": 100, "four": 400})
print("after update:", md3.items())  # "one" обновился, "four" добавлен

# Проверка совместимости с dict.items()
d = {"a": 1, "b": 2}
my_dict.update(d)
print("Merged dict:", my_dict.items())
