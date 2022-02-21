from time import strftime
from pyfiglet import Figlet

def date(format="%Y %d %b, %A", font="graceful"):
    f = Figlet(font=font)
    print(f.renderText(strftime(format)))

