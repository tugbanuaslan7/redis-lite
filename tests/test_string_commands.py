import threading

import pytest

from app.store import Store, Entry
from app.errors import WrongTypeError, InvalidArgumentError
from app.commands.string_commands import del_command, get_command, set_command, incr_command

def test_set_creates_new_string_key():
    store = Store()
    result = set_command(store, "user:1", "Tuğba")
    entry = store.get_entry("user:1")
    assert result == "OK"
    assert entry is not None
    assert entry.data_type == "string"
    assert entry.value == "Tuğba"

def test_set_overwrites_existing_string_key():
    store = Store()
    set_command(store, "user:1", "Tuğba")
    result = set_command(store, "user:1", "Ahmet")
    entry = store.get_entry("user:1")
    assert result == "OK"
    assert entry is not None
    assert entry.data_type == "string"
    assert entry.value == "Ahmet"

def test_get_returns_none_for_missing_key():
    store = Store()
    result = get_command(store, "user:1")
    assert result is None

def test_get_raises_wrong_type_for_hash_key():
    store = Store()
    store.set_entry("user:1", Entry("hash", {"name": "Tuğba"}))
    with pytest.raises(WrongTypeError):
        get_command(store, "user:1")

def test_del_removes_existing_key():
    store = Store()
    set_command(store, "user:1", "Tuğba")
    result = del_command(store, "user:1")
    entry = store.get_entry("user:1")
    assert result == 1
    assert entry is None

def test_del_returns_zero_for_missing_key():
    store = Store()
    result = del_command(store, "user:1")
    assert result == 0

def test_set_raises_wrong_type_for_hash_key():
    store = Store()
    store.set_entry("user:1", Entry("hash", {"name": "Tuğba"}))
    with pytest.raises(WrongTypeError):
        set_command(store, "user:1", "Tuğba")

def test_concurrent_sets_do_not_corrupt_store():
    store = Store()

    def worker(i):
        set_command(store, f"key:{i}", f"value:{i}")

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(100)]

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert len(store.entries) == 100
    for i in range(100):
        entry = store.get_entry(f"key:{i}")
        assert entry is not None
        assert entry.value == f"value:{i}"

def test_incr_creates_key_starting_from_zero():
    store = Store()
    result = incr_command(store, "counter")
    entry = store.get_entry("counter")
    assert result == 1
    assert entry.value == "1"

def test_incr_increments_existing_value():
    store = Store()
    incr_command(store, "counter")
    result = incr_command(store, "counter")
    assert result == 2

def test_incr_raises_invalid_argument_for_non_integer_value():
    store = Store()
    set_command(store, "counter", "not_a_number")
    with pytest.raises(InvalidArgumentError):
        incr_command(store, "counter")

def test_incr_raises_wrong_type_for_hash_key():
    store = Store()
    store.set_entry("counter", Entry("hash", {"a": "b"}))
    with pytest.raises(WrongTypeError):
        incr_command(store, "counter")

def test_concurrent_incr_on_same_key_does_not_lose_updates():
    store = Store()
    set_command(store, "counter", "0")

    def worker():
        incr_command(store, "counter")

    threads = [threading.Thread(target=worker) for _ in range(100)]

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    entry = store.get_entry("counter")
    assert entry.value == "100"