from __future__ import annotations
from typing_extensions import Self


class Service:
    __instance: Self = None

    @classmethod
    def getInsance(self):
        if self.__instance == None:
            self.__instance = self.createInstance()
        return self.__instance

    @classmethod
    def createInstance(self):
        pass
