from src.agents.state import AgentState
from src.utils.llm_client import llm_client
from src.tools.serper_tool import serper_tool
from src.tools.playwright_scraper import playwright_scraper

def clean_url(url: str) -> str:
    """Ensure clean URL without trailing semicolons or punctuation."""
    if not url:
        return "https://www.myscheme.gov.in"
    return url.strip().rstrip(";").rstrip(".").rstrip(",")

# Curated database of major schemes with exact verified myScheme portal URLs, simple benefits, docs, and steps
SCHEME_KNOWLEDGE_BASE = {
    "krishak_durghatna": {
        "name": "Mukhyamantri Krishak Durghatna Kalyan Yojana",
        "short_desc": "Accident compensation up to ₹5 Lakh for farmers injured or killed while working on agricultural land.",
        "highlights": [
            "Up to ₹5 Lakh for accidental death or permanent disability",
            "Direct Bank Transfer (DBT) to farmer/nominee account",
            "For UP farmers aged 18-70 years"
        ],
        "benefits": [
            "Financial compensation of up to Rs 5,00,000 (5 Lakh) in case of accidental death while working on agricultural land.",
            "Financial assistance of Rs 5,00,000 for 100% permanent disability (loss of both hands, both feet, or both eyes).",
            "Financial assistance ranging from Rs 1,00,000 to Rs 2,50,000 for partial permanent disability (loss of one limb or one eye).",
            "Direct Bank Transfer (DBT) credit directly into the bank account of the farmer or legal nominee."
        ],
        "eligibility": "Farmers and leaseholder agricultural laborers aged 18 to 70 years in Uttar Pradesh.",
        "portal": "https://www.myscheme.gov.in/schemes/kdky",
        "docs": [
            "Aadhaar Card of the farmer (linked with active mobile number)",
            "Land Ownership Records (Khasra / Khatauni / Gata Number)",
            "Proof of Residence / Domicile Certificate of Uttar Pradesh",
            "Income Certificate issued by competent Revenue authority (Tehsildar)",
            "Accidental Death Report / Post-Mortem Report or Medical Disability Certificate from Government Hospital",
            "Bank Account Passbook with IFSC code for Direct Benefit Transfer (DBT)"
        ],
        "steps": [
            "🌐 ONLINE METHOD",
            "Visit the official portal (www.myscheme.gov.in/schemes/kdky) or UP e-District portal.",
            "Click 'Apply Online' and log in using your registered mobile number and OTP.",
            "Fill out the digital application form with personal, land, and bank account details.",
            "Upload scanned copies of Aadhaar, Khasra land records, and hospital medical certificate, then click Submit.",
            "🏢 OFFLINE METHOD",
            "Visit your local Tehsil Office, District Magistrate (DM) office, or nearest Common Service Centre (CSC).",
            "Collect the physical Krishak Durghatna Kalyan application form from the Revenue Officer.",
            "Attach self-attested photocopies of Aadhaar, Khasra land records, and hospital death/disability report.",
            "Submit the completed form to the Tehsildar within 45 days of the incident to receive your tracking receipt."
        ]
    },
    "up_old_age_pension": {
        "name": "Uttar Pradesh Old Age Pension Scheme",
        "short_desc": "Monthly pension assistance of ₹1,000 per month for senior citizens (60+ years) from BPL / low-income families.",
        "highlights": [
            "Monthly pension of ₹1,000 per month (₹12,000/year)",
            "Direct Benefit Transfer (DBT) to bank account",
            "For UP senior citizens aged 60 to 150 years"
        ],
        "benefits": [
            "Monthly pension assistance of Rs 1,000 per month (Rs 12,000 per year) credited directly to bank account via Direct Benefit Transfer (DBT).",
            "Financial security and dignity for elderly senior citizens living below the poverty line (BPL) or low income limit.",
            "Transparent online disbursement directly managed by Social Welfare Department of Uttar Pradesh."
        ],
        "eligibility": "Senior citizens aged 60 to 150 years in UP with annual income up to Rs 46,080 (Rural) or Rs 56,460 (Urban).",
        "portal": "https://www.myscheme.gov.in/schemes/upoaps",
        "docs": [
            "Aadhaar Card of senior citizen",
            "Proof of Age (Voter ID / Birth Certificate / Aadhaar)",
            "Income Certificate issued by Tehsildar (Rural <= Rs 46,080 / Urban <= Rs 56,460)",
            "UP Domicile / Residence Certificate",
            "Bank Account Passbook with IFSC code for DBT credit"
        ],
        "steps": [
            "🌐 ONLINE METHOD",
            "Visit sspy-up.gov.in or myscheme.gov.in/schemes/upoaps portal.",
            "Click 'Old Age Pension' -> 'Apply Online'.",
            "Fill out personal, age, address, and bank details.",
            "Upload Aadhaar, income certificate, and photo, then submit application.",
            "🏢 OFFLINE METHOD",
            "Visit local Block Development Office (BDO) or District Social Welfare Officer.",
            "Submit physical form along with Aadhaar, income certificate, and bank passbook photocopy."
        ]
    },
    "pm_kisan": {
        "name": "PM Kisan Samman Nidhi (PM-KISAN)",
        "short_desc": "₹6,000 per year direct income support for all landholding farmer families in 3 installments.",
        "highlights": [
            "₹6,000/year in 3 installments of ₹2,000",
            "100% Central Govt funded via DBT",
            "For small & marginal farmer families"
        ],
        "benefits": [
            "Direct income support of Rs 6,000 per year for all landholding farmer families.",
            "Transferred directly into bank accounts in 3 equal installments of Rs 2,000 every 4 months.",
            "100% Central Sector Scheme with Direct Benefit Transfer (DBT) through Aadhaar payment bridge."
        ],
        "eligibility": "Small and marginal farmer families with cultivable landholding up to 2 hectares.",
        "portal": "https://www.myscheme.gov.in/schemes/pm-kisan",
        "docs": [
            "Aadhaar Card (linked with active mobile number for e-KYC)",
            "Landholding Ownership Document (Khasra / Khatauni)",
            "Savings Bank Account Passbook with IFSC code (linked to Aadhaar)",
            "Domicile / State Residence Certificate"
        ],
        "steps": [
            "🌐 ONLINE METHOD",
            "Visit pmkisan.gov.in or myscheme.gov.in/schemes/pm-kisan portal.",
            "Click on 'Farmers Corner' → 'New Farmer Registration'.",
            "Enter your Aadhaar number, active mobile number, state, and land survey details.",
            "Complete OTP e-KYC verification and submit the online application.",
            "🏢 OFFLINE METHOD",
            "Visit your local Block Development Office (BDO), Tehsil, or nearest CSC Centre.",
            "Submit physical photocopies of your Aadhaar card, land Khatauni passbook, and bank details.",
            "The Agriculture Nodal Officer will verify your land documents and register your profile on the PM-KISAN portal."
        ]
    },
    "pmfby": {
        "name": "Pradhan Mantri Fasal Bima Yojana (PMFBY)",
        "short_desc": "Crop insurance against drought, flood, pest loss — low premium, government pays the rest.",
        "highlights": [
            "Premium just 2% Kharif, 1.5% Rabi crops",
            "Covers drought, flood, pest, hailstorm",
            "Apply via bank or PMFBY portal before cutoff"
        ],
        "benefits": [
            "Insurance cover against non-preventable natural risks (drought, flood, unseasonal rainfall, pests, diseases).",
            "Low farmer premium rates: 2% for Kharif crops, 1.5% for Rabi crops, and 5% for commercial/horticulture crops.",
            "Claim settlement credited directly to the farmer's bank account."
        ],
        "eligibility": "All farmers growing notified crops including sharecroppers and tenant farmers.",
        "portal": "https://www.myscheme.gov.in/schemes/pmfby",
        "docs": [
            "Aadhaar Card of the farmer",
            "Land Record (Khatauni) or Land Tenancy Agreement",
            "Sowing Certificate issued by Patwari / Gram Pradhan",
            "Bank Account Passbook details"
        ],
        "steps": [
            "🌐 ONLINE METHOD",
            "Visit pmfby.gov.in or myscheme.gov.in/schemes/pmfby portal.",
            "Click 'Farmer Application' and log in with your mobile number.",
            "Enter crop details, land survey number, area sown, and bank account info.",
            "Pay nominal premium (1.5% to 2%) via net banking/UPI to download your policy receipt.",
            "🏢 OFFLINE METHOD",
            "Visit your local Commercial Bank branch, Cooperative Bank, or nearest CSC Centre before cut-off date.",
            "Fill the crop insurance application form and attach land sowing certificate and bank passbook copy.",
            "Pay the premium in cash/cheque at bank counter and collect the stamped insurance acknowledgment."
        ]
    },
    "ayushman": {
        "name": "Ayushman Bharat PM-JAY Health Scheme",
        "short_desc": "Free cashless health insurance up to ₹5 Lakh per family per year at any empanelled hospital.",
        "highlights": [
            "₹5 Lakh free health cover per family/year",
            "Cashless at govt & private hospitals",
            "No age, gender, or family size limit"
        ],
        "benefits": [
            "Free cashless health insurance coverage up to Rs 5,00,000 (5 Lakh) per family per year.",
            "Covers pre-hospitalization, hospitalization, surgeries, diagnostics, and medicines across empanelled government and private hospitals.",
            "No restriction on family size, age, or gender."
        ],
        "eligibility": "Low-income families listed under SECC database or senior citizens aged 70+.",
        "portal": "https://www.myscheme.gov.in/schemes/ab-pmjay",
        "docs": [
            "Aadhaar Card / Voter ID Card",
            "Ration Card / Family ID",
            "Active Mobile Number for OTP verification"
        ],
        "steps": [
            "🌐 ONLINE METHOD",
            "Visit beneficiary.nha.gov.in or myscheme.gov.in/schemes/ab-pmjay portal.",
            "Enter your mobile number, verify with OTP, and search your family name.",
            "Complete e-KYC using Aadhaar OTP or facial authentication.",
            "Download your digital Ayushman Card directly to your mobile phone.",
            "🏢 OFFLINE METHOD",
            "Visit the Ayushman Mitra desk at any empanelled Government or Private Hospital.",
            "Present your physical Aadhaar Card and Ration Card to the Ayushman Mitra representative.",
            "Get your biometric e-KYC verified on-site and receive your printed Ayushman PVC Card."
        ]
    },
    "surya_ghar": {
        "name": "PM Surya Ghar Free Electricity Solar Scheme",
        "short_desc": "Get subsidy up to ₹78,000 for rooftop solar and up to 300 units free electricity per month.",
        "highlights": [
            "Subsidy up to ₹78,000 for rooftop solar",
            "Up to 300 units free electricity/month",
            "Sell surplus power back to DISCOM grid"
        ],
        "benefits": [
            "Subsidy up to Rs 78,000 for installing rooftop solar systems.",
            "Up to 300 units of free electricity every month for the household.",
            "Earn extra income by selling surplus electricity back to the DISCOM grid."
        ],
        "eligibility": "Residential households with a suitable roof and valid electricity connection.",
        "portal": "https://www.myscheme.gov.in/schemes/pmsgmby",
        "docs": [
            "Aadhaar Card of home owner",
            "Latest Electricity Bill copy",
            "Proof of Roof Ownership / Property Tax Receipt",
            "Bank Account Passbook for subsidy credit"
        ],
        "steps": [
            "🌐 ONLINE METHOD",
            "Visit pmsuryaghar.gov.in or myscheme.gov.in/schemes/pmsgmby portal.",
            "Register with your State Electricity DISCOM and consumer account number.",
            "Apply for rooftop solar installation and select an empaneled vendor.",
            "After vendor installation, submit net-metering application to receive subsidy direct to bank.",
            "🏢 OFFLINE METHOD",
            "Visit your local Electricity DISCOM divisional office or CSC Kendra.",
            "Submit physical application form along with latest electricity bill and roof ownership document.",
            "DISCOM engineers inspect roof feasibility and assist with offline vendor allocation."
        ]
    },
    "kcc": {
        "name": "Kisan Credit Card (KCC) Scheme",
        "short_desc": "Low-interest credit up to ₹3 Lakh for crop cultivation, animal husbandry, and fisheries.",
        "highlights": [
            "Credit limit up to ₹3 Lakh at 4% interest",
            "2% extra subvention for timely repayment",
            "Covers crops, dairy, poultry & fisheries"
        ],
        "benefits": [
            "Short-term credit at subsidized interest rate of 7% per annum (effective 4% after subvention).",
            "Additional 2% interest subvention for prompt repayment, making effective rate just 4%.",
            "Credit limit up to Rs 3,00,000 for crop cultivation, post-harvest, and allied activities."
        ],
        "eligibility": "All farmers, sharecroppers, tenant farmers, and SHG members engaged in crop/animal husbandry/fisheries.",
        "portal": "https://www.myscheme.gov.in/schemes/kcc",
        "docs": [
            "Aadhaar Card of the farmer",
            "Land Ownership / Tenancy document",
            "Passport size photographs",
            "Bank Account details"
        ],
        "steps": [
            "🌐 ONLINE METHOD",
            "Visit your bank's internet banking portal or PM-KISAN portal (pmkisan.gov.in).",
            "Click 'KCC Application' and fill the online form with land and crop details.",
            "Upload Aadhaar, land records, and submit.",
            "🏢 OFFLINE METHOD",
            "Visit your nearest Commercial Bank, Cooperative Bank, or Regional Rural Bank (RRB).",
            "Fill the KCC application form and submit land ownership documents.",
            "Bank will process and issue the Kisan Credit Card within 14 working days."
        ]
    }
}

