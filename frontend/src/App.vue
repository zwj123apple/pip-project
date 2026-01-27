<template>
  <div id="app">
    <!-- AppHeader 组件内部已有 v-if="isLoggedIn" 判断，会在登录页自动隐藏 -->
    <AppHeader />
    <router-view />
  </div>
</template>

<script setup>
import AppHeader from "@/components/AppHeader.vue";
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  min-height: 100vh;
  background-color: #f5f5f5;
}
</style>
