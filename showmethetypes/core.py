from showmethetypes.registry import get_handler, get_registry, register_handlers


class SMTT:
    def __init__(self, custom_handlers=None):
        self.handlers = get_registry()
        if custom_handlers is not None:
            self.handlers.update(custom_handlers)

    def __call__(self, obj):
        self.lines = []
        self.traverse(obj)
        self.display()

    def traverse(self, thing, indent=0, is_last=True, prefix=""):
        # Determine the type of the current object
        handler = get_handler(type(thing).__name__.lower()) or get_handler("default")
        handler(self, thing, indent, is_last, prefix)

    def register_handlers(self, storage_name):
        register_handlers(storage_name)

    def display(self):
        for line in self.lines:
            print(line)
