<template>
  <div class="enterprise-input-page">
    <el-card class="form-card">
      <div class="card-header">
        <h2>Corporation Loan Application</h2>
      </div>

      <el-form
        ref="loanFormRef"
        :model="loanForm"
        :rules="rules"
        label-position="top"
        class="loan-form"
      >
        <!-- 基本信息 -->
        <div class="form-section">
          <h3 class="section-title">Basic Information</h3>
          <el-form-item label="Company Name" prop="entName">
            <el-input v-model="loanForm.entName" placeholder="" />
          </el-form-item>

          <el-form-item label="Uscc" prop="uscc">
            <el-input
              v-model="loanForm.uscc"
              placeholder="18-digit alphanumeric code, e.g., 91310115MA1K4QLX1L"
              maxlength="18"
            />
          </el-form-item>

          <el-form-item label="Company Email" prop="companyEmail">
            <el-input
              v-model="loanForm.companyEmail"
              placeholder="test@test.com"
            />
          </el-form-item>

          <el-form-item label="Company Address" prop="companyAddress">
            <el-input v-model="loanForm.companyAddress" placeholder="" />
          </el-form-item>

          <el-form-item label="Repay Account Bank" prop="repayAccountBank">
            <el-select
              v-model="loanForm.repayAccountBank"
              placeholder="Please select your repay account bank!"
            >
              <el-option
                v-for="option in bankOptions"
                :key="option.value"
                :label="option.label"
                :value="option.value"
              />
            </el-select>
          </el-form-item>

          <el-form-item label="Account No" prop="repayAccountNo">
            <el-input
              v-model="loanForm.repayAccountNo"
              placeholder=""
              maxlength="19"
              @input="handleAccountNoInput"
            />
          </el-form-item>
        </div>

        <!-- 贷款信息 -->
        <div class="form-section">
          <h3 class="section-title">Loan Information</h3>
          <el-form-item label="Loan Amount" prop="loanAmount">
            <el-input
              v-model="loanForm.loanAmount"
              placeholder=""
              @input="handleLoanAmountInput"
            />
          </el-form-item>

          <el-form-item label="Loan Term" prop="loanTerm">
            <el-select
              v-model="loanForm.loanTerm"
              placeholder="Please select your Loan Term!"
            >
              <el-option
                v-for="option in loanTermOptions"
                :key="option.value"
                :label="option.label"
                :value="option.value"
              />
            </el-select>
          </el-form-item>

          <el-form-item label="Loan Purpose" prop="loanPurpose">
            <el-select
              v-model="loanForm.loanPurpose"
              placeholder="Please choose your loan Purpose!"
              @change="handleLoanPurposeChange"
            >
              <el-option
                v-for="option in loanPurposeOptions"
                :key="option.value"
                :label="option.label"
                :value="option.value"
              />
            </el-select>
          </el-form-item>

          <el-form-item
            label="Property Proof Type (At least one item must be uploaded)"
            prop="propProofType"
          >
            <el-select
              v-model="loanForm.propProofType"
              placeholder="***Please Select*** Unsecured Loan ***Property Proof Type***"
              :disabled="!loanForm.loanPurpose"
            >
              <el-option
                v-for="type in proofTypes"
                :key="type.value"
                :label="type.label"
                :value="type.value"
              />
            </el-select>
          </el-form-item>

          <el-form-item label="* Property Proof Document" prop="propProofDocs">
            <el-upload
              ref="uploadRef"
              :auto-upload="false"
              :limit="1"
              :on-change="handleFileChange"
              :show-file-list="false"
            >
              <el-button type="primary"
                >Please upload your property proof document!</el-button
              >
            </el-upload>
          </el-form-item>
          <div v-if="fileName" class="file-name-display">
            已选择: {{ fileName }}
          </div>

          <el-form-item label="Industry Category" prop="industryCategory">
            <el-select
              v-model="loanForm.industryCategory"
              placeholder="Please choose your Industry Category!"
            >
              <el-option
                v-for="option in industryCategoryOptions"
                :key="option.value"
                :label="option.label"
                :value="option.value"
              />
            </el-select>
          </el-form-item>
        </div>

        <div class="submit-button-container">
          <el-button
            type="success"
            @click="handleSubmit"
            :loading="loading"
            class="submit-button"
          >
            apply
          </el-button>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch, onMounted } from "vue";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";
import { validateAndUpload } from "@/api/loan";
import { authApi } from "@/api/auth";
import { useLoanStore } from "@/store/loan-store";
import {
  bankOptions,
  loanTermOptions,
  loanPurposeOptions,
  industryCategoryOptions,
  getPropertyProofTypeOptions,
} from "@/constants/formOptions";
import { convertLoanFormToBackend } from "@/utils/fieldMapper";

