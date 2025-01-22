<template>
  <div class="l-login">
    <div class="square left-bottom hu_hu_animation bg-secondary">
    </div>
    <div class="square top-right blockR bg-secondary-darken-1">
    </div>
    <div class="home d-flex align-center justify-center" style="min-height: 300px;">
      <h1 class="title">{{ greeting }}</h1>
      <p class="description">
        {{ $t('homePageDescription') }}
      </p>
      <br>
      <v-btn append-icon="mdi-login-variant" color="primary" variant="flat" size="large" @click="handleLoginBtn">
        Login</v-btn>
    </div>
  </div>

</template>

<script setup lang="ts">
  import { useLocale } from 'vuetify';
  import { useAppStore } from '@/stores/app';

  //i18n
  const { t } = useLocale()
  const store = useAppStore()
  // route
  // const route = useRoute()
  // // router
  const router = useRouter()
  // greeting
  const greeting = computed(() => {
    return store.isLogin ? t('homePageWelcomeBack') + store.username : t('homePageWelcome')
  })
  function handleLoginBtn() {
    if(!store.isLogin){
      router.push('/Login')
    }else {
      router.push('/main')
    }
  }

</script>

