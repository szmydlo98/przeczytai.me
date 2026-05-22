# `pass` in a custom exception class is complete, not a placeholder

```python
class StorageError(Exception):
    pass
```

`pass` just fills Python's "block can't be empty" rule. A custom exception inherits
all it needs from `Exception`; its only purpose is to be a **distinct type** you can
catch (`except StorageError:`). The body has no job, so empty is correct/finished.

Contrast: `def upload(): pass` *is* an unfinished stub — a function is expected to act.

**Rule of thumb:** judge a `pass` by what it sits inside, not the keyword. Inside an
exception class → done. Inside a function meant to do something → red flag.

### Example
```
class StorageError(Exception):
      pass
```

StorageError already inherits everything it needs from Exception — how to store a message, how to print, how to be raised and caught. You're not changing any of that behavior. You only
want a distinct type so that elsewhere you can say "catch this specific kind of error, not all errors":

```
try:
    storage.put_text(...)
except StorageError:        # ← the whole point: catch only storage problems
    raise ApiException("storage_error", "Failed to store original text", 500)
```
