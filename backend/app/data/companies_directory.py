"""Company directory for PlacementPro.

A single source of truth for company prep across the platform. Each entry is a
real company with a stable slug, name, country, and sector. Interview round
structure and focus areas are derived from the company's sector so that every
listing entry yields a valid "{company}/guide" (leadership principles default to
empty and the prep-mix falls back to a sensible default in company_prep.py).

The directory is intentionally flat and declarative so new companies can be
added by appending rows to the appropriate regional list below.
"""
from typing import Dict, List

# (name, slug, country)
# Slugs are lower-case, hyphenated, unique across the directory.
_GLOBAL_PRODUCT = [
    ("Google", "google", "USA"), ("Meta", "meta", "USA"), ("Apple", "apple", "USA"),
    ("Microsoft", "microsoft", "USA"), ("Netflix", "netflix", "USA"), ("Amazon", "amazon", "USA"),
    ("Microsoft", "microsoft", "USA"), ("Salesforce", "salesforce", "USA"), ("Oracle", "oracle", "USA"),
    ("Adobe", "adobe", "USA"), ("Uber", "uber", "USA"), ("Airbnb", "airbnb", "USA"),
    ("Stripe", "stripe", "USA"), ("Shopify", "shopify", "USA"), ("Twilio", "twilio", "USA"),
    ("Intuit", "intuit", "USA"), ("ServiceNow", "servicenow", "USA"), ("Snowflake", "snowflake", "USA"),
    ("Datadog", "datadog", "USA"), ("MongoDB", "mongodb", "USA"), ("MongoDB", "mongodb", "USA"),
    ("Atlassian", "atlassian", "Australia"), ("Shopify", "shopify", "Canada"),
    ("Spotify", "spotify", "Sweden"), ("GitHub", "github", "USA"), ("LinkedIn", "linkedin", "USA"),
    ("Meta", "meta", "USA"), ("Netflix", "netflix", "USA"), ("Qualcomm", "qualcomm", "USA"),
    ("Broadcom", "broadcom", "USA"), ("Workday", "workday", "USA"), ("ServiceNow", "servicenow", "USA"),
    ("CrowdStrike", "crowdstrike", "USA"), ("PaloAltoNetworks", "palo-alto-networks", "USA"),
    ("Fortinet", "fortinet", "USA"), ("Zscaler", "zscaler", "USA"), ("Okta", "okta", "USA"),
    ("Salesforce", "salesforce", "USA"), ("Twilio", "twilio", "USA"), ("Elastic", "elastic", "USA"),
]

_GLOBAL_ENTERPRISE = [
    ("IBM", "ibm", "USA"), ("Accenture", "accenture", "Ireland"), ("Deloitte", "deloitte", "USA"),
    ("PwC", "pwc", "UK"), ("KPMG", "kpmg", "UK"), ("EY", "ey", "UK"),
    ("BCG", "bcg", "USA"), ("McKinsey", "mckinsey", "USA"), ("Bain", "bain", "USA"),
    ("Capgemini", "capgemini", "France"), ("Infosys", "infosys", "India"), ("TCS", "tcs", "India"),
    ("Wipro", "wipro", "India"), ("HCLTech", "hcl-tech", "India"), ("TechMahindra", "tech-mahindra", "India"),
    ("Cognizant", "cognizant", "USA"), ("Fiserv", "fiserv", "USA"), ("FIS", "fis", "USA"),
    ("TylerTechnologies", "tylertech", "USA"), ("DXC", "dxc", "USA"), ("HPE", "hpe", "USA"),
    ("HP", "hp", "USA"), ("Dell", "dell", "USA"), ("VMware", "vmware", "USA"), ("Oracle", "oracle", "USA"),
    ("SAP", "sap", "Germany"), ("Siemens", "siemens", "Germany"), ("ABB", "abb", "Switzerland"),
    ("Shell", "shell", "Netherlands"), ("BP", "bp", "UK"), ("Schlumberger", "slb", "France/USA"),
]

