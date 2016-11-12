"""
Using a class within a package
"""

# this works
from MyPackage.packagedgreeting import PackagedGreeting
# this doesn't
#import MyPackage.packagedgreeting


#
# Say hi to some folks

mrmat = PackagedGreeting("MrMat")
mrmat.sayHi()

ee = PackagedGreeting("Eelyn")
ee.sayHi()


