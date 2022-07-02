"""
Interface Segregation Principle 介面隔離原則:
物件不應該依賴或引入自己不相關的功能
"""
from abc import ABCMeta, abstractmethod

# 違反介面隔離原則
class Person1(metaclass=ABCMeta):

    @abstractmethod
    def eat(self):
        pass

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def programming(self):
        pass

class Programming1(Person1):

    def eat(self):
        print("我會吃")

    def run(self):
        print("我會爬")

    def programming(self):
        print("我會寫code")
        pass

class Baby1(Person1):

    def eat(self):
        print("我會吃")

    def run(self):
        print("我會爬")

    # 多出要寫的方法
    def programming(self):
        pass

# 遵守介面隔離原則
class Person2(metaclass=ABCMeta):

    @abstractmethod
    def eat(self):
        pass

    @abstractmethod
    def run(self):
        pass

class WriteCode(metaclass=ABCMeta):
    @abstractmethod
    def programming(self):
        pass

# 要使用 programming 方法，只需多繼承 WriteCode
class Programming2(Person2, WriteCode):

    def eat(self):
        print("我會吃")

    def run(self):
        print("我會爬")

    def programming(self):
        print("我會寫code")
        pass

class Baby2(Person1):

    def eat(self):
        print("我會吃")

    def run(self):
        print("我會爬")
