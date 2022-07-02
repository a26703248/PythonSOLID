"""
Liskov Substitution Principle 里氏替換原則

資料來源網址:https://igouist.github.io/post/2020/11/oo-12-liskov-substitution-principle/

一個好的擴展方式，應該能滿足這些條件：
要求不應該比父類別多
回饋不應該比父類別少

因此當我們想要符合里氏替換原則時候，其實就可以試著遵守：
先驗條件不可以強化：父類別要求的是矩形，子類別就不能要求得更嚴，只准人家給正方形
後驗條件不可以弱化：父類別產出的是正方形，子類別不能說沒關係啦，就給人家隨便一個矩形
不變條件必須保持不變：父類別是一個產生矩形的方法，子類別不能背骨，跑去產生圓形

剛剛有提到LSP的定義為子類別可以擴充套件父類別的功能,但不改變父類別原有的功能，其中還包含以下4層含義。

1.子類別必須完全實現父類別的方法
2.子類別可以有自己的特性
3.重載(Overload)或者實現父類別的方法時輸入參數可以被放大
4.覆蓋或者實現父類別的方法時輸出結果可以被縮小
"""
from collections.abc import Mapping


class Event:
    def __init__(self, raw_data):
        self.raw_data = raw_data

    @staticmethod
    def meets_condition(event_data: dict) -> bool:
        return False

    @staticmethod
    def validate_precondition(event_data: dict):
        """Precondition of the contract of this interface.

        Validate that the ``event_data`` parameter is properly formed.
        """
        if not isinstance(event_data, Mapping):
            raise ValueError(f"{event_data!r} is not a dict")
        for moment in ("before", "after"):
            if moment not in event_data:
                raise ValueError(f"{moment} not in {event_data}")
            if not isinstance(event_data[moment], Mapping):
                raise ValueError(f"event_data[{moment!r}] is not a dict")


class UnknownEvent(Event):
    """A type of event that cannot be identified from its data"""


class LoginEvent(Event):
    @staticmethod
    def meets_condition(event_data: dict) -> bool:
        return (
            event_data["before"].get("session") == 0
            and event_data["after"].get("session") == 1
        )


class LogoutEvent(Event):
    @staticmethod
    def meets_condition(event_data: dict) -> bool:
        return (
            event_data["before"].get("session") == 1
            and event_data["after"].get("session") == 0
        )

class TransactionEvent(Event):
    """Represents a transaction that has just occurred on the system."""

    @staticmethod
    def meets_condition(event_data: dict) -> bool:
        return event_data["after"].get("transaction") is not None


class SystemMonitor:
    """Identify events that occurred in the system

    >>> l1 = SystemMonitor({"before": {"session": 0}, "after": {"session": 1}})
    >>> l1.identify_event().__class__.__name__
    'LoginEvent'

    >>> l2 = SystemMonitor({"before": {"session": 1}, "after": {"session": 0}})
    >>> l2.identify_event().__class__.__name__
    'LogoutEvent'

    >>> l3 = SystemMonitor({"before": {"session": 1}, "after": {"session": 1}})
    >>> l3.identify_event().__class__.__name__
    'UnknownEvent'

    >>> l4 = SystemMonitor({"before": {}, "after": {"transaction": "Tx001"}})
    >>> l4.identify_event().__class__.__name__
    'TransactionEvent'

    """

    def __init__(self, event_data):
        self.event_data = event_data

    def identify_event(self):
        Event.validate_precondition(self.event_data)
        event_cls = next(
            (
                event_cls
                for event_cls in Event.__subclasses__()
                if event_cls.meets_condition(self.event_data)
            ),
            UnknownEvent,
        )
        return event_cls(self.event_data)

