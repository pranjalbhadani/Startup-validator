import {
  FileText, AlertTriangle, TrendingUp, Shield, Lightbulb,
  CheckCircle, ArrowLeft, Activity, Zap, BarChart3
} from 'lucide-react';
import { useValidation } from '../ValidationContext';
import { Link } from 'react-router';
import {
  RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis,
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
  PieChart, Pie, Cell, ResponsiveContainer
} from 'recharts';

// ─── Color Palette ───────────────────────────────────────────────────────────
const COLORS = {
  navy: '#023155', teal: '#0489A7', muted: '#648C9C',
  plum: '#443646', amber: '#F5A406', red: '#AE0E31',
  bg: '#F5F7FA', white: '#ffffff',
};

const SEVERITY_COLORS: Record<string, { bg: string; text: string }> = {
  High: { bg: '#AE0E311A', text: '#AE0E31' },
  Medium: { bg: '#F5A4061A', text: '#F5A406' },
  Low: { bg: '#648C9C1A', text: '#648C9C' },
};
const STRENGTH_COLORS: Record<string, { bg: string; text: string }> = {
  Strong: { bg: '#0489A71A', text: '#0489A7' },
  Moderate: { bg: '#F5A4061A', text: '#F5A406' },
  Weak: { bg: '#648C9C1A', text: '#648C9C' },
};
const PIE_COLORS = ['#AE0E31', '#F5A406', '#648C9C'];

// ─── Helper: Score Gauge SVG ─────────────────────────────────────────────────
function ScoreGauge({ score, max = 100 }: { score: number; max?: number }) {
  const pct = Math.min(score / max, 1);
  const r = 56, circ = 2 * Math.PI * r;
  const color = pct >= 0.7 ? '#0489A7' : pct >= 0.4 ? '#F5A406' : '#AE0E31';
  return (
    <div className="relative w-36 h-36 mx-auto">
      <svg className="w-36 h-36 transform -rotate-90">
        <circle cx="72" cy="72" r={r} stroke="#E5E7EB" strokeWidth="12" fill="none" />
        <circle cx="72" cy="72" r={r} stroke={color} strokeWidth="12" fill="none"
          strokeDasharray={`${pct * circ} ${circ}`} strokeLinecap="round"
          style={{ transition: 'stroke-dasharray 0.8s ease' }} />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className="text-3xl font-bold" style={{ color: COLORS.navy }}>{score}</span>
        <span className="text-xs" style={{ color: COLORS.muted }}>/ {max}</span>
      </div>
    </div>
  );
}

// ─── Helper: Section Wrapper ─────────────────────────────────────────────────
function Section({ title, icon: Icon, children }: { title: string; icon: React.ElementType; children: React.ReactNode }) {
  return (
    <div className="bg-white rounded-2xl shadow-sm p-6" style={{ border: '1px solid #648C9C33' }}>
      <div className="flex items-center gap-3 mb-5">
        <div className="w-10 h-10 rounded-lg flex items-center justify-center" style={{ backgroundColor: '#0489A71A' }}>
          <Icon className="w-5 h-5" style={{ color: COLORS.teal }} />
        </div>
        <h2 className="text-lg font-semibold" style={{ color: COLORS.navy }}>{title}</h2>
      </div>
      {children}
    </div>
  );
}

