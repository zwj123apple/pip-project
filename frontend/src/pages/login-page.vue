<template>
  <div class="login-container">
    <el-card class="login-card">
      <div class="card-header">
        <h2>Login</h2>
      </div>

      <el-form
        ref="loginFormRef"
        :model="loginForm"
        :rules="loginRules"
        label-position="top"
        @submit.prevent="handleLogin"
      >
        <el-form-item label="User Id" prop="userId">
          <el-input v-model="loginForm.userId" placeholder="" clearable />
        </el-form-item>

        <el-form-item label="Password" prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder=""
            maxlength="8"
            show-password
            clearable
          />
        </el-form-item>

        <el-form-item class="login-button-item">
          <el-button
            type="success"
            :loading="loading"
            class="login-button"
            @click="handleLogin"
          >
            login
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from "vue";
import { useUserStore } from "@/store/user-store";

const userStore = useUserStore();
const loginFormRef = ref(null);
const loading = ref(false);

const loginForm = reactive({
  userId: "",
  password: "",
});

// 验证规则
const loginRules = {
  userId: [
    { required: true, message: "Please enter User Id", trigger: "blur" },
  ],
  password: [
    { required: true, message: "Please enter Password", trigger: "blur" },
    {
      min: 8,
      max: 8,
      message: "Password must be exactly 8 characters",
      trigger: "blur",
    },
    {
      pattern: /^[a-zA-Z0-9]+$/,
      message: "Password must contain only letters and numbers",
      trigger: "blur",
    },
  ],
};

const handleLogin = async () => {
  if (!loginFormRef.value) return;

  // 前端验证
  try {
    await loginFormRef.value.validate();
  } catch (error) {
    return;
  }

  // 提交登录
  loading.value = true;

  try {
    await userStore.login({
      user_name: loginForm.userId,
      password: loginForm.password,
    });
    // 登录成功/失败提示已在user-store.js中统一处理
  } catch (error) {
    console.error("登录失败:", error);
    // 错误提示已在user-store.js中统一处理,不在这里重复显示
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: #f5f5f5;
  padding: 20px;
  box-sizing: border-box;
  width: 100%;
}

.login-card {
  width: 400px;
  max-width: 100%;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.card-header {
  text-align: center;
  padding: 20px 0;
}

.card-header h2 {
  margin: 0;
  color: #303133;
  font-size: 36px;
  font-weight: 600;
}

:deep(.el-form-item) {
  margin-bottom: 28px;
}

:deep(.el-form-item__label) {
  color: #303133;
  font-weight: 600;
  font-size: 16px;
}

:deep(.el-form-item__content) {
  justify-content: center;
}

:deep(.el-form-item__error) {
  padding-top: 4px;
  padding-bottom: 4px;
}

:deep(.el-input__wrapper) {
  display: flex;
  align-items: center;
}

:deep(.el-input__inner) {
  line-height: normal;
}

.login-button-item {
  margin-top: 40px;
  margin-bottom: 0;
  display: flex;
  justify-content: center;
}

.login-button {
  width: 50%;
  min-width: 120px;
  background-color: #82b366;
  border-color: #82b366;
  font-size: 16px;
  padding: 12px 20px;
  border-radius: 5px;
}

.login-button:hover {
  background-color: #6fa05a;
  border-color: #6fa05a;
}

/* 中等屏幕适配 */
@media (max-width: 992px) {
  .login-container {
    padding: 15px;
  }
}

/* 响应式设计 - 平板适配 */
@media (max-width: 768px) {
  .login-container {
    padding: 12px;
  }

  .login-card {
    max-width: 100%;
  }

  .card-header h2 {
    font-size: 28px;
  }

  :deep(.el-form-item__label) {
    font-size: 14px;
  }

  .login-button {
    width: 70%;
    font-size: 14px;
    padding: 10px 16px;
  }
}

/* 小屏手机适配 */
@media (max-width: 480px) {
  .login-container {
    padding: 10px;
  }

  .card-header {
    padding: 15px 0;
  }

  .card-header h2 {
    font-size: 24px;
  }

  .login-button {
    width: 80%;
    min-width: 100px;
  }

  .login-button-item {
    margin-top: 30px;
  }
}

/* 超小屏手机适配 */
@media (max-width: 360px) {
  .login-container {
    padding: 8px;
  }

  .card-header h2 {
    font-size: 20px;
  }
}
</style>
