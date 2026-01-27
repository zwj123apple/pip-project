import { createRouter, createWebHistory } from "vue-router";
import { ElMessage } from "element-plus";

const routes = [
  {
    path: "/",
    redirect: "/login",
  },
  {
    path: "/login",
    name: "Login",
    component: () => import("@/pages/login-page.vue"),
    meta: { requiresAuth: false },
  },
  {
    path: "/personal",
    name: "Personal",
    component: () => import("@/pages/personal-page.vue"),
    meta: { requiresAuth: true, userType: "INDIVIDUAL" },
  },
  {
    path: "/input",
    name: "EnterpriseInput",
    component: () => import("@/pages/enterprise-input-page.vue"),
    meta: { requiresAuth: true, userType: "ENTERPRISE" },
  },
  {
    path: "/confirm",
    name: "EnterpriseConfirm",
    component: () => import("@/pages/enterprise-confirm-page.vue"),
    meta: { requiresAuth: true, userType: "ENTERPRISE" },
  },
  {
    path: "/result",
    name: "Result",
    component: () => import("@/pages/result-page.vue"),
    meta: { requiresAuth: true, userType: "ENTERPRISE" },
  },
  {
    path: "/:pathMatch(.*)*",
    name: "NotFound",
    component: () => import("@/pages/not-found-page.vue"),
    meta: { requiresAuth: false },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("token");
  const userInfo = JSON.parse(localStorage.getItem("userInfo") || "null");

  if (to.meta.requiresAuth) {
    if (!token) {
      ElMessage.warning("请先登录");
      next("/login");
      return;
    }

    if (to.meta.userType && userInfo?.user_type !== to.meta.userType) {
      ElMessage.error("没有权限访问该页面");

      if (userInfo?.user_type === "INDIVIDUAL") {
        next("/personal");
      } else if (userInfo?.user_type === "ENTERPRISE") {
        next("/input");
      } else {
        next("/login");
      }
      return;
    }
  }

  if ((to.path === "/login" || to.path === "/register") && token) {
    if (userInfo?.user_type === "INDIVIDUAL") {
      next("/personal");
    } else if (userInfo?.user_type === "ENTERPRISE") {
      next("/input");
    } else {
      next();
    }
    return;
  }

  next();
});

export default router;
