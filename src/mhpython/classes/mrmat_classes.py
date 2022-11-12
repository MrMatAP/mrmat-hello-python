
from mhpython.classes.Greeting import Greeting
from mhpython.classes.GermanGreeting import GermanGreeting


def run():
    print(f'I will say hi in the default language: {Greeting().say_hi()}')
    print(f'I will now say hi in German: {GermanGreeting().say_hi()}')


if __name__ == '__main__':
    run()
