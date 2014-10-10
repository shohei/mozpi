class Dog(object):
    def __init__(self, name):
       self.name = name
 
class UltraDog(Dog):
    def __init__(self, name, type):
        super(UltraDog, self).__init__(name)
        self.type = type
 
ud1 = UltraDog(type="akita",name="taro")
print(ud1.name)
