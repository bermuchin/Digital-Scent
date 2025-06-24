import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { ArrowLeft, Star, Clock, Users, Heart, Share2, BookOpen } from 'lucide-react';
import { perfumeAPI } from '../services/api';

const PerfumeDetail = () => {
  const { id } = useParams();
  const [perfume, setPerfume] = useState(null);
  const [recipes, setRecipes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('info');

  useEffect(() => {
    loadPerfumeData();
  }, [id]);

  const loadPerfumeData = async () => {
    setLoading(true);
    try {
      const [perfumeResponse, recipesResponse] = await Promise.all([
        perfumeAPI.getPerfume(id),
        perfumeAPI.getRecipes(id)
      ]);
      setPerfume(perfumeResponse.data);
      setRecipes(recipesResponse.data);
    } catch (error) {
      console.error('향수 데이터 로드 실패:', error);
    } finally {
      setLoading(false);
    }
  };

  const getCategoryColor = (category) => {
    const colors = {
      floral: 'bg-pink-100 text-pink-800',
      woody: 'bg-amber-100 text-amber-800',
      fresh: 'bg-blue-100 text-blue-800',
      oriental: 'bg-purple-100 text-purple-800',
      citrus: 'bg-green-100 text-green-800'
    };
    return colors[category] || 'bg-gray-100 text-gray-800';
  };

  const getCategoryIcon = (category) => {
    const icons = {
      floral: '🌸',
      woody: '🌳',
      fresh: '🌊',
      oriental: '🕌',
      citrus: '🍋'
    };
    return icons[category] || '💫';
  };

  const getSeasonIcon = (season) => {
    const icons = {
      spring: '🌸',
      summer: '☀️',
      autumn: '🍂',
      winter: '❄️',
      all: '🌍'
    };
    return icons[season] || '🌍';
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50 py-12">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">향수 정보를 불러오는 중...</p>
          </div>
        </div>
      </div>
    );
  }

  if (!perfume) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50 py-12">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">향수를 찾을 수 없습니다</h2>
            <Link
              to="/perfumes"
              className="inline-flex items-center px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
            >
              <ArrowLeft className="w-4 h-4 mr-2" />
              향수 목록으로 돌아가기
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50 py-12">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* 뒤로가기 버튼 */}
        <Link
          to="/perfumes"
          className="inline-flex items-center text-gray-600 hover:text-primary-600 mb-6"
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          향수 목록으로 돌아가기
        </Link>

        {/* 향수 헤더 */}
        <div className="bg-white rounded-2xl shadow-xl p-8 mb-8">
          <div className="flex flex-col lg:flex-row gap-8">
            {/* 향수 이미지 영역 */}
            <div className="lg:w-1/3">
              <div className="w-full h-64 bg-gradient-to-br from-primary-100 to-secondary-100 rounded-xl flex items-center justify-center">
                <div className="text-6xl">
                  {getCategoryIcon(perfume.category)}
                </div>
              </div>
            </div>

            {/* 향수 정보 */}
            <div className="lg:w-2/3">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h1 className="text-3xl font-bold text-gray-900 mb-2">
                    {perfume.name}
                  </h1>
                  <p className="text-xl text-gray-600 mb-4">{perfume.brand}</p>
                </div>
                <div className="flex space-x-2">
                  <button className="p-2 text-gray-400 hover:text-red-500 transition-colors">
                    <Heart className="w-5 h-5" />
                  </button>
                  <button className="p-2 text-gray-400 hover:text-blue-500 transition-colors">
                    <Share2 className="w-5 h-5" />
                  </button>
                </div>
              </div>

              {/* 태그들 */}
              <div className="flex flex-wrap gap-2 mb-6">
                <span className={`px-3 py-1 rounded-full text-sm font-medium ${getCategoryColor(perfume.category)}`}>
                  <span className="mr-1">{getCategoryIcon(perfume.category)}</span>
                  {perfume.category === 'floral' && '플로럴'}
                  {perfume.category === 'woody' && '우디'}
                  {perfume.category === 'fresh' && '프레시'}
                  {perfume.category === 'oriental' && '오리엔탈'}
                  {perfume.category === 'citrus' && '시트러스'}
                </span>
                <span className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm">
                  <span className="mr-1">{getSeasonIcon(perfume.season_suitability)}</span>
                  {perfume.season_suitability === 'spring' && '봄'}
                  {perfume.season_suitability === 'summer' && '여름'}
                  {perfume.season_suitability === 'autumn' && '가을'}
                  {perfume.season_suitability === 'winter' && '겨울'}
                  {perfume.season_suitability === 'all' && '사계절'}
                </span>
                <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                  perfume.price_range === 'budget' ? 'bg-green-100 text-green-800' :
                  perfume.price_range === 'mid-range' ? 'bg-yellow-100 text-yellow-800' :
                  'bg-red-100 text-red-800'
                }`}>
                  {perfume.price_range === 'budget' && '저가'}
                  {perfume.price_range === 'mid-range' && '중가'}
                  {perfume.price_range === 'luxury' && '고가'}
                </span>
              </div>

              {/* 설명 */}
              <p className="text-gray-600 mb-6 leading-relaxed">
                {perfume.description}
              </p>

              {/* 통계 */}
              <div className="flex items-center space-x-6 text-sm text-gray-500">
                <div className="flex items-center">
                  <Star className="w-4 h-4 text-yellow-400 mr-1" />
                  <span>4.8/5</span>
                </div>
                <div className="flex items-center">
                  <Users className="w-4 h-4 mr-1" />
                  <span>1,234명이 추천</span>
                </div>
                <div className="flex items-center">
                  <Clock className="w-4 h-4 mr-1" />
                  <span>지속시간: 6-8시간</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* 탭 네비게이션 */}
        <div className="bg-white rounded-2xl shadow-xl mb-8">
          <div className="border-b border-gray-200">
            <nav className="flex space-x-8 px-8">
              <button
                onClick={() => setActiveTab('info')}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'info'
                    ? 'border-primary-500 text-primary-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                향수 정보
              </button>
              <button
                onClick={() => setActiveTab('recipe')}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'recipe'
                    ? 'border-primary-500 text-primary-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <BookOpen className="w-4 h-4 inline mr-2" />
                제조법
              </button>
            </nav>
          </div>

          <div className="p-8">
            {activeTab === 'info' && (
              <div className="space-y-6">
                {/* 노트 정보 */}
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">향수 노트</h3>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div className="bg-gradient-to-br from-yellow-50 to-orange-50 p-4 rounded-lg">
                      <h4 className="font-medium text-gray-900 mb-2">톱 노트</h4>
                      <p className="text-gray-600 text-sm">{perfume.top_notes}</p>
                    </div>
                    <div className="bg-gradient-to-br from-pink-50 to-purple-50 p-4 rounded-lg">
                      <h4 className="font-medium text-gray-900 mb-2">미들 노트</h4>
                      <p className="text-gray-600 text-sm">{perfume.middle_notes}</p>
                    </div>
                    <div className="bg-gradient-to-br from-amber-50 to-brown-50 p-4 rounded-lg">
                      <h4 className="font-medium text-gray-900 mb-2">베이스 노트</h4>
                      <p className="text-gray-600 text-sm">{perfume.base_notes}</p>
                    </div>
                  </div>
                </div>

                {/* 상세 정보 */}
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">상세 정보</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="flex justify-between py-2 border-b border-gray-100">
                      <span className="text-gray-600">성격 매칭</span>
                      <span className="font-medium">{perfume.personality_match}</span>
                    </div>
                    <div className="flex justify-between py-2 border-b border-gray-100">
                      <span className="text-gray-600">연령대</span>
                      <span className="font-medium">{perfume.age_group}</span>
                    </div>
                    <div className="flex justify-between py-2 border-b border-gray-100">
                      <span className="text-gray-600">성별 타겟</span>
                      <span className="font-medium capitalize">{perfume.gender_target}</span>
                    </div>
                    <div className="flex justify-between py-2 border-b border-gray-100">
                      <span className="text-gray-600">계절 적합성</span>
                      <span className="font-medium capitalize">{perfume.season_suitability}</span>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'recipe' && (
              <div>
                <div className="mb-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">제조법</h3>
                  <p className="text-gray-600">
                    이 향수를 직접 제조할 수 있는 상세한 레시피입니다.
                  </p>
                </div>

                {recipes.length === 0 ? (
                  <div className="text-center py-8">
                    <BookOpen className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                    <p className="text-gray-600">제조법 정보가 없습니다.</p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {recipes.map((recipe, index) => (
                      <div key={index} className="bg-gray-50 rounded-lg p-4">
                        <div className="flex justify-between items-start mb-2">
                          <h4 className="font-medium text-gray-900">{recipe.ingredient_name}</h4>
                          <span className="text-sm font-semibold text-primary-600">
                            {recipe.percentage}%
                          </span>
                        </div>
                        {recipe.notes && (
                          <p className="text-sm text-gray-600">{recipe.notes}</p>
                        )}
                      </div>
                    ))}
                    
                    <div className="mt-6 p-4 bg-blue-50 rounded-lg">
                      <h4 className="font-medium text-blue-900 mb-2">제조 팁</h4>
                      <ul className="text-sm text-blue-800 space-y-1">
                        <li>• 모든 원료를 정확한 비율로 혼합하세요</li>
                        <li>• 알코올 베이스에 에센셜 오일을 천천히 첨가하세요</li>
                        <li>• 완성된 향수는 어두운 곳에서 2-4주 숙성시키세요</li>
                        <li>• 피부 테스트 후 사용하세요</li>
                      </ul>
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>

        {/* 추천 버튼 */}
        <div className="text-center">
          <Link
            to="/recommendation"
            className="inline-flex items-center px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors duration-200"
          >
            <Star className="w-4 h-4 mr-2" />
            나에게 맞는 향수 추천받기
          </Link>
        </div>
      </div>
    </div>
  );
};

export default PerfumeDetail; 