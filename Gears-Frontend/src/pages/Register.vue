<template>
    <v-container>
      <v-form>
        <v-text-field
          label="Email"
          v-model="email"
          outlined
          required
        />
        <v-text-field
          label="Password"
          v-model="password"
          type="password"
          outlined
          required
        />
        <v-select
          label="Role"
          :items="roles"
          v-model="role"
          outlined
          required
        />
        <v-btn color="primary" class="mt-4" @click="handleRegister">
          Register
        </v-btn>
      </v-form>
    </v-container>
  </template>
  
  <script setup lang="ts">
  import { ref } from 'vue'
  
  const email = ref('')
  const password = ref('')
  const roles = ['研究员', '政策分析员']
  const role = ref(roles[0])
  
  function handleRegister() {
    // ...registration logic...
    console.log('Registering user', email.value, role.value)
  }
  </script>