# Smart Home Management System - Katmanlı Mimari (N-Tier Architecture)

Bu doküman QA Stajyerleri için sistemin iskeletini ve temel kavramlarını açıklamak amacıyla oluşturulmuştur.

---

## 📍 Kavramların Kod İçerisindeki Haritası (Reference Map)
Bu adımda istenen kavramlar, projemizin iskeletini ve dosyalarını oluştururken aşağıdaki şekilde kullanılmıştır:

* **KAVRAM #32 (Backend):** `main.py` dosyası ile arka planda çalışacak olan çekirdek uygulamanın girişi (entrypoint) oluşturulurken konsept olarak hayata geçirilmiştir.
* **KAVRAM #33 (Frontend ve Backend ilişkisi):** Backend'den tamamen bağımsız olarak `frontend/index.html` dosyası oluşturularak iki yapının birbirine geçmemesi (decoupling) pratik olarak sağlanmıştır.
* **KAVRAM #40 (Controller):** `app/controllers/` paketi oluşturularak API isteklerini karşılayacak alan rezerve edilmiştir.
* **KAVRAM #41 (Service):** İş kurallarımızın (Business Logic) yazılacağı `app/services/` paketi mimariye dahil edilmiştir.
* **KAVRAM #42 (Repository):** Veritabanı konuşmaları için ayrılan `app/repositories/` paketi yaratılmıştır.
* **KAVRAM #43 (Entity):** Cihaz/Sensör gibi tablolarımızın nesnesel formda bulunacağı `app/entities/` paketi oluşturulmuştur.

---

## 🔍 QA (Test) Perspektifi: Burada Ne Ters Gidebilir?

Test stratejisini kurgularken sadece çalışıp çalışmadığına değil, **mimarinin ihlal edilip edilmediğine** de bakmalıyız.

1. **Katman İhlali (Layer Violation):** 
   * *Risk:* Geliştirici, işlemler hızlı bitsin diye doğrudan Controller içerisinden veritabanına erişebilir (Service ve Repository'i atlayarak).
   * *Sonuç:* Sistem gelecekte test edilemez (Unit test yazılamaz) hale gelir. 
   * *Nasıl Test Edilir?* Kod incelemesi (Code Review) adımlarında veya statik kod analizi araçlarıyla (örn: SonarQube) bu ihlaller aranır.
2. **Sıkı Bağımlılık (Tight Coupling):**
   * *Risk:* Backend (örneğin Service katmanı), içeriğinde doğrudan Frontend'in beklediği HTML formatında bir cevap dönerse.
   * *Sonuç:* Yarın bir Mobil Uygulama eklenmek istendiğinde HTML cevabı mobil çalıştıramayacağı için sistem çuvallar.
   * *Nasıl Test Edilir?* Endpoint testlerinde (API Tests) her zaman sadece JSON (ya da XML) gibi evrensel veri formatlarının döndüğü Assert edilmelidir.
