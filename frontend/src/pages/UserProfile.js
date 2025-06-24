import React, { useState } from 'react';
import { User, Settings, Heart, Clock, Star, Edit3 } from 'lucide-react';

const UserProfile = () => {
  const [activeTab, setActiveTab] = useState('profile');
  const [isEditing, setIsEditing] = useState(false);
  
  // 샘플 사용자 데이터 (실제로는 API에서 가져옴)
  const [userData, setUserData] = useState({
    username: '향수러버',
    email: 'perfume@example.com',
    age: 28,
    gender: 'female',
    personality: 'introvert',
    season_preference: 'spring',
    created_at: '2024-01-15'
  });

  const [preferences, setPreferences] = useState({
    category_preference: 'floral',
    price_preference: 'mid-range',
    intensity_preference: 'medium',
    longevity_preference: 'medium'
  });

  // 샘플 추천 기록
  const recommendationHistory = [
    {
      id: 1,
      perfume_name: 'Rose Garden',
      perfume_brand: 'Floral Essence',
      confidence_score: 0.92,
      reason: '봄철에 어울리는 신선한 꽃향기입니다',
      created_at: '2024-01-20',
      is_liked: true
    },
    {
      id: 2,
      perfume_name: 'Lavender Dreams',
      perfume_brand: 'Nature Scents',
      confidence_score: 0.88,
      reason: '차분한 라벤더 향이 당신의 내면의 깊이를 표현합니다',
      created_at: '2024-01-18',
      is_liked: null
    }
  ];

  const handleSave = () => {
    setIsEditing(false);
    // 실제로는 API 호출로 데이터 저장
    console.log('사용자 정보 저장:', userData);
  };

  const handleInputChange = (field, value) => {
    setUserData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const getPersonalityText = (personality) => {
    const texts = {
      introvert: '내향적',
      extrovert: '외향적',
      balanced: '균형잡힌'
    };
    return texts[personality] || personality;
  };

  const getSeasonText = (season) => {
    const texts = {
      spring: '봄',
      summer: '여름',
      autumn: '가을',
      winter: '겨울'
    };
    return texts[season] || season;
  };

  const getCategoryText = (category) => {
    const texts = {
      floral: '플로럴',
      woody: '우디',
      fresh: '프레시',
      oriental: '오리엔탈',
      citrus: '시트러스'
    };
    return texts[category] || category;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50 py-12">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* 헤더 */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            내 프로필
          </h1>
          <p className="text-xl text-gray-600">
            나의 향수 선호도와 추천 기록을 확인해보세요
          </p>
        </div>

        {/* 프로필 카드 */}
        <div className="bg-white rounded-2xl shadow-xl p-8 mb-8">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center space-x-4">
              <div className="w-16 h-16 bg-gradient-to-r from-primary-500 to-secondary-500 rounded-full flex items-center justify-center">
                <User className="w-8 h-8 text-white" />
              </div>
              <div>
                <h2 className="text-2xl font-bold text-gray-900">{userData.username}</h2>
                <p className="text-gray-600">회원가입: {userData.created_at}</p>
              </div>
            </div>
            <button
              onClick={() => setIsEditing(!isEditing)}
              className="flex items-center px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
            >
              <Edit3 className="w-4 h-4 mr-2" />
              {isEditing ? '취소' : '편집'}
            </button>
          </div>

          {/* 사용자 정보 */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">이메일</label>
              {isEditing ? (
                <input
                  type="email"
                  value={userData.email}
                  onChange={(e) => handleInputChange('email', e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                />
              ) : (
                <p className="text-gray-900">{userData.email}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">나이</label>
              {isEditing ? (
                <input
                  type="number"
                  value={userData.age}
                  onChange={(e) => handleInputChange('age', e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                />
              ) : (
                <p className="text-gray-900">{userData.age}세</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">성별</label>
              {isEditing ? (
                <select
                  value={userData.gender}
                  onChange={(e) => handleInputChange('gender', e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                >
                  <option value="male">남성</option>
                  <option value="female">여성</option>
                  <option value="other">기타</option>
                </select>
              ) : (
                <p className="text-gray-900">
                  {userData.gender === 'male' ? '남성' : userData.gender === 'female' ? '여성' : '기타'}
                </p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">성격</label>
              {isEditing ? (
                <select
                  value={userData.personality}
                  onChange={(e) => handleInputChange('personality', e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                >
                  <option value="introvert">내향적</option>
                  <option value="extrovert">외향적</option>
                  <option value="balanced">균형잡힌</option>
                </select>
              ) : (
                <p className="text-gray-900">{getPersonalityText(userData.personality)}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">선호 계절</label>
              {isEditing ? (
                <select
                  value={userData.season_preference}
                  onChange={(e) => handleInputChange('season_preference', e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                >
                  <option value="spring">봄</option>
                  <option value="summer">여름</option>
                  <option value="autumn">가을</option>
                  <option value="winter">겨울</option>
                </select>
              ) : (
                <p className="text-gray-900">{getSeasonText(userData.season_preference)}</p>
              )}
            </div>
          </div>

          {isEditing && (
            <div className="mt-6 text-center">
              <button
                onClick={handleSave}
                className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
              >
                저장
              </button>
            </div>
          )}
        </div>

        {/* 탭 네비게이션 */}
        <div className="bg-white rounded-2xl shadow-xl">
          <div className="border-b border-gray-200">
            <nav className="flex space-x-8 px-8">
              <button
                onClick={() => setActiveTab('profile')}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'profile'
                    ? 'border-primary-500 text-primary-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <User className="w-4 h-4 inline mr-2" />
                선호도
              </button>
              <button
                onClick={() => setActiveTab('history')}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'history'
                    ? 'border-primary-500 text-primary-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <Clock className="w-4 h-4 inline mr-2" />
                추천 기록
              </button>
            </nav>
          </div>

          <div className="p-8">
            {activeTab === 'profile' && (
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-6">향수 선호도</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="bg-gray-50 rounded-lg p-4">
                    <h4 className="font-medium text-gray-900 mb-2">선호 카테고리</h4>
                    <p className="text-gray-600">{getCategoryText(preferences.category_preference)}</p>
                  </div>
                  <div className="bg-gray-50 rounded-lg p-4">
                    <h4 className="font-medium text-gray-900 mb-2">선호 가격대</h4>
                    <p className="text-gray-600">
                      {preferences.price_preference === 'budget' && '저가'}
                      {preferences.price_preference === 'mid-range' && '중가'}
                      {preferences.price_preference === 'luxury' && '고가'}
                    </p>
                  </div>
                  <div className="bg-gray-50 rounded-lg p-4">
                    <h4 className="font-medium text-gray-900 mb-2">선호 강도</h4>
                    <p className="text-gray-600">
                      {preferences.intensity_preference === 'light' && '약함'}
                      {preferences.intensity_preference === 'medium' && '보통'}
                      {preferences.intensity_preference === 'strong' && '강함'}
                    </p>
                  </div>
                  <div className="bg-gray-50 rounded-lg p-4">
                    <h4 className="font-medium text-gray-900 mb-2">선호 지속시간</h4>
                    <p className="text-gray-600">
                      {preferences.longevity_preference === 'short' && '짧음'}
                      {preferences.longevity_preference === 'medium' && '보통'}
                      {preferences.longevity_preference === 'long' && '길음'}
                    </p>
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'history' && (
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-6">추천 기록</h3>
                {recommendationHistory.length === 0 ? (
                  <div className="text-center py-8">
                    <Clock className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                    <p className="text-gray-600">아직 추천 기록이 없습니다.</p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {recommendationHistory.map((rec) => (
                      <div key={rec.id} className="border border-gray-200 rounded-lg p-4">
                        <div className="flex items-start justify-between mb-2">
                          <div>
                            <h4 className="font-medium text-gray-900">{rec.perfume_name}</h4>
                            <p className="text-sm text-gray-600">{rec.perfume_brand}</p>
                          </div>
                          <div className="flex items-center space-x-2">
                            <span className="flex items-center text-sm text-gray-500">
                              <Star className="w-4 h-4 text-yellow-400 mr-1" />
                              {Math.round(rec.confidence_score * 100)}%
                            </span>
                            {rec.is_liked === true && (
                              <Heart className="w-4 h-4 text-red-500" />
                            )}
                          </div>
                        </div>
                        <p className="text-sm text-gray-600 mb-2">{rec.reason}</p>
                        <p className="text-xs text-gray-500">{rec.created_at}</p>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default UserProfile; 