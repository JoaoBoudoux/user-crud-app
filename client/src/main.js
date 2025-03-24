import { createApp } from 'vue';
import App from './App.vue';
import PrimeVue from 'primevue/config';
import ToastService from 'primevue/toastservice'; 
import router from './router';
import Aura from '@primevue/themes/aura';
import 'primeicons/primeicons.css'; 
import './styles/global.css'; 

const app = createApp(App);
app.use(PrimeVue, {
  theme: {
    preset: Aura,
    options: {
      prefix: 'p',
      darkModeSelector: 'system',
      cssLayer: false,
    },
  },
});
app.use(ToastService); 
app.use(router);
app.mount('#app');

console.log('PrimeVue configurado com tema Aura');