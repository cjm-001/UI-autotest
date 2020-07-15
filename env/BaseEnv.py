import abc

class BaseEnv(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def getUrl(self):
        return '';

    @abc.abstractmethod
    def getOriginItem(self):
        return '';








