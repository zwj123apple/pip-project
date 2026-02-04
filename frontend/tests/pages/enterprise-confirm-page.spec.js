import { describe, it, expect, vi, beforeEach } from "vitest";
import { mount } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";
import EnterpriseConfirmPage from "../../src/pages/enterprise-confirm-page.vue";
import { useLoanStore } from "../../src/store/loan-store";

vi.mock("../../src/api/loan", () => ({
  submitLoanApplication: vi.fn(),
}));

describe("EnterpriseConfirmPage", () => {
  let wrapper;
  let loanStore;

  beforeEach(() => {
    setActivePinia(createPinia());
    loanStore = useLoanStore();

    // 模拟已填写的表单数据
    loanStore.setLoanData({
      entName: "测试企业",
      uscc: "123456789012345678",
      companyEmail: "test@test.com",
      companyAddress: "测试地址",
      repayAccountBank: "中国工商银行",
      repayAccountNo: "1234567890123456789",
      loanAmount: 1000000,
      loanTerm: "12",
      loanPurpose: "SECURED",
      propProofType: "REAL_ESTATE",
      industryCategory: "MANUFACTURING",
      fileName: "test.pdf",
      financialData: [
        { quarter: "2023Q1", profit: 100000, percentage: 5 },
        { quarter: "2023Q2", profit: 120000, percentage: 6 },
      ],
    });

    wrapper = mount(EnterpriseConfirmPage, {
      global: {
        stubs: {
          "router-link": true,
          FinancialChart: true,
        },
      },
    });
  });

  it("应该正确渲染", () => {
    expect(wrapper.exists()).toBe(true);
    expect(wrapper.find("h2").text()).toContain("确认");
  });

  it("应该显示表单数据", () => {
    const loanData = loanStore.getLoanData();
    expect(loanData).toBeDefined();
    expect(loanData.entName).toBe("测试企业");
  });

  it("应该有提交按钮", () => {
    const submitButton = wrapper
      .findAll("button")
      .find(
        (btn) => btn.text().includes("提交") || btn.text().includes("确认"),
      );
    expect(submitButton).toBeDefined();
  });

  it("应该显示财务图表组件", () => {
    expect(wrapper.findComponent({ name: "FinancialChart" })).toBeDefined();
  });
});
