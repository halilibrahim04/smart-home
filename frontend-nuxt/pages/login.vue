<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const step = ref('role') // 'role' or 'login'
const selectedRole = ref('')
const email = ref('')
const password = ref('')
const loadingMessage = ref('')

const proceedToLogin = (role) => {
  selectedRole.value = role
  step.value = 'login'
}

const goBack = () => {
  step.value = 'role'
}

const handleLoginSubmit = async () => {
  loadingMessage.value = 'Ağa Bağlanıyor (Post) ...'
  
  try {
    // KAVRAM #33: SADECE "$fetch" kütüphanesi! Ne JSON, ne header işi yok!
    const response = await $fetch("http://localhost:8000/api/login", {
      method: "POST",
      body: { email: email.value, password: password.value, role: selectedRole.value }
    })
    
    loadingMessage.value = 'JWT Alındı (HTTP 200) ✔ Yönlendiriliyor...'
    
    // Nuxt LocalStorage Senaryosu
    if(process.client) {
      localStorage.setItem('smarthome_token', response.token)
    }
    
    setTimeout(() => {
        router.push('/')
    }, 1500)
    
  } catch(err) {
    loadingMessage.value = ''
    if(err.data && err.data.detail) {
        alert("Sunucu Hatası (HTTP " + err.statusCode + "): " + err.data.detail)
    } else {
        alert("Hata: Backend (FastAPI - 8000) sunucusuna bağlanılamadı.")
    }
  }
}
</script>

<template>
  <div class="login-wrapper">
      <div class="glow-orb orb-1"></div>
      <div class="glow-orb orb-2"></div>

      <div class="login-box glass-panel">
          
          <!-- STATE #1: ROLE SECTION -->
          <div v-if="step === 'role'" id="step-role-selection">
              <div class="logo" style="justify-content: center; margin-bottom: 20px;">
                  <div class="logo-icon"></div>
                  <h2>SmartHome Security</h2>
              </div>
              <p class="info-text">Kurumsal ağa erişmek için önce giriş yapmak istediğiniz <b>yetki düzeyini</b> seçiniz.</p>
              
              <div class="role-cards">
                  <div class="role-card admin" @click="proceedToLogin('admin')">
                      <div style="font-size: 2rem; margin-bottom: 10px;">👑</div>
                      Yönetici Grubu
                  </div>
                  <div class="role-card" @click="proceedToLogin('user')">
                      <div style="font-size: 2rem; margin-bottom: 10px;">👤</div>
                      Standart Üye
                  </div>
              </div>
          </div>

          <!-- STATE #2: LOGIN FORM -->
          <div v-else-if="step === 'login'" id="step-login-form" class="login-form-wrapper">
              <button class="back-btn" @click="goBack">🔙 Geri Dön</button>
              <div class="logo" style="justify-content: center; margin-bottom: 10px;">
                  <div class="logo-icon"></div>
              </div>
              <h2>{{ selectedRole === 'admin' ? 'Yönetici Girişi (Admin)' : 'Üye Girişi (User)' }}</h2>
              <p class="info-text">Lütfen veritabanında kayıtlı kurumsal e-posta adresinizi giriniz.</p>
              <p style="font-size:0.75rem; color:#10b981; margin-top:5px;">(Test Login DB Kayıtları: admin@sirket.com veya uye@sirket.com | Şifre: 123456)</p>
              
              <form @submit.prevent="handleLoginSubmit">
                  <div class="form-group">
                      <label>Kurumsal E-Posta</label>
                      <input type="email" v-model="email" placeholder="isim.soyisim@sirket.com" required>
                  </div>
                  <div class="form-group">
                      <label>Parola</label>
                      <input type="password" v-model="password" placeholder="••••••••" required>
                  </div>
                  <button type="submit" class="btn btn-primary" style="margin-top: 10px;" :style="loadingMessage ? 'background: #10b981' : ''">
                      {{ loadingMessage ? loadingMessage : 'Veritabanında Doğrula' }}
                  </button>
              </form>
          </div>
      </div>
  </div>
</template>

<style scoped>
.login-wrapper { display: flex; align-items: center; justify-content: center; height: 100vh; width: 100vw; position: relative; }
.login-box { width: 450px; padding: 40px; display: flex; flex-direction: column; text-align: center; }
.role-cards { display: flex; gap: 16px; margin-top: 24px; }
.role-card { flex: 1; padding: 24px 12px; border-radius: 16px; cursor: pointer; border: 1px solid var(--glass-border); background: rgba(255,255,255,0.03); transition: 0.3s ease; font-weight: 500; font-size: 1.1rem; }
.role-card:hover { transform: translateY(-5px); border-color: var(--primary-color); background: rgba(56, 189, 248, 0.1); }
.role-card.admin:hover { border-color: var(--success-color); background: rgba(16, 185, 129, 0.1); }
.back-btn { font-size: 0.85rem; color: var(--text-muted); cursor: pointer; border: none; background: transparent; align-self: flex-start; margin-bottom: 20px;}
.back-btn:hover { color: white; }
.info-text { color: var(--text-muted); font-size: 0.9rem; margin-top: 10px; }
.login-form-wrapper form { display: flex; flex-direction: column; gap: 16px; margin-top: 24px; text-align: left; }
</style>
