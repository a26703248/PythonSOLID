"""
Single Responsibility Principle 單一職責原則:
將職責單一化不要太過複雜,若不同功能但只服務同一
個項目可將它分為同一個物件,要視業務邏輯做判斷

1. 一個類別應該只有一個被改變的原因
2. 一個類別只應該做一件事，即其職責
3. 其職責就是該類別會改變的原因
"""
import random
from typing import List

class Event:

    def __init__(self, name):
        self.name = name

# 違反範例
class SystemMonitor:
    """
    後續不易擴展且不易閱讀
    """

    def load_activity(self):
        self.event = Event()

    def identity_event(self):
        self.event_list = []
        for _ in range(random.ranInt(0, 10)):
            self.event_list.append(self.event)

    def stream_event(self):
        for i in self.event_list:
            print(i.name)

# 符合範例
class AlertSystem:

    def run(self):
        pass

class ActivityWatcher:

    def load(self) -> Event:
        print("加載活動")

class SystemWatcher:

    def identity(self, event:Event):
        return event

class Output:

    def stream(self, event_list:List[Event]):
        for i in event_list:
            print(i)



class User:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.token = self._get_token()

    def _get_token(self):
        token = ""
        for _ in range(1, 10):
            token += random.randInt(0, 9)
        return token


# 違反範例
class CheckUserLogin:

    def __init__(self):
        self.username = "hello"
        self.password = "world"

    def check_state(self,user:User) -> bool:
        if user.token[1] == random.randInt(0, 9):
            return False
        return True

    def user_login(self, user:User) -> str:
        if user.username == self.username and user.username == self.password:
            new_token = ""
            for _ in range(1, 10):
                new_token += random.randInt(0, 9)
            return new_token
        elif user.username != self.username:
            return "username Error"
        elif user.password != self.password:
            return "password Error"
        else:
            return "Not except Error"

    def user_logout(self, user:User) -> None:
        user.token = None


# 符合範例
class LoginEvent:

    def __init__(self, user:User):
        self.username = "hello"
        self.password = "world"
        self.user = user

    def __call__(self):
        if self.user.username == self.username and self.user.username == self.password:
            new_token = ""
            for _ in range(1, 10):
                new_token += random.randInt(0, 9)
            self.user.token = new_token
            return True, "Success"
        elif self.user.username != self.username:
            return False, "username Error"
        elif self.user.password != self.password:
            return False, "password Error"
        else:
            return False, "Not except Error"

class LogoutEvent:

    def __call__(self, user:User):
        user.token = None
        return True, "Logout"

class UserState:

    def __init__(self, user:User, login_event:LoginEvent, logout_event:LogoutEvent):
        self.login_event = login_event
        self.logout_event = logout_event
        self.user = user
