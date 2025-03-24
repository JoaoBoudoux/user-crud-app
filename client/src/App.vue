<template>
  <div>
    <Toast /> 
    <router-view />
  </div>
</template>





<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Button from 'primevue/button';
import Dialog from 'primevue/dialog';
import ProgressSpinner from 'primevue/progressspinner';
import UserForm from './components/UserForm.vue';
import Toast from 'primevue/toast';


const route = useRoute();
const users = ref([]);
const loading = ref(false);
const showModal = ref(false);
const selectedUser = ref(null);
const isEdit = ref(false);
const showDeleteConfirm = ref(false);
const userToDelete = ref(null);

const fetchUsers = async () => {
  loading.value = true;
  try {
    console.log('Fazendo requisição para /api/users...');
    const response = await axios.get('/api/users');
    console.log('Usuários recebidos:', response.data);
    users.value = response.data;
    console.log('users.value após atribuição:', users.value);
  } catch (error) {
    console.error('Erro ao buscar usuários:', error);
    console.error('Detalhes do erro:', error.response);
    users.value = [];
    console.log('users.value após erro:', users.value);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  if (route.path === '/') {
    fetchUsers();
  }
});

const showCreateModal = () => {
  selectedUser.value = null;
  isEdit.value = false;
  showModal.value = true;
};

const showEditModal = (user) => {
  selectedUser.value = { ...user };
  isEdit.value = true;
  showModal.value = true;
};

const saveUser = async (userData) => {
  console.log('Salvando usuário:', userData);
  try {
    if (isEdit.value) {
      console.log('Enviando requisição PUT para:', `/api/users/${userData._id}`);
      const response = await axios.put(`/api/users/${userData._id}`, userData);
      console.log('Resposta do PUT:', response.data);
    } else {
      console.log('Enviando requisição POST para /api/users');
      const response = await axios.post('/api/users', userData);
      console.log('Resposta do POST:', response.data);
    }
    fetchUsers();
  } catch (error) {
    console.error('Erro ao salvar usuário:', error);
    console.error('Detalhes do erro:', error.response);
  }
};

const confirmDelete = (user) => {
  userToDelete.value = user;
  showDeleteConfirm.value = true;
};

const deleteUser = async () => {
  await axios.delete(`/api/users/${userToDelete.value._id}`);
  showDeleteConfirm.value = false;
  userToDelete.value = null;
  fetchUsers();
};
</script>