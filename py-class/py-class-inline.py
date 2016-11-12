"""
Inline definition of a class in Python
"""


class Greeting:

    def sayHi(self):
        print("Hi there, {}".format(self.name))

    def __init__(self, name='MrMat'):
        """
        Constructor with a default variable for name. Note how there can only be one constructor

        It would be wrong to define name as a class variable above because such a definition would be the equivalent
        of a static variable in Java and shared by all instances. Instance variables are exclusively declared within
        the __init__ constructor.
        """
        self.name = name

#
# Say hi to some folks

mrmat = Greeting("MrMat")
mrmat.sayHi()

ee = Greeting("Eelyn")
ee.sayHi()
