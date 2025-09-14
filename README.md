# AI Voice Agent Tool for Logistics

A comprehensive full-stack web application that enables non-technical administrators to configure, test, and review calls made by an adaptive AI voice agent for logistics operations.

## 🎯 Project Overview

This application provides an intuitive interface for managing AI-powered voice calls to truck drivers, handling both routine check-ins and emergency situations. The system uses Retell AI for voice capabilities, OpenAI for intelligent conversation management, and provides structured data extraction from call transcripts.

## 🏗️ Architecture

### Frontend (React + Vite)
- **Dashboard**: Single-page application with tabbed interface
- **Agent Configuration**: Dynamic prompt and logic management
- **Call Triggering**: Initiate test calls with driver information
- **Call History**: Review transcripts and structured data

### Backend (FastAPI)
- **REST API**: Serves frontend and manages configurations
- **Webhook Handler**: Processes real-time Retell AI callbacks
- **Call Processing**: Extracts structured data using OpenAI
- **Database Integration**: Supabase for data persistence

### Key Integrations
- **Retell AI**: Voice agent platform for phone calls
- **OpenAI GPT-4**: Conversation logic and data extraction
- **Supabase**: PostgreSQL database with real-time capabilities

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- Supabase account
- OpenAI API key
- Retell AI account

### 1. Clone and Setup

```bash
git clone <your-repo-url>
cd ai-voice-agent-tool
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env` file in backend directory:
```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
OPENAI_API_KEY=your_openai_api_key
RETELL_API_KEY=your_retell_api_key
RETELL_AGENT_ID=your_retell_agent_id
BACKEND_URL=http://localhost:8000  # For development
```

### 3. Database Setup (Supabase)

Run this SQL in your Supabase SQL editor:

```sql
-- Agent configurations table
CREATE TABLE agent_configs (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    system_prompt TEXT NOT NULL,
    conversation_logic TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Call logs table
CREATE TABLE call_logs (
    id SERIAL PRIMARY KEY,
    driver_name VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    load_number VARCHAR(100) NOT NULL,
    call_id VARCHAR(255) UNIQUE,
    transcript TEXT,
    structured_data JSONB,
    call_outcome VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    agent_config_id INTEGER REFERENCES agent_configs(id)
);

-- Insert default configuration
INSERT INTO agent_configs (name, system_prompt, conversation_logic) VALUES (
    'Default Logistics Agent',
    'You are a professional logistics dispatch agent...',
    'CONVERSATION FLOW: NORMAL CHECK-IN...'
);
```

### 4. Retell AI Setup

