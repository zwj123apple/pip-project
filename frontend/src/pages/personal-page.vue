<template>
  <div class="personal-page">
    <el-card class="content-card">
      <div class="content">
        <h1>Individual Loan Application</h1>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { onMounted } from "vue";
import { authApi } from "@/api/auth";

// 页面初始化时验证token
onMounted(async () => {
  try {
    await authApi.testToken();
    console.log("Token验证成功");
  } catch (error) {
    // token过期或无效时，request.js的拦截器会自动处理跳转
    console.log("Token验证失败，将跳转到登录页");
  }
});
</script>

<style scoped>
.personal-page {
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f5f5f5;
  padding: 20px;
}

.content-card {
  max-width: 800px;
  width: 100%;
}

.content {
  text-align: center;
  padding: 60px 40px;
}

.content h1 {
  font-size: 32px;
  color: #303133;
  margin: 0 0 20px 0;
}
</style>
