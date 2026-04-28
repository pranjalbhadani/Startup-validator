import { FileText, Calendar, Download } from 'lucide-react';

export function ReportsPage() {
  return (
    <div className="min-h-screen p-8" style={{ backgroundColor: '#F5F7FA' }}>
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl mb-2" style={{ color: '#023155' }}>Validation Reports</h1>
        <p style={{ color: '#443646' }}>Access all your saved validation reports and insights.</p>
      </div>

      {/* Reports Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <ReportCard
          title="AI-Powered Meal Planning App"
          score={7.2}
          date="March 8, 2026"
          status="completed"
        />
        <ReportCard
          title="B2B SaaS for Remote Teams"
          score={8.1}
          date="March 7, 2026"
          status="completed"
        />
        <ReportCard
          title="Sustainable Fashion Marketplace"
          score={6.8}
          date="March 5, 2026"
          status="completed"
        />
        <ReportCard
          title="EdTech Platform for Coding"
          score={7.9}
          date="March 3, 2026"
          status="completed"
        />
        <ReportCard
          title="HealthTech Telemedicine App"
          score={8.5}
          date="March 1, 2026"
          status="completed"
        />
        <ReportCard
          title="FinTech Expense Tracker"
          score={7.0}
          date="February 28, 2026"
          status="completed"
        />
      </div>
    </div>
  );
}

function ReportCard({ 
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
    <div className="bg-white rounded-xl p-6 hover:shadow-lg transition-shadow group" style={{ border: '1px solid #648C9C33' }}>
      <div className="flex items-start justify-between mb-4">
        <div className="w-12 h-12 rounded-lg flex items-center justify-center" style={{ backgroundColor: '#0489A71A' }}>
          <FileText className="w-6 h-6" style={{ color: '#0489A7' }} />
        </div>
        <button className="opacity-0 group-hover:opacity-100 p-2 hover:bg-gray-100 rounded-lg transition-all">
          <Download className="w-4 h-4" style={{ color: '#443646' }} />
        </button>
      </div>
      
      <h3 className="font-semibold mb-2 line-clamp-2" style={{ color: '#023155' }}>{title}</h3>
      
      <div className="flex items-center gap-2 text-sm mb-4" style={{ color: '#648C9C' }}>
        <Calendar className="w-4 h-4" />
        <span>{date}</span>
      </div>

      <div className="flex items-center justify-between">
        <div>
          <p className="text-2xl font-semibold" style={{ color: '#0489A7' }}>{score}</p>
          <p className="text-xs" style={{ color: '#648C9C' }}>Overall Score</p>
        </div>
        <span className="px-3 py-1 rounded-full text-xs" style={{ backgroundColor: '#648C9C1A', color: '#648C9C' }}>
          {status}
        </span>
      </div>
    </div>
  );
}