const router = useRouter();
const loanStore = useLoanStore();
const loanFormRef = ref(null);
const loading = ref(false);
const uploadedFile = ref(null);
const fileName = ref("");

// 页面初始化时验证token
onMounted(async () => {
  try {
    await authApi.testToken();
    console.log("Token验证成功");
  } catch (error) {
    // token过期或无效时，request.js的拦截器会自动处理跳转
    console.log("Token验证失败，将跳转到登录页");
  }
});

// 前端验证开关 - 设为false可以跳过前端验证，直接测试后端验证
const ENABLE_FRONTEND_VALIDATION = true;

// 表单数据
const loanForm = reactive({
  entName: "",
  uscc: "",
  companyEmail: "",
  companyAddress: "",
  repayAccountBank: "",
  repayAccountNo: "",
  loanAmount: "",
  loanTerm: "",
  loanPurpose: "",
  propProofType: "",
  industryCategory: "",
});

// 从 store 恢复数据
const savedData = loanStore.getLoanData();
if (savedData) {
  Object.assign(loanForm, savedData);
  fileName.value = savedData.fileName || "";
}

watch(
  () => fileName.value,
  (newFileName) => {
    loanStore.setLoanData({
      ...loanForm,
      fileName: newFileName,
    });
  },
);

// 根据贷款目的动态获取财产证明类型选项
const proofTypes = computed(() => {
  return getPropertyProofTypeOptions(loanForm.loanPurpose);
});

// 表单验证规则
const rules = {
  entName: [
    {
      required: true,
      message: "Please enter the company name",
      trigger: "blur",
    },
  ],
  uscc: [
    {
      required: true,
      message: "Please enter the Unified Social Credit Code (Uscc)",
      trigger: "blur",
    },
    {
      len: 18,
      message: "Uscc must be exactly 18 characters",
      trigger: "blur",
    },
    {
      pattern: /^[0-9A-Za-z]$/,
      message: "Uscc must contain only letters and numbers",
      trigger: "blur",
    },
  ],
  companyEmail: [
    {
      required: true,
      message: "Please enter the company email",
      trigger: "blur",
    },
    {
      type: "email",
      message: "Please enter a valid company email (e.g., info@company.com)",
      trigger: "blur",
    },
  ],
  repayAccountBank: [
    {
      required: true,
      message: "Please select a repayment account bank",
      trigger: "change",
    },
  ],
  repayAccountNo: [
    { required: true, message: "Please enter the account no", trigger: "blur" },
    {
      len: 19,
      message: "Account no must be exactly 19 characters",
      trigger: "blur",
    },
    {
      pattern: /^\d+$/,
      message: "Account no must contain only numbers",
      trigger: "blur",
    },
  ],
  loanAmount: [
    {
      required: true,
      message: "Please enter the loan amount",
      trigger: "blur",
    },
    {
      pattern: /^\d+(\.\d{1,2})?$/,
      message:
        "Loan amount must be a valid positive number (e.g., 1000, 5000.50)",
      trigger: "blur",
    },
  ],
  loanTerm: [
    { required: true, message: "Please select a loan term", trigger: "change" },
  ],
  loanPurpose: [
    {
      required: true,
      message: "Please select a loan purpose",
      trigger: "change",
    },
  ],
  propProofType: [
    {
      required: true,
      message: "Please select a property proof type",
      trigger: "change",
    },
  ],
};

// 输入格式化工具函数
const formatNumberInput = (value, allowDecimal = false) => {
  if (allowDecimal) {
    // 只保留数字和一个小数点
    const filtered = value.replace(/[^\d.]/g, "");
    const parts = filtered.split(".");
    return parts.length > 2
      ? parts[0] + "." + parts.slice(1).join("")
      : filtered;
  }
  // 只保留数字
  return value.replace(/\D/g, "");
};

// 创建FormData的公共函数
const createFormData = () => {
  const formData = new FormData();
  const backendData = convertLoanFormToBackend(loanForm);

  // 添加表单字段（使用后端字段名）
  Object.keys(backendData).forEach((key) => {
    if (backendData[key]) {
      formData.append(key, backendData[key]);
    }
  });

  // 添加文件
  if (uploadedFile.value) {
    formData.append(
      "prop_proof_docs",
      uploadedFile.value,
      uploadedFile.value.name,
    );
  }

  return formData;
};

