<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const activeView = ref('dashboard') // SPA State Yönetimi
const userRole = ref('')
const devices = ref([])
const isModalOpen = ref(false)

const newDevName = ref('')
const newDevType = ref('Security')

onMounted(() => {
  const token = localStorage.getItem('smarthome_token')
  if(!token) {
    return router.push('/login')
  }

  // JWT Decode işlemi - Frontend Yetki Ayarı
  try {
    const payloadBase64Url = token.split('.')[1]
    const payloadBase64 = payloadBase64Url.replace(/-/g, '+').replace(/_/g, '/')
    const decoded = JSON.parse(atob(payloadBase64))
    userRole.value = decoded.role
    
    // Veritabanı cihazları simülasyonu
    fetchDevices()
  } catch(e) {
    localStorage.removeItem('smarthome_token')
    router.push('/login')
  }
})

const fetchDevices = () => {
    // Gerçek dünyada burada $fetch("http://localhost:8000/api/devices") olmalıdır
    setTimeout(() => {
        devices.value = [
            { id: "THERM-01", name: "Living Room Thermostat", type: "Climate", status: "online", ip: "192.168.1.50" },
            { id: "CAM-4K-02", name: "Backyard Security", type: "Security", status: "online", ip: "192.168.1.66" },
            { id: "HEAT-X1", name: "Basement Heater", type: "Climate", status: "offline", ip: "192.168.1.18" }
        ]
    }, 800)
}

const addDevice = () => {
  // Modal Submit Olayı
  const newDev = {
    id: "DEV-" + Math.floor(Math.random() * 9000 + 1000),
    name: newDevName.value,
    type: newDevType.value,
    status: "online",
    ip: "192.168.1.100"
  }
  devices.value.unshift(newDev) // State'i Güncelle, UI otomatik tetiklenir!
  
  isModalOpen.value = false
  newDevName.value = ''
}

const logout = () => {
  localStorage.removeItem('smarthome_token')
  router.push('/login')
}
</script>

