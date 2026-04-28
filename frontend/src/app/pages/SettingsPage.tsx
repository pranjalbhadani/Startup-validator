import { User, Bell, CreditCard, Shield } from 'lucide-react';

export function SettingsPage() {
  return (
    <div className="min-h-screen p-8" style={{ backgroundColor: '#F5F7FA' }}>
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl mb-2" style={{ color: '#023155' }}>Settings</h1>
        <p style={{ color: '#443646' }}>Manage your account preferences and settings.</p>
      </div>

      {/* Settings Sections */}
      <div className="max-w-3xl space-y-6">
        {/* Profile Settings */}
        <div className="bg-white rounded-2xl shadow-sm p-6" style={{ border: '1px solid #648C9C33' }}>
          <div className="flex items-center gap-3 mb-6">
            <div className="w-10 h-10 rounded-lg flex items-center justify-center" style={{ backgroundColor: '#0489A71A' }}>
              <User className="w-5 h-5" style={{ color: '#0489A7' }} />
            </div>
            <h2 className="text-xl" style={{ color: '#023155' }}>Profile Settings</h2>
          </div>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2" style={{ color: '#023155' }}>Full Name</label>
              <input
                type="text"
                defaultValue="John Doe"
                className="w-full px-4 py-3 rounded-xl outline-none"
                style={{ border: '1px solid #648C9C', color: '#023155' }}
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
            <div>
              <label className="block text-sm font-medium mb-2" style={{ color: '#023155' }}>Email</label>
              <input
                type="email"
                defaultValue="john@example.com"
                className="w-full px-4 py-3 rounded-xl outline-none"
                style={{ border: '1px solid #648C9C', color: '#023155' }}
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
          </div>
        </div>

        {/* Notifications */}
        <div className="bg-white rounded-2xl shadow-sm p-6" style={{ border: '1px solid #648C9C33' }}>
          <div className="flex items-center gap-3 mb-6">
            <div className="w-10 h-10 rounded-lg flex items-center justify-center" style={{ backgroundColor: '#0489A71A' }}>
              <Bell className="w-5 h-5" style={{ color: '#0489A7' }} />
            </div>
            <h2 className="text-xl" style={{ color: '#023155' }}>Notifications</h2>
          </div>
          
          <div className="space-y-4">
            <SettingToggle
              label="Email notifications"
              description="Receive email updates about your validations"
              defaultChecked={true}
            />
            <SettingToggle
              label="Marketing emails"
              description="Receive news and product updates"
              defaultChecked={false}
            />
          </div>
        </div>

        {/* Billing */}
        <div className="bg-white rounded-2xl shadow-sm p-6" style={{ border: '1px solid #648C9C33' }}>
          <div className="flex items-center gap-3 mb-6">
            <div className="w-10 h-10 rounded-lg flex items-center justify-center" style={{ backgroundColor: '#648C9C1A' }}>
              <CreditCard className="w-5 h-5" style={{ color: '#648C9C' }} />
            </div>
            <h2 className="text-xl" style={{ color: '#023155' }}>Billing & Subscription</h2>
          </div>
          
          <div className="space-y-4">
            <div className="flex items-center justify-between p-4 rounded-xl" style={{ backgroundColor: '#F5F7FA' }}>
              <div>
                <p className="font-medium" style={{ color: '#023155' }}>Free Plan</p>
                <p className="text-sm" style={{ color: '#443646' }}>5 validations per month</p>
              </div>
              <button 
                className="px-4 py-2 text-white rounded-lg transition-colors"
                style={{ backgroundColor: '#0489A7' }}
                onMouseEnter={(e) => e.currentTarget.style.backgroundColor = '#023155'}
                onMouseLeave={(e) => e.currentTarget.style.backgroundColor = '#0489A7'}
              >
                Upgrade
              </button>
            </div>
          </div>
        </div>

        {/* Security */}
        <div className="bg-white rounded-2xl shadow-sm p-6" style={{ border: '1px solid #648C9C33' }}>
          <div className="flex items-center gap-3 mb-6">
            <div className="w-10 h-10 rounded-lg flex items-center justify-center" style={{ backgroundColor: '#4436461A' }}>
              <Shield className="w-5 h-5" style={{ color: '#443646' }} />
            </div>
            <h2 className="text-xl" style={{ color: '#023155' }}>Security</h2>
          </div>
          
          <button 
            className="w-full px-4 py-3 rounded-xl transition-all text-left"
            style={{ border: '1px solid #648C9C', color: '#023155' }}
            onMouseEnter={(e) => e.currentTarget.style.borderColor = '#0489A7'}
            onMouseLeave={(e) => e.currentTarget.style.borderColor = '#648C9C'}
          >
            Change Password
          </button>
        </div>
      </div>
    </div>
  );
}

function SettingToggle({ 
  label, 
  description, 
  defaultChecked 
}: { 
  label: string; 
  description: string; 
  defaultChecked: boolean;
}) {
  return (
    <div className="flex items-center justify-between">
      <div>
        <p className="font-medium" style={{ color: '#023155' }}>{label}</p>
        <p className="text-sm" style={{ color: '#443646' }}>{description}</p>
      </div>
      <label className="relative inline-flex items-center cursor-pointer">
        <input type="checkbox" defaultChecked={defaultChecked} className="sr-only peer" />
        <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all"
          style={{
            '--tw-ring-color': '#0489A71A',
          } as React.CSSProperties}
        ></div>
        <style>{`
          .peer:checked ~ div {
            background-color: #0489A7;
          }
          .peer:focus ~ div {
            box-shadow: 0 0 0 4px #0489A71A;
          }
        `}</style>
      </label>
    </div>
  );
}