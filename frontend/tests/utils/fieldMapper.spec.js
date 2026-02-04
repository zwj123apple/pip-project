import { describe, it, expect } from "vitest";
import {
  loanFormFieldMap,
  loanFormFieldReverseMap,
  convertLoanFormToBackend,
} from "../../src/utils/fieldMapper";

describe("fieldMapper", () => {
  describe("loanFormFieldMap", () => {
    it("应该包含所有必要的字段映射", () => {
      expect(loanFormFieldMap.entName).toBe("ent_name");
      expect(loanFormFieldMap.uscc).toBe("uscc");
      expect(loanFormFieldMap.loanAmount).toBe("loan_amount");
    });
  });

  describe("loanFormFieldReverseMap", () => {
    it("应该是正向映射的反向", () => {
      expect(loanFormFieldReverseMap.ent_name).toBe("entName");
      expect(loanFormFieldReverseMap.uscc).toBe("uscc");
      expect(loanFormFieldReverseMap.loan_amount).toBe("loanAmount");
    });
  });

  describe("convertLoanFormToBackend", () => {
    it("应该正确转换前端格式到后端格式", () => {
      const frontendData = {
        entName: "测试企业",
        uscc: "123456789012345678",
        loanAmount: 1000000,
      };

      const backendData = convertLoanFormToBackend(frontendData);

      expect(backendData.ent_name).toBe("测试企业");
      expect(backendData.uscc).toBe("123456789012345678");
      expect(backendData.loan_amount).toBe(1000000);
    });

    it("应该保留未映射的字段", () => {
      const frontendData = {
        entName: "测试企业",
        customField: "自定义值",
      };

      const backendData = convertLoanFormToBackend(frontendData);

      expect(backendData.ent_name).toBe("测试企业");
      expect(backendData.customField).toBe("自定义值");
    });
  });
});