GENERAL_BENEFITS = [
    "Financial assistance and financial security provided directly by the Government of India / State Government.",
    "Direct Benefit Transfer (DBT) directly into the applicant's verified Aadhaar-linked bank account.",
    "Transparent processing with online application status tracking."
]

GENERAL_DOCS = [
    "Aadhaar Card (linked with active mobile number)",
    "Savings Bank Account Passbook with IFSC code",
    "Proof of Residence / Domicile Certificate",
    "Income Certificate issued by competent Tehsildar / Revenue Authority",
    "Category / Caste Certificate (if SC / ST / OBC / EWS)"
]

GENERAL_STEPS = [
    "🌐 ONLINE METHOD",
    "Visit the official myScheme portal (www.myscheme.gov.in) and search for the scheme name.",
    "Click 'Apply Online', log in using your mobile number and OTP.",
    "Fill out the online application form with your personal and income details.",
    "Upload scanned copies of required documents and click Submit to get reference tracking number.",
    "🏢 OFFLINE METHOD",
    "Visit your local Tehsil Office, Block Development Office (BDO), or nearest Common Service Centre (CSC).",
    "Collect the physical application form from the designated nodal officer.",
    "Attach self-attested photocopies of Aadhaar, income, and domicile certificates.",
    "Submit the completed form to the office counter and retain the acknowledgment receipt."
]

