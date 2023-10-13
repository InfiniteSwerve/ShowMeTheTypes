# Show Me The Types (SMTT)
This is a package designed to provide a single utility:
**showing you the types!**

If you frequently end up handling lists of tuples of tensors, lists of tensors, nested lists and tuples, or other similarly convoluted structures, SMTT might be able to make your life just a bit easier. Instead of thinking about needing `len`, `.shape`, `.size()`, or printing out the structure and parsing the brackets and parens, you can just do `tt(data)`, and get an instant overview of the structure.  

```python
from showmethetypes import SMTT
import torch

tt = SMTT()
structure = [(torch.randn(2,3), torch.randn(500, 5, 128)) for _ in range(5)]

tt(structure)
```
```
list (5)
    |__tuple
        |__Tensor (dtype: torch.float32)
        |   |  (device: cpu)
        |   |__dim_0 (2)
        |   |__dim_1 (3)
        |__Tensor (dtype: torch.float32)
            |  (device: cpu)
            |__dim_0 (500)
            |__dim_1 (5)
            |__dim_2 (128)
```

## Behavior 
SMTT will by default display the type for whatever you pass it, and traverse all nested types if the passed object has a `__getitem__` method.

The default behavior is to iterate across *all* subtypes, which means it will print out everything the object contains. Some types, like lists, are usually monomorphic, so SMTT will assume monomorphism and only print out the nested structure in the first item of the list. 

SMTT will also infer your current imports and use the specific handlers available for any libraries in your `locals()`.
## Coverage

SMTT is quite fresh, and so the current coverage only includes objects that I've needed to work with directly. If you feel sad about any missing types, feel free to raise an issue requesting it, or even make a PR! Creating new handlers for types is quite straightforward. 

The libraries with any coverage are listed here, and you can find detailed coverage information in `handlers.py`. 
| Library | Total Coverage |
|---------|----------------|
| stdlib  | No             |
| Pytorch | No             |