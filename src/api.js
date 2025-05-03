// api.js
import axios from 'axios'
import { API_BASE_URL } from './config'
// fsdfs

const api = axios.create({
  baseURL: API_BASE_URL,
})

export default api
