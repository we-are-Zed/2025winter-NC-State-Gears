<template>
  <div class="login-page">
    <div class="square left-bottom hu_hu_animation bg-secondary"></div>
    <div class="square top-right blockR bg-secondary-darken-1"></div>
    <v-container class="h-100 d-flex align-center justify-center">
      <v-card max-width="400px" width="100%" elevation="8" rounded="lg" class="pa-4">
        <v-card-title class="text-center text-h4 mb-4">
          登录
        </v-card-title>
        <v-form>
          <v-text-field
            label="Username"
            v-model="loginForm.username"
            prepend-inner-icon="mdi-account"
            variant="outlined"
            required
          />
          <v-text-field
            label="Password"
            v-model="loginForm.password"
            prepend-inner-icon="mdi-lock"
            type="password"
            variant="outlined"
            required
          />
          <v-btn 
            color="primary" 
            size="large"
            block
            class="mt-4" 
            @click="login"
          >
            Login
          </v-btn>
        </v-form>
      </v-card>
    </v-container>
  </div>
</template>

<script setup lang="ts">
import {createConnection, toasterOptions} from "../config";
import {createToaster} from "@meforma/vue-toaster";
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAppStore } from "@/stores/app";

const global = useAppStore();

const loginForm = ref({
  username: '',
  password: ''
})
const loginLoading = ref(false)
const router = useRouter()
const conn=createConnection()
const toaster = createToaster(toasterOptions)

function login() {
    // if (loginForm.value.username === '' || loginForm.value.password === '') {
    //     toaster.show('Please fill in all fields', {type: 'error'});
    //     return;
    // }
    // loginLoading.value = true;
    // let formData = new FormData();
    // let username = loginForm.value.username;
    // formData.append('username', username);
    // formData.append('password', loginForm.value.password);
    // conn.post('/login', formData)
    //     .then(res => {
    //         loginLoading.value = false;
    //         if (res.status === 200) {
    //             global.isLogin = true;
    //             toaster.show('Login successful', {type: 'success'});
    //             let json = res.data;
    //             if (typeof json === 'string') {
    //                 json = JSON.parse(json);
    //             }
    //             global.uuid = json.userid;
    //             global.username = username;
    //             setTimeout(() => {
    //                 location.reload();
    //             }, 500);
    //         } else {
    //             toaster.show('Login failed', {type: 'error'});
    //         }
    //     })
    //     .catch(err => {
    //         loginLoading.value = false;
    //         toaster.show('Login failed', {type: 'error'});
    //     });
    router.push('/main')
}





</script>

<style scoped lang="scss">
.login-page {
  height: 100vh;
  width: 100vw;
  position: relative;
  overflow: hidden;
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

/* Animation classes from index.vue */
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
</style>