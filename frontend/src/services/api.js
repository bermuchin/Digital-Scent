import axios from 'axios';

// 배포 환경에서는 환경변수에서 API URL을 가져오고, 로컬에서는 localhost 사용
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

console.log('API Base URL:', API_BASE_URL);

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  // CORS 설정
  withCredentials: false,
});

// 요청 인터셉터 - 로깅
api.interceptors.request.use(
  (config) => {
    console.log('API Request:', config.method?.toUpperCase(), config.url);
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// 응답 인터셉터 - 에러 처리
api.interceptors.response.use(
  (response) => {
    console.log('API Response:', response.status, response.config.url);
    return response;
  },
  (error) => {
    console.error('API Response Error:', error.response?.status, error.response?.data);
    return Promise.reject(error);
  }
);

// 사용자 관련 API
export const userAPI = {
  // 사용자 등록
  register: (userData) => api.post('/api/users/', userData),
  
  // 사용자 목록 조회
  getUsers: (skip = 0, limit = 100) => 
    api.get(`/api/users/?skip=${skip}&limit=${limit}`),
  
  // 특정 사용자 조회
  getUser: (userId) => api.get(`/api/users/${userId}`),
  
  // 사용자 정보 업데이트
  updateUser: (userId, userData) => 
    api.put(`/api/users/${userId}`, userData),
  
  // 사용자 삭제
  deleteUser: (userId) => api.delete(`/api/users/${userId}`),
  
  // 사용자 선호도 생성/업데이트
  createPreference: (userId, preferenceData) => 
    api.post(`/api/users/${userId}/preferences`, preferenceData),
  
  // 사용자 선호도 조회
  getPreference: (userId) => 
    api.get(`/api/users/${userId}/preferences`),
};

// 향수 관련 API
export const perfumeAPI = {
  // 향수 생성
  createPerfume: (perfumeData) => 
    api.post('/api/perfumes/', perfumeData),
  
  // 향수 목록 조회
  getPerfumes: (params = {}) => {
    const queryParams = new URLSearchParams();
    Object.keys(params).forEach(key => {
      if (params[key]) queryParams.append(key, params[key]);
    });
    return api.get(`/api/perfumes/?${queryParams}`);
  },
  
  // 특정 향수 조회
  getPerfume: (perfumeId) => api.get(`/api/perfumes/${perfumeId}`),
  
  // 향수 정보 업데이트
  updatePerfume: (perfumeId, perfumeData) => 
    api.put(`/api/perfumes/${perfumeId}`, perfumeData),
  
  // 향수 삭제
  deletePerfume: (perfumeId) => api.delete(`/api/perfumes/${perfumeId}`),
  
  // 향수 제조법 추가
  createRecipe: (perfumeId, recipeData) => 
    api.post(`/api/perfumes/${perfumeId}/recipes`, recipeData),
  
  // 향수 제조법 조회
  getRecipes: (perfumeId) => 
    api.get(`/api/perfumes/${perfumeId}/recipes`),
  
  // 향수 카테고리 목록
  getCategories: () => api.get('/api/perfumes/categories/list'),
};

// 추천 관련 API
export const recommendationAPI = {
  // 향수 추천
  getRecommendation: (requestData) => 
    api.post('/api/recommendations/', requestData),
  
  // 사용자별 향수 추천
  getUserRecommendation: (userId) => 
    api.post(`/api/recommendations/user/${userId}`),
  
  // 사용자 추천 기록
  getRecommendationHistory: (userId) => 
    api.get(`/api/recommendations/user/${userId}/history`),
  
  // 추천 피드백 제출
  submitFeedback: (recommendationId, feedback) => 
    api.post(`/api/recommendations/feedback/${recommendationId}`, feedback),
  
  // 카테고리별 향수 조회
  getPerfumesByCategory: (category) => 
    api.get(`/api/recommendations/categories/${category}`),
  
  // 인기 향수 조회
  getPopularPerfumes: () => 
    api.get('/api/recommendations/popular'),
};

// 헬스 체크
export const healthCheck = () => api.get('/health');

export default api; 
 