"""SET, GET, DEL, INCR komutlarının davranışları."""

from app.store import Entry, Store
from app.errors import InvalidArgumentError


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

def incr_command(store: Store, key: str) -> int:
    """Key'in integer değerini 1 artırır. Key yoksa 0 kabul edip 1'e çıkarır.
    Key başka tipteyse WrongTypeError, değer sayı değilse InvalidArgumentError fırlatır."""
    entry = store.get_entry(key)

    if entry is None:
        new_entry = Entry("string", "1")
        store.set_entry(key, new_entry)
        return 1

    store.check_type(key, "string")

    try:
        current = int(entry.value)
    except ValueError:
        raise InvalidArgumentError()

    new_value = current + 1
    entry.value = str(new_value)
    return new_value