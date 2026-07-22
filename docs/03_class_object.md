# Smart Home - Class ve Object Kavramları (Adım 3)

Bu belge, OOP'nin (Nesne Yönelimli Programlama) temel yapıtaşları olan Kavram 12'den Kavram 21'e kadar olan teorik bilgileri ve projedeki kullanım noktalarını açıklar.

### 🧠 Teorik Kavramlar ve Cevapları
* **KAVRAM #15 (Class ile Object arasındaki fark):** Class (Sınıf) mimari bir şablon veya bina planıdır. İçinde oturulamaz. Object (Nesne) ise o şablona bakılarak inşa edilmiş gerçek, fiziki bir binadır.
* **KAVRAM #21 (Class Neden Kullanılır?):** Tekrarı azaltmak (Reusability) ve gerçek dünyadaki nesneleri kod ile modellemek için kullanılır. Modularity (Modülerlik) sağlayarak projeyi büyütebilmemize imkan tanır. 100 tane cihaz üreteceksek, bunu 100 ayrı değişken yazarak değil, tek bir `Device` şablonu (Class) ile yaparız.

---

## 📍 Kavramların Kod İçerisindeki Haritası (Reference Map)
Bu kavramlar "temiz kod - clean code" prensibiyle ağırlıklı olarak `app/entities/device.py` ve kullanımı için de `app/services/device_manager.py` altında gerçeklenmiştir:

12. **Class (Sınıf):** `device.py` içerisindeki `class Device:` tanımıdır (Şablondur).
13. **Object (Nesne):** Sınıfın gerçek dünyadaki halidir. Çıktı olarak oluşan verilere nesne denir.
14. **Instance (Örnek):** Object yaratma eylemine (örneklem alma) instance denir. `device_manager.py` içerisinde `thermostat = Device(...)` yapılarak `Device` sınıfından bir `thermostat` instance'ı türetilmiştir. (Object ve Instance genelde eş anlamlı kullanılır).
16. **Property (Özellik):** Cihazın durumunu belirten verilerdir. `name`, `is_connected` gibi değişkenler bu sınıfın property'sidir.
17. **Method (Davranış):** Cihazın işlevleridir. `connect()` ve `disconnect()` metotları cihazın davranışı olarak tanımlanmıştır. Sınıfa ait fonksiyonlara denir.
18. **Constructor (Yapıcı Metot):** Bir sınıf çalıştırıldığında (Instance yaratıldığında) ilk ateşlenen ve nesneyi başlangıç ayarlarına getiren özel metottur. Python'daki karşılığı `def __init__(self, ...):` kısmıdır.
19. **$this / self (Kullanımı):** PHP veya Java'da `$this` (veya `this`), Python'da ise `self` kelimesidir. Anlamı: "Benim içimdeki...", "Bana ait olan..." demektir. Cihazın kendi kendine ulaştığını gösterir (`self.name` = Benim ismim).
20. **Access Modifiers (public, private, protected):** Yetki seviyeleridir. Python'da kural olarak alt çizgiyle tanımlanırlar:
   * **Public (Herkes erişebilir):** `self.name` (Başı boş). Manager içinden direkt `print(thermostat.name)` diyerek rahatça okundu.
   * **Protected (Miras alanlar erişebilir):** `self._type` (Tek alt çizgi).
   * **Private (Sadece sınıfın içi erişebilir):** `self.__ip_address` (Çift alt çizgi). (Bu değişkene Manager gibi dış sınıflardan direkt ulaşılamaz, ulaşırsak hata verir).

---

## 🔍 QA (Test) Perspektifi: Burada Ne Ters Gidebilir?

**1. Sınıf Verisinin Dışarıdan Bozulması (Encapsulation / Access Modifier İhlali)**
* *Risk:* Cihazın özel ağ adresi (`__ip_address`), eğer "Public" olarak yani `ip_address` şeklinde tanımlansaydı; başka bir Junior Developer rastgele `thermostat.ip_address = "0.0.0.0"` yazıp tüm cihaz bağlantılarını ve donanımı sonsuza dek kaybetmemize (network blocking) yol açabilirdi.
* *Test Senaryosu:* QA mühendisi, Unit (Birim) testi yazarken sınıftaki Private alanlara dışarıdan müdahale etmeye (Örn: `thermostat.__ip_address = '1.1.1.1'`) çalışmalıdır. Programın koruma kalkanının (Python'da *AttributeError* hatası) çalıştığını test edip Assert etmelidir (Doğrulamalıdır).

**2. State (Durum) Testlerinin Atlanması**
* *Risk:* Bir metot (Örn: `connect()`) çalıştığında cihaz state'i (`is_connected`) değişir. Bu durum diğer metotlarla koordineli değilse cihaz aynı anda hem kapalı hem de veri üreten bir duruma düşerek sistemi log (çöp) yağmuruna tutabilir.
* *Test Senaryosu (State-Transition Testing):* QA, `connect()` metodu çağrıldıktan *sonra* `is_connected == True` değerini, ardından `disconnect()` çağrıldıktan *sonra* `is_connected == False` değerine geri döndüğünü Lifecycle (Yaşam Döngüsü) testleriyle doğrulamalıdır. Sadece geri dönen "connected" string metni test edilirse, arka plandaki arıza maskelenmiş olur.