// ─── Main Component ──────────────────────────────────────────────────────────
export function ReportsPage() {
  const { result } = useValidation();

  if (!result) {
    return (
      <div className="min-h-screen p-8 flex items-center justify-center" style={{ backgroundColor: COLORS.bg }}>
        <div className="text-center max-w-md">
          <div className="w-20 h-20 rounded-2xl flex items-center justify-center mx-auto mb-6"
            style={{ backgroundColor: '#0489A71A' }}>
            <FileText className="w-10 h-10" style={{ color: COLORS.teal }} />
          </div>
          <h2 className="text-2xl mb-3" style={{ color: COLORS.navy }}>No Validation Report Yet</h2>
          <p className="mb-6" style={{ color: COLORS.plum }}>
            Run a startup validation first to generate your visual report.
          </p>
          <Link to="/validate"
            className="inline-flex items-center gap-2 text-white px-6 py-3 rounded-xl transition-all"
            style={{ background: 'linear-gradient(135deg, #0489A7 0%, #023155 100%)' }}>
            <ArrowLeft className="w-5 h-5" /> Go to Validation
          </Link>
        </div>
      </div>
    );
  }

  const report = result.scoring_report as Record<string, any> | undefined;
  const metrics = report?.metrics ?? {};
  const insights = report?.insights ?? {};
  const recommendations: string[] = report?.recommendations ?? [];
  const riskFactors: { factor: string; severity: string; detail: string }[] = report?.risk_factors ?? [];
  const opportunities: { signal: string; strength: string; detail: string }[] = report?.opportunity_signals ?? [];
  const similarStartups: { name: string; status: string; funding_total_usd: number; source: string }[] = report?.similar_startups ?? [];

  const score = report?.score ?? result.feasibility_score ?? 0;
  const risk = report?.risk ?? result.risk_level ?? 'Unknown';
  const confidence = report?.confidence ?? 'moderate';

  // Chart data
  const radarData = [
    { metric: 'Competition', value: Math.round((1 - (metrics.competition_normalized ?? 0)) * 100) },
    { metric: 'Demand', value: Math.round((metrics.demand_score ?? 0) * 100) },
    { metric: 'Funding', value: Math.round((metrics.funding_score ?? 0) * 100) },
    { metric: 'Survival', value: Math.round((metrics.survival_rate ?? 0) * 100) },
  ];
  const barData = radarData.map(d => ({ name: d.metric, score: d.value }));

  const riskCounts = { High: 0, Medium: 0, Low: 0 };
  riskFactors.forEach(r => { if (r.severity in riskCounts) riskCounts[r.severity as keyof typeof riskCounts]++; });
  const pieData = Object.entries(riskCounts).filter(([, v]) => v > 0).map(([name, value]) => ({ name, value }));

  const riskColor = risk === 'High' ? COLORS.red : risk === 'Medium' ? COLORS.amber : COLORS.teal;
  const confLabel = confidence === 'high' ? 'High' : confidence === 'moderate' ? 'Moderate' : 'Low';

  return (
    <div className="min-h-screen p-8" style={{ backgroundColor: COLORS.bg }}>
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl mb-1" style={{ color: COLORS.navy }}>Validation Report</h1>
          <p style={{ color: COLORS.plum }}>{result.startup_name} — {result.industry_detected}</p>
        </div>
        <Link to="/validate"
          className="flex items-center gap-2 px-4 py-2 text-white rounded-xl"
          style={{ background: 'linear-gradient(135deg, #0489A7 0%, #023155 100%)' }}>
          <ArrowLeft className="w-4 h-4" /> New Validation
        </Link>
      </div>

      {/* Row 1: Summary + Score Gauge + Confidence */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
        <Section title="Summary" icon={BarChart3}>
          <div className="space-y-3 text-sm" style={{ color: COLORS.plum }}>
            <p><span className="font-medium" style={{ color: COLORS.navy }}>Industry:</span> {result.industry_detected}</p>
            <p><span className="font-medium" style={{ color: COLORS.navy }}>Market:</span> {result.target_market}</p>
            <p><span className="font-medium" style={{ color: COLORS.navy }}>Revenue Model:</span> {result.revenue_model}</p>
            <p><span className="font-medium" style={{ color: COLORS.navy }}>Core Proposition:</span> {result.core_proposition}</p>
          </div>
        </Section>

        <Section title="Final Score" icon={Activity}>
          <ScoreGauge score={typeof score === 'number' ? Math.round(score) : 0} />
          <div className="text-center mt-4">
            <span className="inline-flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium"
              style={{ backgroundColor: `${riskColor}1A`, color: riskColor }}>
              <AlertTriangle className="w-4 h-4" /> {risk} Risk
            </span>
          </div>
        </Section>

        <Section title="Confidence" icon={Shield}>
          <div className="flex flex-col items-center gap-4 pt-2">
            <div className="w-20 h-20 rounded-full flex items-center justify-center text-lg font-bold"
              style={{ backgroundColor: '#0489A71A', color: COLORS.teal }}>
              {confLabel}
            </div>
            <p className="text-sm text-center" style={{ color: COLORS.muted }}>
              Based on {metrics.total_startups ?? 0} comparable startups from {metrics.source_count ?? 0} data source(s).
            </p>
            {insights.trend_assessment && (
              <p className="text-xs text-center px-2" style={{ color: COLORS.plum }}>
                Trend: {insights.trend_assessment}
              </p>
            )}
          </div>
        </Section>
      </div>

      {/* Row 2: Radar Chart + Bar Chart */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <Section title="Metrics Overview (Radar)" icon={Activity}>
          <div className="w-full h-72">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart data={radarData} outerRadius="75%">
                <PolarGrid stroke="#648C9C33" />
                <PolarAngleAxis dataKey="metric" tick={{ fill: COLORS.plum, fontSize: 12 }} />
                <PolarRadiusAxis angle={30} domain={[0, 100]} tick={{ fill: COLORS.muted, fontSize: 10 }} />
                <Radar dataKey="value" stroke={COLORS.teal} fill={COLORS.teal} fillOpacity={0.25} />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </Section>

        <Section title="Metric Comparison (Bar)" icon={BarChart3}>
          <div className="w-full h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={barData} barSize={36}>
                <CartesianGrid strokeDasharray="3 3" stroke="#648C9C22" />
                <XAxis dataKey="name" tick={{ fill: COLORS.plum, fontSize: 12 }} />
                <YAxis domain={[0, 100]} tick={{ fill: COLORS.muted, fontSize: 10 }} />
                <Tooltip contentStyle={{ borderRadius: 12, border: '1px solid #648C9C33' }} />
                <Bar dataKey="score" fill={COLORS.teal} radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Section>
      </div>

      {/* Row 3: Risk Donut + Insights */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        {pieData.length > 0 && (
          <Section title="Risk Distribution" icon={AlertTriangle}>
            <div className="w-full h-64 flex items-center justify-center">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie data={pieData} dataKey="value" nameKey="name" cx="50%" cy="50%"
                    innerRadius={50} outerRadius={80} paddingAngle={4} label={({ name, value }) => `${name}: ${value}`}>
                    {pieData.map((_, i) => (
                      <Cell key={i} fill={PIE_COLORS[i % PIE_COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </Section>
        )}

        <Section title="Insights" icon={Lightbulb}>
          <div className="grid grid-cols-2 gap-3">
            <InsightBadge label="Competition" value={insights.competition_level ?? '—'} />
            <InsightBadge label="Market Health" value={insights.market_health ?? '—'} />
            <InsightBadge label="Unicorn Potential" value={insights.unicorn_potential ?? '—'} />
            <InsightBadge label="Trend" value={insights.trend_assessment ?? '—'} />
          </div>
        </Section>
      </div>

      {/* Row 4: Risks + Opportunities */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        {riskFactors.length > 0 && (
          <Section title="Risk Analysis" icon={AlertTriangle}>
            <div className="space-y-3">
              {riskFactors.map((rf, i) => {
                const c = SEVERITY_COLORS[rf.severity] ?? SEVERITY_COLORS.Low;
                return (
                  <div key={i} className="p-3 rounded-xl" style={{ backgroundColor: COLORS.bg }}>
                    <div className="flex items-center gap-2 mb-1">
                      <span className="px-2 py-0.5 rounded text-xs font-medium" style={{ backgroundColor: c.bg, color: c.text }}>{rf.severity}</span>
                      <span className="font-medium text-sm" style={{ color: COLORS.navy }}>{rf.factor}</span>
                    </div>
                    <p className="text-xs" style={{ color: COLORS.muted }}>{rf.detail}</p>
                  </div>
                );
              })}
            </div>
          </Section>
        )}

        {opportunities.length > 0 && (
          <Section title="Opportunity Signals" icon={Zap}>
            <div className="space-y-3">
              {opportunities.map((op, i) => {
                const c = STRENGTH_COLORS[op.strength] ?? STRENGTH_COLORS.Weak;
                return (
                  <div key={i} className="p-3 rounded-xl" style={{ backgroundColor: COLORS.bg }}>
                    <div className="flex items-center gap-2 mb-1">
                      <span className="px-2 py-0.5 rounded text-xs font-medium" style={{ backgroundColor: c.bg, color: c.text }}>{op.strength}</span>
                      <span className="font-medium text-sm" style={{ color: COLORS.navy }}>{op.signal}</span>
                    </div>
                    <p className="text-xs" style={{ color: COLORS.muted }}>{op.detail}</p>
                  </div>
                );
              })}
            </div>
          </Section>
        )}
      </div>

      {/* Row 5: Recommendations */}
      {recommendations.length > 0 && (
        <div className="mb-6">
          <Section title="Recommendations" icon={CheckCircle}>
            <ol className="space-y-3">
              {recommendations.map((rec, i) => (
                <li key={i} className="flex gap-3 p-3 rounded-xl" style={{ backgroundColor: COLORS.bg }}>
                  <span className="flex-shrink-0 w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold text-white"
                    style={{ backgroundColor: COLORS.teal }}>{i + 1}</span>
                  <p className="text-sm leading-relaxed" style={{ color: COLORS.plum }}>{rec}</p>
                </li>
              ))}
            </ol>
          </Section>
        </div>
      )}

      {/* Row 6: Similar Startups (optional) */}
      {similarStartups.length > 0 && (
        <Section title="Similar Startups in Dataset" icon={TrendingUp}>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr style={{ borderBottom: '1px solid #648C9C33' }}>
                  {['Name', 'Status', 'Funding (USD)', 'Source'].map(h => (
                    <th key={h} className="px-4 py-2 text-left font-medium" style={{ color: COLORS.plum }}>{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {similarStartups.map((s, i) => (
                  <tr key={i} style={{ borderTop: '1px solid #648C9C22' }}>
                    <td className="px-4 py-2 font-medium" style={{ color: COLORS.navy }}>{s.name}</td>
                    <td className="px-4 py-2" style={{ color: COLORS.muted }}>{s.status}</td>
                    <td className="px-4 py-2" style={{ color: COLORS.plum }}>${s.funding_total_usd.toLocaleString()}</td>
                    <td className="px-4 py-2">
                      <span className="px-2 py-0.5 rounded text-xs" style={{ backgroundColor: '#0489A71A', color: COLORS.teal }}>
                        {s.source.replace(/_/g, ' ')}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Section>
      )}
    </div>
  );
}

// ─── Sub-Components ──────────────────────────────────────────────────────────
function InsightBadge({ label, value }: { label: string; value: string }) {
  return (
    <div className="p-3 rounded-xl" style={{ backgroundColor: COLORS.bg }}>
      <p className="text-xs font-medium uppercase tracking-wider mb-1" style={{ color: COLORS.muted }}>{label}</p>
      <p className="text-sm font-semibold" style={{ color: COLORS.navy }}>{value}</p>
    </div>
  );
}