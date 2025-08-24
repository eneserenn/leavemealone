 codex/create-self-hosted-email-management-app-japl8l
# LeaveMeAlone (Self-hosted Gmail Unsubscribe Tool)

## Proje Özeti

LeaveMeAlone, Gmail hesabınızda toplu şekilde abonelikten çıkmak ve istenmeyen e-postaları silmek için geliştirilmiş açık kaynak, self-hosted bir araçtır. Unroll.me ve Leave Me Alone gibi servislerin benzeri olan bu uygulama, verilerinizi üçüncü partiye aktarmadan, kendi sunucunuzda çalışır.

## Özellikler

- **Gmail API entegrasyonu (OAuth2):** Hesabınıza güvenli şekilde bağlanır.
- **Web arayüzü:** Kolayca e-posta listesini görüp işlemler yapabilirsiniz.
- **Abonelikten çıkma:** "Unsubscribe" linki olan e-postaları tespit eder, tek tıkla abonelikten çıkmanızı sağlar.
- **Toplu silme:** Abonelikten çıktığınız göndericinin tüm e-postalarını otomatik olarak siler.
- **Kolay Docker kurulumu:** Hem backend (Flask) hem frontend (React) için docker-compose ile hızlı kurulum.

---

## Kurulum Adımları

### 1. Google Cloud Projesi Oluşturma

- [Google Cloud Console](https://console.cloud.google.com/) üzerinden yeni bir proje oluşturun.
- Gmail API'yi etkinleştirin.
- OAuth2 istemci kimlik bilgilerini oluşturun ve `client_secret.json` dosyasını indirin.
- Bu dosyayı **kesinlikle kimseyle paylaşmayın** ve repoya eklemeyin! Sadece `backend` klasörüne ekleyin.

### 2. Ortam Değişkenleri

- `backend/.env` dosyasını oluşturun:
  ```env
  FLASK_SECRET_KEY=super_secret_key
  GOOGLE_CLIENT_ID=your_google_client_id
  GOOGLE_CLIENT_SECRET=your_google_client_secret
  ```
- Örnek için `.env.example` dosyasına bakabilirsiniz.

---

### 3. Docker ile Kurulum (Tavsiye Edilen Yol)

#### Gereken dosyalar:
- `docker-compose.yml`
- `backend/Dockerfile`
- `frontend/Dockerfile`
- `backend/.dockerignore`
- `frontend/.dockerignore`
- `backend/client_secret.json` (manuel eklenmeli)
- `backend/.env` (manuel eklenmeli)

#### Çalıştırmak için:
```bash
docker-compose up --build
```

- Backend Flask API: [http://localhost:5000](http://localhost:5000)
- Frontend React arayüzü: [http://localhost:3000](http://localhost:3000)

---

### 4. Manuel (Docker’sız) Kurulum

#### Backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export FLASK_SECRET_KEY=super_secret_key
export GOOGLE_CLIENT_ID=your_google_client_id
export GOOGLE_CLIENT_SECRET=your_google_client_secret
flask run
```
#### Frontend:
```bash
cd frontend
npm install
npm start
```

---

## Kullanım

1. **Gmail ile Giriş Yap:** Web arayüzünde "Gmail ile Giriş Yap" tuşuna tıklayın, OAuth2 akışını tamamlayın.
2. **Abonelikten Çıkılabilir Mailleri Gör:** Unsubscribe linki bulunan mailler listelenir.
3. **Abonelikten Çık & Toplu Sil:** Her mailin yanında "Unsubscribe ve Mailleri Sil" tuşuna basarak, hem abonelikten çıkılır hem de aynı göndericiden gelen tüm eski mailler silinir.
4. **Çıkış Yap:** Güvenlik için çıkış tuşunu kullanın.

---

## Dosya Açıklamaları

- **backend/app.py:** Flask API ve OAuth2 akışı.
- **backend/gmail_service.py:** Gmail API ile iletişim, unsubscribe ve silme işlemleri.
- **backend/requirements.txt:** Python bağımlılıkları.
- **backend/Dockerfile:** Flask backend için Docker tanımı.
- **frontend/Dockerfile:** React frontend için Docker tanımı.
- **docker-compose.yml:** Tüm sistemi tek komutla ayağa kaldırmak için.
- **.env.example:** Ortam değişkenleri örneği.
- **frontend/src/**: React arayüz kodları.
- **backend/.dockerignore & frontend/.dockerignore:** Gereksiz dosyaların Docker imajına eklenmesini engeller.

---

## Eksikler / Dikkat Edilmesi Gerekenler

- **client_secret.json** ve **.env** dosyalarını repoya eklemeyin! (Sadece kendi sunucunuzda kullanın.)
- **Rate Limit:** Google’ın API sınırlarına dikkat edin, çok fazla toplu işlemde hata alabilirsiniz.
- **Mailto Unsubscribe:** Otomatik olarak “mailto:” ile abonelikten çıkmak mümkün değil; bu tür linklerde elle işlem gerekebilir.
- **Güvenlik:** Kendi sunucunuzda çalıştırdığınız için verileriniz size ait, ancak sunucu güvenliğine dikkat edin.
- **Production için frontend:** Development modunda çalışır, prod için React’ı build edip bir Nginx sunucusuyla host edebilirsiniz.

---

## Geliştirmek İçin İpuçları

- Farklı e-posta servisleri için destek ekleyebilirsiniz.
- Kullanıcıya toplu silmeden önce onay sorulabilir.
- Daha gelişmiş filtreler ve arama özellikleri eklenebilir.
- E-posta silme işlemleri geri alınabilir şekilde tasarlanabilir.

---

## Lisans

Bu proje açık kaynaklıdır, dilediğiniz gibi kullanabilir ve geliştirebilirsiniz.

---

## Sorular ve Destek

Her türlü soru, öneri ve hata bildirimi için GitHub Issues üzerinden iletişime geçebilirsiniz.