class Container:
    def __init__(self):
        self.instances = {}

    def set_instance(self, name, instance):
        self.instances[name] = instance

    def get_instance(self, name):
        return self.instances[name]


container = Container()
