<template>
  <div class="l-login">
    <div class="square left-bottom hu_hu_animation bg-secondary"></div>
    <div class="square top-right blockR bg-secondary-darken-1"></div>
    <div class="home d-flex align-center justify-center">
      <div class="content">
        <h1 class="title">欢迎来到我们的应用</h1>
        <p class="description">请登录或注册以继续</p>
        <div class="buttons">
          <v-btn color="primary" large @click="goToLogin">
            Login
          </v-btn>
          <v-btn color="secondary" large @click="goToRegister">
            Register
          </v-btn>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

function goToLogin() {
  router.push('/login')
}

function goToRegister() {
  router.push('/register')
}
</script>

<style scoped lang="scss">
.l-login {
  transition: opacity 0.8s ease-in-out;
  position: fixed;
  height: 100%;
  width: 100%;
  top: 0;
  left: 0;
  opacity: 1;
  z-index: 100;
  text-align: center;
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

.home {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  font-size: 1.6rem;
  padding: 20px;
}

.content {
  background: rgba(255, 255, 255, 0.85);
  padding: 40px 60px;
  border-radius: 12px;
  box-shadow: 0 3px 15px rgba(0, 0, 0, 0.2);
}

.title {
  margin-bottom: 10px;
  font-weight: bold;
}

.description {
  margin-bottom: 20px;
}

.buttons {
  display: flex;
  gap: 20px;
  justify-content: center;
}

/* Animations */
@keyframes block {
  0% {
    left: -100px;
  }
  50% {
    left: -95px;
  }
  100% {
    left: -100px;
  }
}

@keyframes blockR {
  0% {
    right: -100px;
  }
  60% {
    right: -95px;
  }
  100% {
    right: -100px;
  }
}

.hu_hu_animation {
  animation-name: block;
  animation-duration: 2.5s;
  animation-fill-mode: forwards;
  animation-iteration-count: infinite;
  animation-timing-function: ease-in-out;
}

.blockR {
  animation-name: blockR;
  animation-duration: 2.5s;
  animation-fill-mode: forwards;
  animation-iteration-count: infinite;
  animation-timing-function: ease-in-out;
}

/* Optional background color classes */
.bg-secondary {
  background-color: #6b73ff;
}

.bg-secondary-darken-1 {
  background-color: #000dff;
}
</style>