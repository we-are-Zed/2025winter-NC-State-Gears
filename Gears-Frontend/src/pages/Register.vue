<!-- filepath: /Users/zed99/Documents/GitHub/2025winter-NC-State-Gears/Gears-Frontend/src/pages/Register.vue -->
<template>
  <div class="login-page">
    <div class="square left-bottom hu_hu_animation bg-secondary"></div>
    <div class="square top-right blockR bg-secondary-darken-1"></div>
    <div class="content">
      <v-form>
        <v-text-field
          label="Username"
          v-model="registerForm.username"
          outlined
          required
        />
        <v-text-field
          label="Password"
          v-model="registerForm.password"
          type="password"
          outlined
          required
        />
        <v-select
          label="Role"
          :items="roles"
          v-model="registerForm.role"
          outlined
          required
        />
        <v-btn color="primary" class="mt-4" @click="handleRegister">
          Register
        </v-btn>
      </v-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const registerForm = ref({
  username: '',
  password: '',
  role: ''
})
const roles = ['研究员', '政策分析员']

function handleRegister() {
  
}
</script>

<style scoped lang="scss">
.login-page {
  height: 100vh;
  width: 100vw;
  position: relative;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
}

.square {
  width: 250px;
  height: 250px;
  position: absolute;
  border-radius: 30px;
  transform: rotate(20deg);
}

.square.left-bottom {
  opacity: 0.6;
  bottom: -40px;
  left: -100px;
  box-shadow: 1px 4px 25px rgba(0, 0, 0, 0.33);
}

.square.top-right {
  opacity: 0.6;
  top: -40px;
  right: -100px;
  box-shadow: -5px 4px 9px rgba(0, 0, 0, 0.31);
}

.content {
  background: rgba(255, 255, 255, 0.85);
  padding: 40px 60px;
  border-radius: 12px;
  box-shadow: 0 3px 15px rgba(0, 0, 0, 0.2);
  z-index: 10;
  max-width: 400px;
  width: 100%;
}

.hu_hu_animation {
  animation: block 2.5s ease-in-out infinite;
}

.blockR {
  animation: blockR 2.5s ease-in-out infinite;
}

@keyframes block {
  0%, 100% { left: -100px; }
  50% { left: -95px; }
}

@keyframes blockR {
  0%, 100% { right: -100px; }
  60% { right: -95px; }
}

.bg-secondary {
  background-color: #f5f5f5;
}

.bg-secondary-darken-1 {
  background-color: #e0e0e0;
}
</style>