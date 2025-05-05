// api.js
import axios from 'axios'
import { API_BASE_URL } from './config'
// fsdfs

const api = axios.create({
  baseURL: API_BASE_URL,
})

api.interceptors.response.use(
  res => res,
  error => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      // Redirect to login page
      router.push({ name: 'Login' })
    }
    return Promise.reject(error)
  }
)

export default api
