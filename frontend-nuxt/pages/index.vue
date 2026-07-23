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

          <!-- View 2 & 3: Konfigürasyon ve Güvenlik -->
          <div v-if="activeView === 'config' && userRole === 'admin'" class="view-section active" style="padding:24px;">
              <h2>🛠️ Sistem Konfigürasyonu</h2>
              <p style="color:#94a3b8; margin-top:20px;">Vue State Yönetimi (activeView: 'config') ile bu sayfaya geçiş yaptınız.</p>
          </div>
          
          <div v-if="activeView === 'security' && userRole === 'admin'" class="view-section active" style="padding:24px;">
             <h2 style="color:#ef4444;">🛡️ Güvenlik İhlalleri ve Loglar</h2>
             <p style="color:#94a3b8; margin-top:20px;">Sadece Admin Rolü ('userRole' === 'admin' reaktif değişkeni) ile izleyebilirsiniz.</p>
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
