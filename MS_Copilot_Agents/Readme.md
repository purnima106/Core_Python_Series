This is a dedicated file for noting down the learning key takeaways from the MS Copilot Agents class. 

What is Microsoft Copilot Studio?
Microsoft Copilot Studio is an enterprise platform used to build AI-powered conversational agents,
copilots, and agentic systems.

Enterprise Agent Architecture

User-> Copilot Interface->Intent Detection-> Topics/Convos-> Entities + Variables->Context Management->Knowledge Search->LLM / GPT Model-> Actions/API Calls ->Final Response to User.

Key Enterprise Concepts:

1. Contextual Awareness- Ability to understand the user's intent and provide relevant responses based on the current conversation and user data.
2. Hallucination Control- Techniques used to prevent AI models from generating false or misleading information. 

Enterprises reduce hallucinations using:
RAG
Grounding
Enterprise retrieval
Tool calling
Fallback responses
Guardrails
Validation workflows

3. Data Leakage Prevention- Techniques used to prevent AI models from exposing sensitive information.

Prevention Methods:
Authentication
Authorization
RBAC (Role Based Access Control)
Secure APIs
Permission checks
Tenant isolation
Prompt filtering

4. RAG (Retrieval Augmented Generation)-RAG is an architecture where AI retrieves enterprise knowledge before generating a response.
Instead of answering only from model memory, the system first searches company data.

RAG Architecture
User Question
 ↓
Search Enterprise Knowledge
 ↓
Retrieve Relevant Documents
 ↓
Pass Context to LLM
 ↓
Generate Grounded Response

RAG helps:
Reduce hallucinations
Use latest enterprise information
Improve accuracy
Use private company knowledge

