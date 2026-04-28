import { Link } from 'react-router';
import { ArrowRight, TrendingUp, Target, CheckCircle, BarChart3 } from 'lucide-react';
import { ScoreCard } from '../components/ScoreCard';

export function DashboardPage() {
  return (
    <div className="min-h-screen p-8" style={{ backgroundColor: '#F5F7FA' }}>
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl mb-2" style={{ color: '#023155' }}>Validate Your Startup Idea with AI</h1>
        <p style={{ color: '#443646' }}>
          Analyze market demand, competition, feasibility, and risk using AI-powered validation.
        </p>
      </div>

      {/* Hero Card */}
      <div className="bg-white rounded-2xl shadow-sm p-8 mb-8" style={{ border: '1px solid #648C9C33' }}>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
          <div>
            <h2 className="text-2xl mb-4" style={{ color: '#023155' }}>
              Get Evidence-Based Insights for Your Startup
            </h2>
            <p className="mb-6" style={{ color: '#443646' }}>
              Our AI analyzes thousands of startups to give you accurate predictions about market demand,
              competition levels, and success probability. Make data-driven decisions before investing time and money.
            </p>
            <div className="flex flex-wrap gap-4">
              <Link
                to="/validate"
                className="text-white px-6 py-3 rounded-xl transition-all flex items-center gap-2 group"
                style={{ background: 'linear-gradient(135deg, #0489A7 0%, #023155 100%)' }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.background = 'linear-gradient(135deg, #023155 0%, #0489A7 100%)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.background = 'linear-gradient(135deg, #0489A7 0%, #023155 100%)';
                }}
              >
                Validate New Idea
                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </Link>
              <Link
                to="/results"
                className="px-6 py-3 rounded-xl transition-all"
                style={{ border: '1px solid #648C9C', color: '#023155' }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.borderColor = '#0489A7';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.borderColor = '#648C9C';
                }}
              >
                View Example Report
              </Link>
            </div>
          </div>
          <div className="rounded-xl p-8 flex items-center justify-center" style={{ background: 'linear-gradient(135deg, #0489A71A 0%, #6489C9C1A 100%)' }}>
            <div className="relative">
              <div className="w-48 h-48 bg-white rounded-2xl shadow-lg flex items-center justify-center">
                <BarChart3 className="w-24 h-24" style={{ color: '#0489A7' }} />
              </div>
              <div className="absolute -top-4 -right-4 w-16 h-16 rounded-xl flex items-center justify-center shadow-lg animate-pulse" style={{ backgroundColor: '#F5A406' }}>
                <Sparkles className="w-8 h-8 text-white" />
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <ScoreCard
          title="Market Demand"
          score={7.8}
          maxScore={10}
          icon={TrendingUp}
          color="cyan"
        />
        <ScoreCard
          title="Competition"
          score={6.2}
          maxScore={10}
          icon={Target}
          color="green"
        />
        <ScoreCard
          title="Feasibility"
          score={8.5}
          maxScore={10}
          icon={CheckCircle}
          color="yellow"
        />
        <ScoreCard
          title="Overall Score"
          score={7.5}
          maxScore={10}
          icon={BarChart3}
          color="indigo"
        />
      </div>

      {/* Recent Activity */}
      <div className="bg-white rounded-2xl shadow-sm p-6" style={{ border: '1px solid #648C9C33' }}>
        <h3 className="text-lg mb-4" style={{ color: '#023155' }}>Recent Validations</h3>
        <div className="space-y-3">
          <ActivityItem
            title="AI-powered meal planning app"
            score={7.2}
            date="2 hours ago"
            status="completed"
          />
          <ActivityItem
            title="B2B SaaS for remote teams"
            score={8.1}
            date="1 day ago"
            status="completed"
          />
          <ActivityItem
            title="Sustainable fashion marketplace"
            score={6.8}
            date="3 days ago"
            status="completed"
          />
        </div>
      </div>
    </div>
  );
}

function ActivityItem({ 
  title, 
  score, 
  date, 
  status 
}: { 
  title: string; 
  score: number; 
  date: string; 
  status: string;
}) {
  return (
    <div className="flex items-center justify-between p-4 hover:bg-gray-50 rounded-lg transition-colors">
      <div className="flex items-center gap-4">
        <div className="w-10 h-10 rounded-lg flex items-center justify-center" style={{ backgroundColor: '#0489A71A' }}>
          <BarChart3 className="w-5 h-5" style={{ color: '#0489A7' }} />
        </div>
        <div>
          <p className="font-medium" style={{ color: '#023155' }}>{title}</p>
          <p className="text-sm" style={{ color: '#648C9C' }}>{date}</p>
        </div>
      </div>
      <div className="text-right">
        <p className="text-lg font-semibold" style={{ color: '#0489A7' }}>{score}</p>
        <p className="text-xs" style={{ color: '#648C9C' }}>score</p>
      </div>
    </div>
  );
}

function Sparkles({ className }: { className?: string }) {
  return (
    <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
    </svg>
  );
}