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
    )  # continuation

    if isinstance(thing, str):
        return
    elif hasattr(thing, "__getitem__"):
        items = list(thing)
        for i, item in enumerate(items):
            self.traverse(item, indent + 1, i == len(items) - 1, new_prefix)


def handle_list(self, thing, indent, is_last, prefix):
    dtype_str = f" ({len(thing)})"
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
    self.lines.append(f"{new_prefix}|  (device: {thing.device})")

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

    if len(thing) != 0:
        self.traverse(thing[0], indent + 1, True, new_prefix)


# lowercase type
handler_storage = {
    "std": [("default", default_handler), ("list", handle_list)],
    "torch": [("tensor", handle_tensor), ("subset", handle_subset)],
}


def check_storage(name):
    return handler_storage.get(name, None)
