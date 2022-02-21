from . import date
import locale
import sys

save_loc = locale.getlocale()
locale.setlocale(locale.LC_ALL, 'ru_RU')

args = sys.argv[1:]
date(*args)

locale.setlocale(locale.LC_ALL, save_loc)