// 错误处理公共函数
const handleError = (error) => {
  console.error("提交失败:", error);

  // 如果是认证错误，拦截器已处理
  if (error.isAuthError) {
    return;
  }

  // 处理网络错误或其他异常
  if (error.response?.data) {
    const errorData = error.response.data;
    const errors = errorData.data?.errors;

    if (errors && Array.isArray(errors)) {
      const errorMessages = errors.map((err) => err.msg).join("; ");
      ElMessage.error(errorMessages || "提交失败，请稍后重试");
    } else {
      ElMessage.error(
        errorData.message || errorData.msg || "提交失败，请稍后重试",
      );
    }
  } else {
    ElMessage.error("网络错误，请检查网络连接");
  }
};

// 表单验证函数
const validateForm = async () => {
  if (!ENABLE_FRONTEND_VALIDATION) {
    return true;
  }

  if (!loanFormRef.value) {
    return false;
  }

  try {
    await loanFormRef.value.validate();
  } catch (error) {
    ElMessage.error("请完整填写表单信息");
    return false;
  }

  // 检查文件是否上传
  if (!uploadedFile.value) {
    // 如果有文件名但没有文件对象，说明页面刷新了或从其他页面返回
    if (fileName.value) {
      ElMessage.warning("页面刷新后文件丢失，请重新上传财产证明文件");
      // 清空文件名（watchEffect 会自动保存到 store）
      fileName.value = "";
    } else {
      ElMessage.error("请上传财产证明文件");
    }
    return false;
  }

  return true;
};

// 贷款目的改变时，清空财产证明类型选择
const handleLoanPurposeChange = () => {
  loanForm.propProofType = "";
};

// 处理账户号码输入，只允许数字
const handleAccountNoInput = (value) => {
  loanForm.repayAccountNo = formatNumberInput(value, false);
};

// 处理贷款金额输入，只允许数字和小数点
const handleLoanAmountInput = (value) => {
  loanForm.loanAmount = formatNumberInput(value, true);
};

const handleFileChange = (file) => {
  uploadedFile.value = file.raw;
  fileName.value = file.name;
};

// 提交表单
const handleSubmit = async () => {
  // 表单验证
  if (!(await validateForm())) {
    return;
  }

  loading.value = true;

  try {
    // 创建FormData并调用验证和上传接口
    const formData = createFormData();
    const response = await validateAndUpload(formData);

    if (response.code === 0) {
      ElMessage.success(response.msg || "数据验证成功");

      // API成功后，更新store中的数据，添加返回的文件信息和财务数据
      loanStore.setLoanData({
        ...loanForm,
        fileName: fileName.value,
        propProofDocsPath:
          response.data.file_info?.file_path || response.data.file_info,
        financialData: response.data.financial_data,
      });

      // 延迟跳转到确认页面，让用户看到成功提示
      setTimeout(() => {
        router.push("/confirm");
      }, 1000);
    } else {
      ElMessage.error(response.msg || "数据验证失败");
    }
  } catch (error) {
    handleError(error);
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.enterprise-input-page {
  padding: 20px;
  min-height: 100vh;
  background-color: #f5f5f5;
}

.form-card {
  max-width: 900px;
  margin: 0 auto;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.card-header {
  text-align: center;
  padding: 30px 0;
}

.card-header h2 {
  margin: 0;
  color: #303133;
  font-size: 36px;
  font-weight: 600;
}

.loan-form {
  margin-top: 30px;
  padding: 0 20px;
}

.form-section {
  margin-bottom: 30px;
}

.section-title {
  margin: 0 0 25px 0;
  padding: 15px;
  background-color: #e8f4f8;
  color: #4169e1;
  font-size: 18px;
  font-weight: 600;
  text-align: center;
  border-radius: 4px;
  border: 1px solid #d0e8f0;
}

:deep(.el-form-item) {
  margin-bottom: 28px;
}

:deep(.el-form-item__label) {
  color: #303133;
  font-weight: 600;
  font-size: 16px;
  line-height: 1.5;
  padding-bottom: 8px;
}

:deep(.el-input__wrapper) {
  padding: 8px 12px;
}

:deep(.el-select) {
  width: 100%;
}

.submit-button-container {
  margin-top: 40px;
  margin-bottom: 20px;
  display: flex;
  justify-content: center;
}

.submit-button {
  width: 400px;
  background-color: #82b366;
  border-color: #82b366;
  font-size: 16px;
  padding: 12px 20px;
  border-radius: 8px;
}

.submit-button:hover {
  background-color: #6fa05a;
  border-color: #6fa05a;
}

:deep(.el-upload) {
  width: 100%;
}

:deep(.el-upload .el-button) {
  width: 100%;
  background-color: #4169e1;
  border-color: #4169e1;
  color: white;
}

:deep(.el-upload .el-button:hover) {
  background-color: #5179f1;
  border-color: #5179f1;
}

.file-name-display {
  margin-top: 10px;
  padding: 8px 12px;
  border-radius: 4px;
  font-size: 14px;
}
</style>
