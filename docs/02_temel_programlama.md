# Smart Home - Temel Programlama ve QA

Bu belge, "Temel Programlama Kavramlarının (Değişkenler, Veri Tipleri, Döngüler, Koşullar vb.)" yazılım test, otomasyon (QA) ve güvenlik (Security) süreçlerindeki etkilerini inceler.

---

## 📍 Kavramların Kod İçerisindeki Haritası (Reference Map)
Aşağıda belirtilen kavramların *(Kavram 1-11 arası)* hepsi uygulamalı olarak **`app/utils/device_validator.py`** isimli kod dosyamızda kullanılmıştır:

1. **Değişken (Variable):** `device_name, maxTemperature, is_active, port_number` gibi bir veriyi tutan isimlendirmeler, değişken mantığıyla kodlandı.
2. **Veri Tipi (Data Type):** Python değişkenlere atanan değerden data tiplerini otomatik aldı. QA gereği veri tipine sadık kalındı.
3. **String, Integer, Float, Boolean, Array (List):**
   * String => `"Akıllı Termostat"`
   * Float => `35.5`
   * Boolean => `True`, `False`
   * Integer => `8080`
   * Array => `[22.5, 23.0, 36.1, 21.0]` (Gelen veri yığınının tutulması için)
4. **İsimlendirme Kuralları (camelCase vs snake_case):** `maxTemperature` kelimesinde *camelCase*, `device_name` kelimesinde *snake_case* standardı uygulandı.
5. **Fonksiyon (Function):** Sıcaklık kontrolü için bağımsız bir alt program olarak `check_device_temperatures(...)` fonksiyonu tanımlandı.
6. **Metot (Method - Sınıfa ait fonksiyon):** İleride kullanılacak `DummyDevice` class'ı (sınıf) içerisinde, cihaza ait bir eylem (behavior) olan `turn_on` metodu tanımlandı. (Sınıf dışında olana fonksiyon, sınıf içinde olana metot denir).
7. **Parameter vs Argument:** 
   * **Parameter (Parametre):** Fonksiyon tasarlanırken içeride kullanılsın diye beklenen `temperature_list` ve `limit_temp` verileridir.
   * **Argument (Argüman):** Fonksiyon en sonda aktif bir şekilde çağrılırken (`call` edilirken) gerçeğe dönüşmüş olan ve yollanan `sensor_logs` ve `maxTemperature` verileridir.
8. **Return:** Fonksiyon içinde üretilen hata uyarıları ve güvenli midir kararı (`warning_count, is_safe`), dış dünyaya `return` anahtar kelimesiyle döndürüldü.
9. **Conditionals (Koşullar):** `if current_temp > limit_temp:` kontrol bloğuyla programın bir koşula (condition) göre farklı aksiyon alması sağlandı.
10. **Loop (Döngüler):** Sıcaklık listesinin içindeki (array) tüm değerleri tek tek gezmek için bir döngü işlemi yaratıldı.
11. **Control Structures:** İşi organize etmek için hem iterasyon bazlı Control Structure olan `for` hem de şart bazlı olan `if / else` birlikte kullanıldı.

---

## 🔍 QA (Test) Perspektifi: Burada Ne Ters Gidebilir?

**1. Veri Tipi Hataları (Data Type Mismatch)**
* *Risk:* Python dinamik tiplidir (dynamically typed). Frontend ekibi, sıcaklık limiti olan `limit_temp` verisini Integer/Float (örn: `35.5`) yerine String (örn: `"35.5"`) gönderirse, Python `> ` (büyüktür) karşılaştırması yapmaya çalışırken sistem çalışmayı durdurur (Crash Error).
* *Test Senaryosu (Type Check):* QA test yazarken API'a özel olarak bozucu, örneğin `{"limit_temp": "bozuk_veri"}` şeklinde (String data tipinde) istek atıp (Negative Test) API'in çökmeden uygun Hata Kodunu dönmesini test etmelidir.

**2. Sınır Değer İhlalleri (Boundary Value Analysis)**
* *Risk:* Kod içerisindeki koşul yapısında `if current_temp > limit_temp:` yazıldı. Ya sıcaklık tam olarak limit değere eşitse? Geliştirici eşittir (`>=`) durumunu unutmuş olabilir.
* *Test Senaryosu (BVA):* QA, sınır değer analizi standartlarına göre `limit_temp` verisinin **1 birim altını**, **tam kendisini** ve **1 birim üstünü** teste sokar. Programın eşik değerlerde doğru karar verdiğini doğrular.

**3. Sonsuz Döngüler (Infinite Loop)**
* *Risk:* İleride kullanılacak `while` döngüsünde koşul bitmezse sistem yavaşlar ve kilitlenir (DoS - Denial of Service).
* *Test Senaryosu (Load/Performance):* Parametre olan liste (Array), bilerek yüzbinlerce eleman alacak şekilde doldurulur ve döngünün süre/kalite (Performance Test) limiti hesaplanır.
