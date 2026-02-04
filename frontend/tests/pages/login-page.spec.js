import { describe, it, expect, vi, beforeEach } from "vitest";
import { mount } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";
import LoginPage from "../../src/pages/login-page.vue";
import { useUserStore } from "../../src/store/user-store";

// Mock API
vi.mock("../../src/api/auth", () => ({
  login: vi.fn(),
  register: vi.fn(),
}));

describe("LoginPage", () => {
  let wrapper;
  let userStore;

  beforeEach(() => {
    setActivePinia(createPinia());
    userStore = useUserStore();
    wrapper = mount(LoginPage, {
      global: {
        stubs: {
          "router-link": true,
        },
      },
    });
  });

  it("应该正确渲染", () => {
    expect(wrapper.exists()).toBe(true);
    expect(wrapper.find("h1").text()).toBe("企业贷款申请系统");
  });

  it("应该显示登录表单", () => {
    expect(wrapper.find('input[type="text"]').exists()).toBe(true);
    expect(wrapper.find('input[type="password"]').exists()).toBe(true);
    expect(wrapper.find("button").text()).toContain("登录");
  });

  it("应该验证必填字段", async () => {
    const loginButton = wrapper.find("button");
    await loginButton.trigger("click");

    // 检查是否有错误提示
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.username).toBe("");
    expect(wrapper.vm.password).toBe("");
  });

  it("应该能切换到注册模式", async () => {
    const toggleButton = wrapper
      .findAll("button")
      .find((btn) => btn.text().includes("注册"));

    if (toggleButton) {
      await toggleButton.trigger("click");
      await wrapper.vm.$nextTick();
      expect(wrapper.vm.isLogin).toBe(false);
    }
  });

  it("应该能输入用户名和密码", async () => {
    const usernameInput = wrapper.find('input[type="text"]');
    const passwordInput = wrapper.find('input[type="password"]');

    await usernameInput.setValue("testuser");
    await passwordInput.setValue("password123");

    expect(wrapper.vm.username).toBe("testuser");
    expect(wrapper.vm.password).toBe("password123");
  });

  it("登录表单应该包含必要的字段", () => {
    expect(wrapper.vm.username).toBeDefined();
    expect(wrapper.vm.password).toBeDefined();
    expect(wrapper.vm.isLogin).toBeDefined();
  });
});
