// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
    ssr: false, // SPA moduna sadık kaldık ki JWT LocalStorage döngüsü sorunsuz çalışsın
    css: ['~/assets/css/index.css'], // Global Cam Tasarımlı CSS dahil edildi.
    devtools: { enabled: true }
})
