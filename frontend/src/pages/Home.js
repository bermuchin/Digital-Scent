import React from 'react';
import { Link } from 'react-router-dom';
import { Sparkles, Flower, User, ArrowRight, Star, Users, Award } from 'lucide-react';

const Home = () => {
  const features = [
    {
      icon: Sparkles,
      title: 'AI 기반 추천',
      description: '머신러닝 알고리즘으로 당신에게 최적의 향수를 추천합니다',
      color: 'from-purple-500 to-pink-500'
    },
    {
      icon: Flower,
      title: '다양한 향수',
      description: '플로럴, 우디, 프레시 등 다양한 카테고리의 향수를 만나보세요',
      color: 'from-green-500 to-blue-500'
    },
    {
      icon: User,
      title: '개인화된 경험',
      description: '나이, 성별, 성격, 계절 선호도에 맞춘 맞춤형 서비스',
      color: 'from-orange-500 to-red-500'
    }
  ];

  const stats = [
    { icon: Users, label: '사용자', value: '1,000+' },
    { icon: Flower, label: '향수', value: '50+' },
    { icon: Star, label: '만족도', value: '4.8/5' },
    { icon: Award, label: '추천 정확도', value: '95%' }
  ];

  return (
    <div className="min-h-screen">
      {/* 히어로 섹션 */}
      <section className="relative py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold text-white mb-6">
              당신만을 위한
              <span className="block bg-gradient-to-r from-pink-400 to-purple-400 bg-clip-text text-transparent">
                향수 추천
              </span>
            </h1>
            <p className="text-xl md:text-2xl text-white/90 mb-8 max-w-3xl mx-auto">
              AI가 분석한 당신의 선호도에 맞는 완벽한 향수를 찾아드리고, 
              직접 제조할 수 있는 레시피까지 제공합니다
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to="/recommendation"
                className="inline-flex items-center justify-center px-8 py-4 bg-white text-primary-600 font-semibold rounded-lg hover:bg-gray-100 transition-colors duration-200"
              >
                향수 추천받기
                <ArrowRight className="ml-2 w-5 h-5" />
              </Link>
              <Link
                to="/perfumes"
                className="inline-flex items-center justify-center px-8 py-4 border-2 border-white text-white font-semibold rounded-lg hover:bg-white hover:text-primary-600 transition-colors duration-200"
              >
                향수 둘러보기
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* 통계 섹션 */}
      <section className="py-16 bg-white/10 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {stats.map((stat, index) => {
              const Icon = stat.icon;
              return (
                <div key={index} className="text-center">
                  <div className="inline-flex items-center justify-center w-16 h-16 bg-white/20 rounded-full mb-4">
                    <Icon className="w-8 h-8 text-white" />
                  </div>
                  <div className="text-3xl font-bold text-white mb-2">{stat.value}</div>
                  <div className="text-white/80">{stat.label}</div>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* 기능 소개 섹션 */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              왜 우리 서비스를 선택해야 할까요?
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              과학적 분석과 개인화된 추천으로 당신만의 완벽한 향수를 찾아드립니다
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            {features.map((feature, index) => {
              const Icon = feature.icon;
              return (
                <div key={index} className="text-center p-8 rounded-2xl bg-gray-50 hover:bg-white hover:shadow-xl transition-all duration-300 card-hover">
                  <div className={`inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r ${feature.color} rounded-full mb-6`}>
                    <Icon className="w-8 h-8 text-white" />
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-4">{feature.title}</h3>
                  <p className="text-gray-600">{feature.description}</p>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* CTA 섹션 */}
      <section className="py-20 bg-gradient-to-r from-primary-600 to-secondary-600">
        <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-6">
            지금 바로 시작해보세요
          </h2>
          <p className="text-xl text-white/90 mb-8">
            몇 가지 간단한 질문만으로 당신에게 맞는 향수를 찾아드립니다
          </p>
          <Link
            to="/recommendation"
            className="inline-flex items-center justify-center px-8 py-4 bg-white text-primary-600 font-semibold rounded-lg hover:bg-gray-100 transition-colors duration-200"
          >
            무료로 향수 추천받기
            <ArrowRight className="ml-2 w-5 h-5" />
          </Link>
        </div>
      </section>
    </div>
  );
};

export default Home; 