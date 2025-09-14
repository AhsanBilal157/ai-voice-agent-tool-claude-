
import React, { useState } from 'react';
import { History, AlertTriangle, CheckCircle } from 'lucide-react';

const CallHistory = ({ calls, onRefresh }) => {
  const [selectedCall, setSelectedCall] = useState(null);

  const getOutcomeIcon = (outcome) => {
    if (outcome?.includes('Emergency')) return <AlertTriangle className="w-4 h-4 text-red-500" />;
    if (outcome?.includes('Completed') || outcome?.includes('Confirmation')) return <CheckCircle className="w-4 h-4 text-green-500" />;
    return <div className="w-4 h-4 rounded-full bg-yellow-400"></div>;
  };

  const getOutcomeColor = (outcome) => {
    if (outcome?.includes('Emergency')) return 'text-red-600 bg-red-50';
    if (outcome?.includes('Completed') || outcome?.includes('Confirmation')) return 'text-green-600 bg-green-50';
    if (outcome?.includes('Progress')) return 'text-blue-600 bg-blue-50';
    return 'text-yellow-600 bg-yellow-50';
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-sm border">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <History className="w-5 h-5 text-purple-600" />
          <h2 className="text-xl font-semibold">Call History</h2>
        </div>
        <button
          onClick={onRefresh}
          className="text-sm text-blue-600 hover:text-blue-800"
        >
          Refresh
        </button>
      </div>

      <div className="space-y-3">
        {calls.length === 0 ? (
          <p className="text-gray-500 text-center py-8">No calls yet. Start by triggering a test call.</p>
        ) : (
          calls.map((call) => (
            <div
              key={call.id}
              className="border rounded-lg p-4 hover:bg-gray-50 cursor-pointer"
              onClick={() => setSelectedCall(selectedCall?.id === call.id ? null : call)}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  {getOutcomeIcon(call.call_outcome)}
                  <div>
                    <h3 className="font-medium">{call.driver_name} - {call.load_number}</h3>
                    <p className="text-sm text-gray-600">{call.phone_number}</p>
                  </div>
                </div>
                <div className="text-right">
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${getOutcomeColor(call.call_outcome)}`}>
                    {call.call_outcome || 'Pending'}
                  </span>
                  <p className="text-sm text-gray-500 mt-1">
                    {new Date(call.created_at).toLocaleString()}
                  </p>
                </div>
              </div>

              {selectedCall?.id === call.id && (
                <div className="mt-4 pt-4 border-t">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                    <div>
                      <h4 className="font-medium text-gray-800 mb-2">Structured Data</h4>
                      <div className="bg-gray-50 p-3 rounded text-sm">
                        {call.structured_data ? (
                          <pre className="whitespace-pre-wrap">
                            {JSON.stringify(call.structured_data, null, 2)}
                          </pre>
                        ) : (
                          <p className="text-gray-500">No structured data available</p>
                        )}
                      </div>
                    </div>
                    <div>
                      <h4 className="font-medium text-gray-800 mb-2">Call Details</h4>
                      <div className="space-y-2 text-sm">
                        <div><span className="font-medium">Call ID:</span> {call.call_id || 'N/A'}</div>
                        <div><span className="font-medium">Status:</span> {call.call_outcome}</div>
                        <div><span className="font-medium">Duration:</span> N/A</div>
                      </div>
                    </div>
                  </div>
                  
                  {call.transcript && (
                    <div>
                      <h4 className="font-medium text-gray-800 mb-2">Call Transcript</h4>
                      <div className="bg-gray-50 p-4 rounded max-h-64 overflow-y-auto">
                        <pre className="whitespace-pre-wrap text-sm">{call.transcript}</pre>
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default CallHistory;
