import axios from "axios";
import { ElMessage } from "element-plus";
import router from "@/router";
import { useUserStore } from "@/store/user-store";

// 开发环境使用代理，生产环境使用完整URL
const API_BASE_URL = import.meta.env.PROD
  ? "http://localhost:5000/api"
  : "/api";

const request = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
  },
});

// 请求拦截器
request.interceptors.request.use(
  (config) => {
    console.log("Request:", config.method?.toUpperCase(), config.url);

    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    console.error("Request Error:", error);
    return Promise.reject(error);
  },
);

// 响应拦截器
request.interceptors.response.use(
  (response) => {
    console.log("Response:", response.status, response.config.url);

    const data = response.data;

    // 检查业务错误码（后端所有响应HTTP状态码都是200）
    if (data && data.code !== undefined && data.code !== 0) {
      const errorMessage = data.msg || "请求失败";

      // 处理认证错误（Token过期或无效）
      if (data.code === 10003) {
        console.warn("Token过期或认证失败:", errorMessage);

        // 清除user-store的状态
        const userStore = useUserStore();
        userStore.token = "";
        userStore.userInfo = null;

        // 清除本地存储
        localStorage.removeItem("token");
        localStorage.removeItem("userInfo");
        sessionStorage.clear();

        // 显示错误消息
        ElMessage.error({
          message: errorMessage,
          duration: 2000,
        });

        // 2.2秒后跳转到登录页（略长于消息显示时间）
        setTimeout(() => {
          router.push("/login");
        }, 2200);
        const authError = new Error(errorMessage);
        authError.isAuthError = true; // 添加特殊标记
        return Promise.reject(authError);
      }
      // 其他业务错误不在这里显示ElMessage,由各业务模块自己处理
      const businessError = new Error(errorMessage);
      businessError.response = response;
      businessError.config = response.config;
      return Promise.reject(businessError);
    }

    return data;
  },
  (error) => {
    console.error("Response Error:", error);

    // 处理网络错误（网络连接失败、超时、数据库连接不上等）
    if (!error.response) {
      ElMessage.error({
        message: "网络连接失败，请检查网络或稍后重试",
        duration: 3000,
      });
      error.isNetworkError = true;
      return Promise.reject(error);
    }

    // 处理HTTP状态码错误(500, 404等)
    if (error.response.status >= 500) {
      ElMessage.error({
        message: "服务器错误，请稍后重试",
        duration: 3000,
      });
    } else if (error.response.status === 404) {
      ElMessage.error({
        message: "请求的资源不存在",
        duration: 3000,
      });
    }

    return Promise.reject(error);
  },
);

export default request;
