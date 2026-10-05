import re
from typing import List, Dict, Any, Optional
from src.agents.state import AgentState, UserProfile

# Known government scheme names — used to detect actual scheme references in follow-ups
KNOWN_SCHEMES = [
    "PM Kisan Samman Nidhi", "Pradhan Mantri Kisan Samman Nidhi",
    "Pradhan Mantri Fasal Bima Yojana", "PMFBY",
    "Kisan Credit Card", "KCC",
    "PM Kisan MaanDhan Yojana", "PMKMY",
    "Soil Health Card Scheme",
    "Pradhan Mantri Krishi Sinchayee Yojana", "PMKSY",
    "National Food Security Mission",
    "Rashtriya Krishi Vikas Yojana", "RKVY",
    "eNAM", "National Agriculture Market",
    "Paramparagat Krishi Vikas Yojana", "PKVY",
    "Ayushman Bharat", "PMJAY",
    "PM Jan Dhan Yojana", "PMJDY",
    "PM Awas Yojana", "PMAY",
    "PM SVANidhi", "Street Vendor Loan",
    "NSAP", "National Social Assistance Programme",
    "Post Matric Scholarship",
    "PM Scholarship Scheme",
    "Sukanya Samriddhi Yojana",
    "Atal Pension Yojana",
    "PM Jeevan Jyoti Bima Yojana",
    "PM Suraksha Bima Yojana",
]

# Intent detection patterns
LIST_PATTERNS = [
    r'\blist\b', r'\ball\b.*\bscheme', r'\bscheme.*\ball\b',
    r'\bone.by.one\b', r'\bek.ek\b', r'\bsaari\b', r'\bsari\b',
    r'\bkaun\s+si\b', r'\bkya\s+kya\b', r'\bgi\s+naa\b',
    r'\benumerate\b', r'\bname\s+all\b', r'\btell.*all\b',
    r'\bbatao\b.*\bsab\b', r'\bsab\b.*\bscheme\b', r'\bsaari\s+yojana\b',
    r'\byojana.+list\b', r'\blist.+yojana\b',
]
APPLY_PATTERNS = [
    r'\bapply\b', r'\bapplication\b', r'\bapply\s+kaise\b',
    r'\bkaise\s+apply\b', r'\bkaise\s+karen\b', r'\bstep\b',
    r'\bprocedure\b', r'\bprocess\b', r'\bregistration\b',
    r'\bhow\s+to\b', r'\bkaise\b.*\bkaren\b',
]
FOLLOWUP_PATTERNS = [
    r'\byou\s+told\b', r'\bprevious\b', r'\bwhat\s+was\b',
    r'\bwhat\s+scheme\b', r'\bkonsi\s+scheme\b', r'\bwoh\s+scheme\b',
    r'\baapne\s+batai\b', r'\baapne\s+kaha\b',
    r'\btell\s+me\s+more\b', r'\bmore\s+detail\b', r'\bour\s+batao\b',
]


def detect_intent(query: str) -> str:
    q = query.lower()
    for p in LIST_PATTERNS:
        if re.search(p, q):
            return "list_schemes"
    for p in APPLY_PATTERNS:
        if re.search(p, q):
            return "apply_info"
    for p in FOLLOWUP_PATTERNS:
        if re.search(p, q):
            return "followup"
    return "scheme_query"


def extract_profile_from_history(history) -> Dict[str, Any]:
    """Walk through conversation history to accumulate known profile fields."""
    merged = {}
    for turn in history:
        snap = turn.profile_snapshot or {}
        for field in ("age", "income", "occupation", "state", "category", "gender"):
            if snap.get(field) is not None:
                merged[field] = snap[field]
    return merged


