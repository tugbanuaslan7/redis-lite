# Redis Lite v1


## Şu ana kadar yapılanlar

- Entry modeli ve in-memory Store yazıldı
- String komutları: SET, GET, DEL tamamlandı
- Hash komutları: HSET, HGET, HDEL, HGETALL tamamlandı
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

Şu an 23 test var: string komutları için 8 test (mutlu yol, hata yolu,
eşzamanlı erişim dahil), hash komutları için 15 test (mutlu yol, hata yolu,
yanlış tip senaryoları dahil).

## Nasıl çalışıyor?

Her key'in bir tipi var (string / hash / zset). Bir key belli bir tipte
oluşturulduktan sonra başka tipte bir komutla kullanılmaya çalışılırsa
hata dönüyor (`WRONG_TYPE`). Örneğin hash olarak oluşturulmuş bir key'e
`GET` ile ulaşılmaya çalışılırsa hata alınır. Key'in tipini değiştirmek
için önce key'in silinmesi gerekiyor.

Hash komutlarında bir key altında birden fazla field-value çifti
tutulabiliyor. `HSET` yeni bir field ekliyor veya mevcut field'ın değerini
güncelliyor. `HGET` belirli bir field'ın değerini getiriyor, `HDEL` field'ı
siliyor ve hash boş kaldığında key'i de siliyor. `HGETALL` ise hash içindeki
tüm field-value çiftlerini döndürüyor.

Komutlar (`app/commands/` altındaki dosyalar) FastAPI'den bağımsız yazıldı,
yani API katmanı olmadan da test edilebiliyorlar. Şu an da bu şekilde test
ediliyor.

Var olmayan bir key için hata fırlatılmıyor, komuta göre bir
"bulunamadı" cevabı dönüyor. Örneğin `GET` ve `HGET` için `None`,
`DEL` ve `HDEL` için `0`, `HGETALL` için ise boş bir dictionary (`{}`)
dönüyor.

## Bilinen kısıtlar

- Veri sadece bellekte tutuluyor, kalıcılık yok
- Cluster / replication yok