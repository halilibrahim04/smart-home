/**
 * Frontend SPA (Single Page Application) Router & Modal Logic
 */

document.addEventListener("DOMContentLoaded", () => {

    // 1. KAVRAM #48 & #50: Kimlik Doğrulama (JWT Token var mı?)
    const authToken = localStorage.getItem('smarthome_token');
    const userRole = localStorage.getItem('smarthome_role');

    // Eğer token yoksa güvenlik görevlisi (Middleware) kapıdan çevirir. Login ekranına atar.
    if (!authToken || !userRole) {
        window.location.href = 'login.html';
        return;
    }

    // 2. KAVRAM #49 & #51: Authorization (Arayüz Yetki Kısıtlamaları)
    applyRbacRulesToUI(userRole);

    // 3. Çıkış Yapma Olayı (Logout)
    document.getElementById('logout-btn').addEventListener('click', () => {
        localStorage.removeItem('smarthome_token');
        localStorage.removeItem('smarthome_role');
        window.location.href = 'login.html';
    });

    // İlk Yüklemede Cihazları Çek
    fetchDevicesFromBackend(authToken);

    // 3. SPA Navigasyon Mantığı (Menü Değişimi)
    const navItems = document.querySelectorAll('.nav-item');
    const viewSections = document.querySelectorAll('.view-section');

    navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();

            // Tüm aktif sınıfları temizle
            navItems.forEach(n => n.classList.remove('active'));
            viewSections.forEach(v => {
                v.classList.remove('active');
                v.classList.add('hidden');
            });

            // Tıklananı aktif et
            item.classList.add('active');
            const targetId = item.getAttribute('data-target');
            const targetView = document.getElementById(targetId);

            targetView.classList.remove('hidden');
            setTimeout(() => targetView.classList.add('active'), 10); // Animasyon tetikleyici
        });
    });

    // 4. Modal (Açılır Pencere) Mantığı
    const modal = document.getElementById('device-modal');
    const addDeviceBtn = document.getElementById('add-device-btn');
    const closeModalBtn = document.getElementById('close-modal');
    const newDeviceForm = document.getElementById('new-device-form');

    addDeviceBtn.addEventListener('click', () => {
        modal.classList.remove('hidden');
    });

    closeModalBtn.addEventListener('click', () => {
        modal.classList.add('hidden');
    });

    // Modal Dışı Boşluğa tıklanırsa kapat
    window.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.classList.add('hidden');
        }
    });

    // 5. Dinamik Form Gönderimi (POST KAVRAM #37 & #44 DTO)
    newDeviceForm.addEventListener('submit', (e) => {
        e.preventDefault(); // Sayfanın yenilenmesini engeller

        // Kullanıcının formdan girdiği verileri alıyoruz
        const payloadDTO = {
            brand_name: document.getElementById('input-dev-name').value,
            type: document.getElementById('input-dev-type').value,
            resolution: document.getElementById('input-dev-quality').value
        };

        // Backend'e yollanıyor simülasyonu
        simulateDynamicPostRequest(authToken, payloadDTO);

        // Formu temizle ve Kapat
        newDeviceForm.reset();
        modal.classList.add('hidden');
    });

});

// --- RBAC YETKİLENDİRME (KULLANICI ARAYÜZÜ KISITLAMALARI) ---
function applyRbacRulesToUI(role) {
    const roleBadge = document.getElementById('role-badge');
    const avatarImg = document.getElementById('avatar-img');

    if (role === 'admin') {
        roleBadge.innerText = 'Yetki: YÖNETİCİ';
        roleBadge.className = 'user-role badge-admin';
        avatarImg.src = "https://ui-avatars.com/api/?name=Admin&background=10b981&color=fff";
    } else if (role === 'user') {
        roleBadge.innerText = 'Yetki: STANDART ÜYE';
        roleBadge.className = 'user-role badge-user';
        avatarImg.src = "https://ui-avatars.com/api/?name=User&background=38bdf8&color=fff";

        // STANDART ÜYE İSE KRİTİK İŞLEMLERİ (GÖRSEL OLARAK) YASAKLA
        // Cihaz ekleme butonunu gizle
        document.getElementById('add-device-btn').style.display = 'none';

        // Konfigürasyon ve Güvenlik sekmelerine erişimi sol menüden sakla
        document.querySelector('.nav-item[data-target="view-config"]').style.display = 'none';
        document.querySelector('.nav-item[data-target="view-security"]').style.display = 'none';
    }
}