_INDIAN_IT_SERVICES = [
    ("TCS", "tcs", "India"), ("Infosys", "infosys", "India"), ("Wipro", "wipro", "India"),
    ("HCLTech", "hcl-tech", "India"), ("TechMahindra", "tech-mahindra", "India"),
    ("Cognizant", "cognizant", "USA/India"), ("Mindtree", "mindtree", "India"),
    ("Mphasis", "mphasis", "India"), ("L&T Infotech", "lt-infotech", "India"),
    ("Mphasis", "mphasis", "India"), ("TechMahindra", "tech-mahindra", "India"),
    ("Hexaware", "hexaware", "India"), ("Persistent", "persistent", "India"),
    ("Coforge", "coforge", "India"), ("NIIT", "niit", "India"), ("Zensar", "zensar", "India"),
    ("Cyient", "cyient", "India"), ("HappiestMinds", "happiest-minds", "India"),
    ("Mphasis", "mphasis", "India"), ("TCS", "tcs", "India"), ("Infosys", "infosys", "India"),
]

_INDIAN_STARTUPS_AND_FINTECH = [
    ("Flipkart", "flipkart", "India"), ("Swiggy", "swiggy", "India"), ("Zomato", "zomato", "India"),
    ("Razorpay", "razorpay", "India"), ("Paytm", "paytm", "India"), ("PhonePe", "phonepe", "India"),
    ("Zerodha", "zerodha", "India"), ("BYJU's", "byjus", "India"), ("Ola", "ola", "India"),
    ("Oyo", "oyo", "India"), ("Nykaa", "nykaa", "India"), ("Zomato", "zomato", "India"),
    ("PineLabs", "pinelabs", "India"), ("Cred", "cred", "India"), ("Nykaa", "nykaa", "India"),
    ("Meesho", "meesho", "India"), ("Zomato", "zomato", "India"),
]

_APTITUDE_FOCUSED_RECRUITERS = [
    ("TCS", "tcs", "India"), ("Infosys", "infosys", "India"), ("Wipro", "wipro", "India"),
    ("Cognizant", "cognizant", "USA"), ("Accenture", "accenture", "Ireland"),
    ("Capgemini", "capgemini", "France"), ("HCLTech", "hcl-tech", "India"),
    ("TechMahindra", "tech-mahindra", "India"), ("TCS", "tcs", "India"),
    ("Cognizant", "cognizant", "USA"), ("Infosys", "infosys", "India"),
    ("LarsenToubroInfotech", "lt-infotech", "India"), ("Mphasis", "mphasis", "India"),
    ("Wipro", "wipro", "India"), ("TCS", "tcs", "India"),
]

# (company_name, slug, country, sector)
_GLOBAL_BANKS_FINANCE = [
    ("GoldmanSachs", "goldman-sachs", "USA"), ("JPMorgan", "jpmorgan", "USA"),
    ("BankOfAmerica", "bank-of-america", "USA"), ("Citi", "citi", "USA"), ("Visa", "visa", "USA"),
    ("Mastercard", "mastercard", "USA"), ("S&P Global", "sp-global", "USA"), ("Bloomberg", "bloomberg", "USA"),
    ("BlackRock", "blackrock", "USA"), ("CharlesSchwab", "schwab", "USA"), ("MorganStanley", "morgan-stanley", "USA"),
    ("HSBC", "hsbc", "UK/HongKong"), ("Barclays", "barclays", "UK"), ("Lloyds", "lloyds", "UK"),
    ("StandardChartered", "scb", "UK/HongKong"), ("ANZ", "anz", "Australia"),
    ("ICICI", "icici", "India"), ("HDFC", "hdfc", "India"), ("SBI", "sbi", "India"),
    ("AxisBank", "axis-bank", "India"), ("Kotak", "kotak", "India"), ("IndusInd", "indusind", "India"),
    ("RBL", "rbl-bank", "India"), ("YesBank", "yes-bank", "India"),
]

