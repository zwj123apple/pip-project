<template>
  <div class="result-page">
    <div class="result-container">
      <h1 class="page-title">Risk Information Loan Decision Notification</h1>

      <div class="risk-section">
        <h2 class="section-title">Risk level</h2>
        <div class="risk-badge risk-medium">medium</div>
      </div>

      <div class="info-section">
        <h2 class="section-title">Information</h2>
        <div class="info-box">Suggest add additional materials.</div>
      </div>

      <div class="button-group">
        <button class="btn-reevaluation" @click="handleReEvaluation">
          Re-evaluation
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router";

const router = useRouter();

// 重新评估 - 跳转到企业入力画面，数据已经保存在store中，会自动恢复
const handleReEvaluation = () => {
  // 数据已经保存在loanStore，跳转后会自动恢复
  router.push("/input");
};
</script>

<style scoped>
.result-page {
  min-height: 100vh;
  background-color: #f5f5f5;
  padding: 40px 20px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.result-container {
  max-width: 1000px;
  width: 100%;
  background: white;
  padding: 60px 80px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.page-title {
  font-size: 48px;
  font-weight: bold;
  color: #333;
  text-align: center;
  margin: 0 0 60px 0;
  line-height: 1.3;
}

.risk-section,
.info-section {
  margin-bottom: 50px;
}

.section-title {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin: 0 0 20px 0;
}

.risk-badge {
  padding: 30px;
  border-radius: 8px;
  text-align: center;
  font-size: 36px;
  font-weight: bold;
  font-style: italic;
}

.risk-low {
  background-color: #d4edda;
  color: #155724;
}

.risk-medium {
  background-color: #fff3cd;
  color: #856404;
}

.risk-high {
  background-color: #f8d7da;
  color: #721c24;
}

.info-box {
  padding: 30px;
  background-color: #fff9e6;
  border-radius: 8px;
  font-size: 20px;
  color: #b8860b;
  font-style: italic;
}

.button-group {
  display: flex;
  justify-content: center;
  margin-top: 60px;
}

.btn-reevaluation {
  min-width: 280px;
  padding: 16px 50px;
  font-size: 18px;
  color: #666;
  background-color: #e8e8e8;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-reevaluation:hover {
  background-color: #d5d5d5;
}
</style>
