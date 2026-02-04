<template>
  <div class="enterprise-confirm-page">
    <div class="confirm-container">
      <h1 class="page-title">Loan Information Confirmation</h1>

      <div class="section-tabs">
        <div class="tab active">Corporation Loan</div>
      </div>

      <!-- 基本信息 -->
      <div class="info-section">
        <div class="info-row">
          <div class="info-field">
            <label>Company Name</label>
            <div class="field-value">{{ loanData.entName || "" }}</div>
          </div>
        </div>

        <div class="info-row">
          <div class="info-field">
            <label>Uscc</label>
            <div class="field-value">{{ loanData.uscc || "" }}</div>
          </div>
        </div>

        <div class="info-row">
          <div class="info-field">
            <label>Company Email</label>
            <div class="field-value">{{ loanData.companyEmail || "" }}</div>
          </div>
        </div>

        <div class="info-row">
          <div class="info-field">
            <label>Company Address</label>
            <div class="field-value">{{ loanData.companyAddress || "" }}</div>
          </div>
        </div>

        <div class="info-row">
          <div class="info-field">
            <label>Repay Account Bank</label>
            <div class="field-value">{{ displayData.repayAccountBank }}</div>
          </div>
        </div>

        <div class="info-row">
          <div class="info-field">
            <label>Repay Account No</label>
            <div class="field-value">{{ loanData.repayAccountNo || "" }}</div>
          </div>
        </div>

        <div class="info-row">
          <div class="info-field">
            <label>Loan Amount</label>
            <div class="field-value">
              {{
                loanData.loanAmount !== null &&
                loanData.loanAmount !== undefined
                  ? loanData.loanAmount
                  : ""
              }}
            </div>
          </div>
        </div>

        <div class="info-row">
          <div class="info-field">
            <label>Loan Term</label>
            <div class="field-value">{{ displayData.loanTerm }}</div>
          </div>
        </div>

        <div class="info-row">
          <div class="info-field">
            <label>Loan Purpose</label>
            <div class="field-value">{{ displayData.loanPurpose }}</div>
          </div>
        </div>

        <div class="info-row">
          <div class="info-field">
            <label>Property Proof Type</label>
            <div class="field-value">{{ displayData.propProofType }}</div>
          </div>
        </div>

        <div class="info-row">
          <div class="info-field">
            <label>Property Proof Document</label>
            <div class="field-value">
              {{ loanData.fileName || "" }}
            </div>
          </div>
        </div>

        <div class="info-row">
          <div class="info-field">
            <label>Industry Category</label>
            <div class="field-value">
              {{ displayData.industryCategory || "" }}
            </div>
          </div>
        </div>
      </div>

      <!-- 财务数据图表 -->
      <FinancialChart :data="financialData" />

      <!-- 操作按钮 -->
      <div class="button-group">
        <button class="btn-back" @click="handleBack">back</button>
        <button class="btn-confirm" @click="handleConfirm" :disabled="loading">
          {{ loading ? "Processing..." : "confirm" }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed, onActivated } from "vue";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";
import { confirmLoan, validateAndUpload } from "@/api/loan";
import { useLoanStore } from "@/store/loan-store";
import FinancialChart from "@/components/FinancialChart.vue";
import {
  bankOptions,
  loanTermOptions,
  loanPurposeOptions,
  industryCategoryOptions,
  getLabelByValue,
  getPropertyProofTypeLabel,
} from "@/constants/formOptions";
import { convertLoanFormToBackend } from "@/utils/fieldMapper";

const router = useRouter();
const loanStore = useLoanStore();
const loading = ref(false);
const refreshing = ref(false);
const financialData = ref([]);

// 使用 computed 而不是 reactive，确保响应 store 的变化
const loanData = computed(() => loanStore.getLoanData() || {});

const displayData = computed(() => {
  return {
    repayAccountBank: getLabelByValue(
      bankOptions,
      loanData.value.repayAccountBank,
    ),
    loanTerm: getLabelByValue(loanTermOptions, loanData.value.loanTerm),
    loanPurpose: getLabelByValue(
      loanPurposeOptions,
      loanData.value.loanPurpose,
    ),
    propProofType: getPropertyProofTypeLabel(
      loanData.value.loanPurpose,
      loanData.value.propProofType,
    ),
    industryCategory: getLabelByValue(
      industryCategoryOptions,
      loanData.value.industryCategory,
    ),
  };
});

if (!loanData.value.entName) {
  ElMessage.warning("请先填写贷款申请信息");
  router.push("/input");
}

const loadFinancialData = () => {
  if (loanData.value.financialData && loanData.value.financialData.length > 0) {
    financialData.value = loanData.value.financialData;
  } else {
    ElMessage.warning("未找到财务数据");
  }
};

