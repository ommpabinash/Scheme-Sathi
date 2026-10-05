# MAHARAJA AGRASEN INSTITUTE OF TECHNOLOGY
### Computer Science and Engineering Department
**MINOR PROJECT SYNOPSIS**  
**B.Tech VII Semester, Batch (2023-2027)**

---

| Field | Details |
| :--- | :--- |
| **Team ID** | MNP007 |
| **Project Title** | Government Scheme Discovery & Eligibility Assistant: A Multi-Agent AI Framework for Citizen Empowerment |
| **Track** | Tech for Good / Public Infrastructure |
| **Team Members** | Keshav Jindal (Enrollment No. 00496402723)<br>Vaibhav Garg (Enrollment No. 01196402723) |
| **Project Guide** | Dr. Yogesh Sharma |

---

## 1. Title of the Project
**Government Scheme Discovery & Eligibility Assistant**  
A Hybrid Multi-Agent AI Framework for Citizen Empowerment that flips the paradigm from citizens searching for schemes to the system finding schemes for the citizen using a dual-engine (100 Master Schemes Local RAG + Playwright DOM Scraper + Serper API Web Search) approach and an interactive React web dashboard.

---

## 2. Problem Statement
Millions of citizens, especially those from marginalized or rural communities, fail to benefit from government welfare programs simply because they are unaware of their existence or confused by bureaucratic language defining eligibility. Scheme details are updated frequently and scattered across fragmented departmental portals and dense PDF notifications. A citizen must manually cross-reference their personal demographics (income, caste, gender, occupation, location) against dozens of overlapping criteria just to figure out if they qualify.

---

## 3. Why is the Particular Topic Chosen?
The core challenge in public welfare is a lack of accessible and up-to-date information. This topic was chosen because it sits at the critical intersection of "Tech for Good" and advanced AI. By combining a local RAG Knowledge Base indexing **100+ Master Government Schemes** with Playwright Headless Chromium DOM scraping and live Serper API Web Search (`site:gov.in`), the system covers all 500+ state and central schemes while guaranteeing 100% demo reliability.

---

## 4. Objective(s) and Scope of the Project

### Objectives
- **Natural Language Profile Extraction:** Allow citizens to explain their situation in their own natural words or regional language via text or voice.
- **Dual-Engine Scheme Retrieval:** Retrieve core scheme policies from a local RAG vector store of **100+ Master Schemes**, falling back dynamically to Playwright Chromium DOM scraping and Serper API Web Search for all remaining 500+ schemes.
- **Dynamic Policy Adjudication:** Programmatically evaluate Gemini 2.5 Flash policy rules against the user's demographic profile to filter out ineligible schemes and display disqualification warnings.
- **Explain & Guide:** Summarize schemes in simple terms, generate step-by-step application roadmaps, and provide required document checklists.
- **Multilingual & Voice Support:** Support seamless translation into regional Indian languages with audio playback.

### Scope
The initial prototype focuses on conversational search, a hybrid multi-agent backend pipeline (Profile Extractor, RAG Agent, Playwright Scraper, Serper Web Search Agent, Gemini 2.5 Flash Adjudicator, and Counselor Agent), and an interactive **React.js + Tailwind CSS** web dashboard. Future scope includes integration with government verification APIs (such as DigiLocker) and deployment on messaging channels like WhatsApp.

---

## 5. Hardware, Software, and Technology Stack
- **Frontend Stack:** **React.js + Tailwind CSS + Lucide Icons** (Vite build tool)
- **Backend & AI Frameworks:** Python 3.10+, FastAPI REST API, Python AgentState Multi-Agent Pipeline.
- **DOM Scraper:** Playwright Headless Chromium (scrapes dynamic Next.js React SPA elements `#benefits`, `#eligibility`, `#documents-required`, `#application-process`).
- **LLM Reasoning & Policy Engine:** Google Gemini 2.5 Flash (`gemini-2.5-flash`).
- **Dual Retrieval Engine:** Retrieval-Augmented Generation (RAG) over 100+ Scheme Documents via ChromaDB alongside Serper API (Google Search API).
- **Speech & Multilingual Engine:** Web Speech API (Speech-to-Text), gTTS (Text-to-Speech), and Deep Translator API.

---

## 6. Contribution Towards Society
This system fundamentally empowers marginalized citizens by bringing government welfare directly to their pocket. By removing language barriers through native-tongue translations and breaking down dense legal jargon into actionable, bite-sized summaries, it actively reduces inequality and ensures public infrastructure serves the public.

---

## 7. Schedule of the Project (30-Day Build Plan)

| Phase / Activity | Timeline |
| :--- | :--- |
| Environment Setup & Data Ingestion (100+ Master Schemes) | Days 1–6 |
| Multi-Agent Logic (Profile, RAG, Playwright, Serper, Eligibility Agents) | Days 7–14 |
| FastAPI Backend Development & Audio API Endpoints | Days 15–18 |
| React Frontend Development (React.js + Tailwind CSS + Speech UI) | Days 19–25 |
| Multilingual Integration, Testing & Quantitative Benchmarking | Days 26–28 |
| Final Documentation, Presentation Deck & Defense Prep | Days 29–30 |

---

## 8. Conclusion
The Government Scheme Discovery & Eligibility Assistant proposes a highly scalable, hybrid multi-agent AI solution to public information asymmetry. By combining RAG over 100+ official scheme documents with Playwright DOM scraping and live Serper API search and eligibility prediction capabilities, the system consolidates fragmented bureaucratic processes into a single, user-friendly conversational interface.

---

## 9. References / Bibliography
1. Lewis, P., et al. "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks," *NeurIPS*, 2020.
2. Playwright Documentation: Fast and reliable end-to-end testing for modern web apps. [Online]. Available: https://playwright.dev
3. National Portal of India & myScheme Portal. [Online]. Available: https://www.myscheme.gov.in
4. Serper API Documentation (Google Search API). [Online]. Available: https://serper.dev
