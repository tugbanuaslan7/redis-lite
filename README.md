# Redis Lite v1


## Şu ana kadar yapılanlar

- Entry modeli ve in-memory Store yazıldı
- String komutları: SET, GET, DEL tamamlandı
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

Şu an 8 test var: string komutları için mutlu yol + hata yolu senaryoları,
bir de eşzamanlı erişimi kontrol eden bir test.

## Nasıl çalışıyor?

Her key'in bir tipi var (string / hash / zset). Bir key belli bir tipte
oluşturulduktan sonra başka tipte bir komutla kullanılmaya çalışılırsa
hata dönüyor (`WRONG_TYPE`). Mesela hash olarak set edilmiş bir key'e
`GET` ile ulaşılmay çalışılırsa hata alınır, tipini değiştirmek için önce
key'i silmek gerekiyor.

Komutlar (`app/commands/` altındaki dosyalar) FastAPI'den bağımsız yazıldı,
yani API katmanı olmadan da test edilebiliyorlar. Şu an da bu şekilde test
ediliyor.

Var olmayan bir key için hata fırlatılmıyor, komuta göre bir
"bulunamadı" cevabı dönüyor (GET için None, DEL için 0 gibi).

## Bilinen kısıtlar

- Veri sadece bellekte tutuluyor, kalıcılık yok
- Cluster / replication yok