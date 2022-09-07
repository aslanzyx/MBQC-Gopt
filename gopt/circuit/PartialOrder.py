class PartialOrder:
    def __int__(self):
        self.dependencies: dict[(int, int), set[(int, int)]] = dict()
        pass

    def add_dependency(self, source, target):
        if source not in self.dependencies:
            self.dependencies[source] = set()
        self.dependencies[source].add(target)
