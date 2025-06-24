import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Sparkles, ArrowRight, CheckCircle, Heart, Star } from 'lucide-react';
import { recommendationAPI } from '../services/api';

const Recommendation = () => {
  const navigate = useNavigate();
  const [currentStep, setCurrentStep] = useState(1);
  const [formData, setFormData] = useState({
    age: '',
    gender: '',
    personality: '',
    season_preference: '',
    category_preference: '',
    price_preference: '',
    intensity_preference: '',
    longevity_preference: ''
  });
  const [recommendation, setRecommendation] = useState(null);
  const [loading, setLoading] = useState(false);

  const steps = [
    { id: 1, title: '기본 정보', description: '나이, 성별, 성격' },
    { id: 2, title: '선호도', description: '계절, 카테고리, 가격대' },
    { id: 3, title: '추천 결과', description: 'AI 추천 향수' }
  ];

  const handleInputChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleNext = () => {
    if (currentStep < 2) {
      setCurrentStep(currentStep + 1);
    } else {
      handleSubmit();
    }
  };

  const handleBack = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const response = await recommendationAPI.getRecommendation(formData);
      setRecommendation(response.data);
      setCurrentStep(3);
    } catch (error) {
      console.error('추천 요청 실패:', error);
      alert('추천 요청에 실패했습니다. 다시 시도해주세요.');
    } finally {
      setLoading(false);
    }
  };

  const handleFeedback = async (isLiked) => {
    if (!recommendation) return;
    
    try {
      await recommendationAPI.submitFeedback(recommendation.id, { is_liked: isLiked });
      alert('피드백이 저장되었습니다!');
    } catch (error) {
      console.error('피드백 제출 실패:', error);
    }
  };

  const renderStep1 = () => (
    <div className="space-y-6">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          나이
        </label>
        <input
          type="number"
          value={formData.age}
          onChange={(e) => handleInputChange('age', e.target.value)}
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          placeholder="나이를 입력하세요"
          min="1"
          max="100"
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          성별
        </label>
        <select
          value={formData.gender}
          onChange={(e) => handleInputChange('gender', e.target.value)}
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
        >
          <option value="">성별을 선택하세요</option>
          <option value="male">남성</option>
          <option value="female">여성</option>
          <option value="other">기타</option>
        </select>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          성격
        </label>
        <select
          value={formData.personality}
          onChange={(e) => handleInputChange('personality', e.target.value)}
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
        >
          <option value="">성격을 선택하세요</option>
          <option value="introvert">내향적</option>
          <option value="extrovert">외향적</option>
          <option value="balanced">균형잡힌</option>
        </select>
      </div>
    </div>
  );

  const renderStep2 = () => (
    <div className="space-y-6">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          선호하는 계절
        </label>
        <select
          value={formData.season_preference}
          onChange={(e) => handleInputChange('season_preference', e.target.value)}
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
        >
          <option value="">계절을 선택하세요</option>
          <option value="spring">봄</option>
          <option value="summer">여름</option>
          <option value="autumn">가을</option>
          <option value="winter">겨울</option>
        </select>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          선호하는 향수 카테고리
        </label>
        <select
          value={formData.category_preference}
          onChange={(e) => handleInputChange('category_preference', e.target.value)}
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
        >
          <option value="">카테고리를 선택하세요</option>
          <option value="floral">플로럴</option>
          <option value="woody">우디</option>
          <option value="fresh">프레시</option>
          <option value="oriental">오리엔탈</option>
          <option value="citrus">시트러스</option>
        </select>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          선호하는 가격대
        </label>
        <select
          value={formData.price_preference}
          onChange={(e) => handleInputChange('price_preference', e.target.value)}
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
        >
          <option value="">가격대를 선택하세요</option>
          <option value="budget">저가</option>
          <option value="mid-range">중가</option>
          <option value="luxury">고가</option>
        </select>
      </div>
    </div>
  );

  const renderStep3 = () => {
    if (!recommendation) return null;

    const { perfume, confidence_score, reason, match_factors } = recommendation;

    return (
      <div className="space-y-6">
        <div className="bg-white rounded-2xl shadow-xl p-8">
          <div className="text-center mb-6">
            <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-r from-primary-500 to-secondary-500 rounded-full mb-4">
              <Sparkles className="w-10 h-10 text-white" />
            </div>
            <h3 className="text-2xl font-bold text-gray-900 mb-2">
              {perfume.name}
            </h3>
            <p className="text-lg text-gray-600 mb-4">{perfume.brand}</p>
            <div className="flex items-center justify-center space-x-4 text-sm text-gray-500">
              <span className="flex items-center">
                <Star className="w-4 h-4 text-yellow-400 mr-1" />
                {Math.round(confidence_score * 100)}% 매칭
              </span>
              <span className="capitalize">{perfume.category}</span>
              <span className="capitalize">{perfume.price_range}</span>
            </div>
          </div>

          <div className="space-y-4">
            <div>
              <h4 className="font-semibold text-gray-900 mb-2">추천 이유</h4>
              <p className="text-gray-600">{reason}</p>
            </div>

            <div>
              <h4 className="font-semibold text-gray-900 mb-2">매칭 요소</h4>
              <div className="flex flex-wrap gap-2">
                {match_factors.map((factor, index) => (
                  <span
                    key={index}
                    className="px-3 py-1 bg-primary-100 text-primary-700 rounded-full text-sm"
                  >
                    {factor}
                  </span>
                ))}
              </div>
            </div>

            <div>
              <h4 className="font-semibold text-gray-900 mb-2">향수 정보</h4>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                <div>
                  <span className="font-medium text-gray-700">톱 노트:</span>
                  <p className="text-gray-600">{perfume.top_notes}</p>
                </div>
                <div>
                  <span className="font-medium text-gray-700">미들 노트:</span>
                  <p className="text-gray-600">{perfume.middle_notes}</p>
                </div>
                <div>
                  <span className="font-medium text-gray-700">베이스 노트:</span>
                  <p className="text-gray-600">{perfume.base_notes}</p>
                </div>
              </div>
            </div>

            <div>
              <h4 className="font-semibold text-gray-900 mb-2">설명</h4>
              <p className="text-gray-600">{perfume.description}</p>
            </div>
          </div>

          <div className="mt-8 flex flex-col sm:flex-row gap-4">
            <button
              onClick={() => navigate(`/perfumes/${perfume.id}`)}
              className="flex-1 bg-primary-600 text-white py-3 px-6 rounded-lg hover:bg-primary-700 transition-colors duration-200"
            >
              제조법 보기
            </button>
            <div className="flex gap-2">
              <button
                onClick={() => handleFeedback(true)}
                className="flex-1 bg-green-600 text-white py-3 px-6 rounded-lg hover:bg-green-700 transition-colors duration-200 flex items-center justify-center"
              >
                <Heart className="w-4 h-4 mr-2" />
                좋아요
              </button>
              <button
                onClick={() => handleFeedback(false)}
                className="flex-1 bg-red-600 text-white py-3 px-6 rounded-lg hover:bg-red-700 transition-colors duration-200"
              >
                싫어요
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  };

  const renderCurrentStep = () => {
    switch (currentStep) {
      case 1:
        return renderStep1();
      case 2:
        return renderStep2();
      case 3:
        return renderStep3();
      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50 py-12">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* 진행 단계 표시 */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            {steps.map((step, index) => (
              <div key={step.id} className="flex items-center">
                <div className={`flex items-center justify-center w-10 h-10 rounded-full border-2 ${
                  currentStep >= step.id
                    ? 'bg-primary-600 border-primary-600 text-white'
                    : 'bg-white border-gray-300 text-gray-500'
                }`}>
                  {currentStep > step.id ? (
                    <CheckCircle className="w-6 h-6" />
                  ) : (
                    <span className="font-semibold">{step.id}</span>
                  )}
                </div>
                {index < steps.length - 1 && (
                  <div className={`flex-1 h-1 mx-4 ${
                    currentStep > step.id ? 'bg-primary-600' : 'bg-gray-300'
                  }`} />
                )}
              </div>
            ))}
          </div>
          <div className="flex justify-between mt-4">
            {steps.map((step) => (
              <div key={step.id} className="text-center">
                <div className={`text-sm font-medium ${
                  currentStep >= step.id ? 'text-primary-600' : 'text-gray-500'
                }`}>
                  {step.title}
                </div>
                <div className="text-xs text-gray-400">{step.description}</div>
              </div>
            ))}
          </div>
        </div>

        {/* 메인 컨텐츠 */}
        <div className="bg-white rounded-2xl shadow-xl p-8">
          {currentStep < 3 && (
            <div className="text-center mb-8">
              <h2 className="text-3xl font-bold text-gray-900 mb-4">
                {currentStep === 1 ? '기본 정보를 알려주세요' : '선호도를 알려주세요'}
              </h2>
              <p className="text-gray-600">
                {currentStep === 1 
                  ? '나이, 성별, 성격을 알려주시면 더 정확한 추천을 받을 수 있습니다.'
                  : '선호하는 계절과 향수 스타일을 알려주세요.'
                }
              </p>
            </div>
          )}

          {renderCurrentStep()}

          {/* 네비게이션 버튼 */}
          {currentStep < 3 && (
            <div className="flex justify-between mt-8">
              <button
                onClick={handleBack}
                disabled={currentStep === 1}
                className="px-6 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
              >
                이전
              </button>
              <button
                onClick={handleNext}
                disabled={loading}
                className="px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200 flex items-center"
              >
                {loading ? (
                  '처리 중...'
                ) : (
                  <>
                    {currentStep === 2 ? '추천받기' : '다음'}
                    <ArrowRight className="ml-2 w-4 h-4" />
                  </>
                )}
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Recommendation; 