// 创建FormData的公共函数
const createFormData = () => {
  const formData = new FormData();
  const backendData = convertLoanFormToBackend(loanData.value);

  // 添加表单字段
  Object.keys(backendData).forEach((key) => {
    const value = backendData[key];
    // 修复：0 也应该被添加，只排除 null, undefined, 空字符串，以及特殊字段
    if (
      value !== null &&
      value !== undefined &&
      value !== "" &&
      key !== "financialData" &&
      key !== "propProofDocsPath"
    ) {
      formData.append(key, value);
    }
  });

  if (loanData.value.propProofDocsPath) {
    formData.append("prop_proof_docs", loanData.value.propProofDocsPath);
  }
  if (loanData.value.fileName) {
    formData.append("prop_proof_docs_name", loanData.value.fileName);
  }

  return formData;
};

// 处理错误的公共函数
const handleError = (error) => {
  console.error("操作失败:", error);

  if (error.isAuthError) {
    return;
  }

  if (error.response?.data) {
    const errorData = error.response.data;
    const errors = errorData.data?.errors;

    if (errors && Array.isArray(errors)) {
      // 使用HTML换行符连接多个错误消息
      const errorMessages = errors.map((err) => err.msg).join("<br>");
      ElMessage.error({
        message: errorMessages || "操作失败，请稍后重试",
        dangerouslyUseHTMLString: true,
        duration: 5000,
      });
    } else {
      ElMessage.error(
        errorData.message || errorData.msg || "操作失败，请稍后重试",
      );
    }
  } else if (error.message) {
    ElMessage.error(error.message);
  } else {
    ElMessage.error("网络错误，请检查网络连接");
  }
};

// 重新从服务器获取最新的财务数据（不需要重新上传文件）
const refreshFinancialData = async () => {
  if (refreshing.value) return;

  refreshing.value = true;

  try {
    const formData = createFormData();
    const response = await validateAndUpload(formData);

    if (response.code === 0 && response.data.financial_data) {
      financialData.value = response.data.financial_data;
      loanStore.setLoanData({
        ...loanData.value,
        financialData: response.data.financial_data,
      });
    }
  } catch (error) {
    // 静默失败，不影响用户体验
  } finally {
    refreshing.value = false;
  }
};

const handleBack = () => {
  router.push("/input");
};

const handleConfirm = async () => {
  loading.value = true;

  try {
    const formData = createFormData();
    const response = await confirmLoan(formData);

    if (response.code === 0) {
      ElMessage.success(response.msg || "贷款申请提交成功");

      // 保留文件名到 store，以便 result 页面使用
      loanStore.setLoanData({
        ...loanData.value,
        fileName: loanData.value.fileName,
      });

      router.push("/result");
    } else {
      ElMessage.error(response.msg || "提交失败");
    }
  } catch (error) {
    handleError(error);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  loadFinancialData();
});

// 当从其他页面返回时，重新加载最新的财务数据
onActivated(() => {
  refreshFinancialData();
});
</script>

<style scoped>
.enterprise-confirm-page {
  min-height: 100vh;
  background-color: #f5f5f5;
  padding: 20px;
}

.confirm-container {
  max-width: 960px;
  margin: 0 auto;
  background: white;
  padding: 30px;
  border-radius: 8px;
}

.page-title {
  font-size: 32px;
  font-weight: bold;
  color: #333;
  margin: 0 0 30px 0;
  text-align: center;
}

.section-tabs {
  margin-bottom: 30px;
  position: relative;
}

.tab {
  display: inline-block;
  padding: 10px 0;
  font-size: 18px;
  color: #333;
  font-weight: 500;
  position: relative;
  margin-bottom: -1px;
}

.tab::after {
  content: "";
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  height: 3px;
  width: 200px;
  background-color: #4caf50;
}

.info-section {
  margin-bottom: 30px;
}

.info-row {
  margin-bottom: 20px;
}

.info-field label {
  display: block;
  font-size: 16px;
  font-weight: bold;
  color: #333;
  margin-bottom: 8px;
}

.field-value {
  width: 100%;
  padding: 12px;
  background-color: #f5f5f5;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  font-size: 14px;
  color: #666;
  min-height: 44px;
}

.button-group {
  display: flex;
  justify-content: center;
  flex-direction: column;
  gap: 10px;
  margin-top: 10px;
  padding-top: 10px;
  width: 250px;
  margin-left: auto;
  margin-right: auto;
}

.btn-back,
.btn-confirm {
  min-width: 200px;
  padding: 12px 10px;
  font-size: 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-back {
  background-color: #f5f5f5;
  color: #666;
}

.btn-back:hover {
  background-color: #e0e0e0;
}

.btn-confirm {
  background-color: #4caf50;
  color: white;
}

.btn-confirm:hover:not(:disabled) {
  background-color: #45a049;
}

.btn-confirm:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
