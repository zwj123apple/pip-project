import { defineStore } from "pinia";
import { authApi } from "@/api/auth";
import { ElMessage } from "element-plus";
import router from "@/router";
import { useLoanStore } from "@/store/loan-store";

export const useUserStore = defineStore("user", {
  state: () => ({
    token: localStorage.getItem("token") || "",
    userInfo: JSON.parse(localStorage.getItem("userInfo") || "null"),
  }),

  getters: {
    isLoggedIn: (state) => !!state.token,
    userType: (state) => state.userInfo?.user_type || "",
    isIndividual: (state) => state.userInfo?.user_type === "INDIVIDUAL",
    isEnterprise: (state) => state.userInfo?.user_type === "ENTERPRISE",
  },

  actions: {
    async login(loginData) {
      try {
        const response = await authApi.login(loginData);

        // 新响应格式：response.data包含实际数据
        const data = response.data;

        this.token = data.access_token;
        this.userInfo = data.user;

        localStorage.setItem("token", data.access_token);
        localStorage.setItem("userInfo", JSON.stringify(data.user));

        // 清除之前的贷款申请数据（确保每次登录后表单都是空的）
        const loanStore = useLoanStore();
        loanStore.clearLoanData();

        ElMessage.success(response.msg || "登录成功");

        if (data.user.user_type === "INDIVIDUAL") {
          router.push("/personal");
        } else if (data.user.user_type === "ENTERPRISE") {
          router.push("/input");
        }

        return response;
      } catch (error) {
        // 错误处理:
        // - 业务错误(如用户名密码错误): 这里显示ElMessage
        // - 网络错误: request.js已经显示,这里不显示
        if (!error.isNetworkError && !error.isAuthError) {
          const errorMessage =
            error.message || error.response?.data?.msg || "登录失败,请稍后重试";
          ElMessage.error({
            message: errorMessage,
            duration: 3000,
          });
        }
        throw error;
      }
    },

    async logout() {
      try {
        // 尝试调用后端退出接口
        if (this.token) {
          await authApi.logout();
        }
      } catch (error) {
        console.error("后端退出接口调用失败:", error);
        // 即使后端接口失败，也继续清除前端状态
      } finally {
        // 清除前端状态
        this.token = "";
        this.userInfo = null;
        localStorage.removeItem("token");
        localStorage.removeItem("userInfo");
        router.push("/login");
        ElMessage.success("已退出登录");
      }
    },
  },
});
