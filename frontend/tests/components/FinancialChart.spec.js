import { describe, it, expect, beforeEach, vi } from "vitest";
import { mount } from "@vue/test-utils";
import FinancialChart from "../../src/components/FinancialChart.vue";

// Mock ECharts
vi.mock("echarts", () => ({
  default: {
    init: vi.fn(() => ({
      setOption: vi.fn(),
      resize: vi.fn(),
      dispose: vi.fn(),
    })),
  },
  init: vi.fn(() => ({
    setOption: vi.fn(),
    resize: vi.fn(),
    dispose: vi.fn(),
  })),
}));

describe("FinancialChart", () => {
  let wrapper;

  const mockData = [
    {
      quarter: "2023Q1",
      profit: 100000,
      percentage: 5,
      yoy: "10%",
      qoq: "5%",
    },
    {
      quarter: "2023Q2",
      profit: 120000,
      percentage: 6,
      yoy: "12%",
      qoq: "20%",
    },
  ];

  beforeEach(() => {
    wrapper = mount(FinancialChart, {
      props: {
        data: mockData,
      },
    });
  });

  it("应该正确渲染", () => {
    expect(wrapper.exists()).toBe(true);
  });

  it("应该显示图表标题", () => {
    expect(wrapper.find(".chart-title").text()).toBe("财务数据图表");
  });

  it("应该显示图例", () => {
    const legend = wrapper.find(".legend");
    expect(legend.exists()).toBe(true);
    expect(legend.text()).toContain("利润");
  });

  it("应该有同比和环比复选框", () => {
    const checkboxes = wrapper.findAll('input[type="checkbox"]');
    expect(checkboxes.length).toBe(2);
  });

  it("应该能切换同比显示", async () => {
    const checkbox = wrapper.findAll('input[type="checkbox"]')[0];
    await checkbox.setValue(true);
    expect(wrapper.vm.showYoY).toBe(true);
  });

  it("应该能切换环比显示", async () => {
    const checkbox = wrapper.findAll('input[type="checkbox"]')[1];
    await checkbox.setValue(true);
    expect(wrapper.vm.showMoM).toBe(true);
  });
});
