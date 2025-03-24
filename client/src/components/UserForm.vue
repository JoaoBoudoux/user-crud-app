<template>
  <Dialog :header="isEdit ? 'Edit User' : 'Create User'" :visible="visible" :modal="true" @update:visible="onClose" class="custom-dialog">
    <div class="p-fluid">
      <div class="p-field">
        <label for="username">Username <span class="required">*</span></label>
        <InputText id="username" v-model="form.username" class="custom-input" />
      </div>
      <div class="p-field">
        <label for="password">Password <span class="required">*</span></label>
        <InputText id="password" v-model="form.password" class="custom-input" />
      </div>
      <div class="p-field">
        <label for="roles">Roles <span class="required">*</span></label>
        <MultiSelect id="roles" v-model="form.roles" :options="roleOptions" placeholder="Select Roles" class="custom-input" />
      </div>
      <div class="p-field">
        <label for="timezone">Timezone</label>
        <InputText id="timezone" v-model="form.preferences.timezone" class="custom-input" />
      </div>
      <div class="p-field">
        <label for="active">Active</label>
        <Checkbox id="active" v-model="form.active" :binary="true" />
      </div>
      <div class="p-field">
        <label for="created_ts">Created At (Unix Timestamp)</label>
        <InputText id="created_ts" v-model="form.created_ts" type="number" class="custom-input" />
      </div>
    </div>
    <template #footer>
      <Button label="Cancel" icon="pi pi-times" @click="onClose" class="p-button-text p-button-secondary" />
      <Button label="Save" icon="pi pi-check" @click="save" class="p-button-primary" />
    </template>
  </Dialog>
</template>

<script setup>
import { ref, watch } from 'vue';
import { useToast } from 'primevue/usetoast';
import Dialog from 'primevue/dialog';
import InputText from 'primevue/inputtext';
import MultiSelect from 'primevue/multiselect';
import Checkbox from 'primevue/checkbox';
import Button from 'primevue/button';

const toast = useToast();

const props = defineProps({
  visible: Boolean,
  user: Object,
  isEdit: Boolean,
});

const emit = defineEmits(['update:visible', 'save']);

const form = ref({
  username: '',
  password: '',
  roles: [],
  preferences: { timezone: '' },
  active: true,
  created_ts: Math.floor(Date.now() / 1000),
});

const roleOptions = ref(['admin', 'manager', 'tester']);

watch(
  () => props.user,
  (newUser) => {
    if (newUser) {
      form.value = { ...newUser };
    } else {
      form.value = {
        username: '',
        password: '',
        roles: [],
        preferences: { timezone: '' },
        active: true,
        created_ts: Math.floor(Date.now() / 1000),
      };
    }
  },
  { immediate: true }
);

const onClose = (value) => {
  console.log('Fechando modal, emitindo update:visible com valor:', value);
  emit('update:visible', value);
};

const save = () => {
  if (!props.isEdit) {
    if (!form.value.username) {
      toast.add({
        severity: 'error',
        summary: 'Validation Error',
        detail: 'Username is required',
        life: 3000,
      });
      return;
    }
    if (!form.value.password) {
      toast.add({
        severity: 'error',
        summary: 'Validation Error',
        detail: 'Password is required',
        life: 3000,
      });
      return;
    }
    if (!form.value.roles || form.value.roles.length === 0) {
      toast.add({
        severity: 'error',
        summary: 'Validation Error',
        detail: 'At least one role is required',
        life: 3000,
      });
      return;
    }
  }

  const userData = {
    _id: props.user?._id,
    username: form.value.username,
    password: form.value.password,
    roles: form.value.roles,
    preferences: { timezone: form.value.preferences.timezone },
    active: form.value.active,
    created_ts: parseInt(form.value.created_ts, 10),
  };
  console.log('Dados do formulário ao salvar:', userData);
  if (!userData._id && props.isEdit) {
    console.error('Erro: _id não encontrado no modo de edição');
  }
  emit('save', userData);
  emit('update:visible', false);
};
</script>

<style scoped>
.custom-dialog {
  background-color: var(--background-secondary) !important;
  border: 1px solid var(--border-color) !important;
  border-radius: 4px !important;
  box-shadow: none !important;
  width: 350px !important; 
  min-height: 350px !important; 
  max-height: 380px !important; 
}

.custom-dialog .p-dialog-header {
  background-color: var(--background-secondary) !important;
  color: var(--text-primary) !important;
  border-bottom: 1px solid var(--border-color) !important;
  border-radius: 4px 4px 0 0 !important;
  padding: 0.75rem !important; 
}

.custom-dialog .p-dialog-content {
  background-color: var(--background-secondary) !important;
  color: var(--text-primary) !important;
  border-radius: 0 !important;
  padding: 0.75rem !important; 
  overflow-y: auto !important; 
}

.custom-dialog .p-dialog-footer {
  background-color: var(--background-secondary) !important;
  border-top: 1px solid var(--border-color) !important;
  border-radius: 0 0 4px 4px !important;
  padding: 0.5rem 0.75rem !important; 
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
}

.p-field {
  margin-bottom: 0.75rem !important; 
}

.p-field label {
  color: var(--text-primary) !important;
  font-weight: 500;
  margin-bottom: 0.2rem !important;
  display: block;
}

.required {
  color: var(--button-secondary);
  font-weight: bold;
}

.custom-input {
  background-color: #3A3A3A !important;
  border: 1px solid var(--border-color) !important;
  color: var(--text-primary) !important;
  border-radius: 4px !important;
  padding: 0.4rem !important; 
}

.custom-input:focus {
  border-color: var(--button-primary) !important;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2) !important;
}

.p-button.p-button-text.p-button-secondary {
  color: var(--button-secondary) !important;
}

.p-button.p-button-text.p-button-secondary:hover {
  color: #DC2626 !important;
}
</style>