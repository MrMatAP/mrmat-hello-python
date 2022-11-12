
from mhpython.classes.Greeting import Greeting
from mhpython.classes.GermanGreeting import GermanGreeting


def run():
    print("I will say hi in the default language: %s" % Greeting().say_hi())
    print("I will now say hi in German: %s" % GermanGreeting().say_hi())


if __name__ == '__main__':
    run()
