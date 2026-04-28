import { LucideIcon } from 'lucide-react';

interface ScoreCardProps {
  title: string;
  score: number;
  maxScore: number;
  icon: LucideIcon;
  color: 'indigo' | 'cyan' | 'green' | 'purple' | 'yellow' | 'red';
}

const colorClasses = {
  indigo: { bg: '#0231551A', text: '#023155' },
  cyan: { bg: '#0489A71A', text: '#0489A7' },
  green: { bg: '#648C9C1A', text: '#648C9C' },
  purple: { bg: '#4436461A', text: '#443646' },
  yellow: { bg: '#F5A4061A', text: '#F5A406' },
  red: { bg: '#AE0E311A', text: '#AE0E31' },
};

const progressColors = {
  indigo: '#023155',
  cyan: '#0489A7',
  green: '#648C9C',
  purple: '#443646',
  yellow: '#F5A406',
  red: '#AE0E31',
};

export function ScoreCard({ title, score, maxScore, icon: Icon, color }: ScoreCardProps) {
  const percentage = (score / maxScore) * 100;
  const colors = colorClasses[color];

  return (
    <div className="bg-white rounded-xl shadow-sm p-6 hover:shadow-md transition-shadow" style={{ border: '1px solid #648C9C33' }}>
      <div className="flex items-center justify-between mb-4">
        <div className="w-12 h-12 rounded-lg flex items-center justify-center" style={{ backgroundColor: colors.bg }}>
          <Icon className="w-6 h-6" style={{ color: colors.text }} />
        </div>
        <div className="text-right">
          <p className="text-2xl font-semibold" style={{ color: '#023155' }}>{score}</p>
          <p className="text-sm" style={{ color: '#648C9C' }}>/ {maxScore}</p>
        </div>
      </div>
      <h3 className="text-sm font-medium mb-3" style={{ color: '#443646' }}>{title}</h3>
      <div className="w-full rounded-full h-2" style={{ backgroundColor: '#E5E7EB' }}>
        <div
          className="h-2 rounded-full transition-all"
          style={{ width: `${percentage}%`, backgroundColor: progressColors[color] }}
        />
      </div>
    </div>
  );
}