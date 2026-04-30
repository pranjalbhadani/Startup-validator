import { Download, Copy, ChevronDown, TrendingUp, Target, CheckCircle, BarChart3, AlertTriangle, ArrowLeft } from 'lucide-react';
import { ScoreCard } from '../components/ScoreCard';
import { useState } from 'react';
import { useValidation } from '../ValidationContext';
import { Link } from 'react-router';
import type { CompetitorInfo } from '../api';

export function ResultsPage() {
  const [showReasoning, setShowReasoning] = useState(false);
  const { result } = useValidation();

  // If no result is available, show a prompt to run a validation first
  if (!result) {
    return (
      <div className="min-h-screen p-8 flex items-center justify-center" style={{ backgroundColor: '#F5F7FA' }}>
        <div className="text-center max-w-md">
          <div
            className="w-20 h-20 rounded-2xl flex items-center justify-center mx-auto mb-6"
            style={{ backgroundColor: '#0489A71A' }}
          >
            <BarChart3 className="w-10 h-10" style={{ color: '#0489A7' }} />
          </div>
          <h2 className="text-2xl mb-3" style={{ color: '#023155' }}>
            No Validation Results Yet
          </h2>
          <p className="mb-6" style={{ color: '#443646' }}>
            Submit a startup idea for validation to see your AI-powered analysis results here.
          </p>
          <Link
            to="/validate"
            className="inline-flex items-center gap-2 text-white px-6 py-3 rounded-xl transition-all"
            style={{ background: 'linear-gradient(135deg, #0489A7 0%, #023155 100%)' }}
            onMouseEnter={(e) =>
              (e.currentTarget.style.background = 'linear-gradient(135deg, #023155 0%, #0489A7 100%)')
            }
            onMouseLeave={(e) =>
              (e.currentTarget.style.background = 'linear-gradient(135deg, #0489A7 0%, #023155 100%)')
            }
          >
            <ArrowLeft className="w-5 h-5" />
            Go to Validation
          </Link>
        </div>
      </div>
    );
  }

  // Use actual backend values instead of deriving them client-side
  const competitionScore = result.competition_score ?? 0;
  const feasibilityScore = result.feasibility_score ?? 0;
  const marketScore = result.market_score ?? 0;
  const overallScore = result.overall_validation_score ?? Math.max(0, Math.min(10, 10 - competitionScore * 0.5));
  const riskLevel = result.risk_level ?? (competitionScore >= 7 ? 'High' : competitionScore >= 4 ? 'Medium' : 'Low');
  const riskColor =
    riskLevel === 'High' ? '#AE0E31' : riskLevel === 'Medium' ? '#F5A406' : '#648C9C';

  const handleCopyResults = () => {
    const text = `Startup: ${result.startup_name}
Industry: ${result.industry_detected}
Target Market: ${result.target_market}
Core Proposition: ${result.core_proposition}
Revenue Model: ${result.revenue_model}
Competition Score: ${competitionScore}/10
Feasibility Score: ${feasibilityScore}/100
Market Score: ${marketScore}/10
Overall Score: ${overallScore}/10
Risk Level: ${riskLevel}
Competitors Found: ${result.competitors.length}
${result.competitors.map((c) => `  - ${c.competitor_name} (${c.market}, ${c.status}, similarity: ${((1 / (1 + c.similarity_distance)) * 100).toFixed(0)}%)`).join('\n')}`;
    navigator.clipboard.writeText(text);
  };

  return (
    <div className="min-h-screen p-8" style={{ backgroundColor: '#F5F7FA' }}>
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl mb-2" style={{ color: '#023155' }}>Validation Results</h1>
          <p style={{ color: '#443646' }}>AI-powered analysis of your startup idea</p>
        </div>
        <div className="flex gap-3">
          <button
            onClick={handleCopyResults}
            className="flex items-center gap-2 px-4 py-2 rounded-xl transition-all"
            style={{ border: '1px solid #648C9C', color: '#023155' }}
            onMouseEnter={(e) => (e.currentTarget.style.borderColor = '#0489A7')}
            onMouseLeave={(e) => (e.currentTarget.style.borderColor = '#648C9C')}
          >
            <Copy className="w-4 h-4" />
            Copy Results
          </button>
          <Link
            to="/validate"
            className="flex items-center gap-2 px-4 py-2 text-white rounded-xl transition-all"
            style={{ background: 'linear-gradient(135deg, #0489A7 0%, #023155 100%)' }}
            onMouseEnter={(e) =>
              (e.currentTarget.style.background = 'linear-gradient(135deg, #023155 0%, #0489A7 100%)')
            }
            onMouseLeave={(e) =>
              (e.currentTarget.style.background = 'linear-gradient(135deg, #0489A7 0%, #023155 100%)')
            }
          >
            <ArrowLeft className="w-4 h-4" />
            Validate Another
          </Link>
        </div>
      </div>

      {/* Startup Summary */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        <div className="lg:col-span-2 bg-white rounded-2xl shadow-sm p-6" style={{ border: '1px solid #648C9C33' }}>
          <h2 className="text-xl mb-4" style={{ color: '#023155' }}>{result.startup_name}</h2>
          <p className="mb-4" style={{ color: '#443646' }}>
            {result.core_proposition}
          </p>
          <div className="flex flex-wrap gap-2">
            <span className="px-3 py-1 rounded-full text-sm" style={{ backgroundColor: '#0489A71A', color: '#0489A7' }}>
              {result.industry_detected}
            </span>
            <span className="px-3 py-1 rounded-full text-sm" style={{ backgroundColor: '#648C9C1A', color: '#648C9C' }}>
              {result.target_market}
            </span>
            <span className="px-3 py-1 rounded-full text-sm" style={{ backgroundColor: '#4436461A', color: '#443646' }}>
              {result.revenue_model}
            </span>
          </div>
        </div>

        {/* Risk Badge */}
        <div className="bg-white rounded-2xl shadow-sm p-6" style={{ border: '1px solid #648C9C33' }}>
          <h3 className="text-sm font-medium mb-4" style={{ color: '#443646' }}>Risk Assessment</h3>
          <div className="flex items-center justify-center mb-4">
            <div className="relative w-32 h-32">
              <svg className="w-32 h-32 transform -rotate-90">
                <circle cx="64" cy="64" r="56" stroke="#E5E7EB" strokeWidth="12" fill="none" />
                <circle
                  cx="64"
                  cy="64"
                  r="56"
                  stroke={riskColor}
                  strokeWidth="12"
                  fill="none"
                  strokeDasharray={`${(competitionScore / 10) * 351.86} 351.86`}
                  strokeLinecap="round"
                />
              </svg>
              <div className="absolute inset-0 flex flex-col items-center justify-center">
                <span className="text-3xl font-semibold" style={{ color: '#023155' }}>
                  {competitionScore}
                </span>
                <span className="text-sm" style={{ color: '#648C9C' }}>
                  / 10
                </span>
              </div>
            </div>
          </div>
          <div className="text-center">
            <span
              className="inline-flex items-center gap-2 px-4 py-2 rounded-lg"
              style={{ backgroundColor: `${riskColor}1A`, color: riskColor }}
            >
              <AlertTriangle className="w-4 h-4" />
              {riskLevel} Competition
            </span>
          </div>
        </div>
      </div>

      {/* Score Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <ScoreCard
          title="Competition Level"
          score={competitionScore}
          maxScore={10}
          icon={Target}
          color="cyan"
        />
        <ScoreCard
          title="Market Score"
          score={marketScore}
          maxScore={10}
          icon={TrendingUp}
          color="yellow"
        />
        <ScoreCard
          title="Feasibility"
          score={parseFloat((feasibilityScore / 10).toFixed(1))}
          maxScore={10}
          icon={CheckCircle}
          color="green"
        />
        <ScoreCard
          title="Overall Score"
          score={parseFloat(overallScore.toFixed(1))}
          maxScore={10}
          icon={BarChart3}
          color="green"
        />
      </div>

      {/* Competitor Analysis Table */}
      {result.competitors.length > 0 && (
        <div className="mb-8">
          <h2 className="text-xl mb-4" style={{ color: '#023155' }}>Similar Startups Found</h2>
          <div className="bg-white rounded-2xl shadow-sm overflow-hidden" style={{ border: '1px solid #648C9C33' }}>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead style={{ backgroundColor: '#F5F7FA', borderBottom: '1px solid #648C9C33' }}>
                  <tr>
                    <th className="px-6 py-4 text-left text-sm font-medium" style={{ color: '#443646' }}>
                      Startup Name
                    </th>
                    <th className="px-6 py-4 text-left text-sm font-medium" style={{ color: '#443646' }}>
                      Market
                    </th>
                    <th className="px-6 py-4 text-left text-sm font-medium" style={{ color: '#443646' }}>
                      Status
                    </th>
                    <th className="px-6 py-4 text-left text-sm font-medium" style={{ color: '#443646' }}>
                      Source
                    </th>
                    <th className="px-6 py-4 text-left text-sm font-medium" style={{ color: '#443646' }}>
                      Similarity
                    </th>
                  </tr>
                </thead>
                <tbody style={{ borderTop: '1px solid #648C9C33' }}>
                  {result.competitors.map((competitor, index) => (
                    <CompetitorRow key={index} competitor={competitor} />
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* Core Proposition Detail */}
      <div className="mb-8">
        <h2 className="text-xl mb-4" style={{ color: '#023155' }}>Detailed Analysis</h2>
        <div className="bg-white rounded-2xl shadow-sm p-6" style={{ border: '1px solid #648C9C33' }}>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <DetailCard label="Startup Name" value={result.startup_name} />
            <DetailCard label="Industry Detected" value={result.industry_detected} />
            <DetailCard label="Target Market" value={result.target_market} />
            <DetailCard label="Revenue Model" value={result.revenue_model} />
            <DetailCard label="Risk Level" value={riskLevel} />
            <DetailCard label="Trend Assessment" value={result.trend_assessment || '—'} />
            <DetailCard label="Unicorn Potential" value={result.unicorn_potential || '—'} />
            <DetailCard label="Data Sources" value={(result.data_sources_used || []).join(', ') || '—'} />
          </div>
          <div className="mt-6 p-4 rounded-xl" style={{ backgroundColor: '#F5F7FA' }}>
            <h4 className="text-sm font-medium mb-2" style={{ color: '#023155' }}>
              Core Value Proposition
            </h4>
            <p className="text-sm" style={{ color: '#443646' }}>{result.core_proposition}</p>
          </div>
          {result.market_reasoning && (
            <div className="mt-4 p-4 rounded-xl" style={{ backgroundColor: '#0489A71A' }}>
              <h4 className="text-sm font-medium mb-2" style={{ color: '#023155' }}>
                Market Assessment
              </h4>
              <p className="text-sm" style={{ color: '#443646' }}>{result.market_reasoning}</p>
            </div>
          )}
          {result.risk_reasoning && (
            <div className="mt-4 p-4 rounded-xl" style={{ backgroundColor: '#F5A4061A' }}>
              <h4 className="text-sm font-medium mb-2" style={{ color: '#023155' }}>
                Recommendations
              </h4>
              <p className="text-sm" style={{ color: '#443646' }}>{result.risk_reasoning}</p>
            </div>
          )}
        </div>
      </div>

      {/* AI Reasoning */}
      <div className="bg-white rounded-2xl shadow-sm" style={{ border: '1px solid #648C9C33' }}>
        <button
          onClick={() => setShowReasoning(!showReasoning)}
          className="w-full px-6 py-4 flex items-center justify-between text-left transition-colors"
          style={{ color: '#023155' }}
          onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = '#F5F7FA')}
          onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = 'transparent')}
        >
          <span className="text-lg">AI Reasoning & Methodology</span>
          <ChevronDown
            className={`w-5 h-5 transition-transform ${showReasoning ? 'rotate-180' : ''}`}
            style={{ color: '#648C9C' }}
          />
        </button>
        {showReasoning && (
          <div className="px-6 pb-6 space-y-4" style={{ color: '#443646' }}>
            <p>
              Our multi-agent AI pipeline analyzed your startup idea through multiple stages:
            </p>
            <ul className="list-disc list-inside space-y-2 ml-4">
              <li>
                <strong>Stage 1 — Idea Understanding Agent:</strong> Extracted industry, target market,
                core proposition, and revenue model using the Gemini LLM.
              </li>
              <li>
                <strong>Stage 2 — Retrieval Agent:</strong> Searched a unified vector database of
                startup data across multiple sources (Crunchbase, YC, Unicorns, Indian Funding, Product Hunt)
                using ChromaDB.
              </li>
              <li>
                <strong>Stage 3 — Scoring Engine:</strong> Computed feasibility, competition,
                market demand, trend analysis, and risk scores using weighted metrics.
              </li>
            </ul>
            <p>
              The competition score ({competitionScore}/10) reflects how crowded the market is based on
              the number and similarity of existing startups. A higher score indicates more competition.
            </p>
            <p>
              Feasibility score ({feasibilityScore}/100) is a weighted composite of survival rate,
              competition, demand, funding, trend signals, and unicorn proximity.
            </p>
            <p className="text-sm italic" style={{ color: '#648C9C' }}>
              Data sources: {(result.data_sources_used || []).join(', ') || 'Proprietary startup vector database, Gemini AI analysis'}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

function CompetitorRow({ competitor }: { competitor: CompetitorInfo }) {
  // ChromaDB returns L2 distance (0 = identical, higher = less similar)
  // Convert to a 0-1 similarity score using inverse distance
  const distance = competitor.similarity_distance ?? 1;
  const similarity = 1 / (1 + distance);
  const normalizedSimilarity = Math.max(0, Math.min(1, similarity));

  const statusLower = (competitor.status || 'unknown').toLowerCase();
  const statusColor =
    statusLower.includes('operating') || statusLower.includes('active')
      ? { bg: '#648C9C1A', text: '#648C9C' }
      : statusLower.includes('acquired')
      ? { bg: '#F5A4061A', text: '#F5A406' }
      : statusLower.includes('ipo')
      ? { bg: '#0489A71A', text: '#0489A7' }
      : statusLower.includes('closed') || statusLower.includes('dead') || statusLower.includes('shutdown')
      ? { bg: '#AE0E311A', text: '#AE0E31' }
      : { bg: '#4436461A', text: '#443646' };

  // Format source name for display
  const sourceLabel = (competitor.source || 'unknown').replace(/_/g, ' ');

  return (
    <tr
      className="transition-colors"
      style={{ borderTop: '1px solid #648C9C33' }}
      onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = '#F5F7FA')}
      onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = 'transparent')}
    >
      <td className="px-6 py-4 font-medium" style={{ color: '#023155' }}>
        {competitor.competitor_name}
        {competitor.country && (
          <span className="block text-xs mt-0.5" style={{ color: '#648C9C' }}>
            {competitor.country}
          </span>
        )}
      </td>
      <td className="px-6 py-4" style={{ color: '#443646' }}>
        {competitor.market}
      </td>
      <td className="px-6 py-4">
        <span
          className="px-3 py-1 rounded-full text-sm"
          style={{ backgroundColor: statusColor.bg, color: statusColor.text }}
        >
          {competitor.status}
        </span>
      </td>
      <td className="px-6 py-4">
        <span
          className="px-2 py-0.5 rounded text-xs"
          style={{ backgroundColor: '#0489A71A', color: '#0489A7' }}
        >
          {sourceLabel}
        </span>
      </td>
      <td className="px-6 py-4">
        <div className="flex items-center gap-3">
          <div className="flex-1 rounded-full h-2 max-w-[100px]" style={{ backgroundColor: '#E5E7EB' }}>
            <div
              className="h-2 rounded-full"
              style={{
                width: `${normalizedSimilarity * 100}%`,
                backgroundColor: '#0489A7',
              }}
            />
          </div>
          <span className="text-sm" style={{ color: '#443646' }}>
            {(normalizedSimilarity * 100).toFixed(0)}%
          </span>
        </div>
      </td>
    </tr>
  );
}

function DetailCard({ label, value }: { label: string; value: string }) {
  return (
    <div className="p-4 rounded-xl" style={{ backgroundColor: '#F5F7FA' }}>
      <p className="text-xs font-medium uppercase tracking-wider mb-1" style={{ color: '#648C9C' }}>
        {label}
      </p>
      <p className="font-medium" style={{ color: '#023155' }}>
        {value || '—'}
      </p>
    </div>
  );
}
