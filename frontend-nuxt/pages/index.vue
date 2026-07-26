<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const activeView = ref('dashboard') // SPA State Yönetimi
const userRole = ref('')
const devices = ref([])
const logs = ref([])
const homes = ref([])
const isModalOpen = ref(false)
const isHomeModalOpen = ref(false)

const newDevName = ref('')
const newDevType = ref('Security')
const newDevHome = ref('')

const newHomeName = ref('')
const newHomeCity = ref('İstanbul')

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
    
    // Veritabanı okumaları
    fetchDevices()
    fetchLogs()
    fetchHomes()
  } catch(e) {
    localStorage.removeItem('smarthome_token')
    router.push('/login')
  }
})

const fetchDevices = async () => {
  try {
    const data = await $fetch("http://localhost:8000/api/devices", {
      headers: { Authorization: `Bearer ${localStorage.getItem('smarthome_token')}` }
    })
    devices.value = data
  } catch(err) {
    console.error("Cihaz cihaz bilgileri sunucudan okunamadı.", err)
  }
}

const fetchLogs = async () => {
  try {
    const data = await $fetch("http://localhost:8000/api/devices/logs", {
      headers: { Authorization: `Bearer ${localStorage.getItem('smarthome_token')}` }
    })
    logs.value = data
  } catch(err) {
    console.error("Güvenlik logları okunamadı.", err)
  }
}

const fetchHomes = async () => {
  try {
    const res = await $fetch("http://localhost:8000/api/homes", {
      headers: { Authorization: `Bearer ${localStorage.getItem('smarthome_token')}` }
    })
    // Eğer backend direkt [] dönerse res içerisindedir. Object dönerse res.data
    homes.value = res.data || res || []
  } catch(err) {
    console.warn("Mekanlar okunamadı.")
    homes.value = []
  }
}

const deviceGroups = computed(() => {
    const groups = []
    const homeList = homes.value || []
    
    homeList.forEach(home => {
        groups.push({
            homeId: home.id,
            title: `${home.name} (${home.location_city})`,
            devices: devices.value.filter(d => d.home_id === home.id)
        })
    })

    // Bağımsız cihazları arayüzden tamamen temizledik. Sadece atanan evleri çekecek.
    return groups
})

const addHome = async () => {
  try {
    const res = await $fetch("http://localhost:8000/api/homes", {
      method: "POST",
      headers: { Authorization: `Bearer ${localStorage.getItem('smarthome_token')}` },
      body: { name: newHomeName.value, location_city: newHomeCity.value }
    })
    homes.value.push(res.data) 
    isHomeModalOpen.value = false
    newHomeName.value = ''
  } catch(err) {
    alert("Hata: " + (err.data?.detail || "Sunucu hatası."))
  }
}

const addDevice = async () => {
  try {
    const res = await $fetch("http://localhost:8000/api/devices", {
      method: "POST",
      headers: { Authorization: `Bearer ${localStorage.getItem('smarthome_token')}` },
      body: { name: newDevName.value, device_type: newDevType.value, home_id: newDevHome.value || "" }
    })
    devices.value.unshift(res.data) 
    isModalOpen.value = false
    newDevName.value = ''
    newDevHome.value = ''
  } catch(err) {
    if(err.data && err.data.detail) {
        alert(err.data.detail)
    } else {
        alert("Bağlantı Hatası veya Yetkisiz erişim")
    }
  }
}

const togglePower = async (device) => {
  try {
    const res = await $fetch(`http://localhost:8000/api/devices/${device.id}/toggle`, {
      method: "PATCH",
      headers: { Authorization: `Bearer ${localStorage.getItem('smarthome_token')}` }
    })
    // Ekrana anında yansıması için (Vue Reactivity zorlaması)
    const idx = devices.value.findIndex(d => d.id === device.id)
    if(idx > -1) {
        devices.value[idx] = { ...devices.value[idx], status: res.data.status }
    }
    fetchLogs() // Son logları hemen tazele (Canlı yansıma)
  } catch(err) {
    alert("Cihaz Etkileşim Hatası: " + (err.data?.detail || ""))
  }
}

const logout = () => {
  localStorage.removeItem('smarthome_token')
  router.push('/login')
}

