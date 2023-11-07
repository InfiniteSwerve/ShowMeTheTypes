from showmethetypes.registry import (
    get_handler,
    get_registry,
    register_handlers,
    register_handler,
)
from showmethetypes.handlers import check_storage
from typing import Optional, Any


class SMTT:
    def __init__(
        self,
        *imported_handlers,
        custom_handlers: Optional[list[Any]] = None,
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
                register_handlers(key)

        if imported_handlers != ():
            for storage in imported_handlers:
                register_handlers(storage)
        if custom_handlers != None:
            for name, handler in custom_handlers:
                register_handler(name, handler)

    # TODO: Be able to pass in "monomorphic" = True to make default behavior find all unique lengths..
    def __call__(self, obj) -> None:
        self.lines = []
        self.traverse(obj)
        self.display()

    def traverse(self, thing, indent=0, is_last=True, prefix="") -> None:
        # Determine the type of the current object
        handler = get_handler(type(thing).__name__.lower()) or get_handler("default")
        handler(self, thing, indent, is_last, prefix)

    def display(self) -> None:
        for line in self.lines:
            print(line)