// --- API SİMÜLASYONLARI ---

async function fetchDevicesFromBackend(token) {
    const container = document.getElementById("device-container");
    container.innerHTML = "<p style='color:#94a3b8; padding:20px;'>API'den cihaz listesi çekiliyor (HTTP GET)...</p>";

    setTimeout(() => {
        // Backend DTO dönüş formatı simülasyonu
        const apiResponse = {
            status_code: 200,
            data: [
                { id: "THERM-01", name: "Living Room Thermostat", type: "Climate", status: "online", ip: "192.168.1.50" },
                { id: "CAM-4K-02", name: "Backyard Security", type: "Security", status: "online", ip: "192.168.1.66" },
                { id: "HEAT-X1", name: "Basement Heater", type: "Climate", status: "offline", ip: "192.168.1.18" }
            ]
        };

        renderDevices(apiResponse.data);
    }, 800);
}

async function simulateDynamicPostRequest(token, payloadDTO) {
    console.log("-> Backend'e Giden Request (POST):", payloadDTO);
    alert(`Backend'e Giden Request (Dinamik Payload):\n${JSON.stringify(payloadDTO, null, 2)}`);

    // Yüklenme aşaması simülasyonu
    setTimeout(() => {
        // Başarı (201 Created)
        const apiResponse = {
            status_code: 201,
            data: {
                device_id: "DEV-" + Math.floor(Math.random() * 9000 + 1000), // Rastgele ID,
                brand_name: payloadDTO.brand_name,
                type: payloadDTO.type,
                status: "online"
            }
        };

        // Yeni Cihazı Listeye Ekle
        const grid = document.getElementById("device-container");
        const newHTML = createDeviceCardHTML({
            id: apiResponse.data.device_id,
            name: apiResponse.data.brand_name,
            type: apiResponse.data.type,
            status: "online",
            ip: "192.168.1.100" // Otomatik IP varsayımı
        });

        grid.insertAdjacentHTML('afterbegin', newHTML);

    }, 1200);
}

// --- DOM RENDER YARDIMCILARI ---

function renderDevices(devices) {
    const container = document.getElementById("device-container");
    container.innerHTML = "";
    devices.forEach(device => {
        container.innerHTML += createDeviceCardHTML(device);
    });
}

function createDeviceCardHTML(device) {
    const isOnline = device.status === 'online';
    const statusText = isOnline ? 'Bağlı (Connected)' : 'Cevap Yok (Disconnected)';
    const statusClass = isOnline ? 'badge-connected' : 'badge-disconnected';

    let icon = '⚙️';
    if (device.type === 'Security') icon = '📷';
    if (device.type === 'Climate') icon = '🌡️';
    if (device.type === 'Lighting') icon = '💡';

    return `
        <div class="device-card">
            <div class="card-header">
                <span class="device-type">${device.type} DEVICE</span>
                <div class="device-icon">${icon}</div>
            </div>
            <h3 class="device-title">${device.name}</h3>
            <div class="device-details">
                <div class="detail-row">
                    <span>ID:</span>
                    <span>${device.id}</span>
                </div>
                <div class="detail-row">
                    <span>Ağ Adresi:</span>
                    <span>${device.ip}</span>
                </div>
                <div class="detail-row" style="margin-top: 10px; font-weight: 500;">
                    <span>Durum:</span>
                    <span class="${statusClass}">● ${statusText}</span>
                </div>
            </div>
        </div>
    `;
}
