/**
 * KAVRAM #45 & KAVRAM #33: Request ve Response Modellemeleri (FE/BE İletişimi)
 * Bu JS dosyası, arkada yazdığımız Python API (Örn: device_api.py) noktalarına JSON istekleri yollar,
 * Backend'den gelen DTO formatındaki sonucu ekrana DOM Manipülasyonu ile çizer.
 */

document.addEventListener("DOMContentLoaded", () => {
    // 1. JWT Simülasyonu: LocalStorage'dan auth token çekiyormuş gibi davranalım
    const authToken = "eyJhbGciOiJIUz.payload(user=U01,role=admin).X9signature";
    
    // 2. Cihazları Fetch (Get) edelim
    fetchDevicesFromBackend(authToken);

    // 3. Ekle butonuna tıklandığında POST Request hazırlayalım
    document.getElementById("add-device-btn").addEventListener("click", () => {
        simulatePostRequest(authToken);
    });
});

// GET Metodu Simülasyonu (Kavram #36, #37)
async function fetchDevicesFromBackend(token) {
    const container = document.getElementById("device-container");
    container.innerHTML = "<p style='color:#94a3b8; padding:20px;'>API'den cihaz listesi çekiliyor (HTTP GET)...</p>";

    // Backend sunucumuz aktif yayın yapmadığı için burada bir gecikme (delay) ile 
    // başarılı bir REST API yanıtı dönmüş (HTTP 200 OK) gibi davranıyoruz.
    setTimeout(() => {
        // Backend DTO dönüş formatı simülasyonu
        const apiResponse = {
            status_code: 200,
            data: [
                { id: "THERM-01", name: "Living Room Thermostat", type: "Climate", status: "online", ip: "192.168.1.50" },
                { id: "CAM-4K-02", name: "Backyard Camera", type: "Security", status: "online", ip: "192.168.1.66" },
                { id: "HEAT-X1", name: "Basement Heater", type: "Climate", status: "offline", ip: "192.168.1.18" }
            ]
        };

        renderDevices(apiResponse.data);
    }, 1200);
}

// POST Metodu Simülasyonu -> KAVRAM #37 & #44 (DTO Gönderimi)
async function simulatePostRequest(token) {
    try {
        // 1. Yeni Data Transfer Objesi Payload'ı Hazırlama
        const payloadDTO = {
            brand_name: "Yeni Güvenlik Kamerası",
            resolution: "4k"
        };
        
        console.log("-> Backend'e Giden Request (POST):", payloadDTO);
        
        // Simüle edilmiş Backend Validation kontrolü (Kavram #46)
        // Eğer çözünürlük 4k değil de "8k" olsaydı 400 Bad Request dönecekti.
        alert(`Request (POST) Gönderiliyor:\n${JSON.stringify(payloadDTO, null, 2)}\n\nAPI Yanıtı Bekleniyor...`);
        
        // 2. Başarı Senaryosu Dönüşü (HTTP 201 Created)
        setTimeout(() => {
            const apiResponse = {
                status_code: 201,
                data: {
                    device_id: "CAM-NEW",
                    brand_name: payloadDTO.brand_name,
                    status: "online"
                }
            };
            
            alert(`Backend API Yanıtı (HTTP 201 Created):\nBasariyla Olusturuldu!\nID: ${apiResponse.data.device_id}`);
            
            // Arayüzü güncelleyelim
            const grid = document.getElementById("device-container");
            const newHTML = createDeviceCardHTML({
                id: apiResponse.data.device_id,
                name: apiResponse.data.brand_name,
                type: "Security",
                status: "online",
                ip: "192.168.1.XXX"
            });
            grid.insertAdjacentHTML('afterbegin', newHTML);
            
        }, 1500);

    } catch (error) {
        // HTTP 500 veya 400 hatalarını frontend burada yakalar (Kavram 39)
        console.error("API İletişim Hatası:", error);
        alert("Bir hata oluştu: 500 Internal Server Error");
    }
}

// DOM Rendering (Arayüz Çizimi)
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
    const icon = device.type === 'Security' ? '📷' : '🌡️';

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
