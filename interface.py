from abc import ABC, abstractmethod

class QueryGenerator(ABC):
    @abstractmethod
    def getQuery(self,exp:str):
        """ Generate Query Code """
        raise NotImplementedError
