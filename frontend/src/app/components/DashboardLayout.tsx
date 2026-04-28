import { Outlet, Link, useLocation } from 'react-router';
import { LayoutDashboard, Sparkles, FileText, Database, Settings, Menu, X, Info } from 'lucide-react';
import { useState } from 'react';
import logoImage from '../../assets/logo.png';

const navItems = [
  { icon: LayoutDashboard, label: 'Dashboard', path: '/' },
  { icon: Sparkles, label: 'Validate Idea', path: '/validate' },
  { icon: FileText, label: 'Reports', path: '/reports' },
  { icon: Database, label: 'Dataset Insights', path: '/dataset' },
  { icon: Info, label: 'About', path: '/about' },
  // { icon: Settings, label: 'Settings', path: '/settings' },
];

export function DashboardLayout() {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const location = useLocation();

  return (
    <div className="min-h-screen" style={{ backgroundColor: '#F5F7FA' }}>
      {/* Sidebar */}
      <aside
        className={`fixed left-0 top-0 h-screen bg-white border-r transition-all duration-300 z-40 ${
          sidebarOpen ? 'w-64' : 'w-20'
        }`}
        style={{ borderColor: '#648C9C33' }}
      >
        {/* Logo */}
        <div className="h-16 flex items-center justify-between px-4" style={{ borderBottom: '1px solid #648C9C33' }}>
          {sidebarOpen ? (
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg flex items-center justify-center overflow-hidden">
                <img src={logoImage} alt="Venture Validator Logo" className="w-full h-full object-cover" />
              </div>
              <span className="font-semibold" style={{ color: '#023155' }}>Venture Validator</span>
            </div>
          ) : (
            <div className="w-8 h-8 rounded-lg flex items-center justify-center mx-auto overflow-hidden">
              <img src={logoImage} alt="Venture Validator Logo" className="w-full h-full object-cover" />
            </div>
          )}
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className={`p-2 hover:bg-gray-100 rounded-lg transition-colors ${!sidebarOpen && 'hidden'}`}
          >
            <Menu className="w-5 h-5" style={{ color: '#443646' }} />
          </button>
        </div>

        {/* Navigation */}
        <nav className="p-4 space-y-2">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path;
            
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all`}
                style={isActive ? {
                  backgroundColor: '#0489A71A',
                  color: '#0489A7'
                } : {
                  color: '#443646'
                }}
                onMouseEnter={(e) => {
                  if (!isActive) {
                    e.currentTarget.style.backgroundColor = '#F5F7FA';
                  }
                }}
                onMouseLeave={(e) => {
                  if (!isActive) {
                    e.currentTarget.style.backgroundColor = 'transparent';
                  }
                }}
              >
                <Icon className="w-5 h-5 flex-shrink-0" />
                {sidebarOpen && <span className="text-sm font-medium">{item.label}</span>}
              </Link>
            );
          })}
        </nav>

        {/* Collapse button when closed */}
        {!sidebarOpen && (
          <button
            onClick={() => setSidebarOpen(true)}
            className="absolute bottom-4 left-1/2 -translate-x-1/2 p-2 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
          >
            <Menu className="w-5 h-5" style={{ color: '#443646' }} />
          </button>
        )}
      </aside>

      {/* Main Content */}
      <main className={`transition-all duration-300 ${sidebarOpen ? 'ml-64' : 'ml-20'}`}>
        <Outlet />
      </main>
    </div>
  );
}