class ProfileExtractionAgent:
    """
    Day 7 & 8: Profile Extraction & Clarification Agent.
    Extracts demographic attributes from the current query AND conversation history.
    Detects query intent: scheme_query | list_schemes | apply_info | followup.
    """

    def _extract_from_text(self, text: str, profile: UserProfile) -> UserProfile:
        q = text.lower()

        # Age
        age_match = re.search(r'\b(\d{1,2})\s*(?:years?|yrs?|year\s+old|years\s+old|age|aged|varsh|वर्ष|साल)\b', q)
        if age_match:
            profile.age = int(age_match.group(1))

        # Income — handles ₹80,000, Rs 80000, 1.5 lakh, 80k, income of 80000
        income_match = re.search(r'(?:income\s*(?:of|is)?\s*)?[\₹rs.\s]*(\d[\d,]{3,9})\b', q)
        if income_match and len(income_match.group(1).replace(',', '')) >= 4:
            val_str = income_match.group(1).replace(',', '')
            profile.income = int(float(val_str))
        else:
            unit_match = re.search(r'(\d+(?:\.\d+)?)\s*(lakh|lac|k|thousand)\b', q)
            if unit_match:
                val = float(unit_match.group(1))
                unit = unit_match.group(2)
                if unit in ['lakh', 'lac']:
                    profile.income = int(val * 100000)
                elif unit in ['k', 'thousand']:
                    profile.income = int(val * 1000)

        # Occupation
        occupations = [
            "farmer", "kisan", "किसान", "student", "street vendor",
            "artisan", "unorganized worker", "trader", "senior citizen",
            "widow", "disabled", "craftsman", "labour", "laborer",
        ]
        occ_map = {"kisan": "Farmer", "किसान": "Farmer", "farmer": "Farmer"}
        for occ in occupations:
            if occ in q:
                profile.occupation = occ_map.get(occ, occ.title())
                break

        # Category
        for cat in ["sc", "st", "obc", "ews", "general"]:
            if re.search(rf'\b{cat}\b', q):
                profile.category = cat.upper()
                break

        # Gender
        if any(w in q for w in ["woman", "female", "girl", "mother", "widow", "mahila", "महिला"]):
            profile.gender = "Female"
        elif any(w in q for w in ["man", "male", "boy"]):
            profile.gender = "Male"

        # State
        state_map = {
            "uttar pradesh": "Uttar Pradesh", "up": "Uttar Pradesh",
            "madhya pradesh": "Madhya Pradesh", "mp": "Madhya Pradesh",
            "west bengal": "West Bengal", "wb": "West Bengal",
            "odisha": "Odisha", "maharashtra": "Maharashtra",
            "telangana": "Telangana", "rajasthan": "Rajasthan",
            "delhi": "Delhi", "bihar": "Bihar", "punjab": "Punjab",
            "tamil nadu": "Tamil Nadu", "karnataka": "Karnataka",
            "haryana": "Haryana", "gujarat": "Gujarat",
            "andhra pradesh": "Andhra Pradesh",
        }
        for state_key, state_val in state_map.items():
            if re.search(rf'\b{re.escape(state_key)}\b', q):
                profile.state = state_val
                break

        return profile

    def process(self, state: AgentState) -> AgentState:
        query = state.user_query
        profile = UserProfile()

        # 1. Seed profile from conversation history (both snapshots and turn texts)
        if state.conversation_history:
            merged = extract_profile_from_history(state.conversation_history)
            for field, val in merged.items():
                if val is not None:
                    setattr(profile, field, val)

            # Scan text content of all previous user turns in history
            for turn in state.conversation_history:
                if turn.role == 'user' and turn.content:
                    profile = self._extract_from_text(turn.content, profile)

        # 2. Overlay with what we can extract from the current query
        profile = self._extract_from_text(query, profile)

        # 3. Detect intent
        state.intent = detect_intent(query)
        print(f"[PROFILE AGENT] Intent detected: {state.intent}")
        print(f"[PROFILE AGENT] Profile: age={profile.age}, occupation={profile.occupation}, income={profile.income}, state={profile.state}")

        # 4. For follow-ups and list/apply intents, do NOT ask for clarification
        #    (we already have context from history)
        if state.intent in ("list_schemes", "apply_info", "followup"):
            profile.is_complete = True
            profile.missing_fields = []
            state.clarification_needed = False
            state.user_profile = profile
            return state

        # 5. Clarification only for pure scheme_query with no profile at all
        missing = []
        if not profile.occupation and not profile.age and not profile.income:
            missing.append("profile")
        profile.missing_fields = missing
        profile.is_complete = len(missing) == 0

        state.user_profile = profile

        if not profile.is_complete:
            state.clarification_needed = True
            state.clarification_prompt = (
                "To find the most relevant government schemes for you, could you share: "
                "your age, occupation (e.g. farmer, student, worker), "
                "approximate annual income, and the state you live in?"
            )
        else:
            state.clarification_needed = False

        return state


profile_agent = ProfileExtractionAgent()
