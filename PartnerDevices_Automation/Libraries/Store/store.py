from .exception import *


class Store(object):
    def __init__(self):
        self._objects = {}

    def __iter__(self):
        return (each for each in list(self._objects.values()))

    @property
    def aliases(self):
        return list(self._objects.keys())

    def add(self, value, alias=None):
        alias = self._get_alias(alias)
        if alias in self._objects:
            raise NameIsProtected(f"Alias add: '{str(alias)}' exists")
        self._objects[alias] = value
        print("Added alias with name : ", alias)

    def remove(self, alias=None):
        alias = self._get_alias(alias)
        if alias not in self._objects:
            raise AliasError(f"Alias remove: '{str(alias)}' doesn't exist")
        del self._objects[alias]
        print("Removed alias with name : ", alias)

    def get(self, alias=None):
        # print("Available aliases : ", self.aliases)
        alias = self._get_alias(alias)
        if alias not in self._objects:
            raise AliasError(f"Alias get: '{str(alias)}' doesn't exist")
        return self._objects[alias]

    def has_alias(self, alias=None):
        alias = self._get_alias(alias)
        return alias in self._objects

    def _get_alias(self, alias):
        return "default" if alias is None else alias
