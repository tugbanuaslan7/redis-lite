from app.store import Entry, Store

def hset_command(store: Store, key: str, field: str, value: str) -> int:
    """Key'e hash değer yazar. Key başka tipteyse WrongTypeError fırlatır.
    Field yoksa 1, varsa 0 döner."""
    entry = store.get_entry(key)

    if entry is None:
        store.set_entry(key, Entry("hash", {field: value}))
        return 1

    store.check_type(key, "hash")

    if field in entry.value:
        entry.value[field] = value
        return 0
    else:
        entry.value[field] = value
        return 1

def hget_command(store: Store, key: str, field: str) -> str | None:
    """Key'in hash değerini döner, key yoksa None döner.
    Key başka tipteyse WrongTypeError fırlatır."""
    entry = store.get_entry(key)

    if entry is None:
        return None

    store.check_type(key, "hash")

    return entry.value.get(field)

def hdel_command(store: Store, key: str, field: str) -> int:
    """Key'in hash değerinden field'ı siler. Silindiyse 1, yoksa 0 döner.
    Hash boş kalırsa key'in kendisi de silinir.
    Key başka tipteyse WrongTypeError fırlatır."""
    entry = store.get_entry(key)

    if entry is None:
        return 0

    store.check_type(key, "hash")

    if field not in entry.value:
        return 0

    del entry.value[field]

    if not entry.value:
        store.delete_entry(key)

    return 1

def hgetall_command(store: Store, key: str) -> dict[str, str]:
    """Key'in tüm hash alan-değer çiftlerini döner.
    Key yoksa boş dict ({}) döner. Key başka tipteyse WrongTypeError fırlatır."""
    entry = store.get_entry(key)

    if entry is None:
        return {}

    store.check_type(key, "hash")

    return entry.value.copy()