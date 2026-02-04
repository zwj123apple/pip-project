import { describe, it, expect, vi, beforeEach } from "vitest";
import { mount } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";
import ResultPage from "../../src/pages/result-page.vue";

const mockPush = vi.fn();
vi.mock("vue-router", () => ({
  useRouter: () => ({
    push: mockPush,
  }),
}));

describe("ResultPage", () => {
  let wrapper;

  beforeEach(() => {
    setActivePinia(createPinia());
    mockPush.mockClear();
    wrapper = mount(ResultPage);
  });

  it("应该正确渲染", () => {
    expect(wrapper.exists()).toBe(true);
  });

  it("应该显示结果页标题", () => {
    expect(wrapper.find("h1").text()).toContain(
      "Risk Information Loan Decision Notification",
    );
  });

  it("应该显示风险等级", () => {
    const riskBadge = wrapper.find(".risk-badge");
    expect(riskBadge.exists()).toBe(true);
    expect(riskBadge.text()).toBe("medium");
  });

  it("应该显示信息提示", () => {
    const infoBox = wrapper.find(".info-box");
    expect(infoBox.exists()).toBe(true);
    expect(infoBox.text()).toContain("additional materials");
  });

  it("点击重新评估按钮应该跳转到输入页面", async () => {
    const button = wrapper.find(".btn-reevaluation");
    await button.trigger("click");
    expect(mockPush).toHaveBeenCalledWith("/input");
  });
});
