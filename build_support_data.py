import json, os

os.makedirs('data', exist_ok=True)

# 1. Glossary Data
glossary = [
    {
        'term': 'DBT (Direct Benefit Transfer)',
        'category': 'Banking & Payments',
        'en': 'Subsidies and cash benefits sent directly from government treasury into your bank account without middlemen.',
        'hi': 'सरकारी योजना की राशि बिना किसी बिचौलिए के सीधे आपके बैंक खाते में भेजी जाना।',
        'te': 'ప్రభుత్వ పథకాల నగదు దళారులు లేకుండా నేరుగా మీ బ్యాంక్ ఖాతాకే జమ కావడం.',
        'ta': 'அரசு மானியங்கள் இடைத்தரகர்கள் இல்லாமல் நேரடியாக உங்கள் வங்கிக் கணக்கில் செலுத்தப்படுவது.'
    },
    {
        'term': 'NPCI Aadhaar Seeding',
        'category': 'Banking & Security',
        'en': 'Linking your 12-digit Aadhaar to your bank account via the NPCI mapper so DBT government funds can land automatically.',
        'hi': 'अपने आधार को बैंक खाते से NPCI मैपर पर लिंक करना ताकि सरकारी सहायता बिना रुकावट खाते में आ सके।',
        'te': 'మీ ఆధార్‌ను NPCI ద్వారా బ్యాంక్ ఖాతాకు అనుసంధానించడం, దీనివల్ల ప్రభుత్వ నిధులు సక్రమంగా జమ అవుతాయి.',
        'ta': 'டிபிடி திட்ட நிதி நேரடியாக வர உங்கள் ஆதாரை என்பிசிஐ மேப்பரில் வங்கிக் கணக்குடன் இணைத்தல்.'
    },
    {
        'term': 'RoR / Khatauni / Jamabandi',
        'category': 'Land & Agriculture',
        'en': 'Official government record of rights proving who owns a specific agricultural land parcel and its boundary survey numbers.',
        'hi': 'सरकारी जमीन का अधिकार अभिलेख (खतौनी/जमाबंदी) जो यह साबित करता है कि जमीन का असली मालिक कौन है।',
        'te': 'వ్యవసాయ భూమి యాజమాన్యం మరియు సర్వే నంబర్లను ధృవీకరించే అధికారిక పట్టాదారు పాస్‌బుక్ / 1B రికార్డు.',
        'ta': 'விவசாய நிலத்தின் உரிமையாளர் மற்றும் சர்வே எண்களைக் காட்டும் அதிகாரப்பூர்வ பட்டா/சிட்டா ஆவணம்.'
    },
    {
        'term': 'UDID (Unique Disability ID)',
        'category': 'Disability Support',
        'en': 'Single nationwide digital disability identity card eliminating the need to carry physical hospital medical certificates.',
        'hi': 'दिव्यांगजनों के लिए पूरे भारत में मान्य एक डिजिटल पहचान पत्र जो सभी सरकारी लाभों के लिए मान्य है।',
        'te': 'దివ్యాంగుల కోసం దేశవ్యాప్తంగా చెల్లుబాటు అయ్యే ఒకే డిజిటల్ గుర్తింపు కార్డు (UDID).',
        'ta': 'மாற்றுத்திறனாளிகளுக்கான அகில இந்திய டிஜிட்டல் அடையாள அட்டை (UDID).'
    },
    {
        'term': 'NFSA & Antyodaya (AAY)',
        'category': 'Food & Rations',
        'en': 'National Food Security Act card categories giving poorest households 35kg free foodgrains per month.',
        'hi': 'राष्ट्रीय खाद्य सुरक्षा के तहत अंत्योदय अन्न योजना सबसे गरीब परिवारों को 35 किलो मुफ्त राशन देती है।',
        'te': 'జాతీయ ఆహార భద్రతా చట్టం క్రింద నిరుపేద కుటుంబాలకు నెలకు 35 కిలోల ఉచిత బియ్యం అందించే పథకం.',
        'ta': 'தேசிய உணவுப் பாதுகாப்புச் சட்டத்தின் கீழ் ஏழ்மையான குடும்பங்களுக்கு மாதத்திற்கு 35 கிலோ இலவச தானியம் வழங்கும் அட்டை.'
    },
    {
        'term': 'CSC (Common Service Center)',
        'category': 'Access & Facilitation',
        'en': 'Government-authorized village level digital kiosks where citizens can apply for certificates, schemes, and eKYC.',
        'hi': 'ग्राम स्तर पर सरकारी अधिकृत जन सेवा केंद्र जहां नागरिक प्रमाण पत्र, योजनाएं और eKYC करवा सकते हैं।',
        'te': 'గ్రామాల్లో ప్రభుత్వ పథకాల దరఖాస్తులు, ధృవీకరణ పత్రాలు అందించే కామన్ సర్వీస్ సెంటర్ (గ్రామ వన్).',
        'ta': 'கிராமங்களில் அரசு திட்டங்களுக்கு விண்ணப்பிக்க உதவும் பொது சேவை மையம் (e-Seva மையம்).'
    }
]

