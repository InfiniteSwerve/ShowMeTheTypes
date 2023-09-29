"""
handler class instead of static method
"""


# class Handler:
#     def __init__(
#         self,
#         boilerplate: Callable = None,
#         type_level: Callable = None,
#         continuation: Callable = None,
#     ):
#         self.boilerplate = (
#             boilerplate if boilerplate is not None else self.default_boilerplate
#         )
#         self.type_level = (
#             type_level if type_level is not None else self.default_type_level
#         )
#         self.continuation = (
#             continuation if continuation is not None else self.default_continuation
#         )

#     def handle(self, typetree: TypeTree, thing, indent, is_last, prefix):
#         new_prefix, dtype_str = self.boilerplate(thing, is_last, prefix)
#         typetree.lines.append(self.type_level(thing, indent, new_prefix, dtype_str))
#         self.continuation(thing, typetree, indent, is_last, prefix)

#     def default_boilerplate(self, thing, is_last, prefix):
#         dtype_str = ""
#         if hasattr(thing, "dtype"):
#             dtype_str = f" (dtype: {thing.dtype})"
#         return prefix + ("    " if is_last else "|   "), dtype_str

#     def default_type_level(self, thing, indent, prefix, dtype_str):
#         return (
#             f"{prefix}|__{type(thing).__name__}{dtype_str}"
#             if indent
#             else f"{type(thing).__name__}{dtype_str}"
#         )

#     def default_continuation(self, typetree, thing, indent, is_last, prefix):
#         if isinstance(thing, str):
#             return
#         elif hasattr(thing, "__getitem__"):
#             items = list(thing)
#             for i, item in enumerate(items):
#                 typetree.traverse(item, indent + 1, i == len(items) - 1, prefix)

from typing import Callable, List, Tuple


class Handler:
    def __init__(
        self,
        boilerplate: Callable = None,
        type_level: Callable = None,
        continuation: Callable = None,
    ):
        self.boilerplate = (
            boilerplate if boilerplate is not None else self.default_boilerplate
        )
        self.type_level = (
            type_level if type_level is not None else self.default_type_level
        )
        self.continuation = (
            continuation if continuation is not None else self.default_continuation
        )

    def handle(
        self, thing, indent, is_last, prefix
    ) -> Tuple[List[str], List[Tuple[object, int, bool, str]]]:
        new_prefix, dtype_str = self.boilerplate(thing, is_last, prefix)
        line = self.type_level(thing, indent, new_prefix, dtype_str)
        continuation_data = self.continuation(thing, indent, is_last, new_prefix)

        return ([line], continuation_data)

    def default_boilerplate(self, thing, is_last, prefix) -> Tuple[str, str]:
        dtype_str = ""
        if hasattr(thing, "dtype"):
            dtype_str = f" (dtype: {thing.dtype})"
        return prefix + ("    " if is_last else "|   "), dtype_str

    def default_type_level(self, thing, indent, prefix, dtype_str) -> str:
        return (
            f"{prefix}|__{type(thing).__name__}{dtype_str}"
            if indent
            else f"{type(thing).__name__}{dtype_str}"
        )

    def default_continuation(
        self, thing, indent, is_last, prefix
    ) -> List[Tuple[object, int, bool, str]]:
        if isinstance(thing, str):
            return []

        if hasattr(thing, "__getitem__"):
            items = list(thing)
            return [
                (item, indent + 1, i == len(items) - 1, prefix)
                for i, item in enumerate(items)
            ]

        return []


class TypeTree:
    def __init__(self, obj):
        self.lines = []
        self.traverse(obj)
        self.display()

    def traverse(self, thing, indent=0, is_last=True, prefix=""):
        # Determine the type of the current object
        current_type = type(thing).__name__
        method_name = f"handle_{current_type.lower()}"
        handler = getattr(self, method_name, self.default_handler)
        handler(thing, indent, is_last, prefix)

    def default_handler(self, thing, indent, is_last, prefix):
        # Boilerplate printing
        dtype_str = ""
        if hasattr(thing, "dtype"):
            dtype_str = f" (dtype: {thing.dtype})"
        new_prefix = prefix + ("    " if is_last else "|   ")

        # type-level printing
        self.lines.append(
            f"{prefix}|__{type(thing).__name__}{dtype_str}"
            if indent
            else f"{type(thing).__name__}{dtype_str}"
        )

        # continuation
        if isinstance(thing, str):
            return
        elif hasattr(thing, "__getitem__"):
            items = list(thing)
            for i, item in enumerate(items):
                self.traverse(item, indent + 1, i == len(items) - 1, new_prefix)

    def handle_list(self, thing, indent, is_last, prefix):
        dtype_str = f": {len(thing)}"
        new_prefix = prefix + ("    " if is_last else "|   ")

        self.lines.append(
            f"{prefix}|_{type(thing).__name__}{dtype_str}"
            if indent
            else f"{type(thing).__name__}{dtype_str}"
        )

        if thing is not []:
            self.traverse(thing[0], indent + 1, True, new_prefix)

    def handle_tensor(self, thing, indent, is_last, prefix):
        dtype_str = f" (dtype: {thing.dtype})"
        new_prefix = prefix + ("    " if is_last else "|   ")

        # Print the current object type
        self.lines.append(
            f"{prefix}|__{type(thing).__name__}{dtype_str}"
            if indent
            else f"{type(thing).__name__}{dtype_str}"
        )

        for i in range(thing.dim()):
            dim_str = f"dim_{i} ({thing.size(i)})"
            self.lines.append(f"{new_prefix}|__{dim_str}")

    def handle_subset(self, thing, indent, is_last, prefix):
        dtype_str = f": {len(thing)}"
        new_prefix = prefix + ("    " if is_last else "|   ")

        self.lines.append(
            f"{prefix}|_{type(thing).__name__}{dtype_str}"
            if indent
            else f"{type(thing).__name__}{dtype_str}"
        )

        if len(thing) is not 0:
            self.traverse(thing[0], indent + 1, True, new_prefix)

    def display(self):
        for line in self.lines:
            print(line)
