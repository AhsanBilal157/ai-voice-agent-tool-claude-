import React, { useState } from 'react';
import { Settings, Save } from 'lucide-react';

const AgentConfig = ({ config, onUpdate, onSave }) => {
  const [formData, setFormData] = useState({
    name: config?.name || 'Default Logistics Agent',
    system_prompt: config?.system_prompt || `You are a professional logistics dispatch agent calling to check on driver status. You should:

1. Start with a professional greeting mentioning the driver's name and load number
2. Ask for a status update with an open-ended question
3. Based on their response, ask follow-up questions about:
   - Current location
   - Estimated time of arrival
   - Any delays or issues
4. If they mention an emergency, immediately switch to emergency protocol:
   - Ask for their exact location
   - Determine the type of emergency
   - Assure them a human dispatcher will call back immediately
   - End the call quickly
5. Handle difficult situations professionally:
   - If they give short answers, probe for more details
   - If you can't understand them, ask them to repeat up to 2 times
   - If they remain uncooperative, politely end the call`,
    conversation_logic: config?.conversation_logic || `CONVERSATION FLOW:

NORMAL CHECK-IN:
1. Greeting: "Hi [Name], this is Dispatch calling about load [Load#]. Can you give me an update on your status?"
2. Listen for response and categorize:
   - DRIVING: Ask about location and ETA
   - DELAYED: Ask about reason and new ETA
   - ARRIVED: Confirm delivery details
3. Gather required information and confirm
4. Professional closing

EMERGENCY PROTOCOL:
1. If keywords detected (accident, breakdown, medical, emergency, help, crash, stuck, problem):
2. Immediately say: "I understand this is an emergency. Can you tell me your exact location?"
3. Ask: "What type of emergency are you experiencing?"
4. Say: "A human dispatcher will call you back immediately. Stay safe."
5. End call quickly

DIFFICULT SITUATIONS:
- Short answers: "Can you provide more details about [specific topic]?"
- Unclear speech: "I'm sorry, could you repeat that?" (max 2 times)
- Uncooperative: "I understand. We'll follow up later. Drive safely."`
  });

  const handleChange = (field, value) => {
    const updated = { ...formData, [field]: value };
    setFormData(updated);
    onUpdate(updated);
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-sm border">
      <div className="flex items-center gap-2 mb-4">
        <Settings className="w-5 h-5 text-blue-600" />
        <h2 className="text-xl font-semibold">Agent Configuration</h2>
      </div>
      
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Agent Name
          </label>
          <input
            type="text"
            value={formData.name}
            onChange={(e) => handleChange('name', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            System Prompt
          </label>
          <textarea
            value={formData.system_prompt}
            onChange={(e) => handleChange('system_prompt', e.target.value)}
            rows={8}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Define how the agent should behave and respond..."
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Conversation Logic
          </label>
          <textarea
            value={formData.conversation_logic}
            onChange={(e) => handleChange('conversation_logic', e.target.value)}
            rows={10}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Define the conversation flow and decision logic..."
          />
        </div>

        <button
          onClick={onSave}
          className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors"
        >
          <Save className="w-4 h-4" />
          Save Configuration
        </button>
      </div>
    </div>
  );
};

export default AgentConfig;
