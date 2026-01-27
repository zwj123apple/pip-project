<template>
  <div class="not-found-container">
    <el-card class="not-found-card">
      <div class="content">
        <div class="error-code">404</div>
        <h1>页面不存在</h1>
        <p class="description">抱歉，您访问的页面不存在或已被删除</p>

        <div class="actions">
          <el-button type="primary" size="large" @click="goBack">
            <el-icon style="margin-right: 5px"><ArrowLeft /></el-icon>
            返回上一页
          </el-button>
          <el-button size="large" @click="goHome">
            <el-icon style="margin-right: 5px"><HomeFilled /></el-icon>
            返回首页
          </el-button>
        </div>

        <div class="suggestions">
          <p>您可以：</p>
          <ul>
            <li>检查URL地址是否正确</li>
            <li>返回上一页继续浏览</li>
            <li>前往首页重新开始</li>
          </ul>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router";
import { ArrowLeft, HomeFilled } from "@element-plus/icons-vue";
import { useUserStore } from "@/store/user-store";

const router = useRouter();
const userStore = useUserStore();

const goBack = () => {
  router.back();
};

const goHome = () => {
  if (userStore.isLoggedIn) {
    // 根据用户类型跳转到对应首页
    if (userStore.isIndividual) {
      router.push("/personal");
    } else if (userStore.isEnterprise) {
      router.push("/input");
    } else {
      router.push("/login");
    }
  } else {
    router.push("/login");
  }
};
</script>

<style scoped>
.not-found-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.not-found-card {
  max-width: 600px;
  width: 100%;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
}

.content {
  text-align: center;
  padding: 60px 40px;
}

.error-code {
  font-size: 120px;
  font-weight: bold;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 20px;
  line-height: 1;
}

.content h1 {
  font-size: 32px;
  color: #303133;
  margin: 0 0 15px 0;
}

.description {
  font-size: 16px;
  color: #606266;
  margin-bottom: 40px;
}

.actions {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-bottom: 40px;
  flex-wrap: wrap;
}

.suggestions {
  text-align: left;
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f5f7fa;
  border-radius: 8px;
}

.suggestions p {
  font-size: 14px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 10px 0;
}

.suggestions ul {
  margin: 0;
  padding-left: 20px;
}

.suggestions li {
  font-size: 14px;
  color: #606266;
  line-height: 2;
}
</style>
