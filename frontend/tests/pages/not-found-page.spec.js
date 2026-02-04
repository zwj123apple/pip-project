import { describe, it, expect, vi, beforeEach } from "vitest";
import { mount } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";
import NotFoundPage from "../../src/pages/not-found-page.vue";
import { useUserStore } from "../../src/store/user-store";

const mockPush = vi.fn();
const mockBack = vi.fn();

vi.mock("vue-router", () => ({
  useRouter: () => ({
    push: mockPush,
    back: mockBack,
  }),
}));

describe("NotFoundPage", () => {
  let wrapper;
  let userStore;

  beforeEach(() => {
    setActivePinia(createPinia());
    userStore = useUserStore();
    mockPush.mockClear();
    mockBack.mockClear();

    wrapper = mount(NotFoundPage, {
      global: {
        stubs: {
          ElIcon: true,
          ArrowLeft: true,
          HomeFilled: true,
        },
      },
    });
  });

  it("应该正确渲染", () => {
    expect(wrapper.exists()).toBe(true);
  });

  it("应该显示404错误代码", () => {
    expect(wrapper.find(".error-code").text()).toBe("404");
  });

  it("应该显示页面不存在提示", () => {
    expect(wrapper.find("h1").text()).toContain("页面不存在");
  });

  it("点击返回上一页按钮应该调用router.back", async () => {
    const buttons = wrapper.findAll("button");
    await buttons[0].trigger("click");
    expect(mockBack).toHaveBeenCalled();
  });

  it("未登录用户点击返回首页应跳转到登录页", async () => {
    userStore.isLoggedIn = false;
    const buttons = wrapper.findAll("button");
    await buttons[1].trigger("click");
    expect(mockPush).toHaveBeenCalledWith("/login");
  });

  it("应该显示建议列表", () => {
    const suggestions = wrapper.find(".suggestions ul");
    expect(suggestions.exists()).toBe(true);
    expect(suggestions.findAll("li").length).toBeGreaterThan(0);
  });
});
