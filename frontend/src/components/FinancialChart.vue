<template>
  <div class="financial-chart">
    <div class="chart-header">
      <h3 class="chart-title">财务数据图表</h3>
      <div class="legend">
        <span class="legend-item">
          <span class="legend-color profit"></span>
          利润
        </span>
        <span v-if="showYoY" class="legend-item">
          <span class="legend-icon yoy"></span>
          同比
        </span>
        <span v-if="showMoM" class="legend-item">
          <span class="legend-icon mom"></span>
          环比
        </span>
      </div>
    </div>

    <div class="chart-container">
      <div ref="chartRef" style="width: 100%; height: 400px"></div>
    </div>

    <div class="chart-options">
      <label class="checkbox-label">
        <input type="checkbox" v-model="showYoY" @change="updateChart" />
        <span>同比</span>
      </label>
      <label class="checkbox-label">
        <input type="checkbox" v-model="showMoM" @change="updateChart" />
        <span>环比</span>
      </label>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from "vue";
import * as echarts from "echarts";

const props = defineProps({
  data: {
    type: Array,
    default: () => [],
  },
});

const chartRef = ref(null);
const showYoY = ref(false);
const showMoM = ref(false);
let chartInstance = null;

const quarters = ref([]);
const profits = ref([]);
const percentages = ref([]);
const yoyData = ref([]);
const momData = ref([]);

const processData = () => {
  if (!props.data || props.data.length === 0) return;

  quarters.value = props.data.map((item) => item.quarter || item.period);
  profits.value = props.data.map((item) => parseFloat(item.profit || 0));
  percentages.value = props.data.map((item) =>
    parseFloat(item.percentage || 0),
  );

  // 处理同比数据 - 如果后端提供了yoy数据则使用，否则null
  yoyData.value = props.data.map((item) => {
    if (item.yoy === null || item.yoy === undefined) return null;
    // 移除百分号并转换为数字
    const yoyStr = String(item.yoy).replace("%", "");
    return parseFloat(yoyStr) || null;
  });

  // 处理环比数据 - 如果后端提供了qoq数据则使用，否则null
  momData.value = props.data.map((item) => {
    if (item.qoq === null || item.qoq === undefined) return null;
    // 移除百分号并转换为数字
    const qoqStr = String(item.qoq).replace("%", "");
    return parseFloat(qoqStr) || null;
  });
};

const initChart = () => {
  if (!chartRef.value) return;

  if (chartInstance) {
    chartInstance.dispose();
  }

  chartInstance = echarts.init(chartRef.value);
  updateChart();
};

const updateChart = () => {
  if (!chartInstance) return;

  const series = [
    {
      name: "利润",
      type: "bar",
      data: profits.value,
      itemStyle: {
        color: "#b85450",
      },
      barWidth: "40%",
      yAxisIndex: 0,
    },
  ];

  const yAxisConfig = [
    {
      type: "value",
      name: "利润",
      nameTextStyle: {
        color: "#8B9DD9",
        fontSize: 13,
        padding: [0, 50, 0, 0],
      },
      position: "left",
      axisLine: {
        show: false,
      },
      axisTick: {
        show: false,
      },
      axisLabel: {
        color: "#8B9DD9",
        fontSize: 12,
        formatter: (value) => {
          if (value === 0) return "0";
          return value >= 10000
            ? Math.round(value / 10000) + "0,000"
            : value.toLocaleString();
        },
      },
      splitLine: {
        show: false,
      },
      min: 0,
      max: (value) => {
        return Math.ceil(value.max * 1.1);
      },
    },
  ];

  // 添加同比线条
  if (showYoY.value) {
    series.push({
      name: "同比",
      type: "line",
      data: yoyData.value,
      itemStyle: {
        color: "#5470A6",
      },
      lineStyle: {
        width: 3,
        color: "#5470A6",
      },
      symbol: "circle",
      symbolSize: 10,
      yAxisIndex: 1,
      connectNulls: false, // 不连接null值，null值处断开
    });
  }

  // 添加环比线条
  if (showMoM.value) {
    series.push({
      name: "环比",
      type: "line",
      data: momData.value,
      itemStyle: {
        color: "#73C0DE",
      },
      lineStyle: {
        width: 3,
        color: "#73C0DE",
      },
      symbol: "circle",
      symbolSize: 10,
      yAxisIndex: 1,
      connectNulls: false, // 不连接null值，null值处断开
    });
  }

  // 始终显示百分比Y轴
  yAxisConfig.push({
    type: "value",
    name: "百分比",
    nameTextStyle: {
      color: "#D4988A",
      fontSize: 13,
      padding: [0, 0, 0, 50],
    },
    position: "right",
    min: -10,
    max: 20,
    interval: 5,
    axisLine: {
      show: false,
    },
    axisTick: {
      show: false,
    },
    axisLabel: {
      color: "#D4988A",
      fontSize: 12,
      formatter: "{value} %",
    },
    splitLine: {
      show: false,
    },
  });

  const option = {
    grid: {
      left: "70px",
      right: "90px",
      top: "50px",
      bottom: "60px",
      containLabel: false,
    },
    xAxis: {
      type: "category",
      data: quarters.value,
      axisLine: {
        show: true,
        lineStyle: {
          color: "#999",
          width: 1,
        },
      },
      axisTick: {
        show: true,
        alignWithLabel: true,
        lineStyle: {
          color: "#999",
        },
      },
      axisLabel: {
        color: "#8B9DD9",
        fontSize: 13,
        margin: 15,
        interval: 1, // 隔一个显示一个标签
      },
      splitLine: {
        show: false,
      },
    },
    yAxis: yAxisConfig,
    series: series,
    animation: true,
    animationDuration: 300,
  };

  // 使用 notMerge: true 来完全替换配置，这样可以移除不需要的系列
  chartInstance.setOption(option, true);
};

watch(
  () => props.data,
  () => {
    processData();
    nextTick(() => {
      updateChart();
    });
  },
  { deep: true },
);

onMounted(() => {
  processData();
  nextTick(() => {
    initChart();
  });

  window.addEventListener("resize", () => {
    if (chartInstance) {
      chartInstance.resize();
    }
  });
});
</script>

<style scoped>
.financial-chart {
  margin: 30px 0;
  padding: 20px;
  background: #fff;
  border-radius: 4px;
}

.chart-header {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  margin-bottom: 20px;
  gap: 30px;
}

.chart-title {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin: 0;
}

.legend {
  display: flex;
  gap: 20px;
  align-items: center;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #666;
}

.legend-color {
  width: 20px;
  height: 12px;
  border-radius: 2px;
}

.legend-color.profit {
  background-color: #b85450;
}

.legend-icon {
  width: 24px;
  height: 12px;
  position: relative;
  display: inline-block;
}

.legend-icon::before {
  content: "";
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 24px;
  height: 3px;
}

.legend-icon::after {
  content: "";
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  width: 10px;
  height: 10px;
  border-radius: 50%;
  border: 3px solid;
  background: white;
}

.legend-icon.yoy::before {
  background-color: #5470a6;
}

.legend-icon.yoy::after {
  border-color: #5470a6;
}

.legend-icon.mom::before {
  background-color: #73c0de;
}

.legend-icon.mom::after {
  border-color: #73c0de;
}

.chart-container {
  width: 100%;
  margin-bottom: 20px;
}

.chart-options {
  display: flex;
  justify-content: center;
  gap: 30px;
  margin-top: 20px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  font-size: 14px;
  color: #666;
}

.checkbox-label input[type="checkbox"] {
  width: 18px;
  height: 18px;
  cursor: pointer;
}
</style>
