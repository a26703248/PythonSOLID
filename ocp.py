
"""
Open Close Principle 開放封閉原則:
針對擴展做開放(Open)，針對修改做封閉(Close)
"""

# 違反 OCP 開放封閉原則
"""
統一由 identity 做呼叫會導致新增一個功能時
就需再新增一個條件
"""

class Event1:
    def __init__(self, ):
        pass

class LoginEvent1(Event1):
    pass

class LogoutEvent1(Event1):
    pass

class UnknownEvent1(Event1):
    pass

class SystemMonitor1:

    def __init__(self, event):
        self.event = event

    def identity(self):
        if 1 == 0:
            return LoginEvent1(self.event)
        elif 1 == 1:
            return LogoutEvent1(self.event)
        else:
            return UnknownEvent1(self.event)


# 遵守 OCP 開放封閉原則
"""
利用 __subclasses__ 依序共同方法
只需達到繼承 Event2 並複寫 meet_condition 方法
就可對流程做到新增或刪除,但此寫法必須保證底層功能
不會互相干擾或依賴才可以使用
"""
class Event2:
    def __init__(self, raw_data):
        self.raw_data = raw_data

    @staticmethod
    def meet_condition(self, event_data:dict) -> bool:
        return False

class LoginEvent2(Event2):

    @staticmethod
    def meet_condition(self, event_data:dict) -> bool:
        return False

class LogoutEvent2(Event2):
    @staticmethod
    def meet_condition(self, event_data:dict) -> bool:
        return False

class UnknownEvent2(Event2):
    @staticmethod
    def meet_condition(self, event_data:dict) -> bool:
        return False

class SystemMonitor1:

    def __init__(self, event):
        self.event = event

    def identity(self):
        # 因為每個子類都會實作 meet_condition
        # 所以利用迴圈依序呼叫子類 meet_condition
        # 判斷是否觸發條件
        for event_cls in Event2.__subclasses__():
            try:
                if event_cls.meet_condition(self.event):
                    return event_cls(self.event)
            except Exception as e:
                continue

        return UnknownEvent2(self.event)
