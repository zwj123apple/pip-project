import { describe, it, expect, vi, beforeEach } from "vitest";
import { mount } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";
import AppHeader from "../../src/components/AppHeader.vue";
import { useUserStore } from "../../src/store/user-store";

vi.mock("../../src/api/auth", () => ({
  authApi: {
    logout: vi.fn().mockResolvedValue({ code: 0 }),
  },
}));

vi.mock("vue-router", () => ({
  useRoute: () => ({
    name: "Home",
  }),
}));

describe("AppHeader", () => {
  let wrapper;
  let userStore;

  beforeEach(() => {
    setActivePinia(createPinia());
    userStore = useUserStore();

    // 模拟已登录用户
    userStore.token = "test-token";
    userStore.userInfo = {
      username: "testuser",
      user_type: "ENTERPRISE",
    };

    wrapper = mount(AppHeader, {
      global: {
        stubs: {
          ElIcon: true,
          SwitchButton: true,
        },
      },
    });
  });

  it("应该正确渲染", () => {
    expect(wrapper.exists()).toBe(true);
  });

  it("应该显示Logo", () => {
    expect(wrapper.find(".logo").text()).toBe("金融贷款系统");
  });

  it("应该显示用户信息", () => {
    expect(wrapper.find(".username").text()).toBe("testuser");
  });

  it("应该显示用户类型标签", () => {
    const tag = wrapper.find(".el-tag");
    expect(tag.exists()).toBe(true);
  });

  it("应该显示退出登录按钮", () => {
    const button = wrapper.find("button");
    expect(button.text()).toContain("退出登录");
  });

  it("未登录时不应该显示header", async () => {
    userStore.token = "";
    await wrapper.vm.$nextTick();
    expect(wrapper.find(".app-header").exists()).toBe(false);
  });
});
