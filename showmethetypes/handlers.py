branch = "├── "

trunk = "│   "

end = "└── "
# TODO: custom handler args


# TODO: Compress the handlers
def default_handler(self, thing, indent, is_last, prefix):
    # Boilerplate printing
    dtype_str = ""
    if hasattr(thing, "dtype"):
        dtype_str = f" (dtype: {thing.dtype})"
    new_prefix = prefix + ("    " if is_last else trunk)
    infix = end if is_last else branch

    # type-level printing
    self.lines.append(
        f"{prefix}{infix}{type(thing).__name__}{dtype_str}"
        if indent
        else f"{type(thing).__name__}{dtype_str}"
    )  # continuation

    if isinstance(thing, str):
        return
    elif hasattr(thing, "__getitem__"):
        items = list(thing)
        for i, item in enumerate(items):
            self.traverse(item, indent + 1, i == len(items) - 1, new_prefix)


# TODO: Empty list
def handle_list(self, thing, indent, is_last, prefix):
    dtype_str = f" ({len(thing)})"
    new_prefix = prefix + ("    " if is_last else trunk)
    infix = end if is_last else branch

    self.lines.append(
        f"{prefix}{infix}{type(thing).__name__}{dtype_str}"
        if indent
        else f"{type(thing).__name__}{dtype_str}"
    )

    if thing:
        self.traverse(thing[0], indent + 1, True, new_prefix)


def handle_tensor(self, thing, indent, is_last, prefix):
    dtype_str = f" (dtype: {thing.dtype})"
    new_prefix = prefix + ("    " if is_last else trunk)
    infix = end if is_last else branch

    # Print the current object type
    self.lines.append(
        f"{prefix}{infix}{type(thing).__name__}{dtype_str}"
        if indent
        else f"{type(thing).__name__}{dtype_str}"
    )
    self.lines.append(f"{new_prefix}{trunk}(device: {thing.device})")

    if thing.dim() == 0:
        self.lines.append(f"{new_prefix}{end}{thing.item()}")
    else:
        for i, dim in enumerate(thing.shape):
            infix = end if i == len(thing.shape) - 1 else branch
            dim_str = f"dim_{i} ({dim})"
            self.lines.append(f"{new_prefix}{infix}{dim_str}")


def handle_linear(self, thing, indent, is_last, prefix):
    new_prefix = prefix + ("    " if is_last else trunk)
    infix = end if is_last else branch
    bias = f" (bias: {True if thing.bias is not None else False})"

    # Print the current object type
    self.lines.append(
        f"{prefix}{infix}{type(thing).__name__}{bias}"
        if indent
        else f"{type(thing).__name__}{bias}"
    )
    self.lines.append(f"{new_prefix}{branch}rows ({thing.in_features})")
    self.lines.append(f"{new_prefix}{end}cols ({thing.out_features})")


def handle_subset(self, thing, indent, is_last, prefix):
    dtype_str = f": {len(thing)}"
    new_prefix = prefix + ("    " if is_last else trunk)
    infix = end if is_last else branch

    # Print the current object type
    self.lines.append(
        f"{prefix}{infix}{type(thing).__name__}{dtype_str}"
        if indent
        else f"{type(thing).__name__}{dtype_str}"
    )

    if len(thing) != 0:
        self.traverse(thing[0], indent + 1, True, new_prefix)


def handle_dataloader(self, thing, indent, is_last, prefix):
    dtype_str = f" ({len(thing)})"
    new_prefix = prefix + ("    " if is_last else trunk)
    infix = end if is_last else branch

    # Print the current object type
    self.lines.append(
        f"{prefix}{infix}{type(thing).__name__}{dtype_str}"
        if indent
        else f"{type(thing).__name__}{dtype_str}"
    )

    if len(thing) != 0:
        for d in thing:
            data = d
            break
        self.traverse(data, indent + 1, True, new_prefix)
    else:
        pass


def handle_int64(self, thing, indent, is_last, prefix):
    dtype_str = ""
    # Print the current object type
    self.lines.append(
        f"{prefix}{end}{type(thing).__name__}{dtype_str}: {thing}"
        if indent
        else f"{type(thing).__name__}{dtype_str}: {thing}"
    )


def handle_ndarray(self, thing, indent, is_last, prefix):
    dtype_str = f" (dtype: {thing.dtype})"
    new_prefix = prefix + ("    " if is_last else trunk)
    infix = end if is_last else branch

    # Print the current object type
    self.lines.append(
        f"{prefix}{infix}{type(thing).__name__}{dtype_str}"
        if indent
        else f"{type(thing).__name__}{dtype_str}"
    )

    if thing.shape == ():
        self.lines.append(f"{new_prefix}{end}{thing.item()}")
    else:
        for i, dim in enumerate(thing.shape):
            infix = end if i == len(thing.shape) - 1 else branch
            dim_str = f"dim_{i} ({dim})"
            self.lines.append(f"{new_prefix}{infix}{dim_str}")


# lowercase type
handler_storage = {
    "std": [("default", default_handler), ("list", handle_list)],
    "torch": [
        ("tensor", handle_tensor),
        ("linear", handle_linear),
        ("subset", handle_subset),
        ("dataloader", handle_dataloader),
    ],
    "numpy": [("ndarray", handle_ndarray), ("int64", handle_int64)],
}


def check_storage(name):
    return handler_storage.get(name, None)
