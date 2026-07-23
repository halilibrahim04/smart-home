# Smart Home - OOP Kavramları (Adım 4)

Bu belge, **Kavram 22 ile Kavram 31** arasındaki Nesne Yönelimli Programlama (OOP) ilkelerinin projemizdeki karşılığını ve kalite/test analizini barındırır.

### 🧠 Teorik Kavram Açıklamaları
* **KAVRAM #22 (OOP Mantığı):** Yazılımı yukarıdan aşağı kodlar yığını gibi (Prosedürel) değil, birbirleriyle etkileşimli nesneler/canlılar sistemi olarak tasarlama felsefesidir.
* **KAVRAM #29 (Interface ve Abstract Class Farkı):** Abstract Class (Soyut Sınıf), ortak bir kökenden (babadan) gelen nesneler için kalıtım sağlar, içinde hem dolu (çalışan) hem de boş metotlar barındırabilir. Interface ise akrabalık bağına bakmaz, ortak yetenekleri (örn: WiFi bağlanabilme) sözleşme olarak zorunlu kılar, içi daima boş metotlardan oluşur.
* **KAVRAM #31 (OOP Avantajları):** Modülerlik sağlar, test etmesi ve bakımı kolaydır. Bağımlılık Enjeksiyonu ve Polymorphism sayesinde kod değiştirmeden yetenekleri genleşebilir.

---

## 📍 Kavramların Kod İçerisindeki Haritası (Reference Map)
1. **Encapsulation / Kapsülleme (#23):** `base_device.py` içerisindeki `self.__brand_name` değişkeni dış erişime kapatılmış (Private yapılmış) ve ona okuma izni veren `@property def brand_name(self):` ile güvenli şekilde dış dünyaya açılmıştır. (Get/Set mantığı).
2. **Inheritance / Kalıtım (#24):** `smart_camera.py` dosyasındaki `class SmartCamera(BaseDevice...)` satırı sayesinde, kamera sınıfı ana cihaz şablonunun (BaseDevice) tüm özelliklerini miras (kalıtım) almıştır.
3. **Polymorphism / Çok Biçimlilik (#25):** `base_device.py` içindeki `turn_on()` metodu kamerada Override edilmiş (Kameraya özel yeniden şekillendirilmiş) ve her cihaz tipinin (`SmartCamera`, `SmartHeater`) kendi karakterine göre `turn_on` olması sağlanmıştır.
4. **Abstraction / Soyutlama (#26):** Program karmaşık metot detaylarını gizlemek için tasarlandı. Manager sınıfı (`camera_manager.py`), kameranın network'e *nasıl* tam olarak bağlandığıyla ilgilenmez, sadece `connect_to_network()` komutunu çağırır.
5. **Interface - Arayüz (#27):** `interfaces.py` içindeki `INetworkConnectable` yapısı bir Interface'dir. Tüm ağa bağlanan cihazların (bulaşık makinesi olsa bile) o şablonu uygulamasını zorunlu kılar.
6. **Abstract Class - Soyut Sınıf (#28):** `base_device.py` içindeki `BaseDevice(ABC)` sınıfımızdır. Bu sınıftan doğrudan cihaz üretilemez, sadece diğer cihazlara "ata/kalıtım" olması için vardır.
7. **Dependency Injection - Bağımlılık Enjeksiyonu (#30):** `camera_manager.py` içerisinde Manager kendi başına log kaydı tutmaz. Dışarıdan kendisine `__init__(self, logger: LoggerService)` parametresiyle Logger sınıfı **enjekte edilir**.

---

## 🔍 QA (Test) Perspektifi: Burada Ne Ters Gidebilir?

**1. Dependency Injection ve "Mocking" Gücü**
* *Risk:* Manager kendi içinde (DI kullanmadan) `logger = LoggerService()` diye manuel Logger üretiyor olsaydı, gerçek veritabanı veya dosyaya bağlı olan log sistemi test ortamında sunucuya sızacak veya hata verecekti.
* *Test Senaryosu (Mock Testing):* Tasarladığımız `Dependency Injection` sayesinde QA Stajyeri, Manager'ı teste sokarken ona gerçek Logger yerine `FakeLogger` (sahte test logger'ı) inject edebilir. Böylece asıl sistemi yormadan, sadece fonksiyonun akışını %100 izole test edebilir. Unit Testing'in en büyük dostu DI konseptidir.

**2. Polymorphism (Sözleşme) Hataları**
* *Risk:* Geliştirici, BaseDevice içerisindeki `turn_on()` metodunu `string` dönecek şekilde ayarlamışken; Kamera gibi Sub-Class'larda kalıtımı (Override'ı) uygularken kazara `boolean` bir değer döndürebilir.
* *Test Senaryosu:* Contract Testing (Sözleşme Testi) uygulanır. Bütün `BaseDevice` alt türevlerinin aynı Data Type Return (aynı tip değer dönüşü) sağladığından emin olunmalı, Type Hint (`-> str`) zorunlulukları CI/CD'de Linter aracılığıyla statik zorlamadan geçirilmelidir.
