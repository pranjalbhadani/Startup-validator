import { Sparkles, Brain, Database, Cpu, ArrowRight } from 'lucide-react';
import { Link } from 'react-router';

export function AboutPage() {
  return (
    <div className="min-h-screen p-8" style={{ backgroundColor: '#F5F7FA' }}>
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl mb-2" style={{ color: '#023155' }}>About Venture Validator</h1>
        <p style={{ color: '#443646' }}>
          Discover the AI-powered pipeline driving your startup insights.
        </p>
      </div>

      {/* Hero Intro */}
      <div className="bg-white rounded-2xl shadow-sm p-8 mb-8" style={{ border: '1px solid #648C9C33' }}>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
          <div>
            <h2 className="text-2xl mb-4" style={{ color: '#023155' }}>
              Built with Multi-Agent AI Architecture
            </h2>
            <p className="mb-4" style={{ color: '#443646', lineHeight: '1.6' }}>
              Venture Validator isn't just a simple keyword search. It's built on a complex multi-agent AI pipeline utilizing Google's Gemini models and local vector databases to deeply understand and analyze your business idea.
            </p>
            <p className="mb-6" style={{ color: '#443646', lineHeight: '1.6' }}>
              By analyzing thousands of both successful and failed startups, our system helps founders identify market gaps, evaluate competition, and refine their core value propositions before investing significant time and money.
            </p>
            <div className="flex gap-4">
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
                Try It Now
                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </Link>
            </div>
          </div>
          <div className="rounded-xl p-8 flex items-center justify-center h-full min-h-[300px]" style={{ background: 'linear-gradient(135deg, #0489A71A 0%, #648C9C1A 100%)' }}>
            <div className="relative">
              <div className="w-32 h-32 bg-white rounded-2xl shadow-lg flex items-center justify-center absolute -top-16 -left-16 z-10 animate-pulse">
                <Brain className="w-16 h-16" style={{ color: '#0489A7' }} />
              </div>
              <div className="w-48 h-48 bg-white rounded-full shadow-lg flex items-center justify-center">
                <Cpu className="w-20 h-20" style={{ color: '#023155' }} />
              </div>
              <div className="w-24 h-24 bg-white rounded-2xl shadow-lg flex items-center justify-center absolute -bottom-8 -right-8 z-10">
                <Database className="w-12 h-12" style={{ color: '#648C9C' }} />
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* How It Works */}
      <div className="mb-8">
        <h2 className="text-xl mb-6" style={{ color: '#023155' }}>The Pipeline Explained</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <AgentCard
            icon={Brain}
            title="Stage 1: Idea Understanding"
            description="A Gemini-powered agent takes your raw unstructured idea and extracts structured insights like target market, ideal revenue model, and industry categorization."
            color="#0489A7"
          />
          <AgentCard
            icon={Database}
            title="Stage 2: Vector Search"
            description="Using ChromaDB, your idea is converted into embeddings. The engine searches through a massive localized dataset of startups to find semantic matches."
            color="#648C9C"
          />
          <AgentCard
            icon={Sparkles}
            title="Stage 3: Scoring & Analysis"
            description="The Competitor Similarity Agent evaluates the distances of matched startups, assesses market saturation, and computes dynamic risk scores."
            color="#023155"
          />
        </div>
      </div>

      {/* Tech Stack */}
      <div className="mb-8 bg-white rounded-2xl shadow-sm p-6" style={{ border: '1px solid #648C9C33' }}>
        <h2 className="text-xl mb-4" style={{ color: '#023155' }}>Technical Stack</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <TechBadge name="React 18" category="Frontend" />
          <TechBadge name="Vite" category="Frontend Build" />
          <TechBadge name="Tailwind CSS" category="Styling" />
          <TechBadge name="FastAPI" category="Backend" />
          <TechBadge name="Python" category="Backend" />
          <TechBadge name="ChromaDB" category="Vector DB" />
          <TechBadge name="Google Gemini" category="LLM" />
          <TechBadge name="Pandas" category="Data Processing" />
        </div>
      </div>
    </div>
  );
}

function AgentCard({ icon: Icon, title, description, color }: { icon: any, title: string, description: string, color: string }) {
  return (
    <div className="bg-white rounded-xl p-6 hover:shadow-md transition-shadow" style={{ border: '1px solid #648C9C33' }}>
      <div className="w-12 h-12 rounded-lg flex items-center justify-center mb-4" style={{ backgroundColor: `${color}1A` }}>
        <Icon className="w-6 h-6" style={{ color }} />
      </div>
      <h3 className="font-semibold mb-2" style={{ color: '#023155' }}>{title}</h3>
      <p className="text-sm" style={{ color: '#443646', lineHeight: '1.5' }}>{description}</p>
    </div>
  );
}

function TechBadge({ name, category }: { name: string, category: string }) {
  return (
    <div className="p-4 rounded-xl text-center" style={{ backgroundColor: '#F5F7FA' }}>
      <p className="font-medium" style={{ color: '#023155' }}>{name}</p>
      <p className="text-xs mt-1 uppercase tracking-wider font-semibold" style={{ color: '#648C9C' }}>{category}</p>
    </div>
  );
}
