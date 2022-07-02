"""
Single Responsibility Principle 單一職責原則:
將職責單一化不要太過複雜
1. 一個類別應該只有一個被改變的原因
2. 一個類別只應該做一件事，即其職責
3. 其職責就是該類別會改變的原因
"""
import random
from typing import List

class Event:

    def __init__(self, name):
        self.name = name

# * 違反範例
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

# * 符合範例
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
