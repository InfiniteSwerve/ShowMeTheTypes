from showmethetypes.registry import get_handler, get_registry, register_handlers
from showmethetypes.handlers import check_storage


class SMTT:
    # TODO: imported_handlers can be strings, need an argumnent for user defined handlers
    def __init__(
        self,
        *imported_handlers,
    ):
        import types

        self.handlers = get_registry()
        imported_modules = {
            name: obj
            for name, obj in locals().items()
            if isinstance(obj, types.ModuleType)
        }
        for key in imported_modules.keys():
            handlers = check_storage(key)
            if handlers is not None:
                register_handlers(handlers)

        if imported_handlers != ():
            for storage in imported_handlers:
                register_handlers(storage)

    def __call__(self, obj):
        self.lines = []
        self.traverse(obj)
        self.display()

    def traverse(self, thing, indent=0, is_last=True, prefix=""):
        # Determine the type of the current object
        handler = get_handler(type(thing).__name__.lower()) or get_handler("default")
        handler(self, thing, indent, is_last, prefix)

    def display(self):
        for line in self.lines:
            print(line)
