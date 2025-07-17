import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Sparkles, ArrowRight, CheckCircle, Heart, Star } from 'lucide-react';
import { recommendationAPI } from '../services/api';

const getCategoryName = (cat) => {
  const names = {
    floral: '플로럴',
    woody: '우디',
    fresh: '프레시',
    oriental: '오리엔탈',
    citrus: '시트러스',
    musk: '머스크',
    aquatic: '아쿠아틱',
    green: '그린',
    gourmand: '구르망',
    powdery: '파우더리',
    fruity: '프루티',
    aromatic: '아로마틱',
    chypre: '시프레',
    fougere: '푸제르',
    amber: '앰버',
    spicy: '스파이시',
    cozy: '코지',
    other: '기타'
  };
  return names[cat] || cat;
};

const Recommendation = () => {
  const navigate = useNavigate();
  const [currentStep, setCurrentStep] = useState(1);
  const [formData, setFormData] = useState({
    age: '',
    gender: '',
    personality: '',
    purpose: '',
    fashionstyle: '',
    prefercolor: ''
  });
  const [recommendation, setRecommendation] = useState(null);
  const [loading, setLoading] = useState(false);

  const steps = [
    { id: 1, title: '기본 정보', description: '나이, 성별, 성격' },
    { id: 2, title: '선호도', description: '추천 목적, 패션 스타일, 선호 색상' },
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
      // cost, durability 제거
      const { age, gender, personality, purpose, fashionstyle, prefercolor } = formData;
      const requestData = { age, gender, personality, purpose, fashionstyle, prefercolor };
      const response = await recommendationAPI.getRecommendation(requestData);
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
      alert('피드백 제출에 실패했습니다. 다시 시도해주세요.');
    }
  };

  const mbtiOptions = [
    'ISTJ', 'ISFJ', 'INFJ', 'INTJ', 'ISTP', 'ISFP', 'INFP', 'INTP',
    'ESTP', 'ESFP', 'ENFP', 'ENTP', 'ESTJ', 'ESFJ', 'ENFJ', 'ENTJ'
  ];
  const fashionstyleOptions = ['캐주얼', '미니멀/심플', '스트리트', '클래식/정장', '로맨틱/러블리', '빈티지', '스포티', '모던/시크', '자유로운 스타일(혼합형)'];
  const prefercolorOptions = ['흰색', '검정', '베이지/브라운', '파란색', '분홍/코랄', '빨간색', '초록/민트', '보라색', '노란색/오렌지'];
  const purposeOptions = ['좋은 인상', '기분 전환', '자기만족', '데이트', '공식적인 자리', '특별한 날', '차별화된 스타일'];

  const renderStep1 = () => (
    <div className="space-y-6">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">나이</label>
        <input
          type="number"
          min="15"
          max="65"
          placeholder="15-65세 사이의 나이를 입력하세요"
          value={formData.age}
          onChange={(e) => handleInputChange('age', e.target.value)}
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
        />
        <p className="text-sm text-gray-500 mt-1">15세부터 65세까지 입력 가능합니다</p>
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">성별</label>
        <select
          value={formData.gender}
          onChange={(e) => handleInputChange('gender', e.target.value)}
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
        >
          <option value="">성별을 선택하세요</option>
          <option value="">선택 안함</option>
          <option value="남">남</option>
          <option value="여">여</option>
        </select>
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">성격(MBTI)</label>
        <select
          value={formData.personality}
          onChange={(e) => handleInputChange('personality', e.target.value)}
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
        >
          <option value="">MBTI를 선택하세요</option>
          <option value="">선택 안함</option>
          {mbtiOptions.map((mbti) => (
            <option key={mbti} value={mbti}>{mbti}</option>
          ))}
        </select>
      </div>
    </div>
  );

  const renderStep2 = () => (
    <div className="space-y-6">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">추천 목적</label>
        <select
          value={formData.purpose}
          onChange={(e) => handleInputChange('purpose', e.target.value)}
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
        >
          <option value="">목적을 선택하세요</option>
          <option value="">선택 안함</option>
          {purposeOptions.map((purpose) => (
            <option key={purpose} value={purpose}>{purpose}</option>
          ))}
        </select>
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">패션 스타일</label>
        <select
          value={formData.fashionstyle}
          onChange={(e) => handleInputChange('fashionstyle', e.target.value)}
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
        >
          <option value="">패션 스타일을 선택하세요</option>
          <option value="">선택 안함</option>
          {fashionstyleOptions.map((f) => (
            <option key={f} value={f}>{f}</option>
          ))}
        </select>
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">선호 색상</label>
        <select
          value={formData.prefercolor}
          onChange={(e) => handleInputChange('prefercolor', e.target.value)}
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
        >
          <option value="">색상을 선택하세요</option>
          <option value="">선택 안함</option>
          {prefercolorOptions.map((c) => (
            <option key={c} value={c}>{c}</option>
          ))}
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
              <div className="bg-gradient-to-r from-blue-50 to-purple-50 p-4 rounded-lg border border-blue-200">
                <div className="flex items-start gap-3">
                  <span className="text-2xl">🤖</span>
                  <p className="text-gray-700 leading-relaxed">{reason}</p>
                </div>
              </div>
            </div>

            <div>
              <h4 className="font-semibold text-gray-900 mb-2">예측된 향수 카테고리</h4>
              <p className="text-sm text-gray-600 mb-3">AI가 분석한 결과, 다음 향수 카테고리들이 당신에게 적합할 것으로 예측됩니다:</p>
              <div className="flex flex-wrap gap-2 mb-4">
                {recommendation.predicted_categories?.map((category, index) => {
                  const getCategoryColor = (cat) => {
                    const colors = {
                      floral: 'bg-pink-100 text-pink-800 border-pink-200',
                      woody: 'bg-amber-100 text-amber-800 border-amber-200',
                      fresh: 'bg-blue-100 text-blue-800 border-blue-200',
                      oriental: 'bg-purple-100 text-purple-800 border-purple-200',
                      citrus: 'bg-green-100 text-green-800 border-green-200',
                      musk: 'bg-gray-100 text-gray-800 border-gray-200',
                      aquatic: 'bg-blue-100 text-blue-800 border-blue-200',
                      green: 'bg-green-100 text-green-800 border-green-200',
                      gourmand: 'bg-yellow-100 text-yellow-800 border-yellow-200',
                      powdery: 'bg-pink-100 text-pink-800 border-pink-200',
                      fruity: 'bg-red-100 text-red-800 border-red-200',
                      aromatic: 'bg-green-100 text-green-800 border-green-200',
                      chypre: 'bg-purple-100 text-purple-800 border-purple-200',
                      fougere: 'bg-blue-100 text-blue-800 border-blue-200',
                      amber: 'bg-orange-100 text-orange-800 border-orange-200',
                      spicy: 'bg-red-100 text-red-800 border-red-200',
                      light_floral: 'bg-pink-100 text-pink-800 border-pink-200',
                      white_floral: 'bg-white-100 text-gray-800 border-gray-200',
                      casual: 'bg-gray-100 text-gray-800 border-gray-200',
                      cozy: 'bg-brown-100 text-brown-800 border-brown-200',
                      other: 'bg-gray-100 text-gray-800 border-gray-200'
                    };
                    return colors[cat] || colors.other;
                  };

                  const getCategoryIcon = (cat) => {
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
                      light_floral: '🌸',
                      white_floral: '🌼',
                      casual: '👕',
                      cozy: '🏠',
                      other: '💫'
                    };
                    return icons[cat] || icons.other;
                  };

                  return (
                    <span
                      key={index}
                      className={`px-4 py-2 rounded-full text-sm font-medium border ${getCategoryColor(category)} flex items-center gap-2 shadow-sm hover:shadow-md transition-shadow duration-200`}
                    >
                      <span className="text-lg">{getCategoryIcon(category)}</span>
                      <span>{getCategoryName(category)}</span>
                    </span>
                  );
                })}
              </div>
              {recommendation.predicted_categories?.length > 1 && (
                <p className="text-xs text-gray-500 italic">
                  💡 여러 카테고리가 예측된 경우, 이는 복합적인 향수 조합을 선호한다는 의미입니다.
                </p>
              )}
            </div>

            <div>
              <h4 className="font-semibold text-gray-900 mb-2">매칭 요소</h4>
              <p className="text-sm text-gray-600 mb-3">이 추천이 선택된 주요 이유들입니다:</p>
              <div className="flex flex-wrap gap-2">
                {match_factors.map((factor, index) => (
                  <span
                    key={index}
                    className="px-3 py-2 bg-primary-100 text-primary-700 rounded-full text-sm font-medium border border-primary-200 shadow-sm hover:shadow-md transition-shadow duration-200 flex items-center gap-2"
                  >
                    <span className="text-primary-600">✨</span>
                    <span>{factor}</span>
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

          {recommendation.notes_recommendation && (
            <div className="mt-8">
              <h4 className="font-semibold text-gray-900 mb-2">노트별 추천 향조</h4>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {['top', 'middle', 'base'].map((note) => {
                  const noteKor = note === 'top' ? '탑 노트' : note === 'middle' ? '미들 노트' : '베이스 노트';
                  const rec = recommendation.notes_recommendation[note];
                  return (
                    <div key={note} className="bg-gradient-to-br from-primary-50 to-secondary-50 rounded-xl p-4 border border-primary-100 shadow-sm flex flex-col items-center">
                      <span className="text-xs text-gray-500 mb-1">{noteKor}</span>
                      <span className="text-lg font-bold text-primary-700 mb-1">{rec && rec.category ? getCategoryName(rec.category) : '-'}</span>
                      <span className="text-sm text-gray-600">{rec && rec.confidence !== undefined ? `${Math.round(rec.confidence * 100)}% 매칭` : '-'}</span>
                    </div>
                  );
                })}
              </div>
            </div>
          )}

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