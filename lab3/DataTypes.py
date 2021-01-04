import re
from enum import Enum


class Type(Enum):
    int = 'int'
    const_int = 'const_int'
    char = 'char'
    const_char = 'const_char'
    char_array = 'char_array'
    const_char_array = 'const_char_array'
    int_array = 'int_array'
    const_int_array = 'const_int_array'


def is_int(num):
    return -2147483648 <= int(num) <= 2147483647


def is_char(char):
    char_re = re.compile(r'^\'((?!\\)[\x00-\xff]|\\\\|\\t|\\n|\\0|\\\'|\\\")\'$')
    return char_re.match(char)


def is_const_char_array(string):
    string_re = re.compile(r'^\"((?!\\)[\x00-\xff]|\\\\|\\t|\\n|\\0|\\\'|\\\")*\"$')
    return string_re.match(string)


# Od zavrsnih znakova gramatike, jedino IDN identifikator moze biti l-izraz i to samo ako predstavlja varijablu
# brojevnog tipa (char ili int) bez const-kvalifikatora. Identifikator koji predstavlja funkciju ili niz nije l-izraz.
def is_l_expression(type_: Type):
    if type_.value == 'char' or type_.value == 'int':
        return True
    return False


def is_castable(from_type: Type, to_type: Type):
    if from_type == to_type:
        return True
    if from_type == Type.int and to_type == Type.char:
        return True
    elif from_type == Type.char and to_type == Type.int:
        return True
    elif from_type == Type.char and to_type == Type.const_char:
        return True
    elif from_type == Type.const_char and to_type == Type.char:
        return True
    elif from_type == Type.int and to_type == Type.const_int:
        return True
    elif from_type == Type.const_int and to_type == Type.int:
        return True
    elif from_type == Type.int_array and to_type == Type.const_int_array:
        return True
    elif from_type == Type.char_array and to_type == Type.const_char_array:
        return True
    return False


def array_to_single(array_type: Type):
    if array_type == Type.int_array:
        return Type.int
    elif array_type == Type.char_array:
        return Type.char
    elif array_type == Type.const_int_array:
        return Type.const_int
    elif array_type == Type.const_char_array:
        return Type.const_char
