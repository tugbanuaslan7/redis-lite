# Redis Lite v1


## Şu ana kadar yapılanlar

- Entry modeli ve in-memory Store yazıldı
- String komutları: SET, GET, DEL, INCR tamamlandı
- Store'a thread-safety eklendi (aynı anda birden fazla isteğin veri bütünlüğünü bozmaması için)

## Kurulum

Python 3.12+ ile çalışıyor (ben 3.14 ile denedim).

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e .
```

## Testleri çalıştırma

```powershell
pytest -v
```

Şu an 13 test var: string komutları için mutlu yol, hata yolu ve
eşzamanlı erişim senaryoları.

## Nasıl çalışıyor?

Her key'in bir tipi var (string / hash / zset). Bir key belli bir tipte
oluşturulduktan sonra başka tipte bir komutla kullanılmaya çalışılırsa
hata dönüyor (`WRONG_TYPE`). 

Komutlar (`app/commands/` altındaki dosyalar) FastAPI'den bağımsız yazıldı,
yani API katmanı olmadan da test edilebiliyorlar. Şu an da bu şekilde test
ediliyor.

Var olmayan bir key için hata fırlatılmıyor, komuta göre bir
"bulunamadı" cevabı dönüyor (GET için None, DEL için 0, HGETALL için {} gibi).

Store, aynı anda gelebilecek birden fazla isteğe karşı bir kilit (`Lock`)
ile korunuyor, yani iki istek aynı anda aynı key'e dokunsa bile veri
bozulmuyor. Bu, aynı key'e eşzamanlı INCR çağrılarında da test edildi
(100 thread aynı sayaç key'ine INCR çağırıyor, sonuç kayıpsız 100 çıkıyor).

## Bilinen kısıtlar

- Veri sadece bellekte tutuluyor, kalıcılık yok
- Cluster / replication yok