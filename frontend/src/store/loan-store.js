/**
 * 贷款申请数据管理store
 */
import { defineStore } from "pinia";

export const useLoanStore = defineStore("loan", {
  state: () => ({
    // 当前的贷款申请数据
    currentLoanData: null,
    // 财务数据
    financialData: [],
  }),

  actions: {
    /**
     * 设置贷款申请数据
     * @param {Object} data - 贷款申请数据
     */
    setLoanData(data) {
      this.currentLoanData = data;

      // 保存到sessionStorage
      try {
        sessionStorage.setItem("loanData", JSON.stringify(data));
      } catch (error) {
        console.error("保存数据到sessionStorage失败:", error);
      }
    },

    /**
     * 获取贷款申请数据
     * @returns {Object} 贷款申请数据
     */
    getLoanData() {
      if (!this.currentLoanData) {
        // 尝试从sessionStorage恢复
        const savedData = sessionStorage.getItem("loanData");
        if (savedData) {
          try {
            this.currentLoanData = JSON.parse(savedData);
          } catch (error) {
            console.error("从sessionStorage恢复数据失败:", error);
          }
        }
      }
      return this.currentLoanData;
    },

    /**
     * 清除贷款申请数据
     */
    clearLoanData() {
      this.currentLoanData = null;
      sessionStorage.removeItem("loanData");
    },

    /**
     * 设置财务数据
     * @param {Array} data - 财务数据数组
     */
    setFinancialData(data) {
      this.financialData = data;
    },

    /**
     * 获取财务数据
     * @returns {Array} 财务数据数组
     */
    getFinancialData() {
      return this.financialData;
    },
  },
});
