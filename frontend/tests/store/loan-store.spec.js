import { describe, it, expect, beforeEach, vi } from "vitest";
import { setActivePinia, createPinia } from "pinia";
import { useLoanStore } from "../../src/store/loan-store";

describe("useLoanStore", () => {
  let store;

  beforeEach(() => {
    setActivePinia(createPinia());
    store = useLoanStore();
    sessionStorage.clear();
  });

  it("应该初始化为空状态", () => {
    expect(store.currentLoanData).toBeNull();
    expect(store.financialData).toEqual([]);
  });

  it("应该正确设置贷款数据", () => {
    const testData = {
      entName: "测试企业",
      loanAmount: 1000000,
    };

    store.setLoanData(testData);

    expect(store.currentLoanData).toEqual(testData);
  });

  it("应该正确获取贷款数据", () => {
    const testData = {
      entName: "测试企业",
      loanAmount: 1000000,
    };

    store.setLoanData(testData);
    const retrieved = store.getLoanData();

    expect(retrieved).toEqual(testData);
  });

  it("应该能清除贷款数据", () => {
    const testData = {
      entName: "测试企业",
      loanAmount: 1000000,
    };

    store.setLoanData(testData);
    store.clearLoanData();

    expect(store.currentLoanData).toBeNull();
  });

  it("应该正确设置和获取财务数据", () => {
    const financialData = [
      { quarter: "2023Q1", profit: 100000 },
      { quarter: "2023Q2", profit: 120000 },
    ];

    store.setFinancialData(financialData);

    expect(store.getFinancialData()).toEqual(financialData);
  });

  it("应该将数据保存到sessionStorage", () => {
    const testData = {
      entName: "测试企业",
      loanAmount: 1000000,
    };

    store.setLoanData(testData);

    const saved = sessionStorage.getItem("loanData");
    expect(saved).toBeDefined();
    expect(JSON.parse(saved)).toEqual(testData);
  });
});
