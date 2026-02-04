<template>
  <header class="app-header" v-if="route.name !== 'Login' && isLoggedIn">
    <div class="header-container">
      <div class="header-left">
        <h1 class="logo">金融贷款系统</h1>
      </div>

      <div class="header-right">
        <div class="user-info">
          <span class="username">{{ userInfo?.username || "用户" }}</span>
          <el-tag
            :type="userInfo?.user_type === 'INDIVIDUAL' ? 'success' : 'primary'"
            size="small"
          >
            {{ userInfo?.user_type === "INDIVIDUAL" ? "个人用户" : "企业用户" }}
          </el-tag>
        </div>

        <el-button
          type="danger"
          size="default"
          @click="handleLogout"
          :loading="loading"
        >
          <el-icon style="margin-right: 5px"><SwitchButton /></el-icon>
          退出登录
        </el-button>
      </div>
    </div>
  </header>
</template>

<script setup>
import { computed, ref } from "vue";
import { useUserStore } from "@/store/user-store";
import { ElMessageBox } from "element-plus";
import { SwitchButton } from "@element-plus/icons-vue";
import { authApi } from "@/api/auth";
import { useRoute } from "vue-router";

const route = useRoute();
const userStore = useUserStore();
const loading = ref(false);

const isLoggedIn = computed(() => userStore.isLoggedIn);
const userInfo = computed(() => userStore.userInfo);

const handleLogout = async () => {
  try {
    await ElMessageBox.confirm("确定要退出登录吗？", "提示", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
    });

    loading.value = true;

    // 调用后端退出接口
    try {
      await authApi.logout();
    } catch (error) {
      console.error("后端退出接口调用失败:", error);
      // 即使后端接口失败，也继续清除前端状态
    }

    // 清除前端状态
    userStore.logout();
  } catch (error) {
    // 用户取消操作
    if (error !== "cancel") {
      console.error("退出登录失败:", error);
    }
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.app-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
}

.header-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  height: 64px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  display: flex;
  align-items: center;
}

.logo {
  font-size: 24px;
  font-weight: bold;
  color: white;
  margin: 0;
  letter-spacing: 1px;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
  color: white;
}

.username {
  font-size: 14px;
  font-weight: 500;
}

.el-button {
  font-weight: 500;
}
</style>
