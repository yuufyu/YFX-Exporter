import abc


class Process(metaclass=abc.ABCMeta) :
    @abc.abstractmethod
    def report_info(self, message: str) -> None:
        raise NotImplementedError

class MainProcess(Process) :
    def report_info(self, message: str) -> None:
        print(message)

class SubProcess(Process) :
    def report_info(self, message: str) -> None:
        print(message)
