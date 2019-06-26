import re


def SpecialTranslate(matched):
    return '\\' + matched


def StringHelper(string):
    return re.subn(pattern="%\/'\"", repl=SpecialTranslate, string=string)


