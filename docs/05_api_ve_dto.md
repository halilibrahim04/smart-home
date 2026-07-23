# Smart Home - API, DTO ve Request/Response Modelleri (Adım 5)

Bu belge, **Kavram 34'ten 46'ya** kadar olan web haberleşme standartlarını açıklar. Acele etmeden, adım adım sistemin dış dünyayla (*Frontend veya Mobil Cihazlarla*) nasıl konuştuğunu öğreniyoruz.

### 🧠 Teorik Kavram Açıklamaları
* **KAVRAM #34 (API):** Farklı yazılımların birbiriyle konuşmasını sağlayan köprüdür (Application Programming Interface).
* **KAVRAM #35 (REST API):** Bu köprünün belirli kurallara (Web standartlarına, JSON kullanmaya vb.) oturtulmuş, en çok tercih edilen mimarisidir.
* **KAVRAM #36 ve #37 (HTTP Metotları ve Verbs):** Frontend sistemimize geldiğinde hangi niyette olduğunu belirtmek için bir "Fiil - Verb" kullanır.
  * **GET:** Veri okumak (Listeleme).
  * **POST:** Yeni veri oluşturmak (Kayıt).
  * **PUT/PATCH:** Veri güncellemek.
  * **DELETE:** Veri silmek.
* **KAVRAM #38 ve #39 (HTTP Kodları):** Biz sunucu olarak karşı tarafa "İşlem sonucu nedir?" diye kodlar döneriz:
  * **200 (OK):** Her şey yolunda (Okuma işlemlerinde döneriz).
  * **201 (Created):** Başarıyla yeni kayıt yaratıldı (POST metodunda döneriz).
  * **400 (Bad Request):** Sen bana yanlış/eksik veri gönderdin hatası.
  * **401 (Unauthorized):** Kimliğin doğrulanamadı (Giriş yapmamışsın).
  * **404 (Not Found):** Aradığın şeyi bulamadım.
  * **500 (Internal Server Error):** Benim kodumda (Backend) bir çökme yaşandı hatasıdır.

---

## 📍 Kavramların Kod İçerisindeki Haritası (Reference Map)

1. **DTO - Data Transfer Object (#44):** Klasör yapımıza `dtos/device_dto.py` ekledik. Frontend'den gelen veriyi önce DTO nesnemize çevirdik.
2. **Validation - Doğrulama (#46):** `DeviceCreateRequestDTO` içerisindeki `validate()` fonksiyonuyla içeri giren çözünürlük (`resolution`) verisinin sadece `720p, 1080p veya 4k` olup olmadığını kontrol ettik.
3. **Request ve Response (#45):** `device_api.py` içerisinde dışarıdan bir `request` nesnesi aldık. Her şey doğruysa geriye 201 koduyla `DeviceResponseDTO` (Cevap Objesi) döndürdük.
4. **HTTP Metotları (#36, #37):** Controller içerisinde `request.get("method") == "POST"` satırıyla REST standartlarına uymayanları kapıdan çevirdik.
5. **HTTP Kodları (#38, #39):** Kod içerisinde açıkça hatalarda `400`, oluşturmada `201`, okumada `200` kodlarını dönüyoruz.

---

## 🔍 QA (Test) Perspektifi: Burada Ne Ters Gidebilir?

**1. DTO Payload Testing (Validation Hataları)**
* *Risk:* İstemci (Frontend veya Hacker), sistemi çökertmek için "resolution" alanına `4k` değil de `10000000x120` büyüklüğünde yasadışı bir string gönderebilir, veya `brand_name` alanını hiç yollamayabilir (Null).
* *Test Senaryosu:* QA Stajyeri, Postman veya test otomasyon araçlarıyla sisteme **Null alanlar, çok uzun stringler ve SQL Injection denemeleri** içeren "kasten hatalı istekler (Negative Testing)" yollamalıdır. Sistem çökmek (500 Error) yerine, zarifçe `400 Bad Request` yanıtını `errors` listesiyle birlikte vermelidir.

**2. HTTP Verb (Zafiyet) İhlalleri**
* *Risk:* Kamera oluşturmak için sadece `POST` metoduna izin vermiştik. Eğer bir geliştirici `GET` ile de cihaz silinmesine veya eklenmesine kazara izin verdiyse, sistemi tarayan herkes tesadüfen kameraları silebilir.
* *Test Senaryosu:* Yeni bir cihaz ekleme endpoint'ine kasten `GET` ve `DELETE` fiilleriyle deneme yapılır. Sistemin kesinlikle izin vermeyerek `405 Method Not Allowed` veya `404 Not Found` döndüğü Assert edilmelidir (Doğrulanmalıdır).
