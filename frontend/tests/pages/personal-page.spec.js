import { describe, it, expect, vi, beforeEach } from "vitest";
import { mount } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";
import PersonalPage from "../../src/pages/personal-page.vue";

vi.mock("../../src/api/auth", () => ({
  authApi: {
    testToken: vi.fn().mockResolvedValue({ code: 0 }),
  },
}));

describe("PersonalPage", () => {
  let wrapper;

  beforeEach(() => {
    setActivePinia(createPinia());
    wrapper = mount(PersonalPage, {
      global: {
        stubs: {
          "router-link": true,
        },
      },
    });
  });

  it("应该正确渲染", () => {
    expect(wrapper.exists()).toBe(true);
  });

  it("应该显示个人贷款申请标题", () => {
    expect(wrapper.find("h1").text()).toContain("Individual Loan Application");
  });

  it("应该在挂载时验证token", () => {
    const { authApi } = require("../../src/api/auth");
    expect(authApi.testToken).toHaveBeenCalled();
  });
});
