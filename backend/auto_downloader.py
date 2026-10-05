import os
import json
from fpdf import FPDF

# Directory setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "raw_pdfs")
JSON_OUTPUT = os.path.join(BASE_DIR, "data", "all_schemes.json")
os.makedirs(OUTPUT_DIR, exist_ok=True)

class SchemePDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 11)
        self.cell(0, 10, 'Government of India / State Welfare Scheme - Official Information', 0, new_x="LMARGIN", new_y="NEXT", align='C')
        self.ln(3)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, new_x="RIGHT", new_y="TOP", align='C')

def text_to_pdf(filename, title, category, type_loc, details):
    """Converts scheme details into a formatted PDF file."""
    pdf = SchemePDF()
    pdf.add_page()
    
    # Title
    pdf.set_font("Helvetica", 'B', 13)
    pdf.multi_cell(0, 7, title.encode('latin-1', 'replace').decode('latin-1'))
    pdf.ln(2)
    
    # Category Tag
    pdf.set_font("Helvetica", 'I', 9)
    pdf.multi_cell(0, 5, f"Category: {category} | Type: {type_loc}".encode('latin-1', 'replace').decode('latin-1'))
    pdf.ln(3)
    
    # Body Content
    pdf.set_font("Helvetica", size=9)
    pdf.multi_cell(0, 5, details.encode('latin-1', 'replace').decode('latin-1'))
    
    filepath = os.path.join(OUTPUT_DIR, filename)
    pdf.output(filepath)

