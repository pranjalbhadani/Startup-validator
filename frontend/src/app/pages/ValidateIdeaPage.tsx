import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router';
import { Sparkles, Loader2, AlertCircle, Wifi, WifiOff } from 'lucide-react';
import { validateStartup, checkApiHealth } from '../api';
import { useValidation } from '../ValidationContext';

export function ValidateIdeaPage() {
  const navigate = useNavigate();
  const { setResult, setIsLoading, setError, isLoading } = useValidation();
  const [backendOnline, setBackendOnline] = useState<boolean | null>(null);
  const [formError, setFormError] = useState<string | null>(null);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    targetMarket: '',
    revenueModel: 'subscription',
  });

  // Check backend health on mount
  useEffect(() => {
    checkApiHealth().then(setBackendOnline);
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setFormError(null);
    setError(null);
    setIsLoading(true);

    try {
      const result = await validateStartup({
        startup_name: formData.name,
        idea_description: formData.description,
        target_market: formData.targetMarket,
        revenue_model: formData.revenueModel,
      });

      setResult(result);
      setIsLoading(false);
      navigate('/results');
    } catch (err: any) {
      setIsLoading(false);
      const message =
        err?.message || 'Something went wrong. Please try again.';
      setFormError(message);
      setError(message);
    }
  };

  return (
    <div className="min-h-screen p-8" style={{ backgroundColor: '#F5F7FA' }}>
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl mb-2" style={{ color: '#023155' }}>Validate Your Startup Idea</h1>
        <p style={{ color: '#443646' }}>
          Enter your startup details below and let our AI analyze its potential.
        </p>
      </div>

      {/* Backend Status Indicator */}
      {backendOnline !== null && (
        <div
          className="mb-6 flex items-center gap-2 px-4 py-3 rounded-xl text-sm"
          style={{
            backgroundColor: backendOnline ? '#648C9C1A' : '#AE0E311A',
            color: backendOnline ? '#648C9C' : '#AE0E31',
            border: `1px solid ${backendOnline ? '#648C9C33' : '#AE0E3133'}`,
          }}
        >
          {backendOnline ? (
            <>
              <Wifi className="w-4 h-4" />
              Backend API is online and ready
            </>
          ) : (
            <>
              <WifiOff className="w-4 h-4" />
              Backend API is offline — make sure the FastAPI server is running on port 8000
            </>
          )}
        </div>
      )}

      {/* Error Banner */}
      {formError && (
        <div
          className="mb-6 flex items-start gap-3 px-4 py-3 rounded-xl text-sm"
          style={{
            backgroundColor: '#AE0E311A',
            color: '#AE0E31',
            border: '1px solid #AE0E3133',
          }}
        >
          <AlertCircle className="w-5 h-5 flex-shrink-0 mt-0.5" />
          <div>
            <p className="font-medium">Validation Error</p>
            <p className="mt-1 opacity-90">{formError}</p>
          </div>
        </div>
      )}

      {/* Form Card */}
      <div className="max-w-3xl">
        <div className="bg-white rounded-2xl shadow-sm p-8" style={{ border: '1px solid #648C9C33' }}>
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Startup Name */}
            <div>
              <label className="block text-sm font-medium mb-2" style={{ color: '#023155' }}>
                Startup Name
              </label>
              <input
                type="text"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                className="w-full px-4 py-3 rounded-xl outline-none transition-all"
                style={{ border: '1px solid #648C9C', color: '#023155' }}
                placeholder="e.g., TechFlow Analytics"
                required
                disabled={isLoading}
                onFocus={(e) => {
                  e.currentTarget.style.borderColor = '#0489A7';
                  e.currentTarget.style.boxShadow = '0 0 0 3px #0489A71A';
                }}
                onBlur={(e) => {
                  e.currentTarget.style.borderColor = '#648C9C';
                  e.currentTarget.style.boxShadow = 'none';
                }}
              />
            </div>

            {/* Idea Description */}
            <div>
              <label className="block text-sm font-medium mb-2" style={{ color: '#023155' }}>
                Idea Description
              </label>
              <textarea
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                rows={6}
                className="w-full px-4 py-3 rounded-xl outline-none transition-all resize-none"
                style={{ border: '1px solid #648C9C', color: '#023155' }}
                placeholder="Describe your startup idea in detail. What problem does it solve? How does it work?"
                required
                disabled={isLoading}
                onFocus={(e) => {
                  e.currentTarget.style.borderColor = '#0489A7';
                  e.currentTarget.style.boxShadow = '0 0 0 3px #0489A71A';
                }}
                onBlur={(e) => {
                  e.currentTarget.style.borderColor = '#648C9C';
                  e.currentTarget.style.boxShadow = 'none';
                }}
              />
              <p className="text-sm mt-2" style={{ color: '#648C9C' }}>
                Be specific about the problem you're solving and your solution approach.
              </p>
            </div>

            {/* Target Market */}
            <div>
              <label className="block text-sm font-medium mb-2" style={{ color: '#023155' }}>
                Target Market
              </label>
              <input
                type="text"
                value={formData.targetMarket}
                onChange={(e) => setFormData({ ...formData, targetMarket: e.target.value })}
                className="w-full px-4 py-3 rounded-xl outline-none transition-all"
                style={{ border: '1px solid #648C9C', color: '#023155' }}
                placeholder="e.g., Small businesses in the e-commerce sector"
                required
                disabled={isLoading}
                onFocus={(e) => {
                  e.currentTarget.style.borderColor = '#0489A7';
                  e.currentTarget.style.boxShadow = '0 0 0 3px #0489A71A';
                }}
                onBlur={(e) => {
                  e.currentTarget.style.borderColor = '#648C9C';
                  e.currentTarget.style.boxShadow = 'none';
                }}
              />
            </div>

            {/* Revenue Model */}
            <div>
              <label className="block text-sm font-medium mb-2" style={{ color: '#023155' }}>
                Revenue Model
              </label>
              <select
                value={formData.revenueModel}
                onChange={(e) => setFormData({ ...formData, revenueModel: e.target.value })}
                className="w-full px-4 py-3 rounded-xl outline-none transition-all"
                style={{ border: '1px solid #648C9C', color: '#023155' }}
                disabled={isLoading}
                onFocus={(e) => {
                  e.currentTarget.style.borderColor = '#0489A7';
                  e.currentTarget.style.boxShadow = '0 0 0 3px #0489A71A';
                }}
                onBlur={(e) => {
                  e.currentTarget.style.borderColor = '#648C9C';
                  e.currentTarget.style.boxShadow = 'none';
                }}
              >
                <option value="subscription">Subscription</option>
                <option value="freemium">Freemium</option>
                <option value="marketplace">Marketplace Commission</option>
                <option value="ads">Advertising</option>
                <option value="transaction">Transaction Fees</option>
                <option value="license">Licensing</option>
              </select>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={isLoading || backendOnline === false}
              className="w-full text-white px-6 py-4 rounded-xl transition-all flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
              style={{ background: isLoading ? '#648C9C' : 'linear-gradient(135deg, #0489A7 0%, #023155 100%)' }}
              onMouseEnter={(e) => {
                if (!isLoading) {
                  e.currentTarget.style.background = 'linear-gradient(135deg, #023155 0%, #0489A7 100%)';
                }
              }}
              onMouseLeave={(e) => {
                if (!isLoading) {
                  e.currentTarget.style.background = 'linear-gradient(135deg, #0489A7 0%, #023155 100%)';
                }
              }}
            >
              {isLoading ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  AI Agents analyzing your idea...
                </>
              ) : (
                <>
                  <Sparkles className="w-5 h-5" />
                  Run AI Validation
                </>
              )}
            </button>
          </form>
        </div>

        {/* Info Card */}
        <div className="mt-6 rounded-xl p-6" style={{ backgroundColor: '#0489A71A', border: '1px solid #0489A733' }}>
          <h3 className="text-sm font-semibold mb-2" style={{ color: '#023155' }}>What happens next?</h3>
          <ul className="space-y-2 text-sm" style={{ color: '#443646' }}>
            <li className="flex items-start gap-2">
              <span style={{ color: '#0489A7' }}>•</span>
              <span>AI analyzes market demand and competition using real startup data</span>
            </li>
            <li className="flex items-start gap-2">
              <span style={{ color: '#0489A7' }}>•</span>
              <span>Generate comprehensive SWOT analysis and feasibility scores</span>
            </li>
            <li className="flex items-start gap-2">
              <span style={{ color: '#0489A7' }}>•</span>
              <span>Identify similar startups and their outcomes</span>
            </li>
            <li className="flex items-start gap-2">
              <span style={{ color: '#0489A7' }}>•</span>
              <span>Receive actionable recommendations to improve your idea</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
}