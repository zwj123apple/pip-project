/**
 * 表单选项配置文件
 * 统一管理所有下拉框的选项
 */

// 还款账户银行选项
export const bankOptions = [
  { value: "chinaBank", label: "中国银行" },
  { value: "industryBank", label: "工商银行" },
  { value: "businessBank", label: "招商银行" },
];

// 贷款期限选项
export const loanTermOptions = [
  { value: "0.5", label: "6个月" },
  { value: "1", label: "1年" },
  { value: "2", label: "2年" },
  { value: "3", label: "3年" },
  { value: "5", label: "5年" },
  { value: "10", label: "10年" },
  { value: "20", label: "20年" },
  { value: "30", label: "30年" },
];

// 贷款目的选项
export const loanPurposeOptions = [
  { value: "credit", label: "信用贷款" },
  { value: "mortgage", label: "抵押贷款" },
  { value: "tax", label: "税贷" },
];

// 行业类别选项
export const industryCategoryOptions = [
  { value: "01", label: "农林牧渔" },
  { value: "02", label: "基础化工" },
  { value: "03", label: "非银金融" },
];

// 财产证明类型选项（多级映射）
export const propertyProofTypeOptionsMap = {
  credit: [
    { value: "businessLicense", label: "营业执照" },
    { value: "financialStatements", label: "财务报表" },
    { value: "enterpriseCreditReport", label: "企业信用报告" },
    { value: "taxCertification", label: "纳税证明" },
    { value: "bankStatement", label: "银行流水" },
  ],
  mortgage: [
    { value: "estateCertificate", label: "房产证" },
    { value: "landUseCertificate", label: "土地使用权证" },
    { value: "vehicleRegistrationCertificate", label: "车辆登记证" },
    { value: "equipmentCertificate", label: "设备产权证明" },
  ],
  tax: [
    { value: "taxReport", label: "纳税申报表" },
    { value: "taxPaymentCertificate", label: "纳税凭证" },
  ],
};

/**
 * 通用工具函数：根据value获取label
 * @param {Array} options - 选项数组
 * @param {string} value - 选项的value
 * @returns {string} 对应的label，找不到则返回value本身
 */
export const getLabelByValue = (options, value) => {
  const option = options.find((opt) => opt.value === value);
  return option ? option.label : value;
};

/**
 * 根据贷款目的获取对应的财产证明类型选项
 * @param {string} loanPurpose - 贷款目的 (credit/mortgage/tax)
 * @returns {Array} 财产证明类型选项数组
 */
export const getPropertyProofTypeOptions = (loanPurpose) => {
  return propertyProofTypeOptionsMap[loanPurpose] || [];
};

/**
 * 根据贷款目的和财产证明类型value获取label
 * @param {string} loanPurpose - 贷款目的
 * @param {string} proofTypeValue - 财产证明类型的value
 * @returns {string} 对应的label
 */
export const getPropertyProofTypeLabel = (loanPurpose, proofTypeValue) => {
  const options = getPropertyProofTypeOptions(loanPurpose);
  return getLabelByValue(options, proofTypeValue);
};
