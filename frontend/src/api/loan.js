/**
 * 贷款申请相关的API
 */
import request from "@/utils/request";

/**
 * 验证数据并上传文件（不保存到数据库）
 * 同时返回财务图表数据
 * @param {FormData} formData - 表单数据（包含文件）
 * @returns {Promise}
 */
export function validateAndUpload(formData) {
  return request({
    url: "/loan/apply",
    method: "post",
    data: formData,
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
}

/**
 * 确认并保存贷款申请到数据库
 * @param {FormData} formData - 表单数据
 * @returns {Promise}
 */
export function confirmLoan(formData) {
  return request({
    url: "/loan/confirm",
    method: "post",
    data: formData,
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
}