1. Create account at [Retell AI](https://retellai.com)
2. Create a new agent in the dashboard
3. Configure agent settings:
   - **Voice**: Choose natural-sounding voice
   - **Language**: English
   - **Interruption Sensitivity**: Medium
   - **Backchanneling**: Enabled
   - **Filler Words**: Enabled
4. Set webhook URL to: `https://your-backend-url.com/api/webhook/retell`
5. Copy Agent ID to your `.env` file

### 5. Start Backend

```bash
uvicorn app.main:app --reload --port 8000
```

### 6. Frontend Setup

```bash
cd ../frontend
npm install
npm run dev
```

Visit `http://localhost:5173` to access the application.

## 🎛️ Usage Guide

### 1. Configure Agent
- Navigate to "Configure Agent" tab
- Edit system prompts and conversation logic
- Click "Save Configuration" to store changes

### 2. Trigger Test Call
- Go to "Test Call" tab
- Enter driver name, phone number, and load number
- Click "Start Test Call" to initiate the call

### 3. Review Results
- Check "Call History" tab for completed calls
- Click on any call to see structured data and transcript
- Monitor call outcomes and agent performance

## 🎯 Conversation Scenarios

### Scenario 1: Driver Check-in
**Context**: Routine status update call
- Agent asks open-ended status question
- Dynamically follows up based on driver response
- Extracts: location, ETA, delivery status

**Extracted Data**:
```json
{
  "call_outcome": "In-Transit Update",
  "driver_status": "Driving",
  "current_location": "I-10 near Indio, CA",
  "eta": "Tomorrow, 8:00 AM"
}
```

### Scenario 2: Emergency Protocol
**Context**: Driver reports emergency during call
- Agent immediately shifts to emergency mode
- Gathers critical information quickly
- Escalates to human dispatcher

**Extracted Data**:
```json
{
  "call_outcome": "Emergency Detected",
  "emergency_type": "Breakdown",
  "emergency_location": "I-15 North, Mile Marker 123",
  "escalation_status": "Escalation Flagged"
}
```

## 🛠️ Technical Implementation

### Real-time Conversation Flow
1. Retell AI receives call and streams audio
2. Speech-to-text converts driver responses
3. Webhook sends text to our FastAPI backend
4. OpenAI generates contextual agent response
5. Response sent back to Retell AI for text-to-speech
6. Agent speaks to driver in real-time

### Post-call Processing
1. Call ends, full transcript sent to webhook
2. OpenAI processes transcript for structured data
3. Results stored in Supabase database
4. Frontend displays structured summary and transcript

### Key Features
- **Dynamic Response Handling**: Adapts to uncooperative drivers and noisy environments
- **Emergency Detection**: Immediate protocol shift for safety situations
- **Realistic Voice**: Optimized Retell AI settings for human-like conversation
- **Structured Data**: Automatic extraction of key logistics information

## 🔧 Customization

### Modifying Agent Behavior
Edit prompts in the configuration interface or directly in the database:
- `system_prompt`: Defines agent personality and guidelines
- `conversation_logic`: Specific conversation flows and decision trees

### Adding New Scenarios
1. Update conversation logic in agent configuration
2. Modify `call_processor.py` to handle new data structures
3. Update frontend to display new structured data fields

### Voice Optimization
Adjust Retell AI agent settings:
- **Interruption Sensitivity**: How easily agent can be interrupted
- **Response Speed**: How quickly agent responds
- **Filler Words**: Use of "um", "uh" for natural speech
- **Backchanneling**: "mm-hmm", "I see" responses

## 🚀 Deployment

### Backend (Railway/Render)
1. Connect GitHub repository
2. Set environment variables
3. Deploy from main branch
4. Update Retell AI webhook URL

### Frontend (Vercel/Netlify)
1. Connect GitHub repository  
2. Set build command: `npm run build`
3. Set publish directory: `dist`
4. Deploy from main branch

### Environment Variables for Production
```env
SUPABASE_URL=your_production_supabase_url
SUPABASE_KEY=your_production_supabase_key
OPENAI_API_KEY=your_openai_api_key
RETELL_API_KEY=your_retell_api_key
RETELL_AGENT_ID=your_retell_agent_id
BACKEND_URL=https://your-backend-production-url.com
```

## 📋 Testing Checklist

- [ ] Agent configuration saves successfully
- [ ] Test call triggers and connects
- [ ] Normal check-in scenario extracts correct data
- [ ] Emergency protocol activates on trigger words
- [ ] Uncooperative driver handling works
- [ ] Noisy environment handling functions
- [ ] Call history displays properly
- [ ] Structured data appears in UI

## 🔍 Troubleshooting

### Common Issues
1. **Calls not connecting**: Check Retell AI webhook URL and API keys
2. **No structured data**: Verify OpenAI API key and model access
3. **Database errors**: Confirm Supabase connection and table schema
4. **Frontend not loading**: Check API endpoint URLs match backend

### Debugging
- Check browser console for frontend errors
- Monitor FastAPI logs for backend issues
- Verify Retell AI webhook receives POST requests
- Test OpenAI API calls independently

## 📝 Design Decisions

### Technology Stack Rationale
- **FastAPI**: Fast, async Python framework perfect for webhooks
- **React**: Modern, component-based UI with excellent developer experience
- **Supabase**: PostgreSQL with real-time features and easy setup
- **Retell AI**: Specialized voice AI platform with excellent call quality
- **OpenAI**: Most capable LLM for natural conversation and data extraction

### Architecture Choices
- **Single Page Application**: Reduces complexity for administrators
- **Real-time Webhooks**: Enables dynamic conversation management
- **Structured Data Extraction**: Post-processing ensures consistent data format
- **Configuration-driven**: Non-technical users can modify agent behavior

## 🔮 Future Enhancements

- Multi-tenant support for multiple logistics companies
- Advanced analytics and reporting dashboard
- Integration with existing logistics management systems
- Voice analysis for driver stress/fatigue detection
- Mobile app for field managers
- Automated follow-up call scheduling

## 📄 License

This project is intended for assessment purposes. Please ensure you have proper licenses for all third-party services (OpenAI, Retell AI, Supabase) in production use.