def generate_100_schemes():
    print("Starting 100 Master Government Scheme PDF & Dataset Generator...")
    
    schemes = []

    # --- 1. Agriculture & Farmers (10) ---
    agri = [
        ("pm_kisan", "PM Kisan Samman Nidhi", "Income support of Rs. 6,000/year to landholding farmers in 3 installments.", "All landholding farmer families.", "Institutional landholders, taxpayers, MPs/MLAs.", "Aadhaar, Land Records, Bank Account."),
        ("pm_fasal_bima", "Pradhan Mantri Fasal Bima Yojana (PMFBY)", "Comprehensive crop insurance against natural risks from pre-sowing to post-harvest.", "All farmers including sharecroppers & tenant farmers.", "Non-notified crops.", "Land record, Bank passbook, Sowing certificate."),
        ("pm_kisan_maan_dhan", "PM Kisan Maan-Dhan Yojana (PM-KMY)", "Assured monthly pension of Rs. 3,000 for small and marginal farmers.", "Small and marginal farmers aged 18-40 years with <= 2 hectares land.", "Income tax payers, NPS/EPFO members.", "Aadhaar, Bank Account."),
        ("kisan_credit_card", "Kisan Credit Card (KCC) Scheme", "Concessional credit to farmers for agricultural & allied activity expenses.", "Farmers, individual/joint borrowers, SHGs, tenant farmers.", "Defaulters to bank credit.", "Aadhaar, PAN Card, Land ownership proof."),
        ("soil_health_card", "Soil Health Card Scheme", "Promotes soil test-based nutrient management for sustainable agriculture.", "All farmers across India.", "None.", "Land details, Aadhaar Card."),
        ("pm_ksy_irrigation", "Pradhan Mantri Krishi Sinchayee Yojana (PMKSY)", "Expands cultivable area under assured irrigation (Har Khet Ko Pani).", "Farmers with agricultural land.", "Non-agricultural land.", "Land documents, Aadhaar, Bank Details."),
        ("paramparagat_krishi", "Paramparagat Krishi Vikas Yojana (PKVY)", "Promotes organic farming through cluster approach and Participatory Guarantee System.", "Farmers forming clusters of 50 or more.", "Chemical farming clusters.", "Aadhaar, Land Certificate, Bank Account."),
        ("agri_infrastructure_fund", "Agriculture Infrastructure Fund (AIF)", "Medium-long term debt financing for post-harvest management infrastructure.", "Primary Agricultural Credit Societies, Agri-entrepreneurs, SHGs.", "Non-agri activities.", "Project report, Bank Account, Aadhaar."),
        ("national_beekeeping_mission", "National Beekeeping & Honey Mission (NBHM)", "Promotes holistic development of beekeeping for sweet revolution.", "Individual beekeepers, SHGs, Cooperatives.", "Unregistered entities.", "Aadhaar, Beekeeper registration proof."),
        ("sub_mission_agri_mechanization", "Sub-Mission on Agricultural Mechanization (SMAM)", "Provides subsidies for purchasing farm machinery and establishing custom hiring centers.", "Small, marginal, SC/ST, and women farmers.", "Commercial non-farming entities.", "Aadhaar, Land Document, Machinery Quotation.")
    ]
    for s in agri:
        schemes.append({"id": s[0], "category": "Agriculture & Farmers", "type": "Central Sector", "title": s[1], "obj": s[2], "elig": s[3], "excl": s[4], "docs": s[5]})

    # --- 2. Healthcare & Wellness (10) ---
    health = [
        ("ayushman_bharat_pmjay", "Ayushman Bharat PM-JAY", "Free health cover up to Rs. 5 Lakh/family/year for secondary & tertiary hospitalization.", "Families listed in SECC 2011 & all senior citizens aged 70+.", "High-income categories.", "Aadhaar Card, Ration Card."),
        ("pm_janaushadhi", "PM Bhartiya Janaushadhi Pariyojana (PMBJP)", "Provides quality generic medicines at 50%-90% lower prices.", "Open to all Indian citizens.", "None.", "Doctor Prescription."),
        ("national_health_mission", "National Health Mission (NHM)", "Provides universal access to equitable, affordable & quality healthcare services.", "Rural & urban vulnerable populations.", "None.", "Aadhaar, Health Card."),
        ("rashtriya_vayoshri", "Rashtriya Vayoshri Yojana", "Free physical aids and assisted-living devices for low-income senior citizens.", "Senior citizens aged 60+ belonging to BPL category.", "Non-BPL senior citizens.", "BPL Card, Age Proof, Aadhaar."),
        ("pm_abhim_infrastructure", "PM Ayushman Bharat Health Infrastructure Mission (PM-ABHIM)", "Strengthens urban & rural health infrastructure to prepare for future pandemics.", "Public health centers & general citizens.", "None.", "Not applicable (Institutional)."),
        ("national_tb_elimination", "Nikshay Poshan Yojana (TB Patients)", "Financial support of Rs. 500/month for nutritional needs of TB patients.", "All notified TB patients undergoing treatment.", "Non-notified private unrecorded cases.", "Nikshay ID, Aadhaar, Bank Account."),
        ("janani_suraksha_yojana", "Janani Suraksha Yojana (JSY)", "Promotes institutional delivery among pregnant women with cash assistance.", "Pregnant women from BPL/SC/ST families.", "Non-BPL in high performing states.", "BPL Card, Aadhaar, Bank Account."),
        ("janani_shishu_suraksha", "Janani Shishu Suraksha Karyakram (JSSK)", "Free medical treatment, transport, and diet for sick newborns & mothers.", "Pregnant women and sick infants accessing public health facilities.", "Private hospitals.", "Aadhaar, Hospital Registration."),
        ("pm_poshan_abhiyaan", "POSHAN Abhiyaan (National Nutrition Mission)", "Reduces stunting, under-nutrition, anemia among young children & women.", "Children (0-6 years), pregnant women, lactating mothers.", "None.", "Aadhaar, Anganwadi Registration."),
        ("tele_manas_mental_health", "Tele-MANAS (Mental Health Assistance)", "Free 24/7 tele-mental health services across India.", "All Indian citizens.", "None.", "None (Dial 14416).")
    ]
    for s in health:
        schemes.append({"id": s[0], "category": "Healthcare & Wellness", "type": "Central Sector", "title": s[1], "obj": s[2], "elig": s[3], "excl": s[4], "docs": s[5]})

    # --- 3. Housing & Infrastructure (10) ---
    housing = [
        ("pmay_urban", "PM Awas Yojana - Urban (PMAY-U 2.0)", "Financial assistance for urban households to build or purchase pucca houses.", "EWS (Income <= 3L), LIG (3-6L), MIG (6-18L) owning no pucca house.", "Property owners.", "Aadhaar, Income Proof, Bank Details."),
        ("pmay_gramin", "PM Awas Yojana - Gramin (PMAY-G)", "Assistance of Rs. 1.2-1.3 Lakh for rural homeless households to build pucca houses.", "Rural households identified in SECC 2011 list.", "Kutcha house non-listed.", "Job Card, Aadhaar, Bank Details."),
        ("pm_svanidhi", "PM Street Vendor's AtmaNirbhar Nidhi (PM SVANidhi)", "Collateral-free working capital loans of Rs. 10k, 20k, 50k for street vendors.", "Street vendors with Certificate of Vending.", "Non-vendors.", "Vending ID, Aadhaar Card."),
        ("jal_jeevan_mission", "Jal Jeevan Mission (Har Ghar Jal)", "Provides functional household tap connection to every rural home.", "Rural households across all states.", "Urban commercial.", "Aadhaar, Address Proof."),
        ("pm_gram_sadak", "PM Gram Sadak Yojana (PMGSY)", "Provides all-weather road connectivity to eligible unconnected rural habitations.", "Rural habitations with population 500+ (250+ in hills).", "Already connected habitations.", "N/A (Infrastructure)."),
        ("swachh_bharat_urban", "Swachh Bharat Mission - Urban 2.0", "Financial assistance of Rs. 12,000 for constructing Individual Household Latrines.", "Urban households with no toilet facility.", "Commercial buildings.", "Aadhaar, Bank Account, Photo."),
        ("swachh_bharat_gramin", "Swachh Bharat Mission - Gramin", "Incentive of Rs. 12,000 for BPL/identified APL rural households to build toilets.", "BPL rural households, SC/ST, small farmers.", "High-income households.", "Aadhaar, Bank Account."),
        ("amrut_mission", "AMRUT 2.0 (Urban Rejuvenation)", "Provides universal coverage of water supply & sewage treatment in 500 cities.", "Urban citizens in selected AMRUT cities.", "Rural areas.", "N/A (Infrastructure)."),
        ("smart_cities_mission", "Smart Cities Mission", "Promotes core infrastructure and clean environment in 100 selected cities.", "Residents of selected smart cities.", "Non-selected cities.", "N/A (Urban development)."),
        ("pm_gati_shakti", "PM GatiShakti National Master Plan", "Multimodal connectivity infrastructure platform coordinating railway, road, port projects.", "Infrastructure logistics providers & citizens.", "None.", "N/A (National Infrastructure).")
    ]
    for s in housing:
        schemes.append({"id": s[0], "category": "Housing & Infrastructure", "type": "Central Sector", "title": s[1], "obj": s[2], "elig": s[3], "excl": s[4], "docs": s[5]})

    # --- 4. Education & Scholarships (10) ---
    edu = [
        ("post_matric_scholarship_sc", "Post-Matric Scholarship for SC/ST Students", "Tuition waiver and maintenance allowance for SC/ST post-secondary education.", "SC/ST students with family income <= Rs. 2.5 Lakh/year.", "Income > 2.5 Lakh.", "Caste Certificate, Income Certificate, Marksheet."),
        ("post_matric_scholarship_obc", "Post-Matric Scholarship for OBC Students", "Financial support for OBC students pursuing post-matriculation studies.", "OBC students with family income <= Rs. 1.5 Lakh/year.", "Income > 1.5 Lakh.", "OBC Certificate, Income Proof, Marksheet."),
        ("pm_vidya_lakshmi", "PM Vidya Lakshmi Education Loan Scheme", "Single window education loan portal with interest subsidies for higher education.", "Indian students securing admission to recognized courses.", "Unrecognized private diplomas.", "Admission letter, Fee structure, Marksheet."),
        ("nmms_scholarship", "National Means-cum-Merit Scholarship (NMMSS)", "Rs. 12,000/year scholarship for class 9-12 students to prevent dropouts.", "Class 8 students (55%+ marks) with family income <= 3.5 Lakh.", "KVS/NVS school students.", "Class 8 Marksheet, Income Certificate."),
        ("central_sector_scholarship", "Central Sector Scheme of Scholarship (CSSS)", "Scholarship for top 20th percentile college students from low-income families.", "Class 12 pass students with family income <= 4.5 Lakh.", "Students receiving other central scholarships.", "Class 12 Marksheet, Income Certificate, Aadhaar."),
        ("pm_research_fellowship", "PM Research Fellowship (PMRF)", "Attracts top talent to Ph.D. programs at IITs/IISc with Rs. 70,000-80,000 monthly stipend.", "B.Tech/M.Sc graduates from IITs/NITs with high CGPA/GATE score.", "Low CGPA candidates.", "Degree certificate, GATE score, Research Proposal."),
        ("pragati_scholarship_girls", "AICTE Pragati Scholarship for Girl Students", "Rs. 50,000/year for girls pursuing technical degree/diploma education.", "Girl students admitted to AICTE approved technical courses (Income <= 8 Lakh).", "Income > 8 Lakh.", "Admission Proof, Income Certificate, Aadhaar."),
        ("saksham_scholarship_disabled", "AICTE Saksham Scholarship for Disabled Students", "Rs. 50,000/year for specially-abled students pursuing technical education.", "Differently-abled students (disability >= 40%) with income <= 8 Lakh.", "Disability < 40%.", "Disability Certificate, Admission Proof."),
        ("ishan_uday_north_east", "Ishan Uday Scholarship for North Eastern Region", "Rs. 5,400 to 7,800/month for general/degree/professional students of NER.", "Students domiciled in NER states with family income <= 4.5 Lakh.", "Non-NER domicile.", "Domicile Certificate, Income Certificate."),
        ("pm_poshan_mid_day_meal", "PM POSHAN (Mid-Day Meal Scheme)", "Provides hot cooked meals to elementary school children (Class 1 to 8).", "Students enrolled in Government and Government-aided schools.", "Private un-aided schools.", "School Enrollment.")
    ]
    for s in edu:
        schemes.append({"id": s[0], "category": "Education & Scholarships", "type": "Central Sector", "title": s[1], "obj": s[2], "elig": s[3], "excl": s[4], "docs": s[5]})

    # --- 5. Women & Child Welfare (10) ---
    women = [
        ("sukanya_samriddhi", "Sukanya Samriddhi Yojana (SSY)", "Tax-free savings scheme for girl child education & marriage.", "Girl child aged up to 10 years, opened by natural/legal guardian.", "Age > 10 years.", "Birth Certificate, Guardian ID."),
        ("pm_matru_vandana", "PM Matru Vandana Yojana (PMMVY)", "Cash incentive of Rs. 5,000 for 1st child & Rs. 6,000 for 2nd girl child to pregnant mothers.", "Pregnant & Lactating Mothers meeting social criteria.", "Regular government employees.", "MCP Card, Aadhaar, Bank Passbook."),
        ("lakhpati_didi", "Lakhpati Didi Scheme", "Empowers rural Self-Help Group (SHG) women to earn >= Rs. 1 Lakh/year.", "Women members of DAY-NRLM Self Help Groups.", "Non-SHG members.", "SHG ID, Aadhaar, Bank Details."),
        ("beti_bachao_beti_padhao", "Beti Bachao Beti Padhao (BBBP)", "Addresses declining Child Sex Ratio and promotes education of girl child.", "Girl children across all districts.", "None.", "Birth Certificate, Aadhaar."),
        ("working_women_hostel", "Sakhi Niwas (Working Women Hostel)", "Safe and affordable hostel accommodation for working women.", "Single, widowed, divorced working women with income <= 50,000/month.", "High-income corporate executives.", "Employment Certificate, Income Proof."),
        ("one_stop_centre_sakhi", "One Stop Centre (Sakhi)", "Provides integrated support and assistance to women affected by violence.", "Women facing physical, sexual, emotional, or economic abuse.", "None.", "Identity Proof, Complaint details."),
        ("mahila_samman_savings", "Mahila Samman Savings Certificate (MSSC)", "Small savings scheme for women offering 7.5% fixed interest for 2 years.", "Any woman or guardian on behalf of a minor girl.", "Male applicants.", "Aadhaar, PAN Card, Deposit Amount."),
        ("poshan_vaticana", "Poshan 2.0 Anganwadi Services", "Provides supplementary nutrition, pre-school non-formal education to children & mothers.", "Children (6 months - 6 yrs), pregnant & lactating women.", "None.", "Anganwadi Registration, Aadhaar."),
        ("mission_vatsalya", "Mission Vatsalya (Child Protection)", "Assistance for children in difficult circumstances, institutional and non-institutional care.", "Orphaned, abandoned, or vulnerable children.", "None.", "Child ID, CWC order."),
        ("free_silai_machine", "PM Free Sewing Machine Scheme (States)", "Free sewing machines to poor women to start home-based tailoring business.", "Rural & urban poor women aged 20-40 years with family income <= 1.2 Lakh.", "Income > 1.2 Lakh.", "Income Certificate, Aadhaar, Photo.")
    ]
    for s in women:
        schemes.append({"id": s[0], "category": "Women & Child Welfare", "type": "Central & State", "title": s[1], "obj": s[2], "elig": s[3], "excl": s[4], "docs": s[5]})

    # --- 6. Social Security & Pensions (10) ---
    pension = [
        ("atal_pension_yojana", "Atal Pension Yojana (APY)", "Guaranteed monthly pension of Rs. 1,000 to 5,000 for unorganized workers.", "Citizens aged 18-40 having a bank account. Must not pay income tax.", "Taxpayers.", "Aadhaar, Bank Account."),
        ("nsap_old_age_pension", "Indira Gandhi National Old Age Pension (IGNOAPS)", "Monthly pension for BPL elderly citizens (60+ years).", "BPL citizens aged 60 and above.", "Non-BPL households.", "BPL Card, Age Proof, Bank Account."),
        ("nsap_widow_pension", "Indira Gandhi National Widow Pension (IGNWPS)", "Monthly pension of Rs. 300-500 for destitute widows.", "BPL widows aged 40-79 years.", "Remarried widows / Non-BPL.", "BPL Card, Death Certificate of Husband, Aadhaar."),
        ("nsap_disability_pension", "Indira Gandhi National Disability Pension (IGNDPS)", "Monthly pension support for severely disabled BPL individuals.", "BPL persons aged 18-79 with severe disability (80%+).", "Disability < 80%.", "Disability Certificate, BPL Card, Aadhaar."),
        ("pm_shram_yogi_mandhan", "PM Shram Yogi Maan-dhan (PM-SYM)", "Monthly pension of Rs. 3,000 for unorganized workers (monthly income <= 15,000).", "Unorganized workers aged 18-40 years.", "EPFO/NPS/ESIC members.", "Aadhaar, Savings Bank Account."),
        ("pm_laghu_vyapari_pension", "National Pension Scheme for Traders (NPS-Traders)", "Pension of Rs. 3,000/month for small shopkeepers & retail traders.", "Retail traders & shopkeepers (GST turnover <= 1.5 Crore) aged 18-40.", "Income tax payers.", "GSTIN, Aadhaar, Bank Account."),
        ("e_shram_card", "e-SHRAM Portal Registration", "National database of unorganized workers providing accidental insurance cover of Rs. 2 Lakh.", "Unorganized workers aged 16-59 years.", "Income tax payers, EPFO/ESIC.", "Aadhaar, Mobile linked with Aadhaar, Bank Account."),
        ("pm_suraksha_bima", "Pradhan Mantri Suraksha Bima Yojana (PMSBY)", "Accidental death and disability insurance cover of Rs. 2 Lakh for Rs. 20/year.", "Bank account holders aged 18 to 70 years.", "Age > 70.", "Aadhaar, Bank Account."),
        ("pm_jeevan_jyoti_bima", "Pradhan Mantri Jeevan Jyoti Bima Yojana (PMJJBY)", "Life insurance cover of Rs. 2 Lakh for any cause of death at Rs. 436/year.", "Bank account holders aged 18 to 50 years.", "Age > 50.", "Aadhaar, Bank Account."),
        ("varishtha_pension_bima", "Pradhan Mantri Vaya Vandana Yojana (PMVVY)", "Pension scheme for senior citizens offering guaranteed 7.4%+ annual return.", "Senior citizens aged 60 years and above.", "Age < 60.", "Aadhaar, PAN Card, Deposit Amount.")
    ]
    for s in pension:
        schemes.append({"id": s[0], "category": "Social Security & Pensions", "type": "Central Sector", "title": s[1], "obj": s[2], "elig": s[3], "excl": s[4], "docs": s[5]})

    # --- 7. Entrepreneurship & MSME Loans (10) ---
    msme = [
        ("pm_mudra_yojana", "PM MUDRA Yojana (PMMY)", "Collateral-free micro loans up to Rs. 10 Lakh (Shishu, Kishor, Tarun).", "Non-farm micro entrepreneurs, small shopkeepers, traders.", "Defaulters.", "Identity Proof, Business Proposal."),
        ("stand_up_india", "Stand Up India Scheme", "Bank loans between Rs. 10 Lakh to Rs. 1 Crore for SC/ST and Women entrepreneurs.", "SC/ST and/or Woman entrepreneurs setting up greenfield enterprises.", "Existing businesses.", "Caste Proof, PAN, Business Plan."),
        ("pm_vishwakarma", "PM Vishwakarma Scheme", "Toolkit incentive of Rs. 15,000 and loans up to Rs. 3 Lakh at 5% interest for artisans.", "Artisans in 18 traditional trades (carpenters, potters, blacksmiths, etc.).", "Non-traditional trades.", "Aadhaar, Skill verification."),
        ("pm_egp_employment", "PM Employment Generation Programme (PMEGP)", "Credit-linked subsidy up to 35% for setting up new micro-enterprises.", "Individuals above 18 years; minimum 8th pass for manufacturing > 10L.", "Existing units.", "Project Report, Aadhaar, Caste Certificate."),
        ("credit_guarantee_fund", "CGTMSE (Credit Guarantee Scheme for Micro/Small Enterprises)", "Collateral-free credit facility up to Rs. 5 Crore for MSMEs.", "New and existing Micro and Small Enterprises.", "Retail trade beyond limits.", "MSME Udyam Registration, Loan Application."),
        ("udyam_registration", "Udyam MSME Registration Portal", "Free official registration providing government tender priority & interest subsidies.", "All Micro, Small, and Medium Enterprises.", "Unregistered trading entities.", "Aadhaar, PAN Card, GSTIN."),
        ("ramprasad_bismil_scheme", "PM MSME Champions Scheme (ZED & Lean)", "Financial assistance for Zero Defect Zero Effect (ZED) quality certification.", "Registered MSMEs.", "Non-MSMEs.", "Udyam Registration."),
        ("pm_formalisation_food", "PM Formalisation of Micro Food Processing (PMFME)", "35% subsidy (max Rs. 10 Lakh) for micro food processing enterprises.", "Individual micro food processors, FPOs, SHGs.", "Large food processing industries.", "Udyam, Aadhaar, Project Report."),
        ("scheme_fund_regeneration", "SFURTI (Scheme of Fund for Regeneration of Traditional Industries)", "Organizes traditional artisans into clusters to make them competitive.", "NGOs, SHGs, Field Institutions.", "Individual applicants.", "Cluster proposal."),
        ("startup_india_seed_fund", "Startup India Seed Fund Scheme (SISFS)", "Financial assistance up to Rs. 50 Lakh to early-stage startups for proof of concept.", "DPIIT recognized startups incorporated <= 2 years.", "Non-DPIIT registered entities.", "DPIIT Recognition Certificate, Pitch Deck.")
    ]
    for s in msme:
        schemes.append({"id": s[0], "category": "Entrepreneurship & MSME", "type": "Central Sector", "title": s[1], "obj": s[2], "elig": s[3], "excl": s[4], "docs": s[5]})

    # --- 8. Employment & Skill Development (10) ---
    skill = [
        ("mgnrega", "MGNREGA Rural Employment Guarantee", "Guarantees 100 days of manual wage employment per year for rural households.", "Adult members of rural households.", "Urban residents.", "MGNREGA Job Card, Aadhaar, Bank Account."),
        ("pmkvy_skill_india", "PM Kaushal Vikas Yojana (PMKVY 4.0)", "Free industry-relevant skill training, certification, and job placement.", "Unemployed youth or school/college dropouts (aged 15-45).", "Currently employed.", "Aadhaar, Educational Marksheet."),
        ("ddu_gky_rural_skills", "Deen Dayal Upadhyaya Grameen Kaushalya Yojana (DDU-GKY)", "Placement-linked skill training for rural poor youth (aged 15-35).", "Rural youth from poor families (SC/ST/Minority priority).", "Urban youth.", "Aadhaar, BPL Proof, Education Certificate."),
        ("naps_apprenticeship", "National Apprenticeship Promotion Scheme (NAPS)", "Provides stipend support (25% up to Rs. 1,500/month) for trade apprentices.", "Youth aged 14+ having ITI / Diploma / 10th / 12th qualification.", "Non-registered candidates.", "Aadhaar, Educational Qualification."),
        ("rural_self_employment", "RSETI (Rural Self Employment Training Institutes)", "Short-term residential skill training & bank loan facilitation for rural youth.", "Rural youth aged 18-45 years.", "Urban non-poor.", "Aadhaar, BPL Ration Card."),
        ("national_career_service", "National Career Service (NCS Portal)", "Free online job matching, career counseling, and job fair platform.", "Job seekers, students, and employers across India.", "None.", "Aadhaar, Educational Profile."),
        ("skill_hub_initiative", "Skill Hub Initiative (PMKVY in Schools)", "Integrates vocational skill education in schools and higher education institutes.", "Students from Class 6 to 12 & out-of-school youth.", "None.", "School ID, Aadhaar."),
        ("green_skill_development", "Green Skill Development Programme (GSDP)", "Trains youth in environment, forestry, and sustainable sector jobs.", "Science graduates / 10th-12th dropouts.", "None.", "Marksheet, Aadhaar."),
        ("pm_vishwakarma_skill", "Vishwakarma Basic & Advanced Skill Training", "5-7 days basic skill training with Rs. 500/day stipend for traditional craftsmen.", "Artisans registered under PM Vishwakarma.", "Non-registered.", "PM Vishwakarma ID, Aadhaar."),
        ("agri_clinics_agri_business", "Agri-Clinics and Agri-Business Centres (ACABC)", "45 days free training + 36-44% composite subsidy for agri-graduates.", "Graduates in agriculture and allied subjects.", "Non-agri graduates.", "Agri Degree Certificate, Aadhaar.")
    ]
    for s in skill:
        schemes.append({"id": s[0], "category": "Employment & Skill Development", "type": "Central Sector", "title": s[1], "obj": s[2], "elig": s[3], "excl": s[4], "docs": s[5]})

    # --- 9. State Flagship Schemes (10 Major States) ---
    state_schemes = [
        ("subhadra_yojana_odisha", "Subhadra Yojana (Odisha)", "Financial assistance of Rs. 10,000 per year (total Rs. 50,000 over 5 years) to women.", "Women in Odisha aged 21 to 60 years from low-income families.", "Taxpayers, Govt employees.", "Aadhaar, Bank Passbook, Domicile."),
        ("ladli_behna_mp", "Mukhyamantri Ladli Behna Yojana (Madhya Pradesh)", "Monthly financial assistance of Rs. 1,250 transferred to women's bank accounts.", "Women domiciled in MP aged 21-60 years with family income < 2.5 Lakh.", "Taxpaying families.", "Samagra ID, Aadhaar, Bank Details."),
        ("kanya_sumangala_up", "Mukhya Mantri Kanya Sumangala Yojana (Uttar Pradesh)", "Rs. 25,000 phased financial assistance for girl child from birth to graduation.", "Girls domiciled in UP with annual family income <= 3 Lakh.", "Families with > 2 children.", "Birth Certificate, Income Proof, Domicile."),
        ("majhi_ladki_bahin_mh", "Mukhyamantri Majhi Ladki Bahin Yojana (Maharashtra)", "Monthly financial aid of Rs. 1,500 to women aged 21-65 years.", "Women domiciled in Maharashtra with family income <= 2.5 Lakh.", "Income tax payers.", "Aadhaar, Domicile Certificate, Ration Card."),
        ("lakshmir_bhandar_wb", "Lakshmir Bhandar Scheme (West Bengal)", "Monthly financial assistance of Rs. 1,000 (General) and Rs. 1,200 (SC/ST) to women.", "Female head of household aged 25-60 years domiciled in West Bengal.", "Government employees.", "Swasthyasathi Card, Aadhaar, Caste Certificate."),
        ("rythu_bandhu_telangana", "Rythu Bandhu Scheme (Telangana)", "Investment support of Rs. 10,000 per acre per year for agricultural inputs.", "Landowning farmers in Telangana state.", "Non-landowning tenant farmers.", "Pattadar Passbook, Aadhaar, Bank Details."),
        ("kalia_scheme_odisha", "KALIA Scheme (Odisha)", "Financial support of Rs. 25,000 per family for small/marginal farmers & landless agricultural laborers.", "Small, marginal farmers & landless agricultural laborers in Odisha.", "Taxpayers, MPs/MLAs.", "Aadhaar, Ration Card, Bank Account."),
        ("chiranjeevi_health_rajasthan", "Mukhyamantri Chiranjeevi Swasthya Bima (Rajasthan)", "Health insurance cover up to Rs. 25 Lakh per family per year for Rajasthan residents.", "All families domiciled in Rajasthan state.", "Non-residents.", "Jan Aadhaar Card, Ration Card."),
        ("kanyashree_prakalpa_wb", "Kanyashree Prakalpa (West Bengal)", "Annual scholarship of Rs. 1,000 and one-time grant of Rs. 25,000 to prevent child marriage.", "Unmarried girls aged 13-19 studying in recognized institutions in WB.", "Married girls under 18.", "School Certificate, Unmarried Certificate, Aadhaar."),
        ("delhi_free_bus_pink_ticket", "Delhi Pink Ticket Free Bus Scheme", "Free travel for women in all DTC and cluster city buses in Delhi.", "All female passengers traveling in Delhi city buses.", "Male passengers.", "None (Pink Ticket issued on bus).")
    ]
    for s in state_schemes:
        schemes.append({"id": s[0], "category": "State Flagship Schemes", "type": "State Government", "title": s[1], "obj": s[2], "elig": s[3], "excl": s[4], "docs": s[5]})

    # --- 10. Clean Energy, Environment & Utilities (10) ---
    energy = [
        ("pm_surya_ghar", "PM Surya Ghar: Muft Bijli Yojana", "Up to 300 units free electricity per month via rooftop solar installation with 60% subsidy.", "Households with suitable rooftop & electricity connection.", "Commercial buildings.", "Electricity Bill, Aadhaar, Bank Account."),
        ("pm_ujjwala_yojana", "Pradhan Mantri Ujjwala Yojana (PMUY 2.0)", "Deposit-free LPG gas connection + Rs. 300 subsidy per cylinder refill for poor women.", "Adult women from BPL / SC / ST / PMAY households.", "Existing LPG connection holders.", "Aadhaar, Ration Card, Bank Account."),
        ("pm_kusum_solar_pump", "PM-KUSUM (Solar Pumps for Farmers)", "60% subsidy for installing standalone solar agriculture pumps & solarizing grid pumps.", "Farmers, Panchayats, Farmer Producer Organizations (FPOs).", "Non-farmers.", "Land documents, Aadhaar, Bank Details."),
        ("national_green_hydrogen", "National Green Hydrogen Mission", "Promotes green hydrogen production, manufacturing electrolysers & clean energy transition.", "Clean energy developers, industries.", "Fossil fuel expansion.", "DPIIT registration, Project Report."),
        ("faster_adoption_ev_fame", "FAME India Phase II / PM E-Drive Scheme", "Subsidies & incentives for purchasing Electric Vehicles (2W, 3W, 4W, e-buses).", "EV buyers and charging infrastructure developers.", "ICE petrol/diesel vehicle buyers.", "Aadhaar, Vehicle Purchase Invoice."),
        ("gobardhan_scheme", "GOBARdhan Scheme (Galvanizing Organic Bio-Agro Resources)", "Converts cattle dung and organic waste into Biogas and Compressed Bio-Gas (CBG).", "Farmers, Gram Panchayats, Dairy Cooperatives.", "None.", "Land details, Panchayat resolution."),
        ("namami_gange_mission", "Namami Gange Programme", "Integrated conservation mission to clean, protect, and rejuvenate River Ganga.", "Ganga basin communities, industries, & municipal bodies.", "None.", "N/A (National Project)."),
        ("national_clean_air", "National Clean Air Programme (NCAP)", "Targeted 20-40% reduction in particulate matter (PM2.5/PM10) concentrations in 131 cities.", "Residents of non-attainment Indian cities.", "None.", "N/A (Urban Environment)."),
        ("deep_ocean_mission", "Deep Ocean Mission (Ministry of Earth Sciences)", "Exploration of deep ocean resources and oceanic climate change advisory services.", "Scientific institutions, marine researchers.", "None.", "N/A (Scientific Research)."),
        ("green_credit_programme", "Green Credit Programme (GCP)", "Market-based mechanism incentivizing voluntary environmental actions (tree planting, water conservation).", "Individuals, SHGs, Panchayats, Private Companies.", "None.", "Green Credit Portal Registration.")
    ]
    for s in energy:
        schemes.append({"id": s[0], "category": "Clean Energy & Utilities", "type": "Central Sector", "title": s[1], "obj": s[2], "elig": s[3], "excl": s[4], "docs": s[5]})

    # Process and write all 100 schemes to PDFs & JSON
    formatted_dataset = []
    for s in schemes:
        details_text = f"Objective & Overview:\n{s['obj']}\n\nEligibility Criteria:\n{s['elig']}\n\nExclusion Criteria:\n{s['excl']}\n\nDocuments Required:\n{s['docs']}"
        filename = f"{s['id']}.pdf"
        text_to_pdf(filename, s['title'], s['category'], s['type'], details_text)
        
        formatted_dataset.append({
            "id": s['id'],
            "title": s['title'],
            "category": s['category'],
            "type": s['type'],
            "objective": s['obj'],
            "eligibility": s['elig'],
            "exclusion": s['excl'],
            "documents_required": s['docs']
        })

    # Save Master JSON Dataset
    with open(JSON_OUTPUT, "w", encoding="utf-8") as f:
        json.dump(formatted_dataset, f, indent=4, ensure_ascii=False)

    print(f"\n[SUCCESS] Generated exactly {len(formatted_dataset)} Master Government Scheme PDFs in:\n'{OUTPUT_DIR}'")
    print(f"[SUCCESS] Saved Master JSON dataset ({len(formatted_dataset)} records) in:\n'{JSON_OUTPUT}'!")

if __name__ == "__main__":
    generate_100_schemes()
