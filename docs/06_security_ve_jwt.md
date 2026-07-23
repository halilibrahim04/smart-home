# Smart Home - Güvenlik ve Yetkilendirme (Adım 6 - Final)

Bu belge, **Kavram 47'den 51'e** kadar projenin son adımı olan güvenlik zırhını açıklar.

### 🧠 Teorik Kavram Açıklamaları
* **KAVRAM #47 (Middleware):** Türkçe meali "Arakatman" demektir. Frontend'den gelen istek (Request) Controller'a ulaşmadan önce araya giren güvenlik görevlisidir. İstek kurallara uymazsa içeri alınmaz, işlemler iptal edilir (Örn: `AuthMiddleware`).
* **KAVRAM #48 (Authentication - Kimlik Doğrulama):** "Kimsin sen?" sorusuna yanıt arayan mekanizmadır (Sisteme login olmak). TC Kimlik kartını güvenliğe göstermektir. Başarısız olursa `401 Unauthorized` döner.
* **KAVRAM #49 (Authorization - Yetkilendirme):** Kimliğini ispatladın ama "Bu içeriğe erişim hakkın (yetkin) var mı?" sorusudur. Yönetici odasına çaycının girmesini engellemektir. Başarısız olursa `403 Forbidden` döner. (Kimlik doğru, adres yanlış).
* **KAVRAM #50 (JWT - JSON Web Token):** Kullanıcı adı ve şifreyle login olunduğunda Backend'in verdiği dijital bilettir. Şifrelenmiştir ve Frontend her API isteğinde bu bileti Header üzerinden yanında taşır.
* **KAVRAM #51 (RBAC - Role Based Access Control):** Sistemin her kullanıcısına spesifik tekil yetki atamak yerine, kullanıcıları rollere bağlamaktır (Admin, Guest, Manager).

---

## 📍 Kavramların Kod İçerisindeki Haritası (Reference Map)

1. **Authentication (#48):** `auth_middleware.py` içerisinde `token` var mı yok mu kontrolüyle `401` dönerek uygulandı.
2. **Authorization (#49):** Yine `auth_middleware.py` dosyasında, kullanıcının rolüyle hedeflenen rol uyuşuyor mu diye kontrol edildi.
3. **RBAC (#51):** Yazılan Middleware kuralı `required_role` parametresi aldı. ("admin", "user" gibi roller okundu).
4. **JWT (#50):** `app/core/auth_utils.py` oluşturuldu, token formatı olan `header.payload.signature` yapısı incelendi ve simüle edildi.
5. **Middleware (#47):** Kod mimarisinde doğrudan Controller'a iş aktarmayan, ortada `process_request` adıyla duvar görevi gören `AuthMiddleware` tasarlandı.

---

## 🔍 QA (Test) Perspektifi: Burada Ne Ters Gidebilir?

**1. Privilege Escalation (Yetki Yükseltme) Zafiyeti**
* *Risk:* Sisteme normal `user` rolüyle bilet (JWT) almış bir kişi, sistemdeki "Tüm Kameraları Kapat" isimli `admin` yetkisine sahip API Endpoint'ine HTTP isteği yollarsa ne olur? Middleware yoksa istek çalışır ve sistem çöker.
* *Test Senaryosu (Security Testing):* QA, `role: user` içeren bir JWT üretir (Postman ile) ve `required_role="admin"` olan bir metoda POST isteği yollar. Sunucunun `403 Forbidden` döndüğünü doğrular (Assert). Eğer `200 OK` dönerse, çok kritik bir Güvenlik Zafiyeti (Bug) bulmuş demektir.

**2. Token Süresi (Expiration) ve Kırıklığı Testi**
* *Risk:* JWT Token'lar süresiz olarak verilirse, hacklenen veya işten ayrılan bir kullanıcının bileti sonsuza kadar geçerli kalır. Veya rastgele bir string bilet olarak yollanırsa sistem kod hatası verebilir.
* *Test Senaryosu:* Backend'e süresi geçmiş (Expired) bir token veya son harfi bilerek silinmiş hatalı (Tampered) bir JWT yollanır. Sistemin çökmeden `401 Unauthorized - Invalid Token` yanıtı verdiği doğrulanır.

---
*QA Stajyer Ödevi Başarıyla Tamamlandı.*
