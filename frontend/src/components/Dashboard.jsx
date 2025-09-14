import React, { useState, useEffect } from 'react';
import { Settings, Phone, History } from 'lucide-react';
import AgentConfig from './AgentConfig';
import CallTrigger from './CallTrigger';
import CallHistory from './CallHistory';
import api from '../services/api';

const Dashboard = () => {
  const [activeTab, setActiveTab] = useState('config');
  const [config, setConfig] = useState(null);
  const [calls, setCalls] = useState([]);
  const [loading, setLoading] = useState(false);
  const [notification, setNotification] = useState(null);

  const showNotification = (message, type = 'info') => {
    setNotification({ message, type });
    setTimeout(() => setNotification(null), 5000);
  };

  const loadConfig = async () => {
    try {
      const response = await api.getConfigs();
      if (response.configs.length > 0) {
        setConfig(response.configs[0]);
      }
    } catch (error) {
      console.error('Failed to load config:', error);
      showNotification('Failed to load configuration', 'error');
    }
  };

  const loadCalls = async () => {
    try {
      const response = await api.getCalls();
      setCalls(response.calls);
    } catch (error) {
      console.error('Failed to load calls:', error);
      showNotification('Failed to load call history', 'error');
    }
  };

  const handleConfigUpdate = (updatedConfig) => {
    setConfig(updatedConfig);
  };

  const handleConfigSave = async () => {
    if (!config) return;
    
    setLoading(true);
    try {
      if (config.id) {
        await api.updateConfig(config.id, config);
        showNotification('Configuration updated successfully', 'success');
      } else {
        const response = await api.createConfig(config);
        setConfig(response.config);
        showNotification('Configuration created successfully', 'success');
      }
    } catch (error) {
      console.error('Failed to save config:', error);
      showNotification('Failed to save configuration', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleTriggerCall = async (callData) => {
    setLoading(true);
    try {
      const response = await api.triggerCall(callData);
      showNotification(`Call initiated successfully! Call ID: ${response.call_id}`, 'success');
      setActiveTab('history');
      await loadCalls();
    } catch (error) {
      console.error('Failed to trigger call:', error);
      showNotification('Failed to start call. Please check your configuration.', 'error');
    } finally {
      setLoading(false);
    }
  };

  // Load initial data
  useEffect(() => {
    loadConfig();
    loadCalls();
  }, []);

  const tabs = [
    { id: 'config', label: 'Configure Agent', icon: Settings },
    { id: 'trigger', label: 'Test Call', icon: Phone },
    { id: 'history', label: 'Call History', icon: History },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <h1 className="text-2xl font-bold text-gray-900">AI Voice Agent Tool</h1>
            <div className="text-sm text-gray-500">
              Logistics Dispatch System
            </div>
          </div>
        </div>
      </header>

      {/* Notification */}
      {notification && (
        <div className={`fixed top-4 right-4 p-4 rounded-md shadow-lg z-50 ${
          notification.type === 'error' ? 'bg-red-100 text-red-800 border-red-200' :
          notification.type === 'success' ? 'bg-green-100 text-green-800 border-green-200' :
          'bg-blue-100 text-blue-800 border-blue-200'
        }`}>
          {notification.message}
        </div>
      )}

      {/* Navigation */}
      <nav className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex space-x-8">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center gap-2 px-3 py-4 text-sm font-medium border-b-2 transition-colors ${
                    activeTab === tab.id
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  {tab.label}
                </button>
              );
            })}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'config' && (
          <AgentConfig
            config={config}
            onUpdate={handleConfigUpdate}
            onSave={handleConfigSave}
          />
        )}
        
        {activeTab === 'trigger' && (
          <CallTrigger
            onTriggerCall={handleTriggerCall}
            isLoading={loading}
          />
        )}
        
        {activeTab === 'history' && (
          <CallHistory
            calls={calls}
            onRefresh={loadCalls}
          />
        )}
      </main>
    </div>
  );
};

export default Dashboard;