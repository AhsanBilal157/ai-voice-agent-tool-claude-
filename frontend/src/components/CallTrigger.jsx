import React, { useState } from 'react';
import { Phone, Play } from 'lucide-react';

const CallTrigger = ({ onTriggerCall, isLoading }) => {
  const [formData, setFormData] = useState({
    driver_name: '',
    phone_number: '',
    load_number: ''
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    onTriggerCall(formData);
  };

  const handleChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-sm border">
      <div className="flex items-center gap-2 mb-4">
        <Phone className="w-5 h-5 text-green-600" />
        <h2 className="text-xl font-semibold">Trigger Test Call</h2>
      </div>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Driver Name
            </label>
            <input
              type="text"
              value={formData.driver_name}
              onChange={(e) => handleChange('driver_name', e.target.value)}
              required
              placeholder="e.g., Mike Johnson"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Phone Number
            </label>
            <input
              type="tel"
              value={formData.phone_number}
              onChange={(e) => handleChange('phone_number', e.target.value)}
              required
              placeholder="e.g., +1234567890"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Load Number
            </label>
            <input
              type="text"
              value={formData.load_number}
              onChange={(e) => handleChange('load_number', e.target.value)}
              required
              placeholder="e.g., #7891-B"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>

        <button
          type="submit"
          disabled={isLoading}
          className="flex items-center gap-2 bg-green-600 text-white px-6 py-3 rounded-md hover:bg-green-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <Play className="w-4 h-4" />
          {isLoading ? 'Starting Call...' : 'Start Test Call'}
        </button>
      </form>
    </div>
  );
};

export default CallTrigger;