const changeTemp = async (device, delta) => {
  let current = device.settings?.temperature || 22
  let newTemp = current + delta
  
  if(newTemp < 16) newTemp = 16
  if(newTemp > 30) newTemp = 30
  
  if(current === newTemp) return
  
  try {
    const res = await $fetch(`http://localhost:8000/api/devices/${device.id}/settings`, {
      method: "PATCH",
      headers: { Authorization: `Bearer ${localStorage.getItem('smarthome_token')}` },
      body: { settings: { temperature: newTemp } }
    })
    // Derinlemesine Vue update'i
    const idx = devices.value.findIndex(d => d.id === device.id)
    if(idx > -1) {
        devices.value[idx] = { ...devices.value[idx], settings: res.data.settings }
    }
    fetchLogs()
  } catch(err) {
    alert("Derece ayarlanamadı.")
  }
}
</script>

<template>
  <ClientOnly>
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
              <a href="#" v-if="userRole === 'admin'" :class="['nav-item', activeView === 'config' ? 'active' : '']" @click.prevent="activeView = 'config'">
                  <span>Sistem Konfigürasyonu</span>
              </a>
              <a href="#" v-if="userRole === 'admin'" :class="['nav-item', activeView === 'security' ? 'active' : '']" @click.prevent="activeView = 'security'">
                  <span>Güvenlik İhlalleri</span>
              </a>
          </nav>

          <div class="auth-status" style="flex-direction: column; gap: 15px; padding: 20px;">
              <div style="display: flex; gap: 12px; width: 100%; align-items: center;">
                  <div class="user-avatar">
                     <img :src="userRole === 'admin' ? 'https://ui-avatars.com/api/?name=Admin&background=10b981&color=fff' : 'https://ui-avatars.com/api/?name=User&background=38bdf8&color=fff'">
                  </div>
                  <div class="user-info">
                      <span class="user-name" style="font-size: 0.9rem; font-weight: 500;">Oturum Açık</span>
                      <span :class="['user-role', userRole === 'admin' ? 'badge-admin' : 'badge-user']" style="font-size: 0.7rem;">
                         {{ userRole === 'admin' ? 'SYSTEM ADMIN' : 'USER' }}
                      </span>
                  </div>
              </div>
              <button @click="logout" class="btn" style="width: 100%; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); color: #cbd5e1; font-size: 0.8rem; letter-spacing: 1px; padding: 8px; cursor: pointer; border-radius: 6px; transition: 0.2s;">ÇIKIŞ YAP</button>
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
                    <button v-if="userRole === 'admin'" class="btn btn-primary" @click="isModalOpen = true">
                        + Cihaz Ekle (POST)
                    </button>
                </header>
    
                <section class="main-content">
                    <div v-if="devices.length === 0" style="padding:40px 20px; text-align: center; border-radius: 12px; background: rgba(255,255,255,0.02); border: 1px dashed rgba(255,255,255,0.1); margin-top: 20px; color:#94a3b8">
                        <h2>Bağlı Cihaz Yok</h2>
                        <p style="margin-top: 10px; font-size: 0.9rem;">Eski kurallara ait 'Bağımsız Cihazlarınız' sistemden silindi. Şu an hiçbir cihazınız bulunmuyor.<br> Cihaz eklemeden önce 'Sistem Konfigürasyonu' sayfasından yeni bir ev (mekan) yaratmanız gerekir.</p>
                    </div>
                    
                    <div v-for="group in deviceGroups" :key="group.homeId || 'unassigned'" style="margin-bottom: 50px; margin-top: 30px;">
                        <h2 style="font-size: 1.25rem; font-weight: 600; color: #f8fafc; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 12px; margin-bottom: 25px; display: flex; align-items: center; gap: 10px;">
                            <span v-if="group.homeId" style="color:#38bdf8;">📍</span>
                            <span v-else style="color:#ef4444;">⚠️</span>
                            {{ group.title }}
                        </h2>
                        
                        <div class="device-grid">
                            <div v-for="device in group.devices" :key="device.id" class="device-card">
                                <div class="card-header" style="align-items: center; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 10px; margin-bottom: 15px;">
                                    <span class="device-type" style="letter-spacing: 1px; color:#94a3b8; font-size: 0.75rem;">{{device.device_type.toUpperCase()}}</span>
                                    <div style="width: 8px; height: 8px; border-radius: 50%;" :style="{ background: device.status === 'online' ? '#10b981' : '#ef4444', boxShadow: device.status === 'online' ? '0 0 10px #10b981' : 'none' }"></div>
                                </div>
                                <h3 class="device-title" style="margin-top:0;">{{device.name}}</h3>
                                
                                <div class="device-details">
                                    <div class="detail-row">
                                        <span>ID:</span><span style="font-size:0.75rem;">{{String(device.id).substring(0,8)}}...</span>
                                    </div>
                                    <div class="detail-row">
                                        <span>Ağ Adresi:</span><span>{{device.ip_address}}</span>
                                    </div>
                                    
                                    <!-- CLIMATE CİHAZ YETENEĞİ (DERECE KONTROLÜ) -->
                            <div v-if="device.device_type === 'Climate'" style="margin-top: 15px; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 15px;">
                                <span style="display:block; margin-bottom:10px; font-size: 0.85rem; color: #94a3b8; font-weight: 500;">Derece Kontrolü:</span>
                                <div style="display:flex; align-items:center; gap: 15px; justify-content: flex-start;">
                                    <button class="btn btn-outline" @click="changeTemp(device, -1)" :disabled="device.status !== 'online'" style="padding: 4px; font-size:1.4rem; height: 35px; width: 35px; display:flex; align-items:center; justify-content:center;">-</button>
                                    <strong style="font-size: 1.25rem; color: white; width: 50px; text-align:center; font-weight: 700;">{{ device.settings?.temperature || 22 }}°C</strong>
                                    <button class="btn btn-outline" @click="changeTemp(device, 1)" :disabled="device.status !== 'online'" style="padding: 4px; font-size:1.2rem; height: 35px; width: 35px; display:flex; align-items:center; justify-content:center;">+</button>
                                </div>
                                <span v-if="device.status !== 'online'" style="display:block; margin-top:6px; font-size:0.75rem; color:#ef4444;">Kontrol için güç verin.</span>
                            </div>

                            <div class="detail-row" style="margin-top: 15px; align-items: center; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 10px;">
                                <span style="font-weight: 500;">Durum:</span>
                                <span :class="device.status === 'online' ? 'badge-connected' : 'badge-disconnected'" style="display:flex; align-items:center; gap:5px; font-size: 0.75rem;">
                                    ● {{ device.status === 'online' ? 'Bağlı (Connected)' : 'Cevap Yok' }}
                                </span>
                            </div>        
                                    
                                    <!-- İNTERAKTİF GÜÇ DÜĞMESİ (TOGGLE) -->
                                    <div style="margin-top: 15px;">
                                        <button @click="togglePower(device)" :style="{ width:'100%', padding:'8px', borderRadius:'6px', border:'none', cursor:'pointer', fontWeight:'bold', transition: '0.2s', background: device.status === 'online' ? 'rgba(239, 68, 68, 0.15)' : 'rgba(16, 185, 129, 0.15)', color: device.status === 'online' ? '#ef4444' : '#10b981' }">
                                            {{ device.status === 'online' ? 'Bağlantıyı Kes' : 'Bağlantıyı Kur' }}
                                        </button>
                                    </div>
                                </div>
                            </div>

                            <div v-if="group.devices.length === 0" style="grid-column: 1 / -1; padding: 25px; border-radius: 12px; background: rgba(255,255,255,0.02); text-align: center; color: #64748b; border: 1px dashed rgba(255,255,255,0.1);">
                                Bu mekana bağlı donanım bulunmuyor. Yeni Cihaz Bağla butonunu kullanarak hemen donanım ekleyebilirsiniz.
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
                        <h3 style="margin-bottom:10px;">Kayıtlı Mekanlar (Homes)</h3>
                        <p style="color:#94a3b8; font-size:0.85rem; margin-bottom:15px;">Kayıtlı fiziksel lokasyonlarınızı yönetin.</p>
                        
                        <div v-for="home in homes" :key="home.id" style="background: rgba(0,0,0,0.3); padding: 15px; border-radius: 8px; margin-bottom: 12px; border: 1px solid var(--glass-border); margin-top: 15px;">
                            <strong style="display:inline-block; margin-bottom:6px; font-size:1.05rem; letter-spacing: 0.5px;">{{ home.name }}</strong> <br> 
                            <span style="font-size:0.8rem; color:#10b981;">{{ home.location_city }}</span>
                        </div>
                        
                        <div v-if="homes.length === 0" style="color:var(--text-muted); font-size:0.85rem; padding-bottom:10px;">
                            Sistemde kayıtlı hiçbir mekan/ev bulunmuyor.
                        </div>

                        <button @click="isHomeModalOpen = true" class="btn btn-primary" style="width:100%; font-size:0.85rem; padding: 10px;">+ Yeni Ev/Mekan Ekle</button>
                    </div>
                    
                    <!-- Ağ Ayarları Kartı -->
                    <div class="device-card">
                        <h3 style="margin-bottom:10px;">Ağ & Veritabanı Ayarları</h3>
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
                            <!-- Vue V-FOR ile Dinamik JSONB Logları Döngüsü -->
                            <tr v-for="log in logs" :key="log.id" style="border-bottom: 1px solid var(--glass-border);">
                                <td style="padding: 16px; color: var(--text-muted);">{{ log.created_at }}</td>
                                <td style="padding: 16px; color:white; font-weight:500;">{{ log.action_type }}</td>
                                <td style="padding: 16px;"><code style="background: rgba(0,0,0,0.5); padding: 6px 10px; border-radius: 6px; font-size: 0.85rem; color:#f8fafc;">{{ JSON.stringify(log.details) }}</code></td>
                                <td style="padding: 16px;">
                                    <span v-if="log.action_type === 'CONNECTION_LOST' || log.action_type === 'UNAUTHORIZED_ACCESS'" class="badge-disconnected" style="background: rgba(239, 68, 68, 0.15); padding:6px 10px; border-radius: 12px; font-size:0.75rem; font-weight:bold;">
                                        YÜKSEK RİSK
                                    </span>
                                    <span v-else class="badge-connected" style="background: rgba(16, 185, 129, 0.15); padding:6px 10px; border-radius: 12px; font-size:0.75rem; font-weight:bold;">
                                        DÜŞÜK RİSK
                                    </span>
                                </td>
                            </tr>
                            
                            <!-- Tablo Boşken -->
                            <tr v-if="logs.length === 0">
                                <td colspan="4" style="padding:20px; text-align:center; color:#94a3b8;">Veritabanında hiçbir sistem logu veya ihlali bulunmuyor.</td>
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
                          <option value="Climate">Termostat / Klima (Climate)</option>
                          <option value="Lighting">Akıllı Lamba (Lighting)</option>
                          <option value="Speaker">Akıllı Hoparlör (Speaker)</option>
                          <option value="Vacuum">Robot Süpürge (Vacuum)</option>
                          <option value="Switch">Akıllı Priz (Switch)</option>
                      </select>
                  </div>
                  
                  <div class="form-group">
                      <label>Hangi Mekana Bağlanacak?</label>
                      <select v-model="newDevHome" required :disabled="homes.length === 0">
                          <option value="" disabled selected v-if="homes.length > 0">-- Zorunlu: Bir Mekan Seçiniz --</option>
                          <option value="" disabled selected v-else>⚠️ Uyarı: Önce menüden bir (Ev/Mekan) eklemelisiniz --</option>
                          <option v-for="h in homes" :key="h.id" :value="h.id">{{ h.name }} ({{ h.location_city }})</option>
                      </select>
                      <span v-if="homes.length === 0" style="color:#ef4444; font-size: 0.75rem; display:block; margin-top:5px;">Sistemde evin yok! Sol menü -> Sistem Konfigürasyonu sekmesinden Ev oluştur!</span>
                  </div>

                  <div class="form-group">
                      <label>Cihaz Adı</label>
                      <input type="text" v-model="newDevName" required placeholder="Örn: Bebek Odası Kamerası">
                  </div>
                  <button type="submit" class="btn btn-primary" style="width: 100%; margin-top: 10px;">Ağa Kaydet</button>
              </form>
          </div>
      </div>

      <!-- ADD HOME MODAL -->
      <div v-if="isHomeModalOpen" class="modal-overlay" style="display:flex;">
          <div class="modal-content glass-panel">
              <div class="modal-header">
                  <h2>Yeni Mekan Ekle</h2>
                  <button @click="isHomeModalOpen = false" class="btn-icon">✖</button>
              </div>
              
              <form @submit.prevent="addHome" style="margin-top:20px;">
                  <div class="form-group">
                      <label>Lokasyon / Şehir</label>
                      <select v-model="newHomeCity" required>
                          <option value="İstanbul">İstanbul</option>
                          <option value="Ankara">Ankara</option>
                          <option value="İzmir">İzmir</option>
                          <option value="Antalya">Antalya</option>
                          <option value="Bursa">Bursa</option>
                      </select>
                  </div>
                  <div class="form-group">
                      <label>Mekan Adı</label>
                      <input type="text" v-model="newHomeName" required placeholder="Örn: Yazlık Ev, Merkez Ofis">
                  </div>
                  <button type="submit" class="btn btn-primary" style="width: 100%; margin-top: 10px;">PostgreSQL'e Kaydet</button>
              </form>
          </div>
      </div>
    </div>
  </ClientOnly>
</template>