<template>
  <div>
    <div class="glow-orb orb-1"></div>
    <div class="glow-orb orb-2"></div>
    
    <div v-if="userRole" class="layout-container">
      
      <!-- SIDEBAR -->
      <aside class="sidebar glass-panel">
        <div class="logo">
            <div class="logo-icon"></div>
            <h2>SmartHome</h2>
        </div>
        
        <nav class="nav-menu">
            <a href="#" :class="['nav-item', activeView === 'dashboard' ? 'active' : '']" @click.prevent="activeView = 'dashboard'">
                <span>Ağ Cihazları</span>
            </a>
            <!-- VUE V-IF KAVRAMI: State değiştiği an bu tuş saniyesinde kaybolur (RBAC) -->
            <a href="#" v-if="userRole === 'admin'" :class="['nav-item', activeView === 'config' ? 'active' : '']" @click.prevent="activeView = 'config'">
                <span>Sistem Konfigürasyonu</span>
            </a>
            <a href="#" v-if="userRole === 'admin'" :class="['nav-item', activeView === 'security' ? 'active' : '']" @click.prevent="activeView = 'security'">
                <span>Güvenlik İhlalleri</span>
            </a>
        </nav>

        <div class="auth-status">
            <div style="display: flex; gap: 12px; flex-grow: 1;">
                <div class="user-avatar">
                   <img :src="userRole === 'admin' ? 'https://ui-avatars.com/api/?name=Admin&background=10b981&color=fff' : 'https://ui-avatars.com/api/?name=User&background=38bdf8&color=fff'">
                </div>
                <div class="user-info">
                    <span class="user-name">Giriş Yapıldı</span>
                    <span :class="['user-role', userRole === 'admin' ? 'badge-admin' : 'badge-user']">
                       Yetki: {{ userRole === 'admin' ? 'YÖNETİCİ' : 'STANDART ÜYE' }}
                    </span>
                </div>
            </div>
            <button @click="logout" title="Çıkış Yap" class="btn-icon" style="padding: 10px;">🚪</button>
        </div>
      </aside>

      <!-- MAIN CONTENT -->
      <main class="main-content">
          <!-- View 1: Dashboard -->
          <div v-if="activeView === 'dashboard'" class="view-section active">
              <header class="top-header glass-panel">
                  <div class="header-search">
                      <h1>Cihaz Ağı Yönetimi</h1>
                      <p>Sistem Nuxt Mimarisi İle Yönetilmektedir. (Vue3 & CSR)</p>
                  </div>
                  <!-- Admin değilse Cihaz Ekle Butonunu Sil (Vue v-if direktifi) -->
                  <button v-if="userRole === 'admin'" class="btn btn-primary" @click="isModalOpen = true">
                      + Cihaz Ekle (POST)
                  </button>
              </header>
  
              <section class="device-grid">
                  <div v-if="devices.length === 0" style="padding:20px; color:#94a3b8">Kayıtlı cihaz yükleniyor...</div>
                  
                  <div v-for="device in devices" :key="device.id" class="device-card">
                      <div class="card-header">
                          <span class="device-type">{{device.type}} DEVICE</span>
                          <div class="device-icon">{{ device.type === 'Security' ? '📷' : device.type === 'Climate' ? '🌡️' : '💡' }}</div>
                      </div>
                      <h3 class="device-title">{{device.name}}</h3>
                      <div class="device-details">
                          <div class="detail-row">
                              <span>ID:</span><span>{{device.id}}</span>
                          </div>
                          <div class="detail-row">
                              <span>Ağ Adresi:</span><span>{{device.ip}}</span>
                          </div>
                          <div class="detail-row" style="margin-top: 10px; font-weight: 500;">
                              <span>Durum:</span>
                              <span :class="device.status === 'online' ? 'badge-connected' : 'badge-disconnected'">
                                  ● {{ device.status === 'online' ? 'Bağlı (Connected)' : 'Cevap Yok' }}
                              </span>
                          </div>
                      </div>
                  </div>
              </section>
          </div>

          <!-- View 2: Konfigürasyon -->
          <div v-if="activeView === 'config' && userRole === 'admin'" class="view-section active">
              <header class="top-header glass-panel" style="margin-bottom: 24px;">
                  <div class="header-search">
                      <h1>Sistem ve Mekan Konfigürasyonu</h1>
                      <p>Lokasyonlar (HOMES) tablosu ve genel ortam ayarları</p>
                  </div>
              </header>

              <div class="device-grid">
                  <!-- Mekanlar (Homes) Kartı -->
                  <div class="device-card">
                      <h3 style="margin-bottom:10px;">🏠 Kayıtlı Mekanlar (Homes)</h3>
                      <p style="color:#94a3b8; font-size:0.85rem; margin-bottom:15px;">Kayıtlı fiziksel lokasyonlarınızı yönetin.</p>
                      
                      <div style="background: rgba(0,0,0,0.3); padding: 12px; border-radius: 8px; margin-bottom: 10px; border: 1px solid var(--glass-border);">
                          <strong>Merkez Ofis</strong> <br> 
                          <span style="font-size:0.8rem; color:#10b981;">İstanbul / TR</span>
                      </div>
                       <div style="background: rgba(0,0,0,0.3); padding: 12px; border-radius: 8px; margin-bottom: 15px; border: 1px solid var(--glass-border);">
                          <strong>Datacenter Oda 1</strong> <br> 
                          <span style="font-size:0.8rem; color:#38bdf8;">Ankara / TR</span>
                      </div>

                      <button class="btn btn-primary" style="width:100%; font-size:0.85rem; padding: 10px;">+ Yeni Ev/Mekan Ekle</button>
                  </div>
                  
                  <!-- Ağ Ayarları Kartı -->
                  <div class="device-card">
                      <h3 style="margin-bottom:10px;">⚙️ Ağ & Veritabanı Ayarları</h3>
                      <div class="form-group" style="margin-bottom: 12px;">
                          <label style="font-size:0.8rem; color:var(--text-muted); display:block; margin-bottom:4px;">PostgreSQL Sunucu Adresi</label>
                          <input type="text" value="localhost:5432" disabled style="padding:10px; border-radius:8px; background: rgba(255,255,255,0.05); color:white; border: 1px solid var(--glass-border); width:100%;">
                      </div>
                      <div class="form-group" style="margin-bottom: 12px;">
                          <label style="font-size:0.8rem; color:var(--text-muted); display:block; margin-bottom:4px;">REST API Çalışma Portu</label>
                          <input type="text" value="8000" disabled style="padding:10px; border-radius:8px; background: rgba(255,255,255,0.05); color:white; border: 1px solid var(--glass-border); width:100%;">
                      </div>
                  </div>
              </div>
          </div>
          
          <!-- View 3: Güvenlik -->
          <div v-if="activeView === 'security' && userRole === 'admin'" class="view-section active">
              <header class="top-header glass-panel" style="margin-bottom: 24px;">
                  <div class="header-search">
                      <h1>Güvenlik ve Cihaz Logları</h1>
                      <p>PostgreSQL 'device_logs' tablosu (JSONB destekli canlı izleme ekranı)</p>
                  </div>
              </header>

              <div class="glass-panel" style="padding: 0; overflow:hidden;">
                  <table style="width: 100%; border-collapse: collapse; text-align: left;">
                      <thead style="background: rgba(255,255,255,0.05); border-bottom: 1px solid var(--glass-border);">
                          <tr>
                              <th style="padding: 16px; font-weight: 500;">Tarih / Saat</th>
                              <th style="padding: 16px; font-weight: 500;">Olay (Action)</th>
                              <th style="padding: 16px; font-weight: 500;">Detaylar (JSONB Kolonu)</th>
                              <th style="padding: 16px; font-weight: 500;">Risk</th>
                          </tr>
                      </thead>
                      <tbody>
                          <!-- Row 1 -->
                          <tr style="border-bottom: 1px solid var(--glass-border);">
                              <td style="padding: 16px; color: var(--text-muted);">Bugün 14:02</td>
                              <td style="padding: 16px; color:white; font-weight:500;">CONNECTION_LOST</td>
                              <td style="padding: 16px;"><code style="background: rgba(0,0,0,0.5); padding: 6px 10px; border-radius: 6px; font-size: 0.85rem; color:#f8fafc;">{"error": "timeout", "ping": "999ms"}</code></td>
                              <td style="padding: 16px;"><span class="badge-disconnected" style="background: rgba(239, 68, 68, 0.15); padding:6px 10px; border-radius: 12px; font-size:0.75rem; font-weight:bold;">YÜKSEK</span></td>
                          </tr>
                          <!-- Row 2 -->
                          <tr style="border-bottom: 1px solid var(--glass-border);">
                              <td style="padding: 16px; color: var(--text-muted);">Bugün 11:20</td>
                              <td style="padding: 16px; color:white; font-weight:500;">UNAUTHORIZED_ACCESS</td>
                              <td style="padding: 16px;"><code style="background: rgba(0,0,0,0.5); padding: 6px 10px; border-radius: 6px; font-size: 0.85rem; color:#f8fafc;">{"ip": "45.22.19.1", "attempt": 3}</code></td>
                              <td style="padding: 16px;"><span class="badge-disconnected" style="background: rgba(239, 68, 68, 0.15); padding:6px 10px; border-radius: 12px; font-size:0.75rem; font-weight:bold;">KRİTİK</span></td>
                          </tr>
                          <!-- Row 3 -->
                          <tr>
                              <td style="padding: 16px; color: var(--text-muted);">Dün 09:15</td>
                              <td style="padding: 16px; color:white; font-weight:500;">FIRMWARE_UPDATE</td>
                              <td style="padding: 16px;"><code style="background: rgba(0,0,0,0.5); padding: 6px 10px; border-radius: 6px; font-size: 0.85rem; color:#f8fafc;">{"version": "v2.1", "status": "success"}</code></td>
                              <td style="padding: 16px;"><span class="badge-connected" style="background: rgba(16, 185, 129, 0.15); padding:6px 10px; border-radius: 12px; font-size:0.75rem; font-weight:bold;">DÜŞÜK</span></td>
                          </tr>
                      </tbody>
                  </table>
              </div>
          </div>
      </main>
    </div>

    <!-- ADD DEVICE MODAL: Vue v-if Condition -->
    <div v-if="isModalOpen" class="modal-overlay" style="display:flex;">
        <div class="modal-content glass-panel">
            <div class="modal-header">
                <h2>Cihaz Bağla</h2>
                <button @click="isModalOpen = false" class="btn-icon">✖</button>
            </div>
            
            <form @submit.prevent="addDevice" style="margin-top:20px;">
                <div class="form-group">
                    <label>Cihaz Tipi Seçin</label>
                    <select v-model="newDevType" required>
                        <option value="Security">Güvenlik Kamerası (Security)</option>
                        <option value="Climate">Termostat (Climate)</option>
                        <option value="Lighting">Akıllı Lamba (Lighting)</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Cihaz Adı</label>
                    <input type="text" v-model="newDevName" required placeholder="Örn: Bebek Odası Kamerası">
                </div>
                <button type="submit" class="btn btn-primary" style="width: 100%; margin-top: 10px;">Ağa Kaydet</button>
            </form>
        </div>
    </div>
  </div>
</template>
