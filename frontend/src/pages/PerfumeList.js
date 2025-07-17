import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Search, Filter, Flower, Star } from 'lucide-react';
import { perfumeAPI } from '../services/api';

const PerfumeList = () => {
  const [perfumes, setPerfumes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [selectedPrice, setSelectedPrice] = useState('');
  const [categories, setCategories] = useState([]);

  useEffect(() => {
    loadCategories();
    loadPerfumes();
  }, []);

  const loadCategories = async () => {
    try {
      const response = await perfumeAPI.getCategories();
      setCategories(response.data);
    } catch (error) {
      console.error('카테고리 로드 실패:', error);
    }
  };

  const loadPerfumes = async () => {
    setLoading(true);
    try {
      const params = {};
      if (selectedCategory) params.category = selectedCategory;
      if (selectedPrice) params.price_range = selectedPrice;
      
      const response = await perfumeAPI.getPerfumes(params);
      setPerfumes(response.data);
    } catch (error) {
      console.error('향수 목록 로드 실패:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadPerfumes();
  }, [selectedCategory, selectedPrice]);

  const filteredPerfumes = perfumes.filter(perfume =>
    perfume.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    perfume.brand.toLowerCase().includes(searchTerm.toLowerCase()) ||
    perfume.description.toLowerCase().includes(searchTerm.toLowerCase())
  );

  // 카테고리 통일 함수
  const unifyFloral = (category) => {
    if (["light floral", "white floral", "light_floral", "white_floral"].includes(category)) return "floral";
    return category;
  };

  const getCategoryColor = (category) => {
    const colors = {
      floral: 'bg-pink-100 text-pink-800',
      woody: 'bg-amber-100 text-amber-800',
      fresh: 'bg-blue-100 text-blue-800',
      oriental: 'bg-purple-100 text-purple-800',
      citrus: 'bg-green-100 text-green-800',
      musk: 'bg-gray-100 text-gray-800',
      aquatic: 'bg-blue-100 text-blue-800',
      green: 'bg-green-100 text-green-800',
      gourmand: 'bg-yellow-100 text-yellow-800',
      powdery: 'bg-pink-100 text-pink-800',
      fruity: 'bg-red-100 text-red-800',
      aromatic: 'bg-green-100 text-green-800',
      chypre: 'bg-purple-100 text-purple-800',
      fougere: 'bg-blue-100 text-blue-800',
      amber: 'bg-orange-100 text-orange-800',
      spicy: 'bg-red-100 text-red-800',
      'light_floral': 'bg-pink-100 text-pink-800',
      'white_floral': 'bg-white-100 text-gray-800',
      casual: 'bg-gray-100 text-gray-800',
      cozy: 'bg-brown-100 text-brown-800'
    };
    return colors[category] || 'bg-gray-100 text-gray-800';
  };

  const getCategoryIcon = (category) => {
    const icons = {
      floral: '🌸',
      woody: '🌳',
      fresh: '🌊',
      oriental: '🕌',
      citrus: '🍋',
      musk: '🦨',
      aquatic: '🌊',
      green: '🌿',
      gourmand: '🍰',
      powdery: '🌸',
      fruity: '🍎',
      aromatic: '🌿',
      chypre: '🏛️',
      fougere: '🌿',
      amber: '🟠',
      spicy: '🌶️',
      'light_floral': '🌸',
      'white_floral': '🌼',
      casual: '👕',
      cozy: '🏠'
    };
    return icons[category] || '💫';
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">향수 목록을 불러오는 중...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50 py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* 헤더 */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            향수 컬렉션
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            다양한 향수들을 둘러보고 당신에게 맞는 향수를 찾아보세요
          </p>
        </div>

        {/* 검색 및 필터 */}
        <div className="bg-white rounded-2xl shadow-lg p-6 mb-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            {/* 검색 */}
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input
                type="text"
                placeholder="향수 검색..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              />
            </div>

            {/* 카테고리 필터 */}
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            >
              <option value="">모든 카테고리</option>
              {categories.categories?.map((category) => (
                <option key={category} value={unifyFloral(category)}>
                  {unifyFloral(category) === 'floral' && '플로럴'}
                  {unifyFloral(category) === 'woody' && '우디'}
                  {unifyFloral(category) === 'fresh' && '프레시'}
                  {unifyFloral(category) === 'oriental' && '오리엔탈'}
                  {unifyFloral(category) === 'citrus' && '시트러스'}
                  {unifyFloral(category) === 'musk' && '머스크'}
                  {unifyFloral(category) === 'aquatic' && '아쿠아틱'}
                  {unifyFloral(category) === 'green' && '그린'}
                  {unifyFloral(category) === 'gourmand' && '구르망'}
                  {unifyFloral(category) === 'powdery' && '파우더리'}
                  {unifyFloral(category) === 'fruity' && '프루티'}
                  {unifyFloral(category) === 'aromatic' && '아로마틱'}
                  {unifyFloral(category) === 'chypre' && '시프레'}
                  {unifyFloral(category) === 'fougere' && '푸제르'}
                  {unifyFloral(category) === 'amber' && '앰버'}
                  {unifyFloral(category) === 'spicy' && '스파이시'}
                  {unifyFloral(category) === 'light_floral' && '라이트 플로럴'}
                  {unifyFloral(category) === 'white_floral' && '화이트 플로럴'}
                  {unifyFloral(category) === 'casual' && '캐주얼'}
                  {unifyFloral(category) === 'cozy' && '코지'}
                  {!['floral', 'woody', 'fresh', 'oriental', 'citrus', 'musk', 'aquatic', 'green', 'gourmand', 'powdery', 'fruity', 'aromatic', 'chypre', 'fougere', 'amber', 'spicy', 'light_floral', 'white_floral', 'casual', 'cozy'].includes(unifyFloral(category)) && unifyFloral(category)}
                </option>
              ))}
            </select>

            {/* 가격대 필터 */}
            <select
              value={selectedPrice}
              onChange={(e) => setSelectedPrice(e.target.value)}
              className="px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            >
              <option value="">모든 가격대</option>
              {categories.price_ranges?.map((price) => (
                <option key={price} value={price}>
                  {price === 'budget' && '저가'}
                  {price === 'mid-range' && '중가'}
                  {price === 'luxury' && '고가'}
                </option>
              ))}
            </select>

            {/* 필터 초기화 */}
            <button
              onClick={() => {
                setSelectedCategory('');
                setSelectedPrice('');
                setSearchTerm('');
              }}
              className="px-4 py-3 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors duration-200 flex items-center justify-center"
            >
              <Filter className="w-4 h-4 mr-2" />
              초기화
            </button>
          </div>
        </div>

        {/* 향수 목록 */}
        {filteredPerfumes.length === 0 ? (
          <div className="text-center py-12">
            <Flower className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              검색 결과가 없습니다
            </h3>
            <p className="text-gray-600">
              다른 검색어나 필터를 시도해보세요.
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredPerfumes.map((perfume) => (
              <Link
                key={perfume.id}
                to={`/perfumes/${perfume.id}`}
                className="bg-white rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 card-hover"
              >
                <div className="p-6">
                  {/* 향수 헤더 */}
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex-1">
                      <h3 className="text-xl font-semibold text-gray-900 mb-1">
                        {perfume.name}
                      </h3>
                      <p className="text-gray-600">{perfume.brand}</p>
                    </div>
                    <div className={`px-3 py-1 rounded-full text-sm font-medium ${getCategoryColor(unifyFloral(perfume.category))}`}>
                      <span className="mr-1">{getCategoryIcon(unifyFloral(perfume.category))}</span>
                      {unifyFloral(perfume.category) === 'floral' && '플로럴'}
                      {unifyFloral(perfume.category) === 'woody' && '우디'}
                      {unifyFloral(perfume.category) === 'fresh' && '프레시'}
                      {unifyFloral(perfume.category) === 'oriental' && '오리엔탈'}
                      {unifyFloral(perfume.category) === 'citrus' && '시트러스'}
                      {unifyFloral(perfume.category) === 'musk' && '머스크'}
                      {unifyFloral(perfume.category) === 'aquatic' && '아쿠아틱'}
                      {unifyFloral(perfume.category) === 'green' && '그린'}
                      {unifyFloral(perfume.category) === 'gourmand' && '구르망'}
                      {unifyFloral(perfume.category) === 'powdery' && '파우더리'}
                      {unifyFloral(perfume.category) === 'fruity' && '프루티'}
                      {unifyFloral(perfume.category) === 'aromatic' && '아로마틱'}
                      {unifyFloral(perfume.category) === 'chypre' && '시프레'}
                      {unifyFloral(perfume.category) === 'fougere' && '푸제르'}
                      {unifyFloral(perfume.category) === 'amber' && '앰버'}
                      {unifyFloral(perfume.category) === 'spicy' && '스파이시'}
                      {unifyFloral(perfume.category) === 'light_floral' && '라이트 플로럴'}
                      {unifyFloral(perfume.category) === 'white_floral' && '화이트 플로럴'}
                      {unifyFloral(perfume.category) === 'casual' && '캐주얼'}
                      {unifyFloral(perfume.category) === 'cozy' && '코지'}
                      {!['floral', 'woody', 'fresh', 'oriental', 'citrus', 'musk', 'aquatic', 'green', 'gourmand', 'powdery', 'fruity', 'aromatic', 'chypre', 'fougere', 'amber', 'spicy', 'light_floral', 'white_floral', 'casual', 'cozy'].includes(unifyFloral(perfume.category)) && unifyFloral(perfume.category)}
                    </div>
                  </div>

                  {/* 향수 정보 */}
                  <div className="space-y-3 mb-4">
                    <div>
                      <span className="text-sm font-medium text-gray-700">톱 노트:</span>
                      <p className="text-sm text-gray-600">{perfume.top_notes}</p>
                    </div>
                    <div>
                      <span className="text-sm font-medium text-gray-700">미들 노트:</span>
                      <p className="text-sm text-gray-600">{perfume.middle_notes}</p>
                    </div>
                    <div>
                      <span className="text-sm font-medium text-gray-700">베이스 노트:</span>
                      <p className="text-sm text-gray-600">{perfume.base_notes}</p>
                    </div>
                  </div>

                  {/* 설명 */}
                  <p className="text-gray-600 text-sm mb-4 line-clamp-2">
                    {perfume.description}
                  </p>

                  {/* 하단 정보 */}
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <span className={`px-2 py-1 rounded text-xs font-medium ${
                        perfume.price_range === 'budget' ? 'bg-green-100 text-green-800' :
                        perfume.price_range === 'mid-range' ? 'bg-yellow-100 text-yellow-800' :
                        'bg-red-100 text-red-800'
                      }`}>
                        {perfume.price_range === 'budget' && '저가'}
                        {perfume.price_range === 'mid-range' && '중가'}
                        {perfume.price_range === 'luxury' && '고가'}
                      </span>
                      <span className="text-xs text-gray-500 capitalize">
                        {perfume.gender_target === 'male' && '남성용'}
                        {perfume.gender_target === 'female' && '여성용'}
                        {perfume.gender_target === 'unisex' && '유니섹스'}
                      </span>
                    </div>
                    <Star className="w-4 h-4 text-yellow-400" />
                  </div>
                </div>
              </Link>
            ))}
          </div>
        )}

        {/* 결과 개수 */}
        <div className="mt-8 text-center text-gray-600">
          총 {filteredPerfumes.length}개의 향수를 찾았습니다.
        </div>
      </div>
    </div>
  );
};

export default PerfumeList; 