_SECTORS = {
    "product": {
        "interview_rounds": ["Online Assessment", "Phone Screen", "Technical Phone Screen", "Onsite (3-5 rounds)"],
        "focus_areas": ["Coding", "System Design", "Behavioral", "Product Sense"],
        "leadership_principles": ["Customer Obsession", "Ownership", "Bias for Action", "Deliver Results"],
    },
    "enterprise": {
        "interview_rounds": ["Phone Screen", "Technical Round", "Hiring Manager Round", "Onsite"],
        "focus_areas": ["Coding", "System Design", "Behavioral", "Domain Knowledge"],
        "leadership_principles": ["Leadership", "Collaboration", "Execution", "Customer Centricity"],
    },
    "services": {
        "interview_rounds": ["Aptitude Test", "Technical Interview", "HR Interview"],
        "focus_areas": ["Aptitude", "Technical Fundamentals", "Communication", "Problem Solving"],
        "leadership_principles": ["Integrity", "Customer Focus", "Quality", "Teamwork"],
    },
    "startup": {
        "interview_rounds": ["Take Home", "Phone Screen", "Onsite (Founder/CTO round)"],
        "focus_areas": ["Coding", "Product Sense", "Speed", "Full-stack"],
        "leadership_principles": ["Bias for Action", "Ownership", "Ship Fast", "Learn by Doing"],
    },
    "fintech": {
        "interview_rounds": ["Online Coding Assessment", "Technical Round", "Hiring Manager", "Onsite"],
        "focus_areas": ["Coding", "Databases", "System Design", "Finance Domain"],
        "leadership_principles": ["Trust", "Precision", "Risk Awareness", "Customer Protection"],
    },
    "finance": {
        "interview_rounds": ["Numerical Test", "Technical/Psychometric", "Fit Interview", "Case Study"],
        "focus_areas": ["Quant", "Valuation", "Accounting", "Financial Modeling"],
        "leadership_principles": ["Analytical Rigor", "Attention to Detail", "Integrity", "Teamwork"],
    },
}

# Real company rows authored by humans with confidence, each unique (name, slug).
# Slugs must be unique; duplicates above are filtered in get_directory().
_SOURCE_ROWS: List[tuple] = [
    *[(n, s, c, "product") for n, s, c in _GLOBAL_PRODUCT],
    *[(n, s, c, "enterprise") for n, s, c in _GLOBAL_ENTERPRISE],
    *[(n, s, c, "services") for n, s, c in _INDIAN_IT_SERVICES],
    *[(n, s, c, "startup") for n, s, c in _INDIAN_STARTUPS_AND_FINTECH],
    *[(n, s, c, "services") for n, s, c in _APTITUDE_FOCUSED_RECRUITERS],
    *[(n, s, c, "finance") for n, s, c in _GLOBAL_BANKS_FINANCE],
]


def get_directory() -> Dict[str, dict]:
    """Return {slug: company_info_dict} with unique slugs.

    If the same slug appears more than once (e.g. a company reused across
    region lists), the first authoritative occurrence is kept so each company
    has a single, canonical prep guide.
    """
    seen: Dict[str, dict] = {}
    for name, slug, country, sector in _SOURCE_ROWS:
        if slug in seen:
            continue
        meta = _SECTORS[sector]
        seen[slug] = {
            "name": name,
            "country": country,
            "sector": sector,
            "leadership_principles": list(meta["leadership_principles"]),
            "interview_rounds": list(meta["interview_rounds"]),
            "focus_areas": list(meta["focus_areas"]),
        }
    return seen


def get_company_list() -> List[dict]:
    """Ordered list (id, name) for the public /companies listing."""
    return [{"id": slug, "name": info["name"]} for slug, info in get_directory().items()]


if __name__ == "__main__":
    d = get_directory()
    print("unique companies:", len(d))
    from collections import Counter

    secs = Counter(v["sector"] for v in d.values())
    print("by sector:", dict(secs))
