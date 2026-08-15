from app.store import Entry, Store


def zadd_command(store: Store, key: str, score: float, member: str) -> int:
    """Sorted set'e member ekler veya mevcut member'ın skorunu günceller.
    Yeni member için 1, mevcut member için 0 döner.
    Key başka tipteyse WrongTypeError fırlatır."""
    entry = store.get_entry(key)

    if entry is None:
        store.set_entry(key, Entry("zset", {member: score}))
        return 1

    store.check_type(key, "zset")

    if member in entry.value:
        entry.value[member] = score
        return 0

    entry.value[member] = score
    return 1

def zrange_command(store: Store, key: str, start: int, stop: int) -> list[str]:
    """Sorted set üyelerini score'a göre artan sırada döner.
    Start ve stop dahilidir. Negatif index desteklenir.
    Key yoksa boş liste döner."""
    entry = store.get_entry(key)

    if entry is None:
        return []

    store.check_type(key, "zset")

    sorted_members = sorted(
        entry.value,
        key=lambda member: (entry.value[member], member)
    )

    if stop == -1:
        return sorted_members[start:]

    return sorted_members[start:stop + 1]

def zrem_command(store: Store, key: str, member: str) -> int:
    """Sorted set'ten member'ı siler.
    Member silindiyse 1, bulunamadıysa 0 döner.
    Key yoksa 0 döner.
    Key başka tipteyse WrongTypeError fırlatır."""
    entry = store.get_entry(key)

    if entry is None:
        return 0

    store.check_type(key, "zset")

    if member not in entry.value:
        return 0

    del entry.value[member]

    if not entry.value:
        store.delete_entry(key)

    return 1

def zscore_command(store: Store, key: str, member: str) -> float | None:
    """Sorted set içindeki member'ın score değerini döner.
    Key veya member yoksa None döner.
    Key başka tipteyse WrongTypeError fırlatır."""
    entry = store.get_entry(key)

    if entry is None:
        return None

    store.check_type(key, "zset")

    return entry.value.get(member)