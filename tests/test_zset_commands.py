import pytest

from app.store import Entry, Store
from app.errors import WrongTypeError
from app.commands.zset_commands import zadd_command, zrange_command, zrem_command, zscore_command


def test_zadd_creates_new_zset_key():
    store = Store()

    result = zadd_command(store, "leaderboard", 100, "user1")

    entry = store.get_entry("leaderboard")

    assert result == 1
    assert entry is not None
    assert entry.data_type == "zset"
    assert entry.value == {"user1": 100}


def test_zadd_adds_new_member_to_existing_zset():
    store = Store()

    zadd_command(store, "leaderboard", 100, "user1")
    result = zadd_command(store, "leaderboard", 200, "user2")

    entry = store.get_entry("leaderboard")

    assert result == 1
    assert entry is not None
    assert entry.value == {
        "user1": 100,
        "user2": 200,
    }


def test_zadd_updates_existing_member_score():
    store = Store()

    zadd_command(store, "leaderboard", 100, "user1")
    result = zadd_command(store, "leaderboard", 250, "user1")

    entry = store.get_entry("leaderboard")

    assert result == 0
    assert entry is not None
    assert entry.value["user1"] == 250


def test_zadd_raises_wrong_type_for_string_key():
    store = Store()

    store.set_entry("user1", Entry("string", "Tuğba"))

    with pytest.raises(WrongTypeError):
        zadd_command(store, "user1", 100, "player1")

def test_zrange_returns_members_in_score_order():
    store = Store()

    zadd_command(store, "leaderboard", 200, "player1")
    zadd_command(store, "leaderboard", 100, "player2")
    zadd_command(store, "leaderboard", 150, "player3")

    result = zrange_command(store, "leaderboard", 0, -1)

    assert result == ["player2", "player3", "player1"]


def test_zrange_returns_members_in_inclusive_range():
    store = Store()

    zadd_command(store, "leaderboard", 100, "player1")
    zadd_command(store, "leaderboard", 200, "player2")
    zadd_command(store, "leaderboard", 300, "player3")

    result = zrange_command(store, "leaderboard", 0, 1)

    assert result == ["player1", "player2"]


def test_zrange_supports_negative_stop_index():
    store = Store()

    zadd_command(store, "leaderboard", 100, "player1")
    zadd_command(store, "leaderboard", 200, "player2")
    zadd_command(store, "leaderboard", 300, "player3")

    result = zrange_command(store, "leaderboard", 1, -1)

    assert result == ["player2", "player3"]


def test_zrange_returns_empty_list_for_missing_key():
    store = Store()

    result = zrange_command(store, "leaderboard", 0, -1)

    assert result == []

def test_zrange_sorts_equal_scores_by_member_name():
    store = Store()

    zadd_command(store, "leaderboard", 100, "zeynep")
    zadd_command(store, "leaderboard", 100, "ali")

    result = zrange_command(store, "leaderboard", 0, -1)

    assert result == ["ali", "zeynep"]

def test_zrange_raises_wrong_type_for_string_key():
    store = Store()

    store.set_entry("leaderboard", Entry("string", "test"))

    with pytest.raises(WrongTypeError):
        zrange_command(store, "leaderboard", 0, -1)

def test_zrange_supports_negative_start_index():
    store = Store()
    zadd_command(store, "leaderboard", 100, "player1")
    zadd_command(store, "leaderboard", 200, "player2")
    zadd_command(store, "leaderboard", 300, "player3")
    result = zrange_command(store, "leaderboard", -2, -1)
    assert result == ["player2", "player3"]

def test_zrem_removes_existing_member():
    store = Store()

    zadd_command(store, "leaderboard", 100, "player1")
    zadd_command(store, "leaderboard", 200, "player2")

    result = zrem_command(store, "leaderboard", "player1")

    entry = store.get_entry("leaderboard")

    assert result == 1
    assert entry is not None
    assert entry.value == {"player2": 200}


def test_zrem_returns_zero_for_missing_member():
    store = Store()

    zadd_command(store, "leaderboard", 100, "player1")

    result = zrem_command(store, "leaderboard", "player2")

    assert result == 0


def test_zrem_returns_zero_for_missing_key():
    store = Store()

    result = zrem_command(store, "leaderboard", "player1")

    assert result == 0


def test_zrem_removes_key_when_zset_becomes_empty():
    store = Store()

    zadd_command(store, "leaderboard", 100, "player1")

    result = zrem_command(store, "leaderboard", "player1")

    entry = store.get_entry("leaderboard")

    assert result == 1
    assert entry is None


def test_zrem_raises_wrong_type_for_string_key():
    store = Store()

    store.set_entry("leaderboard", Entry("string", "test"))

    with pytest.raises(WrongTypeError):
        zrem_command(store, "leaderboard", "player1")


def test_zscore_returns_score_for_existing_member():
    store = Store()

    zadd_command(store, "leaderboard", 150, "player1")

    result = zscore_command(store, "leaderboard", "player1")

    assert result == 150


def test_zscore_returns_none_for_missing_member():
    store = Store()

    zadd_command(store, "leaderboard", 150, "player1")

    result = zscore_command(store, "leaderboard", "player2")

    assert result is None


def test_zscore_returns_none_for_missing_key():
    store = Store()

    result = zscore_command(store, "leaderboard", "player1")

    assert result is None


def test_zscore_raises_wrong_type_for_string_key():
    store = Store()

    store.set_entry("leaderboard", Entry("string", "test"))

    with pytest.raises(WrongTypeError):
        zscore_command(store, "leaderboard", "player1")