<template>
  <div class="p-m-4">
    <h1>User Details</h1>
    <div v-if="user" class="card p-p-4">
      <p><strong>Username:</strong> {{ user.username }}</p>
      <p><strong>Roles:</strong> {{ user.roles.join(', ') }}</p>
      <p><strong>Timezone:</strong> {{ user.preferences.timezone }}</p>
      <p><strong>Active:</strong> {{ user.active ? 'Yes' : 'No' }}</p>
      <p><strong>Created At:</strong> {{ new Date(user.created_ts * 1000).toLocaleString() }}</p>
      <Button label="Edit" icon="pi pi-pencil" class="p-mr-2" @click="showEditModal" />
      <Button label="Delete" icon="pi pi-trash" class="p-button-danger" @click="confirmDelete" />
    </div>
    <div v-else>
      <p>User not found.</p>
    </div>

    <Button label="Back to List" icon="pi pi-arrow-left" class="p-mt-4" @click="$router.push('/')" />

    <!-- Modal para Edit -->
    <UserForm v-model:visible="showModal" :user="user" :isEdit="true" @save="saveUser" />

    <!-- Confirmação de Deleção -->
    <Dialog header="Confirm Delete" v-model:visible="showDeleteConfirm" :modal="true">
      <p>Are you sure you want to delete {{ user?.username }}?</p>
      <template #footer>
        <Button label="No" icon="pi pi-times" @click="showDeleteConfirm = false" class="p-button-text" />
        <Button label="Yes" icon="pi pi-check" @click="deleteUser" class="p-button-danger" />
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';
import Button from 'primevue/button';
import Dialog from 'primevue/dialog';
import UserForm from '../components/UserForm.vue';

const route = useRoute();
const router = useRouter();
const user = ref(null);
const showModal = ref(false);
const showDeleteConfirm = ref(false);

const fetchUser = async () => {
  try {
    const response = await axios.get(`/api/users/${route.params.id}`);
    user.value = response.data;
  } catch (error) {
    user.value = null;
  }
};

onMounted(fetchUser);

const showEditModal = () => {
  showModal.value = true;
};

const saveUser = async (userData) => {
  await axios.put(`/api/users/${userData._id}`, userData);
  fetchUser();
};

const confirmDelete = () => {
  showDeleteConfirm.value = true;
};

const deleteUser = async () => {
  await axios.delete(`/api/users/${user.value._id}`);
  showDeleteConfirm.value = false;
  router.push('/');
};

</script>

<style scoped>
.card {
  border: 1px solid #ddd;
  border-radius: 4px;
}
</style>