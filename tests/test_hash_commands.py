import pytest

from app.store import Store, Entry
from app.errors import WrongTypeError
from app.commands.hash_commands import hset_command, hget_command, hdel_command, hgetall_command

def test_hset_raises_wrong_type_for_string_key():
    store = Store()
    store.set_entry("user:1", Entry("string", "Tuğba"))
    with pytest.raises(WrongTypeError):
        hset_command(store, "user:1", "name", "Ahmet")

def test_hset_creates_new_field():
    store = Store()
    result = hset_command(store, "user:2", "name", "Ayşe")
    entry = store.get_entry("user:2")
    assert result == 1
    assert entry.data_type == "hash"
    assert entry.value == {"name": "Ayşe"}

def test_hset_updates_existing_field():
    store = Store()
    hset_command(store, "user:2", "name", "Ayşe")
    result = hset_command(store, "user:2", "name", "Fatma")
    entry = store.get_entry("user:2")
    assert result == 0
    assert entry.value["name"] == "Fatma"

def test_hget_returns_none_for_missing_key():
    store = Store()
    result = hget_command(store, "user:2", "name")
    assert result is None

def test_hget_returns_none_for_missing_field():
    store = Store()
    hset_command(store, "user:2", "name", "Ayşe")
    result = hget_command(store, "user:2", "age")
    assert result is None

def test_hget_returns_value_for_existing_field():
    store = Store()
    hset_command(store, "user:2", "name", "Ayşe")
    result = hget_command(store, "user:2", "name")
    assert result == "Ayşe"

def test_hget_raises_wrong_type_for_string_key():
    store = Store()
    store.set_entry("user:2", Entry("string", "Cüneyt"))
    with pytest.raises(WrongTypeError):
        hget_command(store, "user:2", "name")

def test_hdel_removes_existing_field():
    store = Store()
    hset_command(store, "user:2", "name", "Ayşe")
    hset_command(store, "user:2", "age", "30")
    result = hdel_command(store, "user:2", "name")
    entry = store.get_entry("user:2")
    assert result == 1
    assert entry is not None
    assert "name" not in entry.value
    assert entry.value == {"age": "30"}

def test_hdel_returns_zero_for_missing_field():
    store = Store()
    hset_command(store, "user:2", "name", "Ayşe")
    result = hdel_command(store, "user:2", "age")
    assert result == 0

def test_hdel_returns_zero_for_missing_key():
    store = Store()
    result = hdel_command(store, "user:2", "name")
    assert result == 0

def test_hdel_removes_key_when_hash_becomes_empty():
    store = Store()
    hset_command(store, "user:2", "name", "Ayşe")
    result = hdel_command(store, "user:2", "name")
    entry = store.get_entry("user:2")
    assert result == 1
    assert entry is None

def test_hdel_raises_wrong_type_for_string_key():
    store = Store()
    store.set_entry("user:2", Entry("string", "Cüneyt"))
    with pytest.raises(WrongTypeError):
        hdel_command(store, "user:2", "name")

def test_hgetall_returns_empty_dict_for_missing_key():
    store = Store()
    result = hgetall_command(store, "user:2")
    assert result == {}

def test_hgetall_returns_all_fields():
    store = Store()
    hset_command(store, "user:2", "name", "Ayşe")
    hset_command(store, "user:2", "age", "30")
    result = hgetall_command(store, "user:2")
    assert result == {"name": "Ayşe", "age": "30"}

def test_hgetall_raises_wrong_type_for_string_key():
    store = Store()
    store.set_entry("user:2", Entry("string", "Cüneyt"))
    with pytest.raises(WrongTypeError):
        hgetall_command(store, "user:2")