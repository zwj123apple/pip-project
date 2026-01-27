import request from "@/utils/request";

export const authApi = {
  login(data) {
    return request({
      url: "/auth/login",
      method: "post",
      data,
    });
  },

  logout() {
    return request({
      url: "/auth/logout",
      method: "post",
    });
  },

  testToken() {
    return request({
      url: "/auth/test",
      method: "get",
    });
  },
};
