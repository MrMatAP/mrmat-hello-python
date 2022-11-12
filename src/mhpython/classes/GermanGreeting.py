
from mhpython.classes.Greeting import Greeting


class GermanGreeting(Greeting):
    """
    A German greeting, overriding the say_hi method
    """

    def say_hi(self):
        """
        Overrides the greeting
        :return:
        """
        return "Hallo, {}".format(self.name)