def find_matched_kb_scheme(scheme_title: str):
    """Match scheme title against curated knowledge base."""
    if not scheme_title:
        return None
    title_low = scheme_title.lower()
    
    if "old age" in title_low or "pension" in title_low or "upoaps" in title_low:
        return SCHEME_KNOWLEDGE_BASE["up_old_age_pension"]
    elif "durghatna" in title_low or "kdky" in title_low or "krishak" in title_low:
        return SCHEME_KNOWLEDGE_BASE["krishak_durghatna"]
    elif "pm kisan" in title_low or "samman nidhi" in title_low or "pm-kisan" in title_low:
        return SCHEME_KNOWLEDGE_BASE["pm_kisan"]
    elif "fasal bima" in title_low or "pmfby" in title_low:
        return SCHEME_KNOWLEDGE_BASE["pmfby"]
    elif "ayushman" in title_low or "pm-jay" in title_low or "pmjay" in title_low:
        return SCHEME_KNOWLEDGE_BASE["ayushman"]
    elif "surya ghar" in title_low or "solar" in title_low:
        return SCHEME_KNOWLEDGE_BASE["surya_ghar"]
    elif "kisan credit" in title_low or "kcc" in title_low:
        return SCHEME_KNOWLEDGE_BASE["kcc"]
        
    return None

