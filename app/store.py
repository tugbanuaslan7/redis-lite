"""Entry ve Store: bellek içi veri saklama katmanı."""

import threading

from app.errors import WrongTypeError


class Entry:
    """Store içinde saklanan tek bir key'in verisini temsil eder."""

    def __init__(self, data_type: str, value):
        self.data_type = data_type
        self.value = value


class Store:
    """Tüm key-value verisini bellekte tutan ana veri deposu (store: dict[str, Entry])."""

    def __init__(self):
        self.entries: dict[str, Entry] = {}
        self._lock = threading.Lock()

    def get_entry(self, key: str) -> Entry | None:
        """Verilen key için Entry döner, key yoksa None döner."""
        with self._lock:
            return self.entries.get(key)

    def set_entry(self, key: str, entry: Entry) -> None:
        """Verilen key için Entry'yi kaydeder veya üzerine yazar."""
        with self._lock:
            self.entries[key] = entry

    def delete_entry(self, key: str) -> bool:
        """Key'i tipi ne olursa olsun siler. Silindiyse True, yoksa False döner."""
        with self._lock:
            if key in self.entries:
                del self.entries[key]
                return True
            return False

    def check_type(self, key: str, expected_type: str) -> None:
        """Key varsa ve tipi expected_type ile uyuşmuyorsa WrongTypeError fırlatır.
        Key yoksa sessizce döner (var olmayan key için tip hatası verilmez)."""
        with self._lock:
            entry = self.entries.get(key)
            if entry is None:
                return
            if entry.data_type != expected_type:
                raise WrongTypeError()