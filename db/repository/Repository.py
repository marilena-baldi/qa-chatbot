class Repository:
    def __init__(self, session, table) -> None:
        """
        Initialize the repository.

        :param session: database session
        :type session: SessionLocal
        :param table: object model
        :type table: Base
        """

        self.session = session
        self.table = table

    @staticmethod
    def get_dict(x):
        """ Get the dictionary of the object. """

        return dict((key, value) for key, value in x.__dict__.items()
                    if not callable(value) and not key.startswith('_'))

    def query(self, query_dict):
        """ Query the database. """

        query = self.session.query(self.table)
        for attr, value in query_dict.items():
            query = query.filter(getattr(self.table, attr) == value)

        return query

    def create(self, element):
        """ Create a record. """

        self.session.add(element)
        self.session.flush()

        return element.id

    def read(self, element):
        """ Read records. """

        query_dict = self.get_dict(element)
        records = self.query(query_dict=query_dict).all()

        return records

    def update(self, element_old, element_new):
        """ Update records. """

        query_dict = self.get_dict(element_old)
        param_dict = self.get_dict(element_new)
        num_records = self.query(query_dict=query_dict).update(param_dict, synchronize_session=False)
        self.session.flush()

        return num_records

    def delete(self, element):
        """ Delete records. """

        query_dict = self.get_dict(element)
        num_records = self.query(query_dict=query_dict).delete(synchronize_session=False)

        return num_records
