import request from '@/utils/http/axios'

export function login(data) {
  return request({
    url: '/api/auth/login',
    method: 'post',
    data
  })
} 