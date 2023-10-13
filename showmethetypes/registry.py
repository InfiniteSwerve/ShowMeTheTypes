from showmethetypes.handlers import handler_storage
_HANDLER_REGISTRY = {}

def register_handler(type_name, handler):
    _HANDLER_REGISTRY[type_name] = handler

def get_handler(type_name):
    return _HANDLER_REGISTRY.get(type_name, None)

def get_registry():
    return _HANDLER_REGISTRY

def register_handlers(storage_name):
    for name, handler in handler_storage[storage_name]:
        register_handler(name, handler)

def _register_default_handlers():
    register_handlers("std")

_register_default_handlers()