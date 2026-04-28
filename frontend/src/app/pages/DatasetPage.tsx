import { Database, TrendingUp, AlertCircle } from 'lucide-react';

export function DatasetPage() {
  return (
    <div className="min-h-screen p-8" style={{ backgroundColor: '#F5F7FA' }}>
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl mb-2" style={{ color: '#023155' }}>Dataset Insights</h1>
        <p style={{ color: '#443646' }}>
          Explore our comprehensive startup database and market intelligence.
        </p>
      </div>

      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <StatCard
          title="Total Startups"
          value="50,000+"
          change="+2,500 this month"
          icon={Database}
        />
        <StatCard
          title="Industries Covered"
          value="120+"
          change="Across all sectors"
          icon={TrendingUp}
        />
        <StatCard
          title="Data Points"
          value="5M+"
          change="Continuously updated"
          icon={AlertCircle}
        />
      </div>

      {/* Data Sources */}
      <div className="bg-white rounded-2xl shadow-sm p-6 mb-8" style={{ border: '1px solid #648C9C33' }}>
        <h2 className="text-xl mb-4" style={{ color: '#023155' }}>Data Sources</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <SourceCard
            name="Crunchbase"
            description="Comprehensive startup database with funding and growth metrics"
            status="Active"
          />
          {/* <SourceCard
            name="PitchBook"
            description="Private market data and venture capital insights"
            status="Active"
          /> */}
          {/* <SourceCard
            name="CB Insights"
            description="Technology market intelligence and trend analysis"
            status="Active"
          /> */}
          <SourceCard
            name="Proprietary Database"
            description="Custom-collected startup outcomes and performance data"
            status="Active"
          />
        </div>
      </div>

      {/* Market Trends */}
      <div className="bg-white rounded-2xl shadow-sm p-6" style={{ border: '1px solid #648C9C33' }}>
        <h2 className="text-xl mb-4" style={{ color: '#023155' }}>Top Growing Industries</h2>
        <div className="space-y-4">
          <TrendItem industry="AI & Machine Learning" growth={45} />
          <TrendItem industry="HealthTech" growth={38} />
          <TrendItem industry="FinTech" growth={32} />
          <TrendItem industry="EdTech" growth={28} />
          <TrendItem industry="SaaS" growth={25} />
        </div>
      </div>
    </div>
  );
}

function StatCard({ 
  title, 
  value, 
  change, 
  icon: Icon 
}: { 
  title: string; 
  value: string; 
  change: string; 
  icon: React.ElementType;
}) {
  return (
    <div className="bg-white rounded-xl shadow-sm p-6" style={{ border: '1px solid #648C9C33' }}>
      <div className="flex items-center justify-between mb-4">
        <div className="w-12 h-12 rounded-lg flex items-center justify-center" style={{ backgroundColor: '#0489A71A' }}>
          <Icon className="w-6 h-6" style={{ color: '#0489A7' }} />
        </div>
      </div>
      <p className="text-3xl font-semibold mb-1" style={{ color: '#023155' }}>{value}</p>
      <p className="text-sm font-medium mb-1" style={{ color: '#443646' }}>{title}</p>
      <p className="text-xs" style={{ color: '#648C9C' }}>{change}</p>
    </div>
  );
}

function SourceCard({ 
  name, 
  description, 
  status 
}: { 
  name: string; 
  description: string; 
  status: string;
}) {
  return (
    <div className="rounded-xl p-4" style={{ border: '1px solid #648C9C33' }}>
      <div className="flex items-start justify-between mb-2">
        <h3 className="font-semibold" style={{ color: '#023155' }}>{name}</h3>
        <span className="px-2 py-1 rounded text-xs" style={{ backgroundColor: '#648C9C1A', color: '#648C9C' }}>{status}</span>
      </div>
      <p className="text-sm" style={{ color: '#443646' }}>{description}</p>
    </div>
  );
}

function TrendItem({ industry, growth }: { industry: string; growth: number }) {
  return (
    <div className="flex items-center gap-4">
      <div className="flex-1">
        <div className="flex items-center justify-between mb-2">
          <span className="font-medium" style={{ color: '#023155' }}>{industry}</span>
          <span className="text-sm" style={{ color: '#0489A7' }}>+{growth}%</span>
        </div>
        <div className="w-full rounded-full h-2" style={{ backgroundColor: '#E5E7EB' }}>
          <div
            className="h-2 rounded-full transition-all"
            style={{ width: `${growth}%`, backgroundColor: '#0489A7' }}
          />
        </div>
      </div>
    </div>
  );
}