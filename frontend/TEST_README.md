# Vue 项目单元测试文档

## 测试框架

本项目使用以下测试工具：

- **Vitest**: 快速的单元测试框架，与 Vite 深度集成
- **@vue/test-utils**: Vue.js 官方测试工具库
- **jsdom**: 在 Node.js 环境中模拟浏览器 DOM
- **@vitest/coverage-v8**: 代码覆盖率工具

## 安装测试依赖

```bash
cd frontend
npm install
```

## 运行测试

### 运行所有测试

```bash
npm run test
```

### 运行测试并生成覆盖率报告

```bash
npm run test:coverage
```

### 以 UI 模式运行测试

```bash
npm run test:ui
```

### 监听模式（开发时使用）

```bash
npm run test -- --watch
```

## 测试文件结构

```
frontend/tests/
├── setup.js                          # 测试环境配置
├── pages/                            # 页面组件测试
│   ├── login-page.spec.js
│   ├── enterprise-input-page.spec.js
│   ├── enterprise-confirm-page.spec.js
│   ├── personal-page.spec.js
│   ├── result-page.spec.js
│   └── not-found-page.spec.js
├── components/                       # 公共组件测试
│   ├── AppHeader.spec.js
│   └── FinancialChart.spec.js
├── store/                           # 状态管理测试
│   ├── user-store.spec.js
│   └── loan-store.spec.js
└── utils/                           # 工具函数测试
    └── fieldMapper.spec.js
```

## 测试覆盖范围

### 页面组件

- ✅ login-page.vue - 登录页面
- ✅ enterprise-input-page.vue - 企业贷款申请表单
- ✅ enterprise-confirm-page.vue - 企业贷款确认页面
- ✅ personal-page.vue - 个人贷款页面
- ✅ result-page.vue - 结果展示页面
- ✅ not-found-page.vue - 404页面

### 公共组件

- ✅ AppHeader.vue - 应用头部导航
- ✅ FinancialChart.vue - 财务数据图表

### 状态管理 (Pinia Stores)

- ✅ user-store.js - 用户状态管理
- ✅ loan-store.js - 贷款申请数据管理

### 工具函数

- ✅ fieldMapper.js - 字段映射工具

## GitHub Actions 集成

项目已配置 GitHub Actions 工作流，在以下情况自动运行测试：

- 推送到 `main` 或 `develop` 分支
- 提交 Pull Request 到 `main` 或 `develop` 分支
- 修改 `frontend/` 目录下的文件

工作流配置文件：`.github/workflows/frontend-test.yml`

### 工作流功能

- 在 Node.js 18.x 和 20.x 上运行测试
- 生成代码覆盖率报告
- 上传覆盖率报告到 Codecov

## 测试编写指南

### 基本测试结构

```javascript
import { describe, it, expect, beforeEach } from "vitest";
import { mount } from "@vue/test-utils";
import { createPinia, setActivePinia } from "pinia";
import MyComponent from "@/components/MyComponent.vue";

describe("MyComponent", () => {
  let wrapper;

  beforeEach(() => {
    setActivePinia(createPinia());
    wrapper = mount(MyComponent, {
      props: {
        // 组件属性
      },
      global: {
        stubs: {
          // 需要 stub 的子组件
        },
      },
    });
  });

  it("应该正确渲染", () => {
    expect(wrapper.exists()).toBe(true);
  });
});
```

### Mock 外部依赖

```javascript
// Mock API
vi.mock("@/api/auth", () => ({
  authApi: {
    login: vi.fn(),
    logout: vi.fn(),
  },
}));

// Mock Router
vi.mock("vue-router", () => ({
  useRouter: () => ({
    push: vi.fn(),
    replace: vi.fn(),
  }),
  useRoute: () => ({
    params: {},
    query: {},
  }),
}));
```

### 测试异步操作

```javascript
it("应该处理异步操作", async () => {
  const button = wrapper.find("button");
  await button.trigger("click");
  await wrapper.vm.$nextTick();

  expect(wrapper.vm.loading).toBe(false);
});
```

## 持续改进

### 待添加的测试

- API 模块的单元测试
- 更多的边界情况测试
- E2E 测试

### 测试覆盖率目标

- 语句覆盖率 > 80%
- 分支覆盖率 > 75%
- 函数覆盖率 > 80%
- 行覆盖率 > 80%

## 常见问题

### 1. Element Plus 组件找不到

在测试中使用 `stubs` 来模拟 Element Plus 组件：

```javascript
wrapper = mount(Component, {
  global: {
    stubs: {
      "el-button": true,
      "el-input": true,
    },
  },
});
```

### 2. localStorage/sessionStorage 错误

测试环境已在 `tests/setup.js` 中配置了 mock，无需额外处理。

### 3. Router 相关错误

使用 `vi.mock('vue-router')` 来 mock 路由相关功能。

## 参考资源

- [Vitest 官方文档](https://vitest.dev/)
- [Vue Test Utils 文档](https://test-utils.vuejs.org/)
- [Testing Library 最佳实践](https://testing-library.com/docs/guiding-principles)
