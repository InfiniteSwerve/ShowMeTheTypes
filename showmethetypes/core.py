from showmethetypes.registry import (
    get_handler,
    get_registry,
    register_handlers,
)
from showmethetypes.handlers import check_storage


class SMTT:
    # TODO: imported_handlers can be strings, need an argumnent for user defined handlers
    def __init__(
        self,
        *imported_handlers,
    ):
        import sys
        import types

        self.handlers = get_registry()
        imported_modules = {
            name: obj
            for name, obj in sys.modules.items()
            if isinstance(obj, types.ModuleType)
        }
        for key in imported_modules.keys():
            handlers = check_storage(key)
            if handlers is not None:
                # print("key is", key, "handlers is", handlers)
                register_handlers(key)

        if imported_handlers != ():
            for storage in imported_handlers:
                register_handlers(storage)

    # TODO: Be able to pass in "monomorphic" = True to make default behavior find all unique lengths..
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
