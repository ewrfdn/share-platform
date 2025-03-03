import admin from './admin';

// 配置全局请求拦截器
import axios from 'axios';

// 请求拦截器：添加token到请求头
axios.interceptors.request.use(
  config => {
    const token = localStorage.getItem('accessToken');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

// 响应拦截器：处理错误响应
axios.interceptors.response.use(
  response => {
    return response;
  },
  error => {
    // 处理 401 错误，跳转到登录页
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('accessToken');
      localStorage.removeItem('userInfo');
      
      // 如果不在登录页，跳转到登录页
      if (window.location.pathname !== '/login') {
        window.location.href = '/login?redirect=' + window.location.pathname;
      }
    }
    return Promise.reject(error);
  }
);

export { admin };

export default {
  admin
};
