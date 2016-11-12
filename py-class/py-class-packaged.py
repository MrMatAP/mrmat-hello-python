"""
Using a class defined within a package
"""

from MyPackage import PackagedGreeting


#
# Say hi to some folks

mrmat = PackagedGreeting("MrMat")
mrmat.say_hi()

ee = PackagedGreeting("Eelyn")
ee.say_hi()


