import { describe, it, expect, beforeEach, vi } from "vitest";
import { setActivePinia, createPinia } from "pinia";
import { useUserStore } from "../../src/store/user-store";

vi.mock("../../src/api/auth", () => ({
  authApi: {
    login: vi.fn(),
    logout: vi.fn(),
  },
}));

vi.mock("vue-router", () => ({
  default: {
    push: vi.fn(),
  },
}));

describe("useUserStore", () => {
  let store;

  beforeEach(() => {
    setActivePinia(createPinia());
    store = useUserStore();
    localStorage.clear();
  });

  it("应该初始化为未登录状态", () => {
    expect(store.isLoggedIn).toBe(false);
    expect(store.token).toBe("");
    expect(store.userInfo).toBeNull();
  });

  it("应该正确设置token", () => {
    store.token = "test-token";
    expect(store.token).toBe("test-token");
    expect(store.isLoggedIn).toBe(true);
  });

  it("应该正确设置用户信息", () => {
    store.userInfo = {
      username: "testuser",
      user_type: "ENTERPRISE",
    };
    expect(store.userInfo.username).toBe("testuser");
    expect(store.userType).toBe("ENTERPRISE");
    expect(store.isEnterprise).toBe(true);
    expect(store.isIndividual).toBe(false);
  });

  it("应该正确识别个人用户", () => {
    store.userInfo = {
      username: "testuser",
      user_type: "INDIVIDUAL",
    };
    expect(store.isIndividual).toBe(true);
    expect(store.isEnterprise).toBe(false);
  });

  it("logout应该清除所有状态", () => {
    store.token = "test-token";
    store.userInfo = { username: "test" };

    store.logout();

    expect(store.token).toBe("");
    expect(store.userInfo).toBeNull();
  });
});
