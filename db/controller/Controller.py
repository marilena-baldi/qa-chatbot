class Controller:
    def __init__(self, repository):
        """
        Initialize the controller.

        :param repository: repository to use
        :type repository: Repository
        """

        self.repository = repository
        self.table = self.repository.table

    def get_object_by_schema(self, schema):
        return self.table(**schema.dict(exclude_unset=True, exclude_none=True))

    def insert(self, element):
        """ Insert a new element using the repository. """

        element = self.get_object_by_schema(schema=element)

        return self.repository.create(element=element)

    def get(self, element=None):
        """ Get an element using the repository. """

        element = self.get_object_by_schema(schema=element) if element else self.table()

        return self.repository.read(element=element)

    def update(self, element_old, element_new):
        """ Update an element using the repository. """

        element_old = self.get_object_by_schema(schema=element_old)
        element_new = self.get_object_by_schema(schema=element_new)

        return self.repository.update(element_old=element_old, element_new=element_new)

    def remove(self, element):
        """ Remove an element using the repository. """

        element = self.get_object_by_schema(schema=element)

        return self.repository.delete(element)
