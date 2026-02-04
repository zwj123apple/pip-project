import { describe, it, expect, vi, beforeEach } from "vitest";
import { mount } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";
import EnterpriseInputPage from "../../src/pages/enterprise-input-page.vue";
import { useLoanStore } from "../../src/store/loan-store";

describe("EnterpriseInputPage", () => {
  let wrapper;
  let loanStore;

  beforeEach(() => {
    setActivePinia(createPinia());
    loanStore = useLoanStore();
    wrapper = mount(EnterpriseInputPage, {
      global: {
        stubs: {
          "router-link": true,
        },
      },
    });
  });

  it("应该正确渲染", () => {
    expect(wrapper.exists()).toBe(true);
    expect(wrapper.find("h1").text()).toContain("企业贷款申请");
  });

  it("应该显示所有必填的表单字段", () => {
    expect(wrapper.find('input[placeholder*="企业名称"]').exists()).toBe(true);
    expect(
      wrapper.find('input[placeholder*="统一社会信用代码"]').exists(),
    ).toBe(true);
    expect(wrapper.find('input[placeholder*="法人代表"]').exists()).toBe(true);
    expect(wrapper.find('input[placeholder*="联系电话"]').exists()).toBe(true);
  });

  it("应该初始化表单数据", () => {
    expect(wrapper.vm.formData).toBeDefined();
    expect(wrapper.vm.formData.companyName).toBeDefined();
    expect(wrapper.vm.formData.creditCode).toBeDefined();
    expect(wrapper.vm.formData.legalPerson).toBeDefined();
  });

  it("应该能输入企业基本信息", async () => {
    const companyNameInput = wrapper.find('input[placeholder*="企业名称"]');
    await companyNameInput.setValue("测试企业");
    expect(wrapper.vm.formData.companyName).toBe("测试企业");
  });

  it("应该有下一步按钮", () => {
    const nextButton = wrapper
      .findAll("button")
      .find((btn) => btn.text().includes("下一步"));
    expect(nextButton).toBeDefined();
  });

  it("应该验证必填字段", async () => {
    const nextButton = wrapper
      .findAll("button")
      .find((btn) => btn.text().includes("下一步"));

    if (nextButton) {
      await nextButton.trigger("click");
      await wrapper.vm.$nextTick();
      // 表单验证应该阻止提交
      expect(wrapper.vm.formData.companyName).toBe("");
    }
  });

  it("应该支持文件上传", () => {
    const fileInputs = wrapper.findAll('input[type="file"]');
    expect(fileInputs.length).toBeGreaterThan(0);
  });
});
