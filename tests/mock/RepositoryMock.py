class RepositoryMock:
    def __init__(self, session, table):
        self.table = table

    def create(self, element):
        return 1

    def read(self, element):
        return 1

    def update(self, element):
        return 1

    def delete(self, element):
        return 1