def generate_scheme_cards(state: AgentState):
    """
    Dynamically generates up to 6 scheme recommendation cards from:
    1. Local RAG Vector Search results (state.retrieved_chunks)
    2. Serper Live Web Search results (state.web_search_results)
    3. Demographic scoring against Knowledge Base (age, state, income, occupation)
    """
    profile = state.user_profile
    user_query = state.user_query or ""
    cards = []
    seen_titles = set()

    # Helper to add card
    def add_card(name, short_desc, highlights, key, portal="https://www.myscheme.gov.in"):
        clean_name = name.strip().rstrip('.').rstrip(';')
        norm_name = clean_name.lower()
        if norm_name not in seen_titles and len(clean_name) > 3:
            seen_titles.add(norm_name)
            cards.append({
                "name": clean_name,
                "short_desc": short_desc or f"Government assistance scheme matching your profile in {profile.state or 'India'}.",
                "highlights": highlights[:3] if highlights else [
                    "Direct Benefit Transfer (DBT) eligible",
                    f"State / Central Government scheme for {profile.occupation or 'citizens'}",
                    "Official myScheme portal application"
                ],
                "scheme_key": key,
                "portal": portal
            })

    # 1. Dynamically extract from RAG Vector Chunks & Serper Web Search Results
    retrieved_sources = (state.retrieved_chunks or []) + (state.web_search_results or [])
    for source in retrieved_sources:
        title = source.get("scheme_id") or source.get("title", "")
        snippet = source.get("content") or source.get("snippet", "")
        link = source.get("link") or source.get("url", "https://www.myscheme.gov.in")

        # Skip generic title noise
        if not title or "Enter scheme name" in title or "myScheme" == title.strip():
            continue

        # Check if title matches curated KB scheme
        kb_match = find_matched_kb_scheme(title)
        if kb_match:
            add_card(
                name=kb_match["name"],
                short_desc=kb_match["short_desc"],
                highlights=kb_match["highlights"],
                key=title,
                portal=kb_match["portal"]
            )
        else:
            # Parse snippet into short description and highlights dynamically
            clean_snippet = snippet.strip().rstrip('.').rstrip(';') + "." if snippet else f"Government scheme for {profile.state or 'eligible citizens'}."
            short_desc = clean_snippet
            highlights = [
                f"Apply via official portal ({clean_url(link)})",
                f"Targeted for {profile.state or 'India'} residents",
                "Verified Government Scheme"
            ]
            add_card(name=title, short_desc=short_desc, highlights=highlights, key=title, portal=clean_url(link))

        if len(cards) >= 8:
            break

    # 2. Dynamic demographic scoring to fill remaining relevant slots if needed
    if len(cards) < 3:
        scored_kb = []
        user_age = profile.age or 35
        user_income = profile.income or 100000
        user_state = (profile.state or "").lower()
        user_occ = (profile.occupation or "").lower()

        for key, kb in SCHEME_KNOWLEDGE_BASE.items():
            name_low = kb["name"].lower()
            elig_low = kb["eligibility"].lower()

            if name_low in seen_titles:
                continue

            # Hard Disqualification Filtering: Do not recommend Pension to users under 60 or exceeding income cap
            if ("pension" in name_low or "old age" in name_low or "senior" in elig_low) and user_age < 60:
                continue
            if ("pension" in name_low or "old age" in name_low or "bpl" in elig_low) and user_income > 56460:
                continue

            score = 50

            if "uttar pradesh" in elig_low and ("up" in user_state or "uttar pradesh" in user_state):
                score += 25

            if "farm" in user_occ or "kisan" in user_occ or "krishak" in user_occ:
                if "farm" in elig_low or "kisan" in name_low or "krishak" in name_low:
                    score += 25

            if "70" in elig_low or "senior" in elig_low:
                if user_age >= 60:
                    score += 20
                else:
                    score -= 10
            elif user_age >= 18:
                score += 10

            scored_kb.append((score, kb))

        scored_kb.sort(key=lambda x: x[0], reverse=True)

        for _, kb in scored_kb:
            if len(cards) >= 6:
                break
            add_card(
                name=kb["name"],
                short_desc=kb["short_desc"],
                highlights=kb["highlights"],
                key=kb["name"],
                portal=kb["portal"]
            )

    return cards