# 2. Scams Data
scams = [
    {
        'id': 'scam-01',
        'severity': 'Critical Alert',
        'title': 'Fake PM-KISAN ₹12,000 Installment WhatsApp APK Scam',
        'description': 'Fraudulent WhatsApp messages claiming the Government has doubled PM-KISAN to ₹12,000 with a malicious link ending in .apk or non-gov domains.',
        'victim_impact': 'Steals banking SMS OTPs and drains citizen savings.',
        'countermeasure': 'Government schemes ONLY use official portals ending in .gov.in or .nic.in. Never download APK files from WhatsApp.',
        'reported_date': '18 Nov 2026',
        'status': 'Active Threat Flagged by CERT-In'
    },
    {
        'id': 'scam-02',
        'severity': 'High Alert',
        'title': 'Fake Ayushman Bharat Golden Card ₹499 Courier Fee',
        'description': 'Scammers calling senior citizens claiming their Ayushman 5-Lakh card is ready and asking for ₹499 courier / registration fee via UPI.',
        'victim_impact': 'Financial extortion targeting vulnerable elderly.',
        'countermeasure': 'Ayushman Bharat eKYC and PVC cards are 100% FREE at any government hospital or authorized CSC.',
        'reported_date': '14 Nov 2026',
        'status': 'Verified Fraud'
    },
    {
        'id': 'scam-03',
        'severity': 'Critical Alert',
        'title': 'Bogus PM Mudra Loan Approval Letter with "GST Verification Fee"',
        'description': 'Citizens receive fake stamped approval letters of ₹5,00,000 MUDRA loan asking to pay ₹12,500 advance processing fee into a private account.',
        'victim_impact': 'Upfront fee fraud against small street vendors and entrepreneurs.',
        'countermeasure': 'No government loan scheme asks for advance deposit into personal bank accounts. Mudra loans are issued ONLY by commercial banks.',
        'reported_date': '16 Nov 2026',
        'status': 'Police FIR Registered'
    },
    {
        'id': 'scam-04',
        'severity': 'Medium Alert',
        'title': 'Fake PM Surya Ghar Free Rooftop Solar Survey Agents',
        'description': 'Unauthorized individuals visiting rural homes demanding ₹1,000 cash for "rooftop survey inspection".',
        'victim_impact': 'Direct cash extortion from rural homeowners.',
        'countermeasure': 'Apply only through pmsuryaghar.gov.in. Empanelled vendors never collect cash surveys without portal registration receipt.',
        'reported_date': '10 Nov 2026',
        'status': 'Advisory Issued by MNRE'
    }
]

# 3. Helplines Data
helplines = [
    { 'number': '1930', 'service': 'Cyber Financial Fraud & Scam Emergency', 'hours': '24x7 Toll-Free', 'dept': 'Ministry of Home Affairs (MHA)' },
    { 'number': '14555', 'service': 'Ayushman Bharat PM-JAY Call Center', 'hours': '24x7 Multi-lingual', 'dept': 'National Health Authority' },
    { 'number': '1800-11-5526', 'service': 'Kisan Call Center (Agriculture & Crops)', 'hours': '6:00 AM - 10:00 PM', 'dept': 'Ministry of Agriculture' },
    { 'number': '181', 'service': 'Women Helpline (Domestic & Public Crisis)', 'hours': '24x7 Emergency', 'dept': 'Ministry of Women & Child' },
    { 'number': '1098', 'service': 'Childline (Child Protection & Care)', 'hours': '24x7 Emergency', 'dept': 'Ministry of WCD' },
    { 'number': '14416', 'service': 'Tele-MANAS (Mental Health & Distress Support)', 'hours': '24x7 Free Counseling', 'dept': 'Ministry of Health' },
    { 'number': '155261', 'service': 'National Scholarship Portal Support', 'hours': '9:00 AM - 6:00 PM', 'dept': 'Ministry of Electronics & IT' },
    { 'number': '1800-180-1551', 'service': 'PM Awas Yojana Rural Helpline', 'hours': '9:00 AM - 5:30 PM', 'dept': 'Ministry of Rural Development' }
]

# 4. Regional Issue Trends Data (Feature 30)
trends = [
    { 'region': 'Uttar Pradesh (Varanasi / Gorakhpur)', 'issue': 'PM-KISAN eKYC Facial Authentication Failures', 'rate': '38% of applicants', 'solution': 'Use Iris scanner at CSC or update biometrics at nearest Post Office.', 'trend': 'High' },
    { 'region': 'Maharashtra (Marathwada / Vidarbha)', 'issue': 'Ladki Bahin Bank NPCI Aadhaar Unseeded Rejections', 'rate': '29% of applicants', 'solution': 'Submit DBT mandate form to bank branch; do not open a new account.', 'trend': 'Medium' },
    { 'region': 'Bihar (Patna / Muzaffarpur)', 'issue': 'Student Credit Card College Bonafide Delay', 'rate': '31% of applicants', 'solution': 'Download digilocker certified marksheet to bypass physical college sign-off.', 'trend': 'Medium' },
    { 'region': 'Karnataka (Belagavi / Raichur)', 'issue': 'Gruha Lakshmi Head-of-Family Ration Card mismatch', 'rate': '24% of applicants', 'solution': 'Apply for Ration Card modification on Ahara portal before Seva Sindhu.', 'trend': 'Moderate' },
    { 'region': 'Tamil Nadu (Madurai / Salem)', 'issue': 'Pudhumai Penn EMIS student code not matching college portal', 'rate': '18% of applicants', 'solution': 'School headmaster must verify student exit TC on EMIS server.', 'trend': 'Low' }
]

with open(os.path.join('data', 'glossary.json'), 'w', encoding='utf-8') as f:
    json.dump(glossary, f, indent=2, ensure_ascii=False)

with open(os.path.join('data', 'scams.json'), 'w', encoding='utf-8') as f:
    json.dump(scams, f, indent=2, ensure_ascii=False)

with open(os.path.join('data', 'helplines.json'), 'w', encoding='utf-8') as f:
    json.dump(helplines, f, indent=2, ensure_ascii=False)

with open(os.path.join('data', 'trends.json'), 'w', encoding='utf-8') as f:
    json.dump(trends, f, indent=2, ensure_ascii=False)

print('Successfully generated glossary, scams, helplines, and trends JSON files!')
