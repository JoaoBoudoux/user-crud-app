<template>
  <div class="container">
    <h1>User Details</h1>
    <div v-if="user" class="user-card">
      <p><strong>Username:</strong> {{ user.username }}</p>
      <p><strong>Roles:</strong> {{ user.roles.join(', ') }}</p>
      <p><strong>Timezone:</strong> {{ user.preferences.timezone }}</p>
      <p><strong>Active:</strong> {{ user.active ? 'Yes' : 'No' }}</p>
      <p><strong>Last Updated At:</strong> {{ user.last_updated_at ? new Date(user.last_updated_at * 1000).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' }) : 'N/A' }}</p>
      <p><strong>Created At:</strong> {{ new Date(user.created_ts * 1000).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' }) }}</p>
      <Button label="Back to List" icon="pi pi-arrow-left" @click="goBack" class="back-button" />
    </div>
    <div v-else-if="loading" class="loading-container">
      <ProgressSpinner style="width: 50px; height: 50px" />
      <p>Loading user...</p>
    </div>
    <div v-else class="no-user">
      <p>User not found.</p>
      <Button label="Back to List" icon="pi pi-arrow-left" @click="goBack" class="back-button" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import axios from 'axios';
import Button from 'primevue/button';
import ProgressSpinner from 'primevue/progressspinner';

const route = useRoute();
const router = useRouter();
const user = ref(null);
const loading = ref(false);

const fetchUser = async () => {
  loading.value = true;
  try {
    console.log('Buscando usuário com ID:', route.params.id);
    const response = await axios.get(`/api/users/${route.params.id}`);
    console.log('Usuário recebido:', response.data);
    user.value = response.data;
  } catch (error) {
    console.error('Erro ao buscar usuário:', error);
    console.error('Detalhes do erro:', error.response?.data || error.message);
    user.value = null;
  } finally {
    loading.value = false;
  }
};

onMounted(fetchUser);

const goBack = () => {
  router.push('/');
};
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 2rem;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.user-card {
  background-color: #f9f9f9;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.user-card p {
  font-size: 1.1rem;
  margin: 0.5rem 0;
  color: #2c3e50;
}

.user-card p strong {
  color: #3498db;
  margin-right: 0.5rem;
}

.back-button {
  background: linear-gradient(90deg, #3498db, #2980b9);
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 25px;
  margin-top: 1rem;
}

.back-button:hover {
  background: linear-gradient(90deg, #2980b9, #1f618d);
}

.loading-container {
  text-align: center;
  padding: 2rem;
}

.no-user {
  text-align: center;
  padding: 2rem;
  color: #7f8c8d;
}
</style>