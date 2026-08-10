"""SET, GET, DEL komutlarının davranışları."""

from app.store import Entry, Store


def set_command(store: Store, key: str, value: str) -> str:
    """Key'e string değer yazar. Key başka tipteyse WrongTypeError fırlatır."""
    entry = store.get_entry(key)

    if entry is None:
        store.set_entry(key, Entry("string", value))
        return "OK"

    store.check_type(key, "string")
    entry.value = value
    return "OK"


def get_command(store: Store, key: str) -> str | None:
    """Key'in string değerini döner, key yoksa None döner.
    Key başka tipteyse WrongTypeError fırlatır."""
    entry = store.get_entry(key)

    if entry is None:
        return None

    store.check_type(key, "string")
    return entry.value


def del_command(store: Store, key: str) -> int:
    """Key'i tipi ne olursa olsun siler. Silindiyse 1, yoksa 0 döner."""
    deleted = store.delete_entry(key)
    return 1 if deleted else 0