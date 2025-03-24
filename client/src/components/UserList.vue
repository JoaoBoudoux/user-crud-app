<template>
  <div>
    <h1>Users Management</h1>
    <Button label="Create User" icon="pi pi-plus" @click="showCreateModal" class="p-mb-4 p-button-primary" />
    <div>
      <p>Usuários carregados: {{ users.length }}</p>
      <div v-if="loading" class="p-text-center">
        <ProgressSpinner style="width: 50px; height: 50px" />
        <p>Loading users...</p>
      </div>
      <DataTable v-else-if="users.length > 0" :value="users" :paginator="true" :rows="10" responsiveLayout="scroll">
        <Column field="username" header="Username">
          <template #body="{ data }">
            <router-link :to="`/user/${data._id}`">{{ data.username }}</router-link>
          </template>
        </Column>
        <Column field="roles" header="Roles">
          <template #body="{ data }">
            {{ data.roles.join(', ') }}
          </template>
        </Column>
        <Column field="preferences.timezone" header="Timezone" />
        <Column field="active" header="Is Active?">
          <template #body="{ data }">
            {{ data.active ? 'Yes' : 'No' }}
          </template>
        </Column>
        <Column field="created_ts" header="Created At">
          <template #body="{ data }">
            {{ new Date(data.created_ts * 1000).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' }) }}
          </template>
        </Column>
        <Column header="Actions">
          <template #body="{ data }">
            <Button icon="pi pi-pencil" class="p-button-rounded p-button-success p-mr-2" @click="showEditModal(data)" />
            <Button icon="pi pi-trash" class="p-button-rounded p-button-danger" @click="confirmDelete(data)" />
          </template>
        </Column>
      </DataTable>
      <div v-else>
        <p>No users found. Click "Create User" to add a new user.</p>
      </div>
    </div>

    <UserForm v-model:visible="showModal" :user="selectedUser" :isEdit="isEdit" @save="saveUser" />
    
    <Dialog header="Confirm Delete" v-model:visible="showDeleteConfirm" :modal="true">
      <p>Are you sure you want to delete {{ userToDelete?.username }}?</p>
      <template #footer>
        <Button label="No" icon="pi pi-times" @click="showDeleteConfirm = false" class="p-button-text" />
        <Button label="Yes" icon="pi pi-check" @click="deleteUser" class="p-button-danger" />
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import axios from 'axios';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Button from 'primevue/button';
import Dialog from 'primevue/dialog';
import ProgressSpinner from 'primevue/progressspinner';
import UserForm from './UserForm.vue';

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
    console.error('Detalhes do erro:', error.response?.data || error.message);
    users.value = [];
    console.log('users.value após erro:', users.value);
  } finally {
    loading.value = false;
  }
};

onMounted(fetchUsers);

const showCreateModal = () => {
  selectedUser.value = null;
  isEdit.value = false;
  showModal.value = true;
  console.log('Abrindo modal para criação, showModal:', showModal.value);
};

const showEditModal = (user) => {
  console.log('Usuário selecionado para edição:', user); 
  selectedUser.value = { ...user };
  isEdit.value = true;
  showModal.value = true;
  console.log('selectedUser.value:', selectedUser.value); 
};

const saveUser = async (userData) => {
  console.log('Salvando usuário:', userData);
  try {
    const { _id, ...dataToSend } = userData;
    if (isEdit.value) {
      console.log('Enviando requisição PUT para:', `/api/users/${_id}`);
      const response = await axios.put(`/api/users/${_id}`, dataToSend);
      console.log('Resposta do PUT:', response.data);
    } else {
      console.log('Enviando requisição POST para /api/users');
      const response = await axios.post('/api/users', dataToSend);
      console.log('Resposta do POST:', response.data);
    }
    showModal.value = false;
    fetchUsers();
  } catch (error) {
    console.error('Erro ao salvar usuário:', error);
    console.error('Detalhes do erro:', error.response?.data || error.message);
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

watch(showModal, (newValue) => {
  console.log('showModal alterado para:', newValue);
});
</script>

<style scoped>
.container {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 2rem;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.create-button {
  background: linear-gradient(90deg, #3498db, #2980b9);
  border: none;
  padding: 0.75rem 1.5rem;
  font-size: 1.1rem;
  border-radius: 25px;
}

.create-button:hover {
  background: linear-gradient(90deg, #2980b9, #1f618d);
}

.users-count {
  font-size: 1.1rem;
  color: #7f8c8d;
  margin-bottom: 1rem;
}

.table-wrapper {
  background-color: #fff;
  border-radius: 8px;
  overflow: hidden;
}

.users-table {
  width: 100%;
}

.users-table :deep(.p-datatable-thead > tr > th) {
  background-color: #3498db;
  color: #fff;
  font-weight: 600;
  padding: 1rem;
}

.users-table :deep(.p-datatable-tbody > tr) {
  transition: background-color 0.3s ease;
}

.users-table :deep(.p-datatable-tbody > tr:nth-child(even)) {
  background-color: #f9f9f9;
}

.users-table :deep(.p-datatable-tbody > tr:hover) {
  background-color: #e8f4fd;
}

.action-button {
  width: 40px;
  height: 40px;
}

.edit-button {
  background-color: #2ecc71;
  border-color: #2ecc71;
}

.edit-button:hover {
  background-color: #27ae60;
  border-color: #27ae60;
}

.delete-button {
  background-color: #e74c3c;
  border-color: #e74c3c;
}

.delete-button:hover {
  background-color: #c0392b;
  border-color: #c0392b;
}

.loading-container {
  text-align: center;
  padding: 2rem;
}

.no-users {
  text-align: center;
  padding: 2rem;
  color: #7f8c8d;
}

.delete-dialog {
  max-width: 400px;
  margin: auto;
}
</style>