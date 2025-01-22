<template>
    <v-container>
      <v-form>
        <v-text-field
          label="Username"
          v-model="username"
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
        <v-btn color="primary" class="mt-4" @click="handleLogin">
          Login
        </v-btn>
      </v-form>
    </v-container>
  </template>
  
  <script setup lang="ts">
  import { ref } from 'vue'
  
  const username = ref('')
  const password = ref('')
  
  function handleLogin() {
    // ...login logic...
    console.log('Logging in with', username.value, password.value)
  }
  </script>
  