class CounselorGuidanceAgent:
    """
    Counselor & Guidance Agent.
    Generates scheme carousel cards for initial discovery, and full details for selected scheme.
    """

    def _clean_scheme_name(self, name: str) -> str:
        if not name:
            return None
        low = name.lower()
        junk_signals = ["page ", "june", "july", "august", "2026", "2025", "pdf", "download", "news", "update", "enter scheme name"]
        if any(sig in low for sig in junk_signals) or len(name) > 70:
            return None
        cleaned = name.rstrip(" .…").strip()
        return cleaned if len(cleaned) > 2 else None

    def process(self, state: AgentState) -> AgentState:
        evaluation = state.eligibility_evaluation
        profile = state.user_profile
        mode = state.retrieval_mode

        raw_scheme = evaluation.get("top_scheme", "")
        clean_scheme = self._clean_scheme_name(raw_scheme) if raw_scheme else None
        match_score = evaluation.get("match_score", 75)
        is_eligible = evaluation.get("is_eligible", True)

        target_scheme_query = clean_scheme or raw_scheme or (state.user_query if state.user_query else "")
        kb_match = find_matched_kb_scheme(target_scheme_query)

        target_portal = "https://www.myscheme.gov.in"
        if kb_match:
            target_portal = kb_match["portal"]
        elif state.web_search_results:
            scheme_results = [r for r in state.web_search_results if "/schemes/" in r.get("link", "")]
            if scheme_results:
                target_portal = scheme_results[0].get("link", "https://www.myscheme.gov.in")

        # ── Playwright Headless Chromium DOM Scraping ──
        dom_data = playwright_scraper.scrape_scheme_details(target_portal)
        raw_benefits = dom_data.get("raw_benefits", "")
        raw_eligibility = dom_data.get("raw_eligibility", "")
        raw_docs = dom_data.get("raw_docs", "")
        raw_online = dom_data.get("raw_process_online", "")
        raw_offline = dom_data.get("raw_process_offline", "")

        # ── Gemini LLM Post-Processing on Playwright DOM Text ──
        pw_benefits = []
        pw_docs = []
        pw_steps = []
        pw_eligibility = raw_eligibility

        if raw_benefits or raw_docs or raw_online:
            llm_summary_prompt = f"""
You are an expert Government Scheme Assistant. Clean and summarize the following raw myScheme website DOM text into crisp, clean bullet points.

SCHEME NAME: {target_scheme_query}
PORTAL URL: {target_portal}

RAW BENEFITS TEXT:
{raw_benefits}

RAW DOCUMENTS TEXT:
{raw_docs}

RAW ONLINE PROCESS:
{raw_online}

RAW OFFLINE PROCESS:
{raw_offline}

STRICT FORMATTING RULES:
1. "benefits": Array of 3 to 6 clean, concise benefit bullet statements summarizing financial assistance, insurance, or subsidies. Do NOT output long narrative paragraphs.
2. "docs": Array of clean required document names (e.g. ["Aadhaar Card", "Land Khatauni Record", "Domicile Certificate"]). Do NOT include titles like "List of the required documents".
3. "steps": Array of application steps. Group online steps under "🌐 ONLINE METHOD" and offline steps under "🏢 OFFLINE METHOD". Convert any text referring to "official website" or "portal" into a clickable markdown link: [official website]({target_portal}).

Respond strictly in valid JSON:
{{
  "benefits": ["Benefit statement 1", "Benefit statement 2"],
  "docs": ["Document 1", "Document 2"],
  "steps": ["🌐 ONLINE METHOD", "1. Step 1", "🏢 OFFLINE METHOD", "1. Step 1"]
}}
"""
            llm_res = llm_client.generate_json(llm_summary_prompt)
            if llm_res:
                pw_benefits = llm_res.get("benefits", [])
                pw_docs = llm_res.get("docs", [])
                pw_steps = llm_res.get("steps", [])

        if not pw_benefits:
            pw_benefits = serper_tool.search_scheme_benefits(target_scheme_query)
        if not pw_eligibility:
            pw_eligibility = serper_tool.search_scheme_eligibility(target_scheme_query)

        if kb_match:
            scheme_title = kb_match["name"]
            benefits = pw_benefits if pw_benefits else kb_match["benefits"]
            docs = pw_docs if pw_docs else kb_match["docs"]
            steps = pw_steps if pw_steps else kb_match["steps"]
            exact_eligibility_text = pw_eligibility if pw_eligibility else kb_match.get("eligibility", "Verified myScheme eligibility criteria.")
            citations = [{
                "type": "Government Portal (myScheme)",
                "title": f"{kb_match['name']} - myScheme",
                "url": clean_url(kb_match["portal"])
            }]
        elif clean_scheme:
            scheme_title = clean_scheme
            benefits = pw_benefits if pw_benefits else GENERAL_BENEFITS
            docs = pw_docs if pw_docs else GENERAL_DOCS
            steps = pw_steps if pw_steps else GENERAL_STEPS
            exact_eligibility_text = pw_eligibility if pw_eligibility else "Retrieved directly from official myScheme portal policy text."
            
            citations = []
            if mode == "web_search" and state.web_search_results:
                scheme_results = [r for r in state.web_search_results if "/schemes/" in r.get("link", "")]
                target_result = scheme_results[0] if scheme_results else state.web_search_results[0]
                
                raw_url = target_result.get("link", "https://www.myscheme.gov.in")
                target_url = clean_url(raw_url)
                title = target_result.get("title", f"{clean_scheme} - myScheme")
                if "Enter scheme name" in title:
                    title = f"{clean_scheme} - myScheme"

                citations = [{
                    "type": "Government Portal (myScheme)",
                    "title": title,
                    "url": target_url
                }]
            else:
                citations = [{
                    "type": "Government Portal (myScheme)",
                    "title": f"{clean_scheme} - myScheme",
                    "url": "https://www.myscheme.gov.in"
                }]
        else:
            default_kb = SCHEME_KNOWLEDGE_BASE["krishak_durghatna"] if (profile.occupation and "farm" in profile.occupation.lower()) else SCHEME_KNOWLEDGE_BASE["pm_kisan"]
            scheme_title = default_kb["name"]
            benefits = pw_benefits if pw_benefits else default_kb["benefits"]
            docs = pw_docs if pw_docs else default_kb["docs"]
            steps = pw_steps if pw_steps else default_kb["steps"]
            exact_eligibility_text = pw_eligibility if pw_eligibility else default_kb.get("eligibility", "Verified myScheme eligibility criteria.")
            citations = [{
                "type": "Government Portal (myScheme)",
                "title": f"{default_kb['name']} - myScheme",
                "url": clean_url(default_kb["portal"])
            }]

        # ── Check if query is for a specific scheme inspection vs initial discovery ──
        query_low = (state.user_query or "").lower()
        is_specific_scheme_request = "tell me full details about" in query_low or "full details" in query_low or "how to apply for" in query_low
        
        scheme_cards = [] if is_specific_scheme_request else generate_scheme_cards(state)

        # ── Formulate Summary Message ──
        matched_items = evaluation.get("matched_criteria", ["Demographic profile alignment"])
        verify_items = evaluation.get("unmatched_criteria", [])

        if scheme_cards:
            # 1. INITIAL DISCOVERY MODE (6 Carousel Cards): General introduction, NO single scheme evaluation
            profile_desc_parts = []
            if profile.age: profile_desc_parts.append(f"{profile.age}-year-old")
            if profile.occupation: profile_desc_parts.append(profile.occupation.capitalize())
            if profile.state: profile_desc_parts.append(f"in {profile.state.title()}")
            profile_str = " ".join(profile_desc_parts) if profile_desc_parts else "your demographic profile"

            summary = (
                f"Welcome! Based on **{profile_str}**, I have matched **{len(scheme_cards)} top government schemes** you may qualify for.\n\n"
                f"👇 **Click on any scheme card below** to check its full eligibility criteria, benefits, documents required, and application steps!"
            )
        else:
            # 2. SPECIFIC SCHEME INSPECTION MODE: Single scheme criteria breakdown & evaluation
            matched_points = "\n".join([f"  • {item}" for item in matched_items])
            if not is_eligible or match_score == 0:
                disqual_points = "\n".join([f"  • {item}" for item in verify_items])
                summary = (
                    f"⚠️ **Ineligibility Notice**: Based on your profile details, you do not currently qualify for **{scheme_title}**.\n\n"
                    f"❌ **Disqualification Reasons**:\n{disqual_points}\n\n"
                    f"✅ **Criteria You Currently Hold**:\n{matched_points}\n\n"
                    f"💡 Please check the recommended schemes in the carousel for options you fully qualify for!"
                )
            elif verify_items:
                verify_points = "\n".join([f"  • {item}" for item in verify_items])
                verify_short = ", ".join(verify_items)
                summary = (
                    f"Good news! Based on the details provided, you match the primary requirements for **{scheme_title}**.\n\n"
                    f"✅ **Criteria You Currently Hold**:\n{matched_points}\n\n"
                    f"⚠️ **Criteria We Need to Check**:\n{verify_points}\n\n"
                    f"👇 **Please share your details for ({verify_short})**, and I will confirm whether you qualify or not!"
                )
            else:
                summary = (
                    f"Great news! Based on your profile, you hold full eligibility for **{scheme_title}**.\n\n"
                    f"✅ **Criteria You Currently Hold**:\n{matched_points}\n\n"
                    f"✓ **Disqualifiers Check**: No disqualifiers found.\n\n"
                    f"👇 If you'd like me to double-check any specific condition (like your exact landholding size or income certificate limit), please share your details below and I will verify it for you!"
                )

        print(f"\n================ [EXACT SCHEME ELIGIBILITY EXTRACTED] ================")
        print(f"Scheme: {scheme_title}")
        print(f"Exact Requirement: {exact_eligibility_text}")
        print(f"========================================================================\n")

        print(f"\n================ [SCHEME BENEFITS EXTRACTED] ================")
        print(f"Scheme: {scheme_title}")
        for b in benefits:
            print(f"  * {b}")
        print(f"===========================================================\n")

        guidance = {
            "summary": summary,
            "top_scheme": scheme_title,
            "match_score": match_score,
            "is_eligible": is_eligible,
            "matched_criteria": matched_items,
            "unmatched_criteria": verify_items if verify_items else [],
            "benefits": benefits,
            "document_checklist": docs,
            "application_steps": steps,
            "citations": citations,
            "retrieval_mode": mode,
            "scheme_cards": scheme_cards,
        }

        state.guidance_response = guidance
        state.final_output = guidance
        return state

counselor_agent = CounselorGuidanceAgent()
