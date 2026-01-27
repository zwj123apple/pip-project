/**
 * 贷款申请表单字段映射（前端 -> 后端）
 * 用于提交数据时的字段转换
 */
export const loanFormFieldMap = {
  entName: "ent_name",
  uscc: "uscc",
  companyEmail: "company_email",
  companyAddress: "company_address",
  repayAccountBank: "repay_account_bank",
  repayAccountNo: "repay_account_no",
  loanAmount: "loan_amount",
  loanTerm: "loan_term",
  loanPurpose: "loan_purpose",
  propProofType: "prop_proof_type",
  industryCategory: "industry_category",
};

/**
 * 贷款申请表单字段反向映射（后端 -> 前端）
 * 用于接收数据时的字段转换
 */
export const loanFormFieldReverseMap = Object.fromEntries(
  Object.entries(loanFormFieldMap).map(([key, value]) => [value, key]),
);

/**
 * 转换贷款表单数据（前端格式 -> 后端格式）
 * @param {Object} frontendData - 前端格式的数据
 * @returns {Object} 后端格式的数据
 */
export const convertLoanFormToBackend = (frontendData) => {
  const backendData = {};

  Object.keys(frontendData).forEach((key) => {
    const backendKey = loanFormFieldMap[key] || key;
    backendData[backendKey] = frontendData[key];
  });

  return backendData;
};
