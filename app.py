import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import altair as alt
import random
import os
import requests
import time
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="SUHAIL - Saudi Real Estate Platform",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced UI
custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;800&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css');
    
    * {
        font-family: 'Tajawal', sans-serif;
    }
    
    .main {
        background-color: #f8f9fa;
    }
    
    .stApp {
        background: linear-gradient(to bottom, #f8f9fa, #eaeff4);
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background-color: #172b4d;
        color: white;
    }
    
    /* Hero section styling */
    .hero-section {
        background: linear-gradient(135deg, #1e3c72, #2a5298);
        color: white;
        padding: 3rem;
        border-radius: 15px;
        margin-bottom: 30px;
        text-align: center;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
    }
    
    .hero-logo {
        font-size: 52px;
        font-weight: 800;
        margin-bottom: 20px;
        background: linear-gradient(45deg, #9a86fe, #bba3ff);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        display: inline-block;
    }
    
    .hero-subtitle {
        font-size: 24px;
        font-weight: 400;
        margin-bottom: 20px;
        opacity: 0.9;
    }
    
    /* Feature cards styling */
    .feature-card {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
        border-left: 5px solid #9a86fe;
    }
    
    .feature-card:hover {
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
        transform: translateY(-5px);
    }
    
    .feature-card h3 {
        color: #2a5298;
        margin-bottom: 15px;
    }
    
    .feature-card i {
        font-size: 24px;
        color: #9a86fe;
        margin-right: 10px;
        vertical-align: middle;
    }
    
    /* Property card styling */
    .property-card {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
    }
    
    .property-card:hover {
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
        transform: translateY(-5px);
    }
    
    .property-price {
        font-size: 24px;
        font-weight: 700;
        color: #1e3c72;
    }
    
    .property-address {
        color: #666;
        font-size: 14px;
    }
    
    .property-features {
        display: flex;
        justify-content: space-between;
        margin-top: 15px;
        padding-top: 15px;
        border-top: 1px solid #eee;
    }
    
    .property-feature {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    
    .property-feature-icon {
        font-size: 20px;
        color: #9a86fe;
        margin-bottom: 5px;
    }
    
    /* Risk analysis section styling */
    .risk-low {
        color: #2ecc71;
        font-weight: bold;
    }
    
    .risk-medium {
        color: #f39c12;
        font-weight: bold;
    }
    
    .risk-high {
        color: #e74c3c;
        font-weight: bold;
    }
    
    /* Chat styling */
    .chat-message {
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
        max-width: 80%;
    }
    
    .chat-message-user {
        background-color: #ddeeff;
        text-align: right;
        margin-left: auto;
        border-top-right-radius: 0;
    }
    
    .chat-message-bot {
        background-color: #f0f2f5;
        border-top-left-radius: 0;
    }
    
    /* Service section styling */
    .service-card {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
        border-top: 5px solid #9a86fe;
        text-align: center;
    }
    
    .service-icon {
        font-size: 36px;
        color: #9a86fe;
        margin-bottom: 15px;
    }
    
    .service-title {
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 10px;
        color: #2a5298;
    }
    
    /* Progress steps */
    .progress-steps {
        display: flex;
        justify-content: space-between;
        margin: 40px 0;
        position: relative;
    }
    
    .progress-steps:before {
        content: '';
        position: absolute;
        top: 20px;
        left: 0;
        width: 100%;
        height: 3px;
        background-color: #ddd;
        z-index: -1;
    }
    
    .step {
        display: flex;
        flex-direction: column;
        align-items: center;
        z-index: 1;
    }
    
    .step-number {
        width: 40px;
        height: 40px;
        background-color: #9a86fe;
        color: white;
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        font-weight: bold;
        margin-bottom: 10px;
    }
    
    .step-title {
        font-size: 14px;
        color: #555;
        text-align: center;
        max-width: 120px;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: white;
        border-radius: 5px 5px 0 0;
        gap: 1px;
        padding-left: 16px;
        padding-right: 16px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #9a86fe !important;
        color: white !important;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Initialize OpenAI client
def get_ai_response(prompt, history=None):
    try:
        # Create system message with additional instruction to prevent repeated greetings
        system_message = "You are Suhail, an AI assistant specialized in Saudi Arabian real estate. Provide detailed information about properties, neighborhoods, financing options, and transaction processes. Always respond in both Arabic (first) and English (second). Be helpful, detailed, and concise. DO NOT repeat greeting messages if the user has already greeted you - continue the conversation naturally."
        # Create HTTP headers
        api_key = st.secrets["OPENAI_API_KEY"]
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        # Create the system message
        # Create the system message
        messages = [{"role": "system", "content": "You are Suhail, an AI assistant specialized in Saudi Arabian real estate. Provide detailed information about properties, neighborhoods, financing options, and transaction processes. Always respond in both Arabic (first) and English (second). Be helpful, detailed, and concise. If the user asks the same question multiple times, don't repeat your previous answer verbatim - acknowledge you've answered it before and ask if they need additional details."}]
        
        # Add chat history if available
        if history:
            # Only include the last 10 messages
            for msg in history[-10:]:
                if msg["role"] in ["user", "assistant"]:
                    messages.append(msg)
        
        # Add the current user prompt
        messages.append({"role": "user", "content": prompt})
        
        # Prepare request body
       # In the API call settings
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": messages,
            "max_tokens": 500,  # Lower from 800 to prevent long responses
            "temperature": 0.7
        }
        
        # Make the API call with timeout
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=10  # Add 10-second timeout
        )
        
        # Check for successful response
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"Error: {response.status_code}. Please try again."
            
    except Exception as e:
        return "Sorry, there was an error connecting to my knowledge base. Please try again later."

# Sample data - Properties
@st.cache_data
def load_properties():
    properties = [
        {
            "id": "RYD001",
            "title": "Modern Villa in Al Nakheel",
            "title_ar": "فيلا حديثة في النخيل",
            "price": 3500000,
            "size_sqm": 450,
            "bedrooms": 5,
            "bathrooms": 6,
            "type": "Villa",
            "area": "Al Nakheel",
            "description": "Luxury modern villa with high-end finishes in the prestigious Al Nakheel district",
            "description_ar": "فيلا فاخرة مع تشطيبات راقية في حي النخيل المميز",
            "features": ["Private Pool", "Garden", "Smart Home System", "Security System"],
            "features_ar": ["مسبح خاص", "حديقة", "نظام منزل ذكي", "نظام أمان متطور"],
            "location": {"lat": 24.758913, "lng": 46.637417},
            "rating": 4.8,
            "verified": True,
            "date_added": "2025-04-15",
            "roi_estimate": "7.2%"
        },
        {
            "id": "RYD002",
            "title": "Family Apartment in Al Olaya",
            "title_ar": "شقة عائلية في العليا",
            "price": 1200000,
            "size_sqm": 180,
            "bedrooms": 3,
            "bathrooms": 2,
            "type": "Apartment",
            "area": "Al Olaya",
            "description": "Spacious family apartment in a prime location near King Fahd Road",
            "description_ar": "شقة واسعة في موقع ممتاز بالقرب من طريق الملك فهد",
            "features": ["Gym", "Covered Parking", "Children's Play Area", "24/7 Security"],
            "features_ar": ["صالة رياضية", "مواقف مغطاة", "منطقة لعب للأطفال", "أمن على مدار الساعة"],
            "location": {"lat": 24.690595, "lng": 46.685419},
            "rating": 4.5,
            "verified": True,
            "date_added": "2025-05-02",
            "roi_estimate": "5.8%"
        },
        {
            "id": "RYD003",
            "title": "Penthouse in Kingdom Tower",
            "title_ar": "بنتهاوس في برج المملكة",
            "price": 7500000,
            "size_sqm": 320,
            "bedrooms": 4,
            "bathrooms": 5,
            "type": "Penthouse",
            "area": "Al Olaya",
            "description": "Luxury penthouse with stunning city views from Kingdom Tower",
            "description_ar": "شقة فاخرة مع إطلالات رائعة على المدينة من برج المملكة",
            "features": ["Private Elevator", "Panoramic Views", "Smart Home", "Concierge Service"],
            "features_ar": ["مصعد خاص", "إطلالات بانورامية", "منزل ذكي", "خدمة كونسيرج"],
            "location": {"lat": 24.711667, "lng": 46.674167},
            "rating": 4.9,
            "verified": True,
            "date_added": "2025-05-10",
            "roi_estimate": "4.1%"
        },
        {
            "id": "RYD004",
            "title": "Affordable Home in Al Naseem",
            "title_ar": "منزل بأسعار معقولة في النسيم",
            "price": 850000,
            "size_sqm": 220,
            "bedrooms": 3,
            "bathrooms": 2,
            "type": "House",
            "area": "Al Naseem",
            "description": "Affordable family home in a quiet residential neighborhood",
            "description_ar": "منزل عائلي بأسعار معقولة في حي سكني هادئ",
            "features": ["Small Garden", "Covered Parking", "Storage Room"],
            "features_ar": ["حديقة صغيرة", "مواقف مغطاة", "غرفة تخزين"],
            "location": {"lat": 24.774772, "lng": 46.831479},
            "rating": 4.0,
            "verified": True,
            "date_added": "2025-04-28",
            "roi_estimate": "6.5%"
        },
        {
            "id": "RYD005",
            "title": "New Townhouse in Hittin",
            "title_ar": "تاون هاوس جديد في حطين",
            "price": 1800000,
            "size_sqm": 260,
            "bedrooms": 4,
            "bathrooms": 3,
            "type": "Townhouse",
            "area": "Hittin",
            "description": "Newly built modern townhouse in the expanding Hittin neighborhood",
            "description_ar": "تاون هاوس حديث البناء في حي حطين المتنامي",
            "features": ["Modern Design", "Energy Efficient", "Private Entrance", "Small Garden"],
            "features_ar": ["تصميم عصري", "موفر للطاقة", "مدخل خاص", "حديقة صغيرة"],
            "location": {"lat": 24.790107, "lng": 46.694477},
            "rating": 4.6,
            "verified": True,
            "date_added": "2025-05-08",
            "roi_estimate": "5.9%"
        },
        {
            "id": "RYD006",
            "title": "Investment Apartment in Al Malaz",
            "title_ar": "شقة استثمارية في الملز",
            "price": 650000,
            "size_sqm": 120,
            "bedrooms": 2,
            "bathrooms": 1,
            "type": "Apartment",
            "area": "Al Malaz",
            "description": "Affordable investment opportunity in a high-rental yield area",
            "description_ar": "فرصة استثمارية بأسعار معقولة في منطقة ذات عائد إيجار مرتفع",
            "features": ["Balcony", "Covered Parking", "24/7 Security"],
            "features_ar": ["شرفة", "مواقف مغطاة", "أمن على مدار الساعة"],
            "location": {"lat": 24.674667, "lng": 46.751472},
            "rating": 4.2,
            "verified": True,
            "date_added": "2025-05-01", 
            "roi_estimate": "8.3%"
        }
    ]
    return properties

# Sample data - Banks & Financing options
@st.cache_data
def load_banks():
    banks = [
        {
            "name": "Al Rajhi Bank",
            "name_ar": "مصرف الراجحي",
            "logo": "https://upload.wikimedia.org/wikipedia/ar/c/c1/Al_Rajhi_Bank.svg",
            "interest_rate": 3.5,
            "max_loan_term": 25,
            "min_down_payment": 10,
            "processing_fee": 1.0,
            "special_offers": ["First-time buyer discount", "Government employee discount"],
            "requirements": ["Saudi national or resident", "Minimum 6 months employment", "Salary transfer"]
        },
        {
            "name": "Saudi National Bank",
            "name_ar": "البنك الأهلي السعودي",
            "logo": "https://upload.wikimedia.org/wikipedia/en/1/19/Saudi_National_Bank_logo.svg",
            "interest_rate": 3.2,
            "max_loan_term": 30,
            "min_down_payment": 15,
            "processing_fee": 0.8,
            "special_offers": ["Zero early settlement fees", "Fixed rate options"],
            "requirements": ["Saudi national or resident", "Minimum income SAR 8,000", "Clean credit history"]
        },
        {
            "name": "Riyad Bank",
            "name_ar": "بنك الرياض",
            "logo": "https://upload.wikimedia.org/wikipedia/en/5/5a/Riyad_Bank_logo.svg",
            "interest_rate": 3.8,
            "max_loan_term": 25,
            "min_down_payment": 10,
            "processing_fee": 0.75,
            "special_offers": ["Family home discount", "Competitive insurance rates"],
            "requirements": ["Saudi national or resident", "Minimum income SAR 7,000", "Age under 60 at end of loan term"]
        },
        {
            "name": "Alinma Bank",
            "name_ar": "مصرف الإنماء",
            "logo": "https://upload.wikimedia.org/wikipedia/en/e/ea/Alinma_bank_logo.svg",
            "interest_rate": 3.6,
            "max_loan_term": 30,
            "min_down_payment": 10,
            "processing_fee": 0.7,
            "special_offers": ["Sharia-compliant options", "Flexible payment schedule"],
            "requirements": ["Saudi national or resident", "Minimum income SAR 6,000", "6+ months with current employer"]
        }
    ]
    return banks

# Sample data - Real Estate Consultants
@st.cache_data
def load_consultants():
    consultants = [
        {
            "id": "CONS001",
            "name": "Ahmed Al-Qahtani",
            "name_ar": "أحمد القحطاني",
            "specialty": "Luxury Properties",
            "specialty_ar": "العقارات الفاخرة",
            "experience": 12,
            "areas": ["Al Olaya", "Al Nakheel", "Hittin"],
            "languages": ["Arabic", "English"],
            "rating": 4.9,
            "reviews": 124,
            "fee": "2% of property value",
            "availability": "Available",
            "certifications": ["REGA Licensed", "International Real Estate Association"]
        },
        {
            "id": "CONS002",
            "name": "Fatima Al-Harbi",
            "name_ar": "فاطمة الحربي",
            "specialty": "Family Homes",
            "specialty_ar": "المنازل العائلية",
            "experience": 8,
            "areas": ["Al Naseem", "Al Malaz", "Hittin"],
            "languages": ["Arabic", "English", "Urdu"],
            "rating": 4.7,
            "reviews": 98,
            "fee": "Fixed fee - 5,000 SAR",
            "availability": "Busy until May 30",
            "certifications": ["REGA Licensed", "Family Housing Specialist"]
        },
        {
            "id": "CONS003",
            "name": "Khalid Alsudairi",
            "name_ar": "خالد السديري",
            "specialty": "Investment Properties",
            "specialty_ar": "العقارات الاستثمارية",
            "experience": 15,
            "areas": ["All Riyadh Areas"],
            "languages": ["Arabic", "English", "French"],
            "rating": 4.8,
            "reviews": 211,
            "fee": "1.5% of property value",
            "availability": "Limited Availability",
            "certifications": ["REGA Licensed", "Investment Property Analyst", "MBA in Real Estate"]
        },
        {
            "id": "CONS004",
            "name": "Noura Al-Dossary",
            "name_ar": "نورة الدوسري",
            "specialty": "First-time Buyers",
            "specialty_ar": "المشترين لأول مرة",
            "experience": 6,
            "areas": ["Al Naseem", "Al Malaz", "Al Wizarat"],
            "languages": ["Arabic", "English"],
            "rating": 4.6,
            "reviews": 67,
            "fee": "Fixed fee - 4,000 SAR",
            "availability": "Available",
            "certifications": ["REGA Licensed", "First-time Buyer Specialist"]
        }
    ]
    return consultants

# Sample data - Building Inspectors
@st.cache_data
def load_inspectors():
    inspectors = [
        {
            "id": "INSP001",
            "name": "Mohammed Al-Shammari",
            "name_ar": "محمد الشمري",
            "specialty": "Structural Engineering",
            "specialty_ar": "الهندسة الإنشائية",
            "experience": 15,
            "inspection_types": ["Pre-purchase", "Structural", "Comprehensive"],
            "languages": ["Arabic", "English"],
            "rating": 4.9,
            "reviews": 187,
            "fee_range": "1,500 - 3,000 SAR",
            "availability": "Available",
            "certifications": ["Certified Structural Engineer", "ASNT Level III", "Saudi Engineering Council"]
        },
        {
            "id": "INSP002",
            "name": "Sara Al-Otaibi",
            "name_ar": "سارة العتيبي",
            "specialty": "Electrical Systems",
            "specialty_ar": "أنظمة كهربائية",
            "experience": 8,
            "inspection_types": ["Electrical", "Smart Home Systems", "Safety"],
            "languages": ["Arabic", "English"],
            "rating": 4.7,
            "reviews": 92,
            "fee_range": "1,200 - 2,500 SAR",
            "availability": "Available",
            "certifications": ["Certified Electrical Engineer", "Saudi Engineering Council"]
        },
        {
            "id": "INSP003",
            "name": "Abdullah Al-Ghamdi",
            "name_ar": "عبدالله الغامدي",
            "specialty": "Complete Home Inspection",
            "specialty_ar": "فحص المنزل الشامل",
            "experience": 12,
            "inspection_types": ["Pre-purchase", "Comprehensive", "Maintenance"],
            "languages": ["Arabic", "English", "Filipino"],
            "rating": 4.8,
            "reviews": 154,
            "fee_range": "2,000 - 4,000 SAR",
            "availability": "Busy until May 25",
            "certifications": ["Master Builder", "Certified Home Inspector", "Saudi Engineering Council"]
        }
    ]
    return inspectors

# Sample data - Environmental risks
@st.cache_data
def load_risk_data():
    return [
        {"name": "Al Olaya", "flood_risk": 25, "air_pollution": 65, "heat_island": 75, "water_quality": 30},
        {"name": "Al Nakheel", "flood_risk": 15, "air_pollution": 50, "heat_island": 60, "water_quality": 25},
        {"name": "Hittin", "flood_risk": 20, "air_pollution": 45, "heat_island": 55, "water_quality": 35},
        {"name": "Al Malaz", "flood_risk": 40, "air_pollution": 70, "heat_island": 70, "water_quality": 40},
        {"name": "Al Naseem", "flood_risk": 60, "air_pollution": 55, "heat_island": 65, "water_quality": 45}
    ]

# Sample data - Neighborhoods
@st.cache_data
def load_neighborhoods():
    return [
        {
            "name": "Al Olaya",
            "safety": 85,
            "schools": 90,
            "healthcare": 88,
            "shopping": 95,
            "transportation": 80,
        },
        {
            "name": "Al Nakheel",
            "safety": 92,
            "schools": 85,
            "healthcare": 82,
            "shopping": 75,
            "transportation": 68,
        },
        {
            "name": "Hittin",
            "safety": 90,
            "schools": 82,
            "healthcare": 70,
            "shopping": 68,
            "transportation": 65,
        },
        {
            "name": "Al Malaz",
            "safety": 75,
            "schools": 80,
            "healthcare": 85,
            "shopping": 82,
            "transportation": 88,
        },
        {
            "name": "Al Naseem",
            "safety": 75,
            "schools": 65,
            "healthcare": 70,
            "shopping": 60,
            "transportation": 60,
        }
    ]

# Helper function to get risk level
def get_risk_level(value):
    if value < 30:
        return "Low", "risk-low"
    elif value < 60:
        return "Medium", "risk-medium"
    else:
        return "High", "risk-high"

# Function to visualize environmental risks
def plot_environmental_risks(area):
    risks = next((r for r in load_risk_data() if r["name"] == area), None)
    
    if not risks:
        st.write("No risk data available for this area.")
        return
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    categories = ['Flood Risk', 'Air Pollution', 'Heat Island', 'Water Quality']
    values = [risks['flood_risk'], risks['air_pollution'], risks['heat_island'], risks['water_quality']]
    
    x = np.arange(len(categories))
    
    # Different colors based on risk level
    colors = []
    for v in values:
        if v < 30:
            colors.append('#2ecc71')  # Green
        elif v < 60:
            colors.append('#f39c12')  # Orange
        else:
            colors.append('#e74c3c')  # Red
    
    bars = ax.bar(x, values, color=colors)
    
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.set_ylim(0, 100)
    ax.set_ylabel('Risk Level')
    ax.set_title(f'Environmental Risk Analysis: {area}')
    
    # Add risk level labels
    for i, bar in enumerate(bars):
        height = bar.get_height()
        level, _ = get_risk_level(height)
        ax.text(bar.get_x() + bar.get_width()/2., height + 5,
                f'{level}', ha='center', va='bottom')
    
    fig.tight_layout()
    return fig

# Function to visualize neighborhood quality
def plot_neighborhood_quality(area):
    neighborhood = next((n for n in load_neighborhoods() if n["name"] == area), None)
    
    if not neighborhood:
        st.write("No neighborhood data available for this area.")
        return
    
    # Create data for radar chart
    categories = ['Safety', 'Schools', 'Healthcare', 'Shopping', 'Transportation']
    values = [
        neighborhood['safety'], 
        neighborhood['schools'], 
        neighborhood['healthcare'], 
        neighborhood['shopping'], 
        neighborhood['transportation']
    ]
    
    # Number of variables
    N = len(categories)
    
    # Create angles for each category
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]  # Close the loop
    
    # Values need to be closed too
    values += values[:1]
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    
    # Draw one axis per variable and add labels
    plt.xticks(angles[:-1], categories, size=12)
    
    # Draw the chart
    ax.plot(angles, values, linewidth=2, linestyle='solid', color='#9a86fe')
    ax.fill(angles, values, alpha=0.25, color='#9a86fe')
    
    # Set y-limits
    ax.set_ylim(0, 100)
    
    # Add title
    plt.title(f'Neighborhood Quality: {area}', size=15, y=1.1)
    
    return fig

# Function to calculate mortgage
def calculate_mortgage(property_price, down_payment_percent, interest_rate, loan_years):
    loan_amount = property_price * (1 - down_payment_percent / 100)
    monthly_interest = interest_rate / 100 / 12
    num_payments = loan_years * 12
    
    monthly_payment = loan_amount * (monthly_interest * (1 + monthly_interest) ** num_payments) / ((1 + monthly_interest) ** num_payments - 1)
    
    total_payment = monthly_payment * num_payments
    total_interest = total_payment - loan_amount
    
    return {
        "loan_amount": loan_amount,
        "monthly_payment": monthly_payment,
        "total_payment": total_payment,
        "total_interest": total_interest
    }

# Function to display property card
def display_property_card(prop, show_button=True, button_text="View Details"):
    with st.container():
        st.markdown(f"""
        <div class="property-card">
            <div style="background-color:#f0f0f0; height:200px; border-radius:5px; display:flex; 
            justify-content:center; align-items:center; margin-bottom:15px;">
            <p style="color:#505050;">Property Image</p>
            </div>
            <h3>{prop["title"]}</h3>
            <p class="property-address">{prop["area"]}, Riyadh</p>
            <div style="display:flex; justify-content:space-between; align-items:center; margin:10px 0;">
                <div>
                    <p class="property-price">{prop["price"]:,} SAR</p>
                </div>
                <div>
                    <span style="background-color:#e6f4ff; color:#1e3c72; padding:5px 10px; border-radius:4px; font-size:14px;">
                        {"✓ Verified" if prop.get("verified", False) else "Pending Verification"}
                    </span>
                </div>
            </div>
            <div class="property-features">
                <div class="property-feature">
                    <i class="fas fa-bed property-feature-icon"></i>
                    <span>{prop["bedrooms"]} Beds</span>
                </div>
                <div class="property-feature">
                    <i class="fas fa-bath property-feature-icon"></i>
                    <span>{prop["bathrooms"]} Baths</span>
                </div>
                <div class="property-feature">
                    <i class="fas fa-ruler-combined property-feature-icon"></i>
                    <span>{prop["size_sqm"]} m²</span>
                </div>
                <div class="property-feature">
                    <i class="fas fa-star property-feature-icon"></i>
                    <span>{prop.get("rating", 4.0)}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if show_button:
            if st.button(button_text, key=f"prop_btn_{prop['id']}"):
                st.session_state.selected_property = prop["id"]
                if "page" in st.session_state:
                    st.session_state.page = "Property Search"
                st.rerun()

# Application layout
def main():
    # Initialize session state
    if "page" not in st.session_state:
        st.session_state.page = "Home"
    
    # Language session state
    if "language" not in st.session_state:
        st.session_state.language = "English"
    
    # Sidebar for navigation
    with st.sidebar:
        # Logo
        st.markdown("""
        <div style="text-align:center; margin-bottom:30px;">
            <h1 style="color:#9a86fe; font-size:40px; font-weight:800;">SUHAIL</h1>
            <p style="color:#eaeff4; margin-top:-15px;">REAL ESTATE</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Language selection
        language = st.radio("Language / اللغة", ["English", "العربية"], index=0 if st.session_state.language == "English" else 1)
        if language != st.session_state.language:
            st.session_state.language = language
        
        st.markdown("---")
        
        # Navigation
        st.markdown('<p style="font-size:16px; font-weight:600; margin-bottom:15px;">NAVIGATION</p>', unsafe_allow_html=True)
        
        if st.button("🏠 Home", use_container_width=True, key="nav_home"):
            st.session_state.page = "Home"
            st.rerun()
            
        if st.button("🔍 Property Search", use_container_width=True, key="nav_search"):
            st.session_state.page = "Property Search"
            st.rerun()
            
        if st.button("🌊 Environmental Analysis", use_container_width=True, key="nav_env"):
            st.session_state.page = "Environmental Analysis"
            st.rerun()
            
        if st.button("🏙️ Neighborhood Comparison", use_container_width=True, key="nav_neighborhood"):
            st.session_state.page = "Neighborhood Comparison"
            st.rerun()
            
        if st.button("💰 Financing Hub", use_container_width=True, key="nav_financing"):
            st.session_state.page = "Financing Hub"
            st.rerun()
            
        if st.button("🧪 Building Inspection", use_container_width=True, key="nav_inspection"):
            st.session_state.page = "Building Inspection"
            st.rerun()
            
        if st.button("👨‍💼 Real Estate Consultants", use_container_width=True, key="nav_consultants"):
            st.session_state.page = "Real Estate Consultants"
            st.rerun()
            
        if st.button("💬 Chat with AI", use_container_width=True, key="nav_chat"):
            st.session_state.page = "Chat with AI"
            st.rerun()
            
        st.markdown("---")
        
        # Get started with buying process
        st.markdown('<p style="font-size:16px; font-weight:600; margin-bottom:15px;">START YOUR JOURNEY</p>', unsafe_allow_html=True)
        if st.button("🚀 Get Started with Buying", use_container_width=True, key="nav_journey"):
            st.session_state.page = "Buying Journey"
            st.rerun()
    
    # Main content based on selected page
    if st.session_state.page == "Home":
        show_home()
    elif st.session_state.page == "Property Search":
        show_property_search()
    elif st.session_state.page == "Environmental Analysis":
        show_environmental_analysis()
    elif st.session_state.page == "Neighborhood Comparison":
        show_neighborhood_comparison()
    elif st.session_state.page == "Financing Hub":
        show_financing_hub()
    elif st.session_state.page == "Building Inspection":
        show_building_inspection()
    elif st.session_state.page == "Real Estate Consultants":
        show_consultants_page()
    elif st.session_state.page == "Chat with AI":
        show_ai_chat()
    elif st.session_state.page == "Buying Journey":
        show_buying_journey()

# Home page
def show_home():
    # Hero section
    st.markdown("""
    <div class="hero-section">
        <div class="hero-logo">SUHAIL</div>
        <h2>Transforming Saudi Real Estate</h2>
        <p class="hero-subtitle">The complete platform for finding, financing, and securing your perfect property</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background-color:white; padding:20px; border-radius:10px; text-align:center; box-shadow:0 4px 8px rgba(0,0,0,0.05);">
            <h1 style="color:#9a86fe; font-size:48px; margin:0;">64%</h1>
            <p style="margin:0;">Current Homeownership</p>
            <p style="font-size:14px; color:#666;">Saudi homeownership rate as of 2023</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background-color:white; padding:20px; border-radius:10px; text-align:center; box-shadow:0 4px 8px rgba(0,0,0,0.05);">
            <h1 style="color:#9a86fe; font-size:48px; margin:0;">70%</h1>
            <p style="margin:0;">2030 Target</p>
            <p style="font-size:14px; color:#666;">Government homeownership goal</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background-color:white; padding:20px; border-radius:10px; text-align:center; box-shadow:0 4px 8px rgba(0,0,0,0.05);">
            <h1 style="color:#9a86fe; font-size:48px; margin:0;">84%</h1>
            <p style="margin:0;">Purchase Intent</p>
            <p style="font-size:14px; color:#666;">Tenants planning to buy within a year</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Core services
    st.markdown("<h2 style='text-align:center;'>Our Core Services</h2>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="service-card">
            <div class="service-icon"><i class="fas fa-search-location"></i></div>
            <div class="service-title">Marketplace & Discovery</div>
            <p>Browse verified listings with AI-powered recommendations tailored to your needs.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="service-card">
            <div class="service-icon"><i class="fas fa-tools"></i></div>
            <div class="service-title">Building Safety Inspections</div>
            <p>Access to certified building safety inspectors for comprehensive property evaluations.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="service-card">
            <div class="service-icon"><i class="fas fa-hand-holding-usd"></i></div>
            <div class="service-title">Financing Hub</div>
            <p>Compare and choose from multiple bank options with personalized rates and terms.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="service-card">
            <div class="service-icon"><i class="fas fa-user-tie"></i></div>
            <div class="service-title">Expert Consultations</div>
            <p>Connect with certified real estate consultants for professional advice and support.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Featured properties
    st.markdown("<h2>Featured Properties</h2>", unsafe_allow_html=True)
    
    properties = load_properties()
    
    # Show top 3 properties
    cols = st.columns(3)
    for i, prop in enumerate(properties[:3]):
        with cols[i]:
            display_property_card(prop)
    
    # How it works
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center;'>How It Works</h2>", unsafe_allow_html=True)
    
    # Progress steps
    st.markdown("""
    <div class="progress-steps">
        <div class="step">
            <div class="step-number">1</div>
            <div class="step-title">Search & Discover Properties</div>
        </div>
        <div class="step">
            <div class="step-number">2</div>
            <div class="step-title">Compare Options & Financing</div>
        </div>
        <div class="step">
            <div class="step-number">3</div>
            <div class="step-title">Inspection & Assessment</div>
        </div>
        <div class="step">
            <div class="step-number">4</div>
            <div class="step-title">Complete Transaction</div>
        </div>
        <div class="step">
            <div class="step-number">5</div>
            <div class="step-title">Move In & Support</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Call to action
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("Start Your Home Buying Journey Today", use_container_width=True, type="primary"):
            st.session_state.page = "Buying Journey"
            st.rerun()

# Property search page
def show_property_search():
    # Check if we're viewing a particular property
    if 'selected_property' in st.session_state:
        show_property_details()
        return
    
    st.markdown("<h1>Property Search / البحث عن العقار</h1>", unsafe_allow_html=True)
    
    # Tabs for different search types
    tabs = st.tabs(["Search by Criteria", "Search by Map", "Search by Investment Potential"])
    
    with tabs[0]:
        # Advanced search filters in an expander
        with st.expander("Advanced Search Filters", expanded=True):
            # Search filters in three columns
            col1, col2, col3 = st.columns(3)
            
            with col1:
                min_price = st.number_input("Min Price / الحد الأدنى للسعر", min_value=0, max_value=10000000, step=100000, value=0)
                bedrooms = st.multiselect("Bedrooms / غرف النوم", options=list(range(1, 6+1)))
            
            with col2:
                max_price = st.number_input("Max Price / الحد الأعلى للسعر", min_value=0, max_value=10000000, step=100000, value=10000000)
                bathrooms = st.multiselect("Bathrooms / الحمامات", options=list(range(1, 6+1)))
            
            with col3:
                property_type = st.multiselect("Property Type / نوع العقار", options=["Villa", "Apartment", "Penthouse", "House", "Townhouse"])
                area = st.multiselect("Area / المنطقة", options=["Al Olaya", "Al Nakheel", "Hittin", "Al Malaz", "Al Naseem"])
            
            # Additional filters
            col1, col2, col3 = st.columns(3)
            
            with col1:
                min_size = st.number_input("Min Size (sqm)", min_value=0, max_value=1000, step=10, value=0)
            
            with col2:
                max_size = st.number_input("Max Size (sqm)", min_value=0, max_value=1000, step=10, value=1000)
            
            with col3:
                verified_only = st.checkbox("Verified Properties Only", value=True)
        
        # Apply filters
        properties = load_properties()
        filtered_properties = properties.copy()
        
        if min_price > 0:
            filtered_properties = [p for p in filtered_properties if p['price'] >= min_price]
        if max_price < 10000000:
            filtered_properties = [p for p in filtered_properties if p['price'] <= max_price]
        if bedrooms:
            filtered_properties = [p for p in filtered_properties if p['bedrooms'] in bedrooms]
        if bathrooms:
            filtered_properties = [p for p in filtered_properties if p['bathrooms'] in bathrooms]
        if property_type:
            filtered_properties = [p for p in filtered_properties if p['type'] in property_type]
        if area:
            filtered_properties = [p for p in filtered_properties if p['area'] in area]
        if min_size > 0:
            filtered_properties = [p for p in filtered_properties if p['size_sqm'] >= min_size]
        if max_size < 1000:
            filtered_properties = [p for p in filtered_properties if p['size_sqm'] <= max_size]
        if verified_only:
            filtered_properties = [p for p in filtered_properties if p.get('verified', False)]
        
        # Search results
        st.markdown(f"<h3>Found {len(filtered_properties)} properties / تم العثور على {len(filtered_properties)} عقار</h3>", unsafe_allow_html=True)
        
        # Display in grid
        if filtered_properties:
            # Display sort options
            col1, col2 = st.columns([3, 1])
            with col2:
                sort_option = st.selectbox("Sort By", ["Price (Low to High)", "Price (High to Low)", "Newest First", "Highest Rated"])
            
            # Sort properties based on selection
            if sort_option == "Price (Low to High)":
                filtered_properties.sort(key=lambda x: x['price'])
            elif sort_option == "Price (High to Low)":
                filtered_properties.sort(key=lambda x: x['price'], reverse=True)
            elif sort_option == "Newest First":
                filtered_properties.sort(key=lambda x: x.get('date_added', '2025-01-01'), reverse=True)
            elif sort_option == "Highest Rated":
                filtered_properties.sort(key=lambda x: x.get('rating', 4.0), reverse=True)
            
            # Display properties in a grid (2 per row)
            for i in range(0, len(filtered_properties), 2):
                cols = st.columns(2)
                for j in range(2):
                    if i + j < len(filtered_properties):
                        with cols[j]:
                            display_property_card(filtered_properties[i + j])
        else:
            st.info("No properties match your search criteria. Try adjusting your filters.")
    
    with tabs[1]:
        st.markdown("""
        <div style="background-color:#f0f0f0; height:400px; border-radius:5px; display:flex; 
        justify-content:center; align-items:center; margin-bottom:15px;">
            <p style="color:#505050;">Interactive Map View Coming Soon</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.info("Our interactive map search is currently under development. Please check back soon!")
    
    with tabs[2]:
        st.subheader("Investment Property Search")
        
        col1, col2 = st.columns(2)
        
        with col1:
            min_roi = st.slider("Minimum Expected ROI (%)", min_value=0.0, max_value=10.0, value=5.0, step=0.1)
            max_price_inv = st.number_input("Maximum Investment Budget", min_value=500000, max_value=10000000, value=2000000, step=100000)
        
        with col2:
            areas_investment = st.multiselect("Target Areas", options=["Al Olaya", "Al Nakheel", "Hittin", "Al Malaz", "Al Naseem"], default=["Al Malaz"])
            property_type_inv = st.multiselect("Property Types", options=["Apartment", "Villa", "Townhouse"], default=["Apartment"])
        
        # Filter properties for investment
        investment_properties = [p for p in properties if float(p.get('roi_estimate', '5.0%').strip('%')) >= min_roi]
        investment_properties = [p for p in investment_properties if p['price'] <= max_price_inv]
        
        if areas_investment:
            investment_properties = [p for p in investment_properties if p['area'] in areas_investment]
        
        if property_type_inv:
            investment_properties = [p for p in investment_properties if p['type'] in property_type_inv]
        
        # Sort by ROI
        investment_properties.sort(key=lambda x: float(x.get('roi_estimate', '5.0%').strip('%')), reverse=True)
        
        st.markdown(f"<h3>Found {len(investment_properties)} investment properties</h3>", unsafe_allow_html=True)
        
        # Create a table to compare investment properties
        if investment_properties:
            data = []
            for p in investment_properties:
                data.append({
                    "Property": p["title"],
                    "Type": p["type"],
                    "Area": p["area"],
                    "Price (SAR)": f"{p['price']:,}",
                    "Size (sqm)": p["size_sqm"],
                    "Est. ROI": p.get("roi_estimate", "5.0%"),
                    "Action": ""
                })
            
            df = pd.DataFrame(data)
            st.table(df[["Property", "Type", "Area", "Price (SAR)", "Size (sqm)", "Est. ROI"]])
            
            # Display the top 3 investment properties
            st.subheader("Top Investment Opportunities")
            cols = st.columns(3)
            for i, prop in enumerate(investment_properties[:3]):
                with cols[i]:
                    # Add a badge for ROI
                    display_property_card(prop)
                    st.markdown(f"<div style='text-align: center; background-color: #e6f4ff; padding: 10px; border-radius: 5px; margin-top: -10px;'><b>Expected ROI: {prop.get('roi_estimate', '5.0%')}</b></div>", unsafe_allow_html=True)

# Property details page
def show_property_details():
    property_id = st.session_state.selected_property
    properties = load_properties()
    prop = next((p for p in properties if p['id'] == property_id), None)
    
    if not prop:
        st.error("Property not found / لم يتم العثور على العقار")
        del st.session_state.selected_property
        st.rerun()
        return
    
    # Back button
    st.button("← Back to Search Results", on_click=lambda: st.session_state.pop("selected_property"))
    
    # Property title
    st.markdown(f"<h1>{prop['title']}</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='direction: rtl; text-align: right; font-weight: 400; margin-top: -10px;'>{prop['title_ar']}</h3>", unsafe_allow_html=True)
    
    # Property location and price
    st.markdown(f"<p style='font-size: 18px;'><i class='fas fa-map-marker-alt' style='color:#9a86fe;'></i> {prop['area']}, Riyadh</p>", unsafe_allow_html=True)
    
    # Main content
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Overview", "Environmental Risk", "Neighborhood", "Financing Options", "Transaction Process"])
    
    with tab1:
        col1, col2 = st.columns([3, 2])
        
        with col1:
            # Property image placeholder
            st.markdown("""
            <div style="background-color:#f0f0f0; height:300px; border-radius:5px; display:flex; 
            justify-content:center; align-items:center; margin-bottom:15px;">
                <p style="color:#505050;">Property Image Gallery</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Property description
            st.subheader("Description / الوصف")
            st.write(prop['description'])
            st.write(prop['description_ar'])
            
            # Features
            st.subheader("Features / الميزات")
            
            # Display features in an attractive way
            feature_html = "<div style='display: flex; flex-wrap: wrap; gap: 10px; margin-top: 10px;'>"
            
            for feature in prop['features']:
                feature_html += f"""
                <div style='background-color: #f0f2f5; padding: 8px 15px; border-radius: 20px;'>
                    <i class='fas fa-check' style='color: #9a86fe; margin-right: 5px;'></i> {feature}
                </div>
                """
            
            feature_html += "</div>"
            st.markdown(feature_html, unsafe_allow_html=True)
            
            # Arabic features
            feature_ar_html = "<div style='display: flex; flex-wrap: wrap; gap: 10px; margin-top: 10px; direction: rtl;'>"
            
            for feature in prop['features_ar']:
                feature_ar_html += f"""
                <div style='background-color: #f0f2f5; padding: 8px 15px; border-radius: 20px;'>
                    <i class='fas fa-check' style='color: #9a86fe; margin-right: 5px;'></i> {feature}
                </div>
                """
            
            feature_ar_html += "</div>"
            st.markdown(feature_ar_html, unsafe_allow_html=True)
        
        with col2:
            # Price and stats card
            st.markdown(f"""
            <div style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.05); text-align: center; margin-bottom: 20px;">
                <h1 style="color: #1e3c72; font-size: 32px; margin-bottom: 10px;">{prop['price']:,} SAR</h1>
                <p>Property ID: {prop['id']}</p>
                <div style="margin: 15px 0; border-top: 1px solid #eee; padding-top: 15px;">
                    <div style="display: flex; justify-content: space-around; margin-bottom: 15px;">
                        <div>
                            <i class="fas fa-bed" style="font-size: 24px; color: #9a86fe;"></i>
                            <p style="margin: 5px 0 0 0;"><b>{prop['bedrooms']}</b> Bedrooms</p>
                        </div>
                        <div>
                            <i class="fas fa-bath" style="font-size: 24px; color: #9a86fe;"></i>
                            <p style="margin: 5px 0 0 0;"><b>{prop['bathrooms']}</b> Bathrooms</p>
                        </div>
                    </div>
                    <div style="display: flex; justify-content: space-around;">
                        <div>
                            <i class="fas fa-ruler-combined" style="font-size: 24px; color: #9a86fe;"></i>
                            <p style="margin: 5px 0 0 0;"><b>{prop['size_sqm']}</b> sqm</p>
                        </div>
                        <div>
                            <i class="fas fa-home" style="font-size: 24px; color: #9a86fe;"></i>
                            <p style="margin: 5px 0 0 0;"><b>{prop['type']}</b></p>
                        </div>
                    </div>
                </div>
                <div style="margin: 20px 0; text-align: left;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                        <span>Expected ROI:</span>
                        <span style="font-weight: bold; color: #1e3c72;">{prop.get('roi_estimate', '5.0%')}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                        <span>Listed on:</span>
                        <span>{prop.get('date_added', 'May 10, 2025')}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <span>Verification Status:</span>
                        <span style="color: green; font-weight: bold;">{"✓ Verified" if prop.get("verified", False) else "Pending Verification"}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Quick actions
            st.markdown("<h4>Quick Actions</h4>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.button("Contact Agent", type="primary", use_container_width=True)
                st.button("Request Inspection", use_container_width=True)
            
            with col2:
                st.button("Save Property", use_container_width=True)
                st.button("Calculate Mortgage", use_container_width=True, on_click=lambda: setattr(st.session_state, "page", "Financing Hub"))
    
    with tab2:
        # Environmental risk analysis
        st.subheader("Environmental Risk Analysis")
        fig = plot_environmental_risks(prop['area'])
        if fig:
            st.pyplot(fig)
            
            # Risk recommendations
            st.subheader("Risk Recommendations")
            area_risks = next((r for r in load_risk_data() if r["name"] == prop['area']), None)
            
            if area_risks:
                for risk_type, value in [
                    ("Flood Risk", area_risks['flood_risk']),
                    ("Air Pollution", area_risks['air_pollution']),
                    ("Heat Island", area_risks['heat_island']),
                    ("Water Quality", area_risks['water_quality'])
                ]:
                    level, css_class = get_risk_level(value)
                    st.markdown(f"<div style='background-color: white; padding: 15px; border-radius: 8px; margin-bottom: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);'><h4 style='margin:0;'>{risk_type} <span class='{css_class}'>({level} - {value}%)</span></h4></div>", unsafe_allow_html=True)
                    
                    recommendation = ""
                    if level == "Low":
                        recommendation = "✅ No special measures needed. The property has minimal risk in this category."
                    elif level == "Medium":
                        recommendation = "⚠️ Consider basic precautions. We recommend discussing this with a building inspector."
                    else:  # High
                        recommendation = "🚨 Special measures recommended. Consult with our experts for specific mitigation strategies."
                    
                    st.markdown(f"<div style='padding: 0 15px 15px 15px;'>{recommendation}</div>", unsafe_allow_html=True)
    
    with tab3:
        # Neighborhood quality
        st.subheader("Neighborhood Quality Analysis")
        
        fig = plot_neighborhood_quality(prop['area'])
        if fig:
            st.pyplot(fig)
            
            # Neighborhood metrics
            neighborhood = next((n for n in load_neighborhoods() if n["name"] == prop['area']), None)
            
            if neighborhood:
                st.subheader("Detailed Ratings")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    for metric, value in [
                        ("Safety", neighborhood['safety']),
                        ("Schools", neighborhood['schools']),
                        ("Healthcare", neighborhood['healthcare'])
                    ]:
                        st.markdown(f"""
                        <div style="background-color: white; padding: 15px; border-radius: 8px; margin-bottom: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <span style="font-size: 16px; font-weight: 500;">{metric}</span>
                                <span style="font-weight: bold; color: #1e3c72;">{value}%</span>
                            </div>
                            <div style="margin-top: 8px; background-color: #f0f2f5; height: 8px; border-radius: 4px;">
                                <div style="width: {value}%; background-color: #9a86fe; height: 8px; border-radius: 4px;"></div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
                with col2:
                    for metric, value in [
                        ("Shopping", neighborhood['shopping']),
                        ("Transportation", neighborhood['transportation']),
                        ("Overall", sum([neighborhood['safety'], neighborhood['schools'], neighborhood['healthcare'], neighborhood['shopping'], neighborhood['transportation']]) / 5)
                    ]:
                        st.markdown(f"""
                        <div style="background-color: white; padding: 15px; border-radius: 8px; margin-bottom: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <span style="font-size: 16px; font-weight: 500;">{metric}</span>
                                <span style="font-weight: bold; color: #1e3c72;">{value if isinstance(value, int) else value:.1f}%</span>
                            </div>
                            <div style="margin-top: 8px; background-color: #f0f2f5; height: 8px; border-radius: 4px;">
                                <div style="width: {value if isinstance(value, int) else value:.1f}%; background-color: #9a86fe; height: 8px; border-radius: 4px;"></div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Neighborhood amenities
                st.subheader("Nearby Amenities")
                
                col1, col2, col3 = st.columns(3)
                
                amenities = {
                    "Schools": ["International School of Riyadh", "Al Nakheel Academy", "British International School"],
                    "Hospitals": ["King Faisal Hospital", "Saudi German Hospital", "Dr. Sulaiman Al Habib Hospital"],
                    "Shopping": ["Kingdom Centre Mall", "Al Nakheel Mall", "Granada Mall"]
                }
                
                with col1:
                    st.markdown("""
                    <div style="background-color: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                        <div style="font-size: 18px; font-weight: 500; margin-bottom: 10px; color: #1e3c72;">
                            <i class="fas fa-school" style="margin-right: 8px;"></i> Schools
                        </div>
                        <ul style="padding-left: 20px; margin: 0;">
                    """, unsafe_allow_html=True)
                    
                    for school in amenities["Schools"]:
                        st.markdown(f"<li>{school}</li>", unsafe_allow_html=True)
                    
                    st.markdown("</ul></div>", unsafe_allow_html=True)
                
                with col2:
                    st.markdown("""
                    <div style="background-color: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                        <div style="font-size: 18px; font-weight: 500; margin-bottom: 10px; color: #1e3c72;">
                            <i class="fas fa-hospital" style="margin-right: 8px;"></i> Hospitals
                        </div>
                        <ul style="padding-left: 20px; margin: 0;">
                    """, unsafe_allow_html=True)
                    
                    for hospital in amenities["Hospitals"]:
                        st.markdown(f"<li>{hospital}</li>", unsafe_allow_html=True)
                    
                    st.markdown("</ul></div>", unsafe_allow_html=True)
                
                with col3:
                    st.markdown("""
                    <div style="background-color: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                        <div style="font-size: 18px; font-weight: 500; margin-bottom: 10px; color: #1e3c72;">
                            <i class="fas fa-shopping-cart" style="margin-right: 8px;"></i> Shopping
                        </div>
                        <ul style="padding-left: 20px; margin: 0;">
                    """, unsafe_allow_html=True)
                    
                    for mall in amenities["Shopping"]:
                        st.markdown(f"<li>{mall}</li>", unsafe_allow_html=True)
                    
                    st.markdown("</ul></div>", unsafe_allow_html=True)
    
    with tab4:
        # Financing options
        st.subheader("Financing Calculator")
        
        col1, col2 = st.columns(2)
        
        with col1:
            property_price = st.number_input("Property Price", min_value=500000, max_value=10000000, value=prop['price'], step=10000, format="%d")
            down_payment_percent = st.slider("Down Payment (%)", min_value=10, max_value=50, value=20, step=5)
            loan_years = st.slider("Loan Term (Years)", min_value=5, max_value=30, value=25, step=5)
        
        with col2:
            interest_rate = st.slider("Interest Rate (%)", min_value=1.0, max_value=8.0, value=3.5, step=0.1)
            
            # Calculate down payment amount
            down_payment_amount = property_price * (down_payment_percent / 100)
            st.write(f"Down Payment Amount: **{down_payment_amount:,.0f} SAR**")
            
            # Calculate loan amount
            loan_amount = property_price - down_payment_amount
            st.write(f"Loan Amount: **{loan_amount:,.0f} SAR**")
        
        # Calculate mortgage
        mortgage_info = calculate_mortgage(property_price, down_payment_percent, interest_rate, loan_years)
        
        # Display mortgage information
        st.markdown("""
        <div style="background-color: #f0f8ff; padding: 20px; border-radius: 10px; margin: 20px 0;">
            <h3 style="color: #1e3c72; margin-top: 0;">Monthly Payment Estimate</h3>
            <h1 style="color: #9a86fe; font-size: 36px; margin: 10px 0;">{:,.0f} SAR/month</h1>
            <p>Based on {:.1f}% interest over {} years with {}% down payment</p>
        </div>
        """.format(mortgage_info['monthly_payment'], interest_rate, loan_years, down_payment_percent), unsafe_allow_html=True)
        
        # Additional mortgage details
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style="background-color: white; padding: 15px; border-radius: 8px; text-align: center; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                <h4 style="margin: 0; color: #666;">Loan Amount</h4>
                <h2 style="margin: 10px 0; color: #1e3c72;">{:,.0f} SAR</h2>
            </div>
            """.format(mortgage_info['loan_amount']), unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background-color: white; padding: 15px; border-radius: 8px; text-align: center; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                <h4 style="margin: 0; color: #666;">Total Interest</h4>
                <h2 style="margin: 10px 0; color: #1e3c72;">{:,.0f} SAR</h2>
            </div>
            """.format(mortgage_info['total_interest']), unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="background-color: white; padding: 15px; border-radius: 8px; text-align: center; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                <h4 style="margin: 0; color: #666;">Total Payment</h4>
                <h2 style="margin: 10px 0; color: #1e3c72;">{:,.0f} SAR</h2>
            </div>
            """.format(mortgage_info['total_payment']), unsafe_allow_html=True)
        
        # Bank options
        st.subheader("Available Financing Options")
        banks = load_banks()
        
        for i, bank in enumerate(banks):
            st.markdown(f"""
            <div style="background-color: white; padding: 20px; border-radius: 10px; margin-bottom: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                    <h3 style="margin: 0;">{bank['name']} <span style="font-size: 16px; color: #666; font-weight: normal;"> / {bank['name_ar']}</span></h3>
                    <button style="background-color: #9a86fe; color: white; border: none; padding: 8px 15px; border-radius: 5px; cursor: pointer;">Apply Now</button>
                </div>
                <div style="display: flex; flex-wrap: wrap; gap: 20px; margin-bottom: 15px;">
                    <div>
                        <span style="color: #666;">Interest Rate</span>
                        <h4 style="margin: 5px 0; color: #1e3c72;">{bank['interest_rate']}%</h4>
                    </div>
                    <div>
                        <span style="color: #666;">Max Loan Term</span>
                        <h4 style="margin: 5px 0; color: #1e3c72;">{bank['max_loan_term']} years</h4>
                    </div>
                    <div>
                        <span style="color: #666;">Min Down Payment</span>
                        <h4 style="margin: 5px 0; color: #1e3c72;">{bank['min_down_payment']}%</h4>
                    </div>
                    <div>
                        <span style="color: #666;">Processing Fee</span>
                        <h4 style="margin: 5px 0; color: #1e3c72;">{bank['processing_fee']}%</h4>
                    </div>
                </div>
                <div>
                    <h4 style="margin: 0 0 10px 0;">Special Offers</h4>
                    <div style="display: flex; flex-wrap: wrap; gap: 10px;">
            """, unsafe_allow_html=True)
            
            for offer in bank['special_offers']:
                st.markdown(f"""
                <span style="background-color: #f0f8ff; color: #1e3c72; padding: 5px 10px; border-radius: 5px;">
                    <i class="fas fa-tag" style="margin-right: 5px;"></i> {offer}
                </span>
                """, unsafe_allow_html=True)
            
            st.markdown("</div></div></div>", unsafe_allow_html=True)
        
        # Call to action
        st.button("Compare All Financing Options", type="primary", use_container_width=True, on_click=lambda: setattr(st.session_state, "page", "Financing Hub"))
    
    with tab5:
        # Transaction process
        st.subheader("Transaction Process Overview")
        
        st.markdown("""
        <div class="progress-steps">
            <div class="step">
                <div class="step-number">1</div>
                <div class="step-title">Property Selection</div>
            </div>
            <div class="step">
                <div class="step-number">2</div>
                <div class="step-title">Financing Approval</div>
            </div>
            <div class="step">
                <div class="step-number">3</div>
                <div class="step-title">Building Inspection</div>
            </div>
            <div class="step">
                <div class="step-number">4</div>
                <div class="step-title">Legal Verification</div>
            </div>
            <div class="step">
                <div class="step-number">5</div>
                <div class="step-title">Closing the Deal</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Process details
        st.subheader("Step-by-Step Process")
        
        with st.expander("1. Property Selection", expanded=True):
            st.markdown("""
            <div style="display: flex; align-items: flex-start; gap: 15px;">
                <div style="min-width: 60px; height: 60px; background-color: #9a86fe; color: white; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 24px; font-weight: bold;">1</div>
                <div>
                    <h4 style="margin: 0 0 10px 0;">Property Selection</h4>
                    <p>This step involves searching for and selecting a property that matches your requirements. You've already completed this step by selecting this property.</p>
                    <ul>
                        <li>Review property details and features</li>
                        <li>Consider location and neighborhood factors</li>
                        <li>Evaluate environmental risks</li>
                        <li>Check investment potential</li>
                    </ul>
                    <div style="background-color: #e6f4ff; padding: 10px; border-radius: 5px; margin-top: 10px;">
                        <b><i class="fas fa-info-circle" style="color: #1e3c72; margin-right: 5px;"></i> Status:</b> Completed
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with st.expander("2. Financing Approval"):
            st.markdown("""
            <div style="display: flex; align-items: flex-start; gap: 15px;">
                <div style="min-width: 60px; height: 60px; background-color: #9a86fe; color: white; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 24px; font-weight: bold;">2</div>
                <div>
                    <h4 style="margin: 0 0 10px 0;">Financing Approval</h4>
                    <p>Secure financing through one of our partner banks or your own financial institution.</p>
                    <ul>
                        <li>Compare financing options from multiple banks</li>
                        <li>Submit loan application with required documents</li>
                        <li>Receive pre-approval for the loan</li>
                        <li>Complete financial verification</li>
                    </ul>
                    <div style="display: flex; gap: 10px; margin-top: 15px;">
                        <button style="background-color: #9a86fe; color: white; border: none; padding: 8px 15px; border-radius: 5px; cursor: pointer; flex: 1;">Apply for Financing</button>
                        <button style="background-color: white; color: #1e3c72; border: 1px solid #1e3c72; padding: 8px 15px; border-radius: 5px; cursor: pointer; flex: 1;">Check Eligibility</button>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with st.expander("3. Building Inspection"):
            st.markdown("""
            <div style="display: flex; align-items: flex-start; gap: 15px;">
                <div style="min-width: 60px; height: 60px; background-color: #9a86fe; color: white; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 24px; font-weight: bold;">3</div>
                <div>
                    <h4 style="margin: 0 0 10px 0;">Building Inspection</h4>
                    <p>Arrange for a professional building inspection to ensure the property is in good condition.</p>
                    <ul>
                        <li>Choose a certified building inspector</li>
                        <li>Schedule and attend the inspection</li>
                        <li>Review comprehensive inspection report</li>
                        <li>Negotiate repairs or price adjustments if needed</li>
                    </ul>
                    <div style="display: flex; gap: 10px; margin-top: 15px;">
                        <button style="background-color: #9a86fe; color: white; border: none; padding: 8px 15px; border-radius: 5px; cursor: pointer; flex: 1;">Schedule Inspection</button>
                        <button style="background-color: white; color: #1e3c72; border: 1px solid #1e3c72; padding: 8px 15px; border-radius: 5px; cursor: pointer; flex: 1;">View Inspectors</button>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with st.expander("4. Legal Verification"):
            st.markdown("""
            <div style="display: flex; align-items: flex-start; gap: 15px;">
                <div style="min-width: 60px; height: 60px; background-color: #9a86fe; color: white; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 24px; font-weight: bold;">4</div>
                <div>
                    <h4 style="margin: 0 0 10px 0;">Legal Verification</h4>
                    <p>Ensure all legal aspects of the property are clear and legitimate through our integrated verification system.</p>
                    <ul>
                        <li>Title verification through official government systems</li>
                        <li>Verify property registration status</li>
                        <li>Check for any legal claims or disputes</li>
                        <li>Verify compliance with building regulations</li>
                    </ul>
                    <div style="display: flex; gap: 10px; margin-top: 15px;">
                        <button style="background-color: #9a86fe; color: white; border: none; padding: 8px 15px; border-radius: 5px; cursor: pointer; flex: 1;">Request Verification</button>
                        <button style="background-color: white; color: #1e3c72; border: 1px solid #1e3c72; padding: 8px 15px; border-radius: 5px; cursor: pointer; flex: 1;">Consult Legal Expert</button>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with st.expander("5. Closing the Deal"):
            st.markdown("""
            <div style="display: flex; align-items: flex-start; gap: 15px;">
                <div style="min-width: 60px; height: 60px; background-color: #9a86fe; color: white; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 24px; font-weight: bold;">5</div>
                <div>
                    <h4 style="margin: 0 0 10px 0;">Closing the Deal</h4>
                    <p>Complete all paperwork and transactions to finalize the property purchase.</p>
                    <ul>
                        <li>Sign purchase agreement and financing documents</li>
                        <li>Pay closing costs and fees</li>
                        <li>Transfer property ownership through Najiz system</li>
                        <li>Receive property keys and documentation</li>
                    </ul>
                    <div style="display: flex; gap: 10px; margin-top: 15px;">
                        <button style="background-color: #9a86fe; color: white; border: none; padding: 8px 15px; border-radius: 5px; cursor: pointer; flex: 1;">Schedule Closing</button>
                        <button style="background-color: white; color: #1e3c72; border: 1px solid #1e3c72; padding: 8px 15px; border-radius: 5px; cursor: pointer; flex: 1;">View Requirements</button>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Get started CTA
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("Start Transaction Process", type="primary", use_container_width=True, on_click=lambda: setattr(st.session_state, "page", "Buying Journey"))

# Environmental analysis page
def show_environmental_analysis():
    st.markdown("<h1>Environmental Risk Analysis / تحليل المخاطر البيئية</h1>", unsafe_allow_html=True)
    
    # Select area
    area = st.selectbox("Select Area / اختر المنطقة", 
                       ["Al Olaya", "Al Nakheel", "Hittin", "Al Malaz", "Al Naseem"])
    
    # Plot environmental risks
    fig = plot_environmental_risks(area)
    if fig:
        st.pyplot(fig)
    
    # Risk details
    st.subheader("Risk Details / تفاصيل المخاطر")
    
    area_risks = next((r for r in load_risk_data() if r["name"] == area), None)
    
    if area_risks:
        # Create a table with risk levels and descriptions
        risk_data = []
        
        for risk_type, value in [
            ("Flood Risk / مخاطر الفيضانات", area_risks['flood_risk']),
            ("Air Pollution / تلوث الهواء", area_risks['air_pollution']),
            ("Heat Island / الجزيرة الحرارية", area_risks['heat_island']),
            ("Water Quality / جودة المياه", area_risks['water_quality'])
        ]:
            level, _ = get_risk_level(value)
            
            # Get description based on level
            if level == "Low":
                description = "Minimal risk, no special precautions needed / مخاطر ضئيلة، لا حاجة لإجراءات خاصة"
            elif level == "Medium":
                description = "Moderate risk, basic precautions recommended / مخاطر متوسطة، يوصى باتخاذ احتياطات أساسية"
            else:  # High
                description = "High risk, significant precautions recommended / مخاطر عالية، يوصى باتخاذ احتياطات كبيرة"
            
            risk_data.append({
                "Risk Type": risk_type,
                "Level": level,
                "Value": f"{value}%",
                "Description": description
            })
        
        # Convert to DataFrame and display
        risk_df = pd.DataFrame(risk_data)
        st.table(risk_df)
        
        # Risk comparison with other areas
        st.subheader("Risk Comparison / مقارنة المخاطر")
        
        # Choose risk type to compare
        risk_type = st.selectbox("Select Risk Type / اختر نوع المخاطر",
                                ["flood_risk", "air_pollution", "heat_island", "water_quality"],
                                format_func=lambda x: {
                                    "flood_risk": "Flood Risk / مخاطر الفيضانات",
                                    "air_pollution": "Air Pollution / تلوث الهواء",
                                    "heat_island": "Heat Island / الجزيرة الحرارية",
                                    "water_quality": "Water Quality / جودة المياه"
                                }[x])
        
        # Create comparison data
        risk_comparison = [{"Area": r["name"], "Risk": r[risk_type]} for r in load_risk_data()]
        risk_comparison_df = pd.DataFrame(risk_comparison)
        
        # Sort by risk level
        risk_comparison_df = risk_comparison_df.sort_values("Risk", ascending=False)
        
        # Create bar chart
        chart = alt.Chart(risk_comparison_df).mark_bar().encode(
            x=alt.X('Risk:Q', title='Risk Level'),
            y=alt.Y('Area:N', title='Area', sort='-x'),
            color=alt.Color('Risk:Q', scale=alt.Scale(scheme='reds', domain=[0, 100])),
            tooltip=['Area', 'Risk']
        ).properties(
            width=600,
            height=300,
            title=f"{risk_type.replace('_', ' ').title()} Comparison"
        )
        
        st.altair_chart(chart, use_container_width=True)
        
        # AI-generated recommendations
        st.subheader("AI Risk Mitigation Recommendations / توصيات تخفيف المخاطر")
        
        # Use AI to generate personalized recommendations
        highest_risk = max(area_risks.items(), key=lambda x: x[1] if x[0] != 'name' else 0)
        highest_risk_name = {
            'flood_risk': 'Flood Risk',
            'air_pollution': 'Air Pollution',
            'heat_island': 'Heat Island',
            'water_quality': 'Water Quality'
        }.get(highest_risk[0], '')
        
        if highest_risk_name:
            # Use AI to generate recommendations
            risk_prompt = f"What are the best ways to mitigate {highest_risk_name} in {area}, Riyadh, which has a risk level of {highest_risk[1]}%? Give 4-5 specific recommendations. Be concise."
            
            with st.spinner("Generating recommendations..."):
                try:
                    recommendations = get_ai_response(risk_prompt)
                    st.write(recommendations)
                except Exception as e:
                    recommendations = f"""
                    فيما يلي بعض التوصيات لتخفيف مخاطر {highest_risk_name} في منطقة {area}:
                    
                    • تركيب أنظمة تهوية وتنقية الهواء داخل المنزل
                    • زراعة الأشجار والنباتات حول المنزل للمساعدة في تنقية الهواء
                    • استخدام مواد عازلة عالية الجودة للتقليل من تأثير الحرارة
                    • الاستثمار في أنظمة تدوير وتنقية المياه
                    • التواصل مع البلدية المحلية للتأكد من البنية التحتية للصرف
                    
                    Here are some recommendations to mitigate {highest_risk_name} risks in {area}:
                    
                    • Install indoor air ventilation and purification systems
                    • Plant trees and vegetation around the property to help filter the air
                    • Use high-quality insulation materials to reduce heat effects
                    • Invest in water recycling and purification systems
                    • Coordinate with local municipality to ensure proper drainage infrastructure
                    """
                    st.write(recommendations)

# Neighborhood comparison page
def show_neighborhood_comparison():
    st.markdown("<h1>Neighborhood Comparison / مقارنة الأحياء</h1>", unsafe_allow_html=True)
    
    # Select areas to compare
    st.subheader("Select Neighborhoods to Compare / اختر الأحياء للمقارنة")
    
    neighborhoods = load_neighborhoods()
    area_names = [n["name"] for n in neighborhoods]
    
    col1, col2 = st.columns(2)
    
    with col1:
        area1 = st.selectbox("Area 1", area_names, index=0)
    
    with col2:
        area2 = st.selectbox("Area 2", area_names, index=1 if len(area_names) > 1 else 0)
    
    # Get neighborhood data
    neighborhood1 = next((n for n in neighborhoods if n["name"] == area1), None)
    neighborhood2 = next((n for n in neighborhoods if n["name"] == area2), None)
    
    if neighborhood1 and neighborhood2:
        # Create comparison data for radar chart
        categories = ['Safety', 'Schools', 'Healthcare', 'Shopping', 'Transportation']
        
        # Data for area 1
        values1 = [
            neighborhood1['safety'], 
            neighborhood1['schools'], 
            neighborhood1['healthcare'], 
            neighborhood1['shopping'], 
            neighborhood1['transportation']
        ]
        
        # Data for area 2
        values2 = [
            neighborhood2['safety'], 
            neighborhood2['schools'], 
            neighborhood2['healthcare'], 
            neighborhood2['shopping'], 
            neighborhood2['transportation']
        ]
        
        # Number of variables
        N = len(categories)
        
        # Create angles for each category
        angles = [n / float(N) * 2 * np.pi for n in range(N)]
        angles += angles[:1]  # Close the loop
        
        # Values need to be closed too
        values1 += values1[:1]
        values2 += values2[:1]
        
        # Create the plot
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
        
        # Draw one axis per variable and add labels
        plt.xticks(angles[:-1], categories, size=12)
        
        # Draw the charts
        ax.plot(angles, values1, linewidth=2, linestyle='solid', color='#9a86fe', label=area1)
        ax.fill(angles, values1, alpha=0.1, color='#9a86fe')
        
        ax.plot(angles, values2, linewidth=2, linestyle='solid', color='#f39c12', label=area2)
        ax.fill(angles, values2, alpha=0.1, color='#f39c12')
        
        # Set y-limits
        ax.set_ylim(0, 100)
        
        # Add legend
        plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
        
        # Add title
        plt.title(f'Neighborhood Comparison: {area1} vs {area2}', size=15, y=1.1)
        
        # Show the chart
        st.pyplot(fig)
        
        # Show detailed comparison
        st.subheader("Detailed Comparison / مقارنة تفصيلية")
        
        # Create comparison table
        comparison_data = []
        
        for metric in ['safety', 'schools', 'healthcare', 'shopping', 'transportation']:
            metric_name = metric.capitalize()
            value1 = neighborhood1[metric]
            value2 = neighborhood2[metric]
            difference = value1 - value2
            winner = area1 if difference > 0 else area2 if difference < 0 else "Tie"
            
            comparison_data.append({
                "Metric": metric_name,
                f"{area1}": f"{value1}%",
                f"{area2}": f"{value2}%",
                "Difference": f"{abs(difference)}%",
                "Better Area": winner
            })
        
        # Add average row
        avg1 = sum([neighborhood1[metric] for metric in ['safety', 'schools', 'healthcare', 'shopping', 'transportation']]) / 5
        avg2 = sum([neighborhood2[metric] for metric in ['safety', 'schools', 'healthcare', 'shopping', 'transportation']]) / 5
        avg_diff = avg1 - avg2
        avg_winner = area1 if avg_diff > 0 else area2 if avg_diff < 0 else "Tie"
        
        comparison_data.append({
            "Metric": "Overall Average",
            f"{area1}": f"{avg1:.1f}%",
            f"{area2}": f"{avg2:.1f}%",
            "Difference": f"{abs(avg_diff):.1f}%",
            "Better Area": avg_winner
        })
        
        # Convert to DataFrame and display
        comparison_df = pd.DataFrame(comparison_data)
        st.table(comparison_df)
        
        # Environmental risks comparison
        st.subheader("Environmental Risks Comparison / مقارنة المخاطر البيئية")
        
        # Get risk data
        risk_data = load_risk_data()
        risk1 = next((r for r in risk_data if r["name"] == area1), None)
        risk2 = next((r for r in risk_data if r["name"] == area2), None)
        
        if risk1 and risk2:
            # Create comparison data
            risk_comparison_data = []
            
            for risk_type in ['flood_risk', 'air_pollution', 'heat_island', 'water_quality']:
                risk_name = risk_type.replace('_', ' ').title()
                value1 = risk1[risk_type]
                value2 = risk2[risk_type]
                difference = value2 - value1  # Note: Lower risk is better, so the sign is reversed
                winner = area1 if difference > 0 else area2 if difference < 0 else "Tie"
                
                risk_comparison_data.append({
                    "Risk Type": risk_name,
                    f"{area1}": f"{value1}%",
                    f"{area2}": f"{value2}%",
                    "Difference": f"{abs(difference)}%",
                    "Better Area": winner
                })
            
            # Convert to DataFrame and display
            risk_comparison_df = pd.DataFrame(risk_comparison_data)
            st.table(risk_comparison_df)
            
            # Create bar chart for visual comparison
            risks = ['Flood Risk', 'Air Pollution', 'Heat Island', 'Water Quality']
            values1 = [risk1['flood_risk'], risk1['air_pollution'], risk1['heat_island'], risk1['water_quality']]
            values2 = [risk2['flood_risk'], risk2['air_pollution'], risk2['heat_island'], risk2['water_quality']]
            
            # Create comparison chart
            fig, ax = plt.subplots(figsize=(10, 6))
            
            x = np.arange(len(risks))
            width = 0.35
            
            # Plot bars
            bars1 = ax.bar(x - width/2, values1, width, label=area1, color='#9a86fe', alpha=0.7)
            bars2 = ax.bar(x + width/2, values2, width, label=area2, color='#f39c12', alpha=0.7)
            
            # Add labels and title
            ax.set_xlabel('Risk Type')
            ax.set_ylabel('Risk Level (%)')
            ax.set_title('Environmental Risk Comparison')
            ax.set_xticks(x)
            ax.set_xticklabels(risks)
            ax.legend()
            
            # Set y-limit
            ax.set_ylim(0, 100)
            
            # Add risk level labels
            for bars in [bars1, bars2]:
                for bar in bars:
                    height = bar.get_height()
                    level, _ = get_risk_level(height)
                    ax.annotate(f'{level}',
                                xy=(bar.get_x() + bar.get_width() / 2, height),
                                xytext=(0, 3),  # 3 points vertical offset
                                textcoords="offset points",
                                ha='center', va='bottom')
            
            # Show the chart
            st.pyplot(fig)
        
        # Nearby amenities comparison
        st.subheader("Nearby Amenities Comparison / مقارنة المرافق القريبة")
        
        # Sample amenities data (in a real app, this would come from a database)
        amenities_data = {
            "Al Olaya": {
                "Schools": ["International School of Riyadh", "Al Olaya Academy", "British International School"],
                "Hospitals": ["King Faisal Specialist Hospital", "Saudi German Hospital", "Dr. Sulaiman Al Habib Hospital"],
                "Shopping": ["Kingdom Centre Mall", "Olaya Malls Complex", "Centria Mall"]
            },
            "Al Nakheel": {
                "Schools": ["American International School", "Al Nakheel Academy", "French International School"],
                "Hospitals": ["Al Nakheel Medical Center", "Saudi German Hospital", "Dr. Sulaiman Al Habib Hospital"],
                "Shopping": ["Al Nakheel Mall", "Hayat Mall", "Localizer Mall"]
            },
            "Hittin": {
                "Schools": ["Hittin International School", "Al Hittin Academy", "KAUST School"],
                "Hospitals": ["Hittin Medical Center", "Healthcare Clinic", "Family Medical Center"],
                "Shopping": ["Riyadh Front", "Al Hittin Plaza", "U-Walk"]
            },
            "Al Malaz": {
                "Schools": ["Al Malaz Public School", "Eastern Academy", "Technical College"],
                "Hospitals": ["Al Malaz Hospital", "Security Forces Hospital", "Red Crescent Center"],
                "Shopping": ["Al Malaz Commercial Center", "Al Makan Mall", "Traditional Souq"]
            },
            "Al Naseem": {
                "Schools": ["Al Naseem Academy", "Modern Education School", "Technical Institute"],
                "Hospitals": ["Al Naseem Medical Center", "Family Clinic", "Eastern Hospital"],
                "Shopping": ["Al Naseem Plaza", "Corner Mall", "Eastern Market"]
            }
        }
        
        # Get amenities for selected areas
        amenities1 = amenities_data.get(area1, {"Schools": [], "Hospitals": [], "Shopping": []})
        amenities2 = amenities_data.get(area2, {"Schools": [], "Hospitals": [], "Shopping": []})
        
        # Create side-by-side comparison
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"<h4>{area1}</h4>", unsafe_allow_html=True)
            
            st.markdown("""
            <div style="background-color: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); margin-bottom: 10px;">
                <div style="font-size: 16px; font-weight: 500; margin-bottom: 10px; color: #1e3c72;">
                    <i class="fas fa-school" style="margin-right: 8px;"></i> Schools
                </div>
                <ul style="padding-left: 20px; margin: 0;">
            """, unsafe_allow_html=True)
            
            for school in amenities1["Schools"]:
                st.markdown(f"<li>{school}</li>", unsafe_allow_html=True)
            
            st.markdown("</ul></div>", unsafe_allow_html=True)
            
            st.markdown("""
            <div style="background-color: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); margin-bottom: 10px;">
                <div style="font-size: 16px; font-weight: 500; margin-bottom: 10px; color: #1e3c72;">
                    <i class="fas fa-hospital" style="margin-right: 8px;"></i> Hospitals
                </div>
                <ul style="padding-left: 20px; margin: 0;">
            """, unsafe_allow_html=True)
            
            for hospital in amenities1["Hospitals"]:
                st.markdown(f"<li>{hospital}</li>", unsafe_allow_html=True)
            
            st.markdown("</ul></div>", unsafe_allow_html=True)
            
            st.markdown("""
            <div style="background-color: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                <div style="font-size: 16px; font-weight: 500; margin-bottom: 10px; color: #1e3c72;">
                    <i class="fas fa-shopping-cart" style="margin-right: 8px;"></i> Shopping
                </div>
                <ul style="padding-left: 20px; margin: 0;">
            """, unsafe_allow_html=True)
            
            for mall in amenities1["Shopping"]:
                st.markdown(f"<li>{mall}</li>", unsafe_allow_html=True)
            
            st.markdown("</ul></div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"<h4>{area2}</h4>", unsafe_allow_html=True)
            
            st.markdown("""
            <div style="background-color: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); margin-bottom: 10px;">
                <div style="font-size: 16px; font-weight: 500; margin-bottom: 10px; color: #1e3c72;">
                    <i class="fas fa-school" style="margin-right: 8px;"></i> Schools
                </div>
                <ul style="padding-left: 20px; margin: 0;">
            """, unsafe_allow_html=True)
            
            for school in amenities2["Schools"]:
                st.markdown(f"<li>{school}</li>", unsafe_allow_html=True)
            
            st.markdown("</ul></div>", unsafe_allow_html=True)
            
            st.markdown("""
            <div style="background-color: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); margin-bottom: 10px;">
                <div style="font-size: 16px; font-weight: 500; margin-bottom: 10px; color: #1e3c72;">
                    <i class="fas fa-hospital" style="margin-right: 8px;"></i> Hospitals
                </div>
                <ul style="padding-left: 20px; margin: 0;">
            """, unsafe_allow_html=True)
            
            for hospital in amenities2["Hospitals"]:
                st.markdown(f"<li>{hospital}</li>", unsafe_allow_html=True)
            
            st.markdown("</ul></div>", unsafe_allow_html=True)
            
            st.markdown("""
            <div style="background-color: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                <div style="font-size: 16px; font-weight: 500; margin-bottom: 10px; color: #1e3c72;">
                    <i class="fas fa-shopping-cart" style="margin-right: 8px;"></i> Shopping
                </div>
                <ul style="padding-left: 20px; margin: 0;">
            """, unsafe_allow_html=True)
            
            for mall in amenities2["Shopping"]:
                st.markdown(f"<li>{mall}</li>", unsafe_allow_html=True)
            
            st.markdown("</ul></div>", unsafe_allow_html=True)
        
        # AI neighborhood recommendation
        st.subheader("AI Neighborhood Recommendation / توصية الذكاء الاصطناعي للحي")
        
        with st.expander("Get Personalized Recommendation", expanded=False):
            # Form for user preference
            st.write("Please rank your priorities to get a personalized recommendation:")
            
            col1, col2 = st.columns(2)
            
            priorities = {}
            
            with col1:
                priorities["safety"] = st.slider("Safety / الأمان", 1, 5, 3)
                priorities["schools"] = st.slider("Schools / المدارس", 1, 5, 3)
                priorities["healthcare"] = st.slider("Healthcare / الرعاية الصحية", 1, 5, 3)
            
            with col2:
                priorities["shopping"] = st.slider("Shopping / التسوق", 1, 5, 3)
                priorities["transportation"] = st.slider("Transportation / المواصلات", 1, 5, 3)
                priorities["environmental"] = st.slider("Environmental Safety / السلامة البيئية", 1, 5, 3)
            
            price_range = st.select_slider("Price Range / نطاق السعر", options=["Budget", "Mid-range", "Luxury"], value="Mid-range")
            family_size = st.slider("Family Size / حجم العائلة", 1, 10, 4)
            
            if st.button("Get Recommendation", type="primary"):
                # Calculate weighted scores
                scores = {}
                
                for n in neighborhoods:
                    area_name = n["name"]
                    
                    # Calculate environmental score (inverse of risk - higher is better)
                    risk = next((r for r in risk_data if r["name"] == area_name), None)
                    if risk:
                        env_score = 100 - (sum([risk['flood_risk'], risk['air_pollution'], risk['heat_island'], risk['water_quality']]) / 4)
                    else:
                        env_score = 50  # Default
                    
                    # Calculate weighted score
                    score = (
                        priorities["safety"] * n["safety"] +
                        priorities["schools"] * n["schools"] +
                        priorities["healthcare"] * n["healthcare"] +
                        priorities["shopping"] * n["shopping"] +
                        priorities["transportation"] * n["transportation"] +
                        priorities["environmental"] * env_score
                    ) / sum(priorities.values())
                    
                    # Adjust for price preference
                    if price_range == "Budget" and area_name in ["Al Naseem", "Al Malaz"]:
                        score += 15
                    elif price_range == "Mid-range" and area_name in ["Hittin"]:
                        score += 15
                    elif price_range == "Luxury" and area_name in ["Al Olaya", "Al Nakheel"]:
                        score += 15
                    
                    # Adjust for family size
                    if family_size >= 6 and area_name in ["Al Nakheel", "Hittin"]:
                        score += 10
                    elif 3 <= family_size <= 5 and area_name in ["Al Olaya", "Al Naseem"]:
                        score += 5
                    elif family_size <= 2 and area_name in ["Al Olaya"]:
                        score += 10
                    
                    scores[area_name] = score
                
                # Find best neighborhood
                best_neighborhood = max(scores, key=scores.get)
                best_score = scores[best_neighborhood]
                
                # Display recommendation
                st.markdown(f"""
                <div style="background-color: #f0f8ff; padding: 20px; border-radius: 10px; margin-top: 20px;">
                    <h3 style="color: #1e3c72; margin-top: 0;">Our Recommendation</h3>
                    <h2 style="color: #9a86fe; margin: 10px 0;">{best_neighborhood}</h2>
                    <p>Based on your preferences, we recommend {best_neighborhood} as the best neighborhood for you with a match score of {best_score:.1f}%.</p>
                    <p>Would you like to see available properties in {best_neighborhood}?</p>
                    <button style="background-color: #9a86fe; color: white; border: none; padding: 8px 15px; border-radius: 5px; cursor: pointer;">View Properties in {best_neighborhood}</button>
                </div>
                """, unsafe_allow_html=True)
                
                # Show explanation
                st.markdown("<br>", unsafe_allow_html=True)
                st.subheader("Why We Recommended This Neighborhood")
                
                neighborhood_details = next((n for n in neighborhoods if n["name"] == best_neighborhood), None)
                
                if neighborhood_details:
                    # Create explanation text
                    explanation = f"{best_neighborhood} scored highest based on your priorities. "
                    
                    # Add highest scoring attributes
                    high_scores = []
                    for attr in ["safety", "schools", "healthcare", "shopping", "transportation"]:
                        if neighborhood_details[attr] >= 85:
                            high_scores.append(attr.capitalize())
                    
                    if high_scores:
                        explanation += f"It excels in {', '.join(high_scores)}. "
                    
                    # Add price range explanation
                    if price_range == "Budget" and best_neighborhood in ["Al Naseem", "Al Malaz"]:
                        explanation += "It offers great value for budget-conscious buyers. "
                    elif price_range == "Mid-range" and best_neighborhood in ["Hittin"]:
                        explanation += "It provides an excellent balance of quality and affordability. "
                    elif price_range == "Luxury" and best_neighborhood in ["Al Olaya", "Al Nakheel"]:
                        explanation += "It offers premium living experience with high-end amenities. "
                    
                    # Add family size explanation
                    if family_size >= 6 and best_neighborhood in ["Al Nakheel", "Hittin"]:
                        explanation += "It's ideal for larger families with spacious properties. "
                    elif 3 <= family_size <= 5 and best_neighborhood in ["Al Olaya", "Al Naseem"]:
                        explanation += "It's perfect for medium-sized families with good schools and amenities. "
                    elif family_size <= 2 and best_neighborhood in ["Al Olaya"]:
                        explanation += "It's great for singles or couples with urban lifestyle preferences. "
                    
                    st.write(explanation)
                    
                    # Show top 3 properties in that neighborhood
                    st.subheader(f"Top Properties in {best_neighborhood}")
                    
                    properties = [p for p in load_properties() if p["area"] == best_neighborhood]
                    if properties:
                        cols = st.columns(min(3, len(properties)))
                        for i, prop in enumerate(properties[:3]):
                            with cols[i]:
                                display_property_card(prop)
                    else:
                        st.info(f"No properties available in {best_neighborhood} at the moment.")

# Financing hub page
def show_financing_hub():
    st.markdown("<h1>Financing Hub / مركز التمويل</h1>", unsafe_allow_html=True)
    
    # Tabs for different financing options
    tabs = st.tabs(["Mortgage Calculator", "Bank Comparison", "Financing Assistant"])
    
    with tabs[0]:
        st.subheader("Mortgage Calculator / حاسبة الرهن العقاري")
        
        col1, col2 = st.columns(2)
        
        with col1:
            property_price = st.number_input("Property Price / سعر العقار", min_value=500000, max_value=10000000, value=2000000, step=50000, format="%d")
            down_payment_percent = st.slider("Down Payment (%) / الدفعة المقدمة", min_value=10, max_value=50, value=20, step=5)
            loan_years = st.slider("Loan Term (Years) / مدة القرض بالسنوات", min_value=5, max_value=30, value=25, step=5)
        
        with col2:
            interest_rate = st.slider("Interest Rate (%) / معدل الفائدة", min_value=1.0, max_value=8.0, value=3.5, step=0.1)
            
            # Calculate down payment amount
            down_payment_amount = property_price * (down_payment_percent / 100)
            st.write(f"Down Payment Amount / مبلغ الدفعة المقدمة: **{down_payment_amount:,.0f} SAR**")
            
            # Calculate loan amount
            loan_amount = property_price - down_payment_amount
            st.write(f"Loan Amount / مبلغ القرض: **{loan_amount:,.0f} SAR**")
        
        # Calculate mortgage
        mortgage_info = calculate_mortgage(property_price, down_payment_percent, interest_rate, loan_years)
        
        # Display mortgage information
        st.markdown("""
        <div style="background-color: #f0f8ff; padding: 20px; border-radius: 10px; margin: 20px 0;">
            <h3 style="color: #1e3c72; margin-top: 0;">Monthly Payment Estimate / تقدير الدفعة الشهرية</h3>
            <h1 style="color: #9a86fe; font-size: 36px; margin: 10px 0;">{:,.0f} SAR/month</h1>
            <p>Based on {:.1f}% interest over {} years with {}% down payment</p>
        </div>
        """.format(mortgage_info['monthly_payment'], interest_rate, loan_years, down_payment_percent), unsafe_allow_html=True)
        
        # Additional mortgage details
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style="background-color: white; padding: 15px; border-radius: 8px; text-align: center; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                <h4 style="margin: 0; color: #666;">Total Loan Amount / إجمالي مبلغ القرض</h4>
                <h2 style="margin: 10px 0; color: #1e3c72;">{:,.0f} SAR</h2>
            </div>
            """.format(mortgage_info['loan_amount']), unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background-color: white; padding: 15px; border-radius: 8px; text-align: center; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                <h4 style="margin: 0; color: #666;">Total Interest / إجمالي الفائدة</h4>
                <h2 style="margin: 10px 0; color: #1e3c72;">{:,.0f} SAR</h2>
            </div>
            """.format(mortgage_info['total_interest']), unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="background-color: white; padding: 15px; border-radius: 8px; text-align: center; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                <h4 style="margin: 0; color: #666;">Total Payment / إجمالي المدفوعات</h4>
                <h2 style="margin: 10px 0; color: #1e3c72;">{:,.0f} SAR</h2>
            </div>
            """.format(mortgage_info['total_payment']), unsafe_allow_html=True)
        
        # Amortization schedule
        st.subheader("Amortization Schedule / جدول الإطفاء")
        
        with st.expander("View Full Amortization Schedule", expanded=False):
            # Create amortization schedule
            amortization_data = []
            remaining_balance = mortgage_info['loan_amount']
            monthly_interest_rate = interest_rate / 100 / 12
            monthly_payment = mortgage_info['monthly_payment']
            
            for year in range(1, loan_years + 1):
                yearly_principal = 0
                yearly_interest = 0
                
                for month in range(1, 13):
                    # Calculate interest for this month
                    month_interest = remaining_balance * monthly_interest_rate
                    
                    # Calculate principal for this month
                    month_principal = monthly_payment - month_interest
                    
                    # Update remaining balance
                    remaining_balance -= month_principal
                    
                    # Add to yearly totals
                    yearly_principal += month_principal
                    yearly_interest += month_interest
                
                # Add yearly data to amortization schedule
                amortization_data.append({
                    "Year": year,
                    "Principal Paid": yearly_principal,
                    "Interest Paid": yearly_interest,
                    "Total Paid": yearly_principal + yearly_interest,
                    "Remaining Balance": max(0, remaining_balance)
                })
            
            # Convert to DataFrame
            amortization_df = pd.DataFrame(amortization_data)
            
            # Format columns
            amortization_df["Principal Paid"] = amortization_df["Principal Paid"].map("SAR {:,.0f}".format)
            amortization_df["Interest Paid"] = amortization_df["Interest Paid"].map("SAR {:,.0f}".format)
            amortization_df["Total Paid"] = amortization_df["Total Paid"].map("SAR {:,.0f}".format)
            amortization_df["Remaining Balance"] = amortization_df["Remaining Balance"].map("SAR {:,.0f}".format)
            
            # Display the table
            st.table(amortization_df)
        
        # Payment visualization
        st.subheader("Payment Visualization / تصور المدفوعات")
        
        # Create data for payment visualization
        principal_amount = mortgage_info['loan_amount']
        interest_amount = mortgage_info['total_interest']
        down_payment_amount = property_price * (down_payment_percent / 100)
        
        # Create pie chart
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Create data for pie chart
        labels = ['Principal', 'Interest', 'Down Payment']
        sizes = [principal_amount, interest_amount, down_payment_amount]
        colors = ['#9a86fe', '#f39c12', '#2ecc71']
        explode = (0.1, 0, 0)  # explode the 1st slice (Principal)
        
        # Plot the pie chart
        ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
               shadow=True, startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        
        # Add title
        plt.title('Mortgage Payment Breakdown')
        
        # Show the chart
        st.pyplot(fig)
        
        # Affordability analysis
        st.subheader("Affordability Analysis / تحليل القدرة على تحمل التكاليف")
        
        monthly_income = st.number_input("Monthly Household Income / الدخل الشهري للأسرة", min_value=5000, max_value=100000, value=20000, step=1000, format="%d")
        
        # Calculate debt-to-income ratio
        dti_ratio = (monthly_payment := mortgage_info['monthly_payment']) / monthly_income * 100
        
        # Determine affordability status
        if dti_ratio <= 30:
            affordability_status = "Affordable / ميسور التكلفة"
            affordability_color = "#2ecc71"  # Green
        elif dti_ratio <= 40:
            affordability_status = "Moderately Affordable / معتدل التكلفة"
            affordability_color = "#f39c12"  # Orange
        else:
            affordability_status = "Potentially Unaffordable / قد يكون غير ميسور التكلفة"
            affordability_color = "#e74c3c"  # Red
        
        # Display affordability card
        st.markdown(f"""
        <div style="background-color: white; padding: 20px; border-radius: 10px; margin: 20px 0; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
            <h3 style="color: #1e3c72; margin-top: 0;">Affordability Status / حالة القدرة على تحمل التكاليف</h3>
            <h2 style="color: {affordability_color}; margin: 10px 0;">{affordability_status}</h2>
            <p>Your monthly mortgage payment would be <b>{monthly_payment:,.0f} SAR</b>, which is <b>{dti_ratio:.1f}%</b> of your monthly income.</p>
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-top: 15px;">
                <p style="margin: 0;"><i class="fas fa-info-circle" style="color: #1e3c72; margin-right: 5px;"></i> <b>Recommendation:</b> Financial experts recommend your mortgage payment should not exceed 30% of your monthly income.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Show other expenses to consider
        with st.expander("Other Expenses to Consider / مصاريف أخرى يجب مراعاتها", expanded=False):
            st.markdown("""
            When budgeting for your home purchase, remember to consider these additional expenses:
            
            1. **Property Tax / ضريبة الممتلكات**: Typically around 2.5% of the property value.
            2. **Home Insurance / تأمين المنزل**: Approximately 0.5% of the property value annually.
            3. **Maintenance / الصيانة**: Budget about 1% of the property value annually for maintenance costs.
            4. **Utilities / المرافق**: Electricity, water, and internet services.
            5. **Homeowners Association Fees / رسوم جمعية الملاك**: If applicable.
            
            These costs can add significantly to your monthly housing expenses, so it's important to factor them into your budget planning.
            """)
    
    with tabs[1]:
        st.subheader("Bank Comparison / مقارنة البنوك")
        
        # Load banks data
        banks = load_banks()
        
        # Display comparison table
        comparison_data = []
        
        for bank in banks:
            comparison_data.append({
                "Bank": bank["name"],
                "Interest Rate": f"{bank['interest_rate']}%",
                "Max Loan Term": f"{bank['max_loan_term']} years",
                "Min Down Payment": f"{bank['min_down_payment']}%",
                "Processing Fee": f"{bank['processing_fee']}%"
            })
        
        # Convert to DataFrame
        comparison_df = pd.DataFrame(comparison_data)
        st.table(comparison_df)
        
        # Detailed bank information
        st.subheader("Detailed Bank Information / معلومات مفصلة عن البنوك")
        
        for bank in banks:
            with st.expander(f"{bank['name']} / {bank['name_ar']}", expanded=False):
                col1, col2 = st.columns([1, 3])
                
                with col1:
                    st.image(bank['logo'], width=150)
                
                with col2:
                    st.markdown(f"""
                    <h3 style="margin-top: 0;">{bank['name']} / {bank['name_ar']}</h3>
                    <div style="display: flex; flex-wrap: wrap; gap: 20px; margin: 15px 0;">
                        <div>
                            <span style="color: #666;">Interest Rate / معدل الفائدة</span>
                            <h4 style="margin: 5px 0; color: #1e3c72;">{bank['interest_rate']}%</h4>
                        </div>
                        <div>
                            <span style="color: #666;">Max Loan Term / الحد الأقصى لمدة القرض</span>
                            <h4 style="margin: 5px 0; color: #1e3c72;">{bank['max_loan_term']} years</h4>
                        </div>
                        <div>
                            <span style="color: #666;">Min Down Payment / الحد الأدنى للدفعة المقدمة</span>
                            <h4 style="margin: 5px 0; color: #1e3c72;">{bank['min_down_payment']}%</h4>
                        </div>
                        <div>
                            <span style="color: #666;">Processing Fee / رسوم المعالجة</span>
                            <h4 style="margin: 5px 0; color: #1e3c72;">{bank['processing_fee']}%</h4>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Special offers
                    st.markdown("<h4 style='margin-bottom: 10px;'>Special Offers / عروض خاصة</h4>", unsafe_allow_html=True)
                    
                    offers_html = "<div style='display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 15px;'>"
                    
                    for offer in bank['special_offers']:
                        offers_html += f"""
                        <span style="background-color: #f0f8ff; color: #1e3c72; padding: 5px 10px; border-radius: 5px;">
                            <i class="fas fa-tag" style="margin-right: 5px;"></i> {offer}
                        </span>
                        """
                    
                    offers_html += "</div>"
                    st.markdown(offers_html, unsafe_allow_html=True)
                    
                    # Requirements
                    st.markdown("<h4 style='margin-bottom: 10px;'>Requirements / المتطلبات</h4>", unsafe_allow_html=True)
                    
                    requirements_html = "<ul style='margin-top: 0;'>"
                    
                    for req in bank['requirements']:
                        requirements_html += f"<li>{req}</li>"
                    
                    requirements_html += "</ul>"
                    st.markdown(requirements_html, unsafe_allow_html=True)
                    
                    # Apply button
                    st.button(f"Apply with {bank['name']}", key=f"apply_{bank['name']}")
    
    with tabs[2]:
        st.subheader("Financing Assistant / مساعد التمويل")
        
        # Introduction
        st.markdown("""
        Our AI-powered Financing Assistant can help you find the best financing options based on your specific situation.
        Just answer a few questions, and we'll provide personalized recommendations.
        
        مساعد التمويل المدعوم بالذكاء الاصطناعي يمكنه مساعدتك في العثور على أفضل خيارات التمويل بناءً على وضعك الخاص.
        فقط أجب على بعض الأسئلة، وسنقدم لك توصيات مخصصة.
        """)
        
        # Questionnaire
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("Tell Us About Your Situation / أخبرنا عن وضعك")
        
        col1, col2 = st.columns(2)
        
        with col1:
            monthly_income = st.number_input("Monthly Income / الدخل الشهري", min_value=5000, max_value=100000, value=20000, step=1000, format="%d")
            employment_type = st.selectbox("Employment Type / نوع العمل", ["Government Employee", "Private Sector", "Self-Employed", "Retired", "Other"])
            employment_duration = st.slider("Years at Current Job / سنوات في الوظيفة الحالية", min_value=0, max_value=30, value=3, step=1)
        
        with col2:
            savings = st.number_input("Available Savings / المدخرات المتاحة", min_value=0, max_value=10000000, value=500000, step=50000, format="%d")
            credit_score = st.select_slider("Credit Status / حالة الائتمان", options=["Poor", "Fair", "Good", "Excellent"], value="Good")
            nationality = st.selectbox("Nationality / الجنسية", ["Saudi Citizen", "Expatriate with Permanent Residency", "Expatriate with Temporary Residency"])
        
        # Property information
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("Property Information / معلومات العقار")
        
        col1, col2 = st.columns(2)
        
        with col1:
            property_price = st.number_input("Target Property Price / سعر العقار المستهدف", min_value=500000, max_value=10000000, value=2000000, step=50000, format="%d")
            property_type = st.selectbox("Property Type / نوع العقار", ["Villa", "Apartment", "Penthouse", "House", "Townhouse"])
        
        with col2:
            property_location = st.selectbox("Property Location / موقع العقار", ["Al Olaya", "Al Nakheel", "Hittin", "Al Malaz", "Al Naseem", "Other Riyadh Areas", "Outside Riyadh"])
            purpose = st.radio("Purchase Purpose / الغرض من الشراء", ["Primary Residence", "Investment"])
        
        # Financing preferences
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("Financing Preferences / تفضيلات التمويل")
        
        col1, col2 = st.columns(2)
        
        with col1:
            down_payment_percent = st.slider("Down Payment (%) / الدفعة المقدمة", min_value=10, max_value=50, value=20, step=5)
            preferred_term = st.slider("Preferred Loan Term (Years) / المدة المفضلة للقرض بالسنوات", min_value=5, max_value=30, value=25, step=5)
        
        with col2:
            rate_preference = st.radio("Rate Preference / تفضيل المعدل", ["Fixed Rate", "Variable Rate", "Islamic Financing", "No Preference"])
            monthly_payment_max = st.number_input("Maximum Monthly Payment / الحد الأقصى للدفعة الشهرية", min_value=1000, max_value=50000, value=8000, step=500, format="%d")
        
        # Get recommendations
        if st.button("Get Financing Recommendations / الحصول على توصيات التمويل", type="primary"):
            with st.spinner("Analyzing your information..."):
                # Simulate processing time
                time.sleep(1)
                
                # Calculate some metrics
                loan_amount = property_price * (1 - down_payment_percent / 100)
                dti_ratio = monthly_payment_max / monthly_income * 100
                ltv_ratio = loan_amount / property_price * 100
                
                # Determine eligibility
                eligible = True
                eligibility_notes = []
                
                if dti_ratio > 45:
                    eligible = False
                    eligibility_notes.append("Your debt-to-income ratio is too high (should be under 45%).")
                
                if ltv_ratio > 90:
                    eligible = False
                    eligibility_notes.append("Your loan-to-value ratio is too high (should be under 90%).")
                
                if employment_duration < 1 and employment_type in ["Private Sector", "Self-Employed"]:
                    eligible = False
                    eligibility_notes.append("You need at least 1 year of employment history in your current job.")
                
                if credit_score == "Poor":
                    eligible = False
                    eligibility_notes.append("Your credit score is too low for most lenders.")
                
                if monthly_income < 8000:
                    eligible = False
                    eligibility_notes.append("Your monthly income is below the minimum required by most lenders (SAR 8,000).")
                
                # Display eligibility status
                if eligible:
                    st.markdown("""
                    <div style="background-color: #e6f7ff; border-left: 4px solid #1e90ff; padding: 15px; margin-bottom: 20px;">
                        <h3 style="margin-top: 0; color: #1e90ff;">✅ Good news! You are likely eligible for financing.</h3>
                        <p style="margin-bottom: 0;">Based on the information you provided, you should be eligible for several financing options from our partner banks.</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style="background-color: #fff2e6; border-left: 4px solid #ff9933; padding: 15px; margin-bottom: 20px;">
                        <h3 style="margin-top: 0; color: #ff9933;">⚠️ There may be some challenges with your financing.</h3>
                        <p>Based on the information you provided, you might face some challenges in getting approved for a mortgage. However, there are still options available to you.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("<h4>Areas that need attention:</h4>", unsafe_allow_html=True)
                    for note in eligibility_notes:
                        st.markdown(f"- {note}")
                
                # Recommended banks
                st.subheader("Recommended Financing Options / خيارات التمويل الموصى بها")
                
                banks = load_banks()
                
                # Filter and score banks based on user preferences
                bank_scores = []
                
                for bank in banks:
                    # Skip if disqualified
                    if not eligible and bank["name"] not in ["Alinma Bank", "Saudi National Bank"]:
                        continue
                    
                    # Basic match score
                    score = 0
                    
                    # Check if bank meets basic requirements
                    if bank["max_loan_term"] >= preferred_term:
                        score += 10
                    
                    if bank["min_down_payment"] <= down_payment_percent:
                        score += 10
                    
                    # Additional scoring based on preferences
                    if rate_preference == "Islamic Financing" and bank["name"] in ["Al Rajhi Bank", "Alinma Bank"]:
                        score += 20
                    
                    if employment_type == "Government Employee" and "Government employee discount" in bank["special_offers"]:
                        score += 15
                    
                    if purpose == "Primary Residence" and "First-time buyer discount" in bank["special_offers"]:
                        score += 15
                    
                    if purpose == "Primary Residence" and "Family home discount" in bank["special_offers"]:
                        score += 10
                    
                    # Adjust score based on interest rate
                    avg_rate = sum(b["interest_rate"] for b in banks) / len(banks)
                    if bank["interest_rate"] < avg_rate:
                        score += 10
                    
                    # Add the bank with its score
                    bank_scores.append((bank, score))
                
                # Sort banks by score
                bank_scores.sort(key=lambda x: x[1], reverse=True)
                
                # Display recommended banks
                for i, (bank, score) in enumerate(bank_scores[:3]):
                    # Calculate mortgage based on this bank
                    mortgage = calculate_mortgage(property_price, down_payment_percent, bank["interest_rate"], preferred_term)
                    
                    st.markdown(f"""
                    <div style="background-color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                            <h3 style="margin: 0;">{bank['name']} / {bank['name_ar']}</h3>
                            <span style="background-color: {['#FFD700', '#C0C0C0', '#CD7F32'][i] if i < 3 else '#f0f2f5'}; color: #333; padding: 5px 10px; border-radius: 20px; font-weight: bold;">{['Top Pick', 'Runner Up', 'Third Place'][i] if i < 3 else 'Recommended'}</span>
                        </div>
                        
                        <div style="display: flex; flex-wrap: wrap; gap: 20px; margin-bottom: 15px;">
                            <div>
                                <span style="color: #666;">Interest Rate / معدل الفائدة</span>
                                <h4 style="margin: 5px 0; color: #1e3c72;">{bank['interest_rate']}%</h4>
                            </div>
                            <div>
                                <span style="color: #666;">Monthly Payment / الدفعة الشهرية</span>
                                <h4 style="margin: 5px 0; color: #1e3c72;">{mortgage['monthly_payment']:,.0f} SAR</h4>
                            </div>
                            <div>
                                <span style="color: #666;">Max Loan Term / الحد الأقصى لمدة القرض</span>
                                <h4 style="margin: 5px 0; color: #1e3c72;">{bank['max_loan_term']} years</h4>
                            </div>
                            <div>
                                <span style="color: #666;">Processing Fee / رسوم المعالجة</span>
                                <h4 style="margin: 5px 0; color: #1e3c72;">{bank['processing_fee']}%</h4>
                            </div>
                        </div>
                        
                        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 15px;">
                            <h4 style="margin-top: 0;">Why this bank? / لماذا هذا البنك؟</h4>
                    """, unsafe_allow_html=True)
                    
                    # Generate recommendations reasons
                    reasons = []
                    
                    if bank["interest_rate"] < avg_rate:
                        reasons.append(f"Lower than average interest rate ({bank['interest_rate']}% vs. {avg_rate:.1f}% market average)")
                    
                    if mortgage['monthly_payment'] <= monthly_payment_max:
                        reasons.append(f"Monthly payment of {mortgage['monthly_payment']:,.0f} SAR is within your budget")
                    
                    if rate_preference == "Islamic Financing" and bank["name"] in ["Al Rajhi Bank", "Alinma Bank"]:
                        reasons.append("Offers Islamic financing options aligned with your preferences")
                    
                    if employment_type == "Government Employee" and "Government employee discount" in bank["special_offers"]:
                        reasons.append("Offers special discounts for government employees")
                    
                    if "Zero early settlement fees" in bank["special_offers"]:
                        reasons.append("No early settlement fees if you decide to pay off your loan early")
                    
                    if bank["max_loan_term"] >= preferred_term:
                        reasons.append(f"Offers your preferred loan term of {preferred_term} years")
                    
                    # Add reasons as bullet points
                    for reason in reasons:
                        st.markdown(f"<p><i class='fas fa-check' style='color: #2ecc71; margin-right: 5px;'></i> {reason}</p>", unsafe_allow_html=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Special offers
                    st.markdown("<h4 style='margin-bottom: 10px;'>Special Offers / عروض خاصة</h4>", unsafe_allow_html=True)
                    
                    offers_html = "<div style='display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 15px;'>"
                    
                    for offer in bank['special_offers']:
                        offers_html += f"""
                        <span style="background-color: #f0f8ff; color: #1e3c72; padding: 5px 10px; border-radius: 5px;">
                            <i class="fas fa-tag" style="margin-right: 5px;"></i> {offer}
                        </span>
                        """
                    
                    offers_html += "</div>"
                    st.markdown(offers_html, unsafe_allow_html=True)
                    
                    # Apply button
                    st.markdown("""
                    <div style="display: flex; gap: 10px;">
                        <button style="background-color: #9a86fe; color: white; border: none; padding: 8px 15px; border-radius: 5px; cursor: pointer; flex: 1;">Apply Now</button>
                        <button style="background-color: white; color: #1e3c72; border: 1px solid #1e3c72; padding: 8px 15px; border-radius: 5px; cursor: pointer; flex: 1;">Save for Later</button>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                
                # Next steps
                st.subheader("Next Steps / الخطوات التالية")
                
                st.markdown("""
                <div class="progress-steps">
                    <div class="step">
                        <div class="step-number">1</div>
                        <div class="step-title">Pre-Qualification</div>
                    </div>
                    <div class="step">
                        <div class="step-number">2</div>
                        <div class="step-title">Application</div>
                    </div>
                    <div class="step">
                        <div class="step-number">3</div>
                        <div class="step-title">Documentation</div>
                    </div>
                    <div class="step">
                        <div class="step-number">4</div>
                        <div class="step-title">Approval</div>
                    </div>
                    <div class="step">
                        <div class="step-number">5</div>
                        <div class="step-title">Closing</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("""
                <div style="margin-top: 30px;">
                    <p>To begin the financing process, follow these steps:</p>
                    <ol>
                        <li>Click "Apply Now" for your preferred bank to start the pre-qualification process.</li>
                        <li>Prepare your required documents (income verification, ID, etc.).</li>
                        <li>Complete the formal application with the bank.</li>
                        <li>Wait for the approval decision (typically 5-7 business days).</li>
                        <li>Complete the closing process once approved.</li>
                    </ol>
                    <p>Need help with any of these steps? Our financing specialists are available to assist you.</p>
                    <button style="background-color: #1e3c72; color: white; border: none; padding: 8px 15px; border-radius: 5px; cursor: pointer;">Contact a Financing Specialist</button>
                </div>
                """, unsafe_allow_html=True)

# Building inspection page
def show_building_inspection():
    st.markdown("<h1>Building Inspection / فحص المباني</h1>", unsafe_allow_html=True)
    
    # Introduction
    st.markdown("""
    Professional building inspection is a crucial step in the home buying process. It helps identify any potential issues with the property
    before finalizing your purchase, saving you from unexpected expenses and safety concerns down the line.
    
    الفحص المهني للمباني هو خطوة حاسمة في عملية شراء المنزل. يساعد على تحديد أي مشاكل محتملة في العقار
    قبل إتمام الشراء، مما يوفر عليك النفقات غير المتوقعة ومخاوف السلامة في المستقبل.
    """)
    
    # Tabs for different sections
    tabs = st.tabs(["Find an Inspector", "Inspection Types", "What to Expect", "Common Issues"])
    
    with tabs[0]:
        st.subheader("Find a Professional Inspector / ابحث عن مفتش محترف")
        
        # Search filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            specialty = st.selectbox("Specialty / التخصص", ["All", "Structural Engineering", "Electrical Systems", "Complete Home Inspection"])
        
        with col2:
            inspection_type = st.multiselect("Inspection Type / نوع الفحص", ["Pre-purchase", "Structural", "Electrical", "Comprehensive", "Maintenance"])
        
        with col3:
            availability = st.radio("Availability / التوفر", ["All", "Available Now", "Available This Week"])
        
        # Load inspectors data
        inspectors = load_inspectors()
        
        # Filter inspectors based on selection
        filtered_inspectors = inspectors.copy()
        
        if specialty != "All":
            filtered_inspectors = [i for i in filtered_inspectors if i["specialty"] == specialty]
        
        if inspection_type:
            filtered_inspectors = [i for i in filtered_inspectors if any(t in i["inspection_types"] for t in inspection_type)]
        
        if availability == "Available Now":
            filtered_inspectors = [i for i in filtered_inspectors if i["availability"] == "Available"]
        elif availability == "Available This Week":
            filtered_inspectors = [i for i in filtered_inspectors if "Available" in i["availability"] or "until" in i["availability"]]
        
        # Display inspectors
        if filtered_inspectors:
            st.markdown(f"<h3>Found {len(filtered_inspectors)} inspectors / تم العثور على {len(filtered_inspectors)} مفتش</h3>", unsafe_allow_html=True)
            
            for inspector in filtered_inspectors:
                st.markdown(f"""
                <div style="background-color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                        <h3 style="margin: 0;">{inspector['name']} / {inspector['name_ar']}</h3>
                        <span style="background-color: {'#e6f4ff' if inspector['availability'] == 'Available' else '#fff2e6'}; color: {'#1e3c72' if inspector['availability'] == 'Available' else '#ff9933'}; padding: 5px 10px; border-radius: 4px; font-size: 14px;">
                            {inspector['availability']}
                        </span>
                    </div>
                    
                    <div style="display: flex; flex-wrap: wrap; gap: 20px; margin-bottom: 15px;">
                        <div>
                            <span style="color: #666;">Specialty / التخصص</span>
                            <h4 style="margin: 5px 0; color: #1e3c72;">{inspector['specialty']} / {inspector['specialty_ar']}</h4>
                        </div>
                        <div>
                            <span style="color: #666;">Experience / الخبرة</span>
                            <h4 style="margin: 5px 0; color: #1e3c72;">{inspector['experience']} years</h4>
                        </div>
                        <div>
                            <span style="color: #666;">Rating / التقييم</span>
                            <h4 style="margin: 5px 0; color: #1e3c72;">{inspector['rating']} <small>({inspector['reviews']} reviews)</small></h4>
                        </div>
                        <div>
                            <span style="color: #666;">Fee Range / نطاق الرسوم</span>
                            <h4 style="margin: 5px 0; color: #1e3c72;">{inspector['fee_range']}</h4>
                        </div>
                    </div>
                    
                    <div style="margin-bottom: 15px;">
                        <h4 style="margin-bottom: 10px;">Inspection Types / أنواع الفحص</h4>
                        <div style="display: flex; flex-wrap: wrap; gap: 10px;">
                """, unsafe_allow_html=True)
                
                for inspection in inspector['inspection_types']:
                    st.markdown(f"""
                    <span style="background-color: #f0f2f5; padding: 5px 10px; border-radius: 20px;">
                        <i class="fas fa-clipboard-check" style="color: #9a86fe; margin-right: 5px;"></i> {inspection}
                    </span>
                    """, unsafe_allow_html=True)
                
                st.markdown("</div></div>", unsafe_allow_html=True)
                
                # Certifications
                st.markdown("""
                <div style="margin-bottom: 15px;">
                    <h4 style="margin-bottom: 10px;">Certifications / الشهادات</h4>
                    <div style="display: flex; flex-wrap: wrap; gap: 10px;">
                """, unsafe_allow_html=True)
                
                for cert in inspector['certifications']:
                    st.markdown(f"""
                    <span style="background-color: #e6f4ff; color: #1e3c72; padding: 5px 10px; border-radius: 20px;">
                        <i class="fas fa-certificate" style="margin-right: 5px;"></i> {cert}
                    </span>
                    """, unsafe_allow_html=True)
                
                st.markdown("</div></div>", unsafe_allow_html=True)
                
                # Languages
                st.markdown("""
                <div style="margin-bottom: 15px;">
                    <h4 style="margin-bottom: 10px;">Languages / اللغات</h4>
                    <div style="display: flex; flex-wrap: wrap; gap: 10px;">
                """, unsafe_allow_html=True)
                
                for lang in inspector['languages']:
                    st.markdown(f"""
                    <span style="background-color: #f0f2f5; padding: 5px 10px; border-radius: 20px;">
                        <i class="fas fa-language" style="color: #9a86fe; margin-right: 5px;"></i> {lang}
                    </span>
                    """, unsafe_allow_html=True)
                
                st.markdown("</div></div>", unsafe_allow_html=True)
                
                # Action buttons
                st.markdown("""
                <div style="display: flex; gap: 10px;">
                    <button style="background-color: #9a86fe; color: white; border: none; padding: 8px 15px; border-radius: 5px; cursor: pointer; flex: 1;">Schedule Inspection</button>
                    <button style="background-color: white; color: #1e3c72; border: 1px solid #1e3c72; padding: 8px 15px; border-radius: 5px; cursor: pointer; flex: 1;">Contact Inspector</button>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("No inspectors match your search criteria. Try adjusting your filters.")
        
        # Schedule inspection form
        st.subheader("Schedule an Inspection / جدولة فحص")
        
        with st.form("inspection_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                property_address = st.text_input("Property Address / عنوان العقار")
                inspection_date = st.date_input("Inspection Date / تاريخ الفحص")
                inspection_time = st.selectbox("Preferred Time / الوقت المفضل", ["Morning (8 AM - 12 PM)", "Afternoon (12 PM - 4 PM)", "Evening (4 PM - 8 PM)"])
            
            with col2:
                inspector_preference = st.selectbox("Inspector Preference / تفضيل المفتش", ["No Preference"] + [i["name"] for i in inspectors])
                inspection_type_form = st.selectbox("Inspection Type / نوع الفحص", ["Pre-purchase", "Structural", "Electrical", "Comprehensive", "Maintenance"])
                special_instructions = st.text_area("Special Instructions / تعليمات خاصة", height=100)
            
            submit_button = st.form_submit_button("Schedule Inspection / جدولة الفحص")
            
            if submit_button:
                st.success("Your inspection has been scheduled! We'll contact you shortly to confirm the details.")
    
    with tabs[1]:
        st.subheader("Inspection Types / أنواع الفحص")
        
        # Create cards for different inspection types
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style="background-color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                <div style="text-align: center; margin-bottom: 15px;">
                    <i class="fas fa-home" style="font-size: 36px; color: #9a86fe;"></i>
                </div>
                <h3 style="text-align: center; margin-bottom: 15px;">Pre-purchase Inspection / فحص ما قبل الشراء</h3>
                <p>A comprehensive evaluation of the property before purchasing, identifying any issues that may affect your decision or negotiation.</p>
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-top: 15px;">
                    <h4 style="margin-top: 0;">What's Included:</h4>
                    <ul style="margin-bottom: 0;">
                        <li>Foundation and structural assessment</li>
                        <li>Roof condition evaluation</li>
                        <li>Electrical system check</li>
                        <li>Plumbing system examination</li>
                        <li>HVAC system testing</li>
                        <li>Doors, windows, and insulation check</li>
                    </ul>
                </div>
                <div style="text-align: center; margin-top: 15px;">
                    <span style="background-color: #e6f4ff; color: #1e3c72; padding: 5px 10px; border-radius: 5px; display: inline-block;">
                        <i class="fas fa-tag" style="margin-right: 5px;"></i> From 2,000 SAR
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style="background-color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                <div style="text-align: center; margin-bottom: 15px;">
                    <i class="fas fa-bolt" style="font-size: 36px; color: #9a86fe;"></i>
                </div>
                <h3 style="text-align: center; margin-bottom: 15px;">Electrical Inspection / الفحص الكهربائي</h3>
                <p>A detailed assessment of the property's electrical systems to ensure safety and identify any potential hazards or needed upgrades.</p>
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-top: 15px;">
                    <h4 style="margin-top: 0;">What's Included:</h4>
                    <ul style="margin-bottom: 0;">
                        <li>Electrical panel inspection</li>
                        <li>Wiring and circuit check</li>
                        <li>Outlet and switch testing</li>
                        <li>Light fixture examination</li>
                        <li>GFCI protection verification</li>
                        <li>Safety hazard identification</li>
                    </ul>
                </div>
                <div style="text-align: center; margin-top: 15px;">
                    <span style="background-color: #e6f4ff; color: #1e3c72; padding: 5px 10px; border-radius: 5px; display: inline-block;">
                        <i class="fas fa-tag" style="margin-right: 5px;"></i> From 1,200 SAR
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background-color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                <div style="text-align: center; margin-bottom: 15px;">
                    <i class="fas fa-columns" style="font-size: 36px; color: #9a86fe;"></i>
                </div>
                <h3 style="text-align: center; margin-bottom: 15px;">Structural Inspection / الفحص الهيكلي</h3>
                <p>A focused evaluation of the property's structural elements to identify any issues with the foundation, walls, or supporting components.</p>
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-top: 15px;">
                    <h4 style="margin-top: 0;">What's Included:</h4>
                    <ul style="margin-bottom: 0;">
                        <li>Foundation assessment</li>
                        <li>Wall structure evaluation</li>
                        <li>Roof framing inspection</li>
                        <li>Support beam and column check</li>
                        <li>Crack analysis</li>
                        <li>Settlement evaluation</li>
                    </ul>
                </div>
                <div style="text-align: center; margin-top: 15px;">
                    <span style="background-color: #e6f4ff; color: #1e3c72; padding: 5px 10px; border-radius: 5px; display: inline-block;">
                        <i class="fas fa-tag" style="margin-right: 5px;"></i> From 1,500 SAR
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style="background-color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                <div style="text-align: center; margin-bottom: 15px;">
                    <i class="fas fa-clipboard-list" style="font-size: 36px; color: #9a86fe;"></i>
                </div>
                <h3 style="text-align: center; margin-bottom: 15px;">Comprehensive Inspection / الفحص الشامل</h3>
                <p>A thorough examination of all aspects of the property, providing a complete assessment of its condition and identifying any issues.</p>
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-top: 15px;">
                    <h4 style="margin-top: 0;">What's Included:</h4>
                    <ul style="margin-bottom: 0;">
                        <li>All elements of structural inspection</li>
                        <li>All elements of electrical inspection</li>
                        <li>Plumbing system assessment</li>
                        <li>HVAC system evaluation</li>
                        <li>Insulation and ventilation check</li>
                        <li>Interior and exterior examination</li>
                        <li>Detailed report with recommendations</li>
                    </ul>
                </div>
                <div style="text-align: center; margin-top: 15px;">
                    <span style="background-color: #e6f4ff; color: #1e3c72; padding: 5px 10px; border-radius: 5px; display: inline-block;">
                        <i class="fas fa-tag" style="margin-right: 5px;"></i> From 3,000 SAR
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Custom inspection
        st.subheader("Custom Inspection / فحص مخصص")
        
        st.markdown("""
        <div style="background-color: #f0f8ff; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
            <h3 style="margin-top: 0;">Need a Custom Inspection?</h3>
            <p>We can create a tailored inspection plan based on your specific requirements and concerns. Our experts will focus on the areas that matter most to you.</p>
            <button style="background-color: #9a86fe; color: white; border: none; padding: 8px 15px; border-radius: 5px; cursor: pointer;">Request Custom Inspection</button>
        </div>
        """, unsafe_allow_html=True)
    
    with tabs[2]:
        st.subheader("What to Expect During an Inspection / ماذا تتوقع خلال الفحص")
        
        # Inspection process
        st.markdown("""
        <div class="progress-steps">
            <div class="step">
                <div class="step-number">1</div>
                <div class="step-title">Scheduling</div>
            </div>
            <div class="step">
                <div class="step-number">2</div>
                <div class="step-title">Inspection Day</div>
            </div>
            <div class="step">
                <div class="step-number">3</div>
                <div class="step-title">Report Delivery</div>
            </div>
            <div class="step">
                <div class="step-number">4</div>
                <div class="step-title">Review & Follow-up</div>
            </div>
            <div class="step">
                <div class="step-number">5</div>
                <div class="step-title">Decision Making</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Step details
        with st.expander("1. Scheduling / الجدولة", expanded=True):
            st.markdown("""
            <div style="display: flex; align-items: flex-start; gap: 15px;">
                <div style="min-width: 60px; height: 60px; background-color: #9a86fe; color: white; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 24px; font-weight: bold;">1</div>
                <div>
                    <h4 style="margin: 0 0 10px 0;">Scheduling / الجدولة</h4>
                    <p>The first step is to schedule your inspection. You can do this through our platform by selecting your preferred inspector, date, and time.</p>
                    <ul>
                        <li>Choose the type of inspection you need</li>
                        <li>Select a qualified inspector</li>
                        <li>Pick a convenient date and time</li>
                        <li>Provide property access information</li>
                    </ul>
                    <p>We recommend scheduling the inspection as soon as possible after your offer is accepted, as it may take a few days to get an appointment with your preferred inspector.</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with st.expander("2. Inspection Day / يوم الفحص", expanded=False):
            st.markdown("""
            <div style="display: flex; align-items: flex-start; gap: 15px;">
                <div style="min-width: 60px; height: 60px; background-color: #9a86fe; color: white; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 24px; font-weight: bold;">2</div>
                <div>
                    <h4 style="margin: 0 0 10px 0;">Inspection Day / يوم الفحص</h4>
                    <p>On the day of the inspection, the inspector will arrive at the property at the scheduled time. The inspection typically takes 2-4 hours, depending on the property size and inspection type.</p>
                    <ul>
                        <li>The inspector will examine all accessible areas of the property</li>
                        <li>They will take photos and notes throughout the process</li>
                        <li>You are welcome to attend the inspection (recommended)</li>
                        <li>The inspector can explain their findings as they go</li>
                        <li>Feel free to ask questions during the inspection</li>
                    </ul>
                    <p>Attending the inspection allows you to see any issues firsthand and get a better understanding of the property's condition.</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with st.expander("3. Report Delivery / تسليم التقرير", expanded=False):
            st.markdown("""
            <div style="display: flex; align-items: flex-start; gap: 15px;">
                <div style="min-width: 60px; height: 60px; background-color: #9a86fe; color: white; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 24px; font-weight: bold;">3</div>
                <div>
                    <h4 style="margin: 0 0 10px 0;">Report Delivery / تسليم التقرير</h4>
                    <p>After the inspection, you will receive a detailed report of the findings. This is typically delivered within 24-48 hours.</p>
                    <ul>
                        <li>The report will include photos and descriptions of any issues found</li>
                        <li>Items will be categorized by severity (critical, major, minor)</li>
                        <li>The report will highlight safety concerns</li>
                        <li>Recommendations for repairs or further evaluation will be provided</li>
                        <li>The report will be delivered in both English and Arabic</li>
                    </ul>
                    <p>Our inspection reports are comprehensive and easy to understand, with clear explanations of all findings.</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with st.expander("4. Review & Follow-up / المراجعة والمتابعة", expanded=False):
            st.markdown("""
            <div style="display: flex; align-items: flex-start; gap: 15px;">
                <div style="min-width: 60px; height: 60px; background-color: #9a86fe; color: white; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 24px; font-weight: bold;">4</div>
                <div>
                    <h4 style="margin: 0 0 10px 0;">Review & Follow-up / المراجعة والمتابعة</h4>
                    <p>After receiving the report, you'll have the opportunity to review it and ask any questions you may have.</p>
                    <ul>
                        <li>The inspector is available for follow-up questions</li>
                        <li>You can request clarification on any items in the report</li>
                        <li>Additional documentation or photos can be provided if needed</li>
                        <li>You may request recommendations for contractors to address issues</li>
                    </ul>
                    <p>Our inspectors are committed to ensuring you fully understand the condition of the property and the implications of any issues found.</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with st.expander("5. Decision Making / اتخاذ القرار", expanded=False):
            st.markdown("""
            <div style="display: flex; align-items: flex-start; gap: 15px;">
                <div style="min-width: 60px; height: 60px; background-color: #9a86fe; color: white; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 24px; font-weight: bold;">5</div>
                <div>
                    <h4 style="margin: 0 0 10px 0;">Decision Making / اتخاذ القرار</h4>
                    <p>Based on the inspection report, you can make informed decisions about your property purchase.</p>
                    <ul>
                        <li>Decide whether to proceed with the purchase</li>
                        <li>Negotiate repairs or price adjustments with the seller</li>
                        <li>Request further specialized inspections if needed</li>
                        <li>Plan for future repairs and maintenance</li>
                    </ul>
                    <p>The inspection report serves as a valuable tool for negotiation and planning, helping you make the best decision about your investment.</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Sample report
        st.subheader("Sample Inspection Report / نموذج تقرير الفحص")
        
        with st.expander("View Sample Report", expanded=False):
            st.markdown("""
            <div style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                <h3 style="text-align: center; margin-bottom: 20px;">BUILDING INSPECTION REPORT</h3>
                
                <div style="margin-bottom: 20px;">
                    <h4>Property Information</h4>
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr>
                            <td style="padding: 8px; border: 1px solid #ddd; width: 30%;"><strong>Address:</strong></td>
                            <td style="padding: 8px; border: 1px solid #ddd;">123 Al Nakheel Street, Riyadh</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; border: 1px solid #ddd;"><strong>Property Type:</strong></td>
                            <td style="padding: 8px; border: 1px solid #ddd;">Villa</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; border: 1px solid #ddd;"><strong>Year Built:</strong></td>
                            <td style="padding: 8px; border: 1px solid #ddd;">2018</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; border: 1px solid #ddd;"><strong>Square Footage:</strong></td>
                            <td style="padding: 8px; border: 1px solid #ddd;">450 m²</td>
                        </tr>
                    </table>
                </div>
                
                <div style="margin-bottom: 20px;">
                    <h4>Inspection Summary</h4>
                    <p>This comprehensive inspection was conducted on May 15, 2025. The property is in overall good condition with some minor issues noted. No critical safety concerns were identified.</p>
                </div>
                
                <div style="margin-bottom: 20px;">
                    <h4>Structural Elements</h4>
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr>
                            <th style="padding: 8px; border: 1px solid #ddd; text-align: left; background-color: #f0f2f5;">Item</th>
                            <th style="padding: 8px; border: 1px solid #ddd; text-align: left; background-color: #f0f2f5;">Condition</th>
                            <th style="padding: 8px; border: 1px solid #ddd; text-align: left; background-color: #f0f2f5;">Notes</th>
                        </tr>
                        <tr>
                            <td style="padding: 8px; border: 1px solid #ddd;">Foundation</td>
                            <td style="padding: 8px; border: 1px solid #ddd;"><span style="color: #2ecc71;">Good</span></td>
                            <td style="padding: 8px; border: 1px solid #ddd;">No significant settlement or cracks observed.</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; border: 1px solid #ddd;">Exterior Walls</td>
                            <td style="padding: 8px; border: 1px solid #ddd;"><span style="color: #2ecc71;">Good</span></td>
                            <td style="padding: 8px; border: 1px solid #ddd;">Well-maintained with no significant issues.</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; border: 1px solid #ddd;">Roof</td>
                            <td style="padding: 8px; border: 1px solid #ddd;"><span style="color: #f39c12;">Fair</span></td>
                            <td style="padding: 8px; border: 1px solid #ddd;">Minor wear observed. Recommend maintenance within the next year.</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; border: 1px solid #ddd;">Windows</td>
                            <td style="padding: 8px; border: 1px solid #ddd;"><span style="color: #2ecc71;">Good</span></td>
                            <td style="padding: 8px; border: 1px solid #ddd;">All windows functional with good sealing.</td>
                        </tr>
                    </table>
                </div>
                
                <div style="margin-bottom: 20px;">
                    <h4>Electrical System</h4>
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr>
                            <th style="padding: 8px; border: 1px solid #ddd; text-align: left; background-color: #f0f2f5;">Item</th>
                            <th style="padding: 8px; border: 1px solid #ddd; text-align: left; background-color: #f0f2f5;">Condition</th>
                            <th style="padding: 8px; border: 1px solid #ddd; text-align: left; background-color: #f0f2f5;">Notes</th>
                        </tr>
                        <tr>
                            <td style="padding: 8px; border: 1px solid #ddd;">Electrical Panel</td>
                            <td style="padding: 8px; border: 1px solid #ddd;"><span style="color: #2ecc71;">Good</span></td>
                            <td style="padding: 8px; border: 1px solid #ddd;">Modern panel with appropriate capacity and circuit protection.</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; border: 1px solid #ddd;">Wiring</td>
                            <td style="padding: 8px; border: 1px solid #ddd;"><span style="color: #2ecc71;">Good</span></td>
                            <td style="padding: 8px; border: 1px solid #ddd;">Modern copper wiring throughout the property.</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; border: 1px solid #ddd;">Outlets & Switches</td>
                            <td style="padding: 8px; border: 1px solid #ddd;"><span style="color: #f39c12;">Fair</span></td>
                            <td style="padding: 8px; border: 1px solid #ddd;">Two outlets in the kitchen not functioning. Recommend repair.</td>
                        </tr>
                    </table>
                </div>
                
                <div style="margin-bottom: 20px;">
                    <h4>Recommendations</h4>
                    <ol style="margin-top: 0;">
                        <li>Repair non-functioning outlets in the kitchen.</li>
                        <li>Schedule roof maintenance within the next year.</li>
                        <li>Consider upgrading HVAC filters for improved efficiency.</li>
                        <li>Seal minor cracks in garage floor to prevent water intrusion.</li>
                    </ol>
                </div>
                
                <div style="text-align: center; margin-top: 30px;">
                    <p><strong>Inspection conducted by: Mohammed Al-Shammari, Certified Building Inspector</strong></p>
                    <p>SUHAIL Building Inspection Services</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with tabs[3]:
        st.subheader("Common Issues Found in Inspections / المشاكل الشائعة التي تم العثور عليها في عمليات الفحص")
        
        # Create expandable sections for common issues
        with st.expander("Structural Issues / مشاكل هيكلية", expanded=True):
            st.markdown("""
            <div style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                <h4 style="margin-top: 0; color: #1e3c72;">Common Structural Issues / المشاكل الهيكلية الشائعة</h4>
                
                <div style="margin-bottom: 15px;">
                    <h5 style="color: #9a86fe; margin-bottom: 5px;">Foundation Cracks / تشققات الأساس</h5>
                    <p style="margin-top: 0;">Foundation cracks can indicate settlement issues or water damage. Vertical cracks are usually less concerning than horizontal ones.</p>
                    <p style="margin-top: 0;"><strong>Severity:</strong> <span style="color: #f39c12;">Medium to High</span></p>
                    <p style="margin-top: 0;"><strong>Repair Cost:</strong> 5,000 - 30,000 SAR depending on severity</p>
                </div>
                
                <div style="margin-bottom: 15px;">
                    <h5 style="color: #9a86fe; margin-bottom: 5px;">Roof Damage / تلف السقف</h5>
                    <p style="margin-top: 0;">Roof damage can lead to water leaks and significant interior damage if not addressed promptly.</p>
                    <p style="margin-top: 0;"><strong>Severity:</strong> <span style="color: #f39c12;">Medium to High</span></p>
                    <p style="margin-top: 0;"><strong>Repair Cost:</strong> 3,000 - 20,000 SAR depending on the extent</p>
                </div>
                
                <div style="margin-bottom: 0;">
                    <h5 style="color: #9a86fe; margin-bottom: 5px;">Wall Cracks / تشققات الجدران</h5>
                    <p style="margin-top: 0;">Wall cracks can be cosmetic or indicators of structural issues. Diagonal cracks are often more concerning.</p>
                    <p style="margin-top: 0;"><strong>Severity:</strong> <span style="color: #2ecc71;">Low to Medium</span></p>
                    <p style="margin-top: 0;"><strong>Repair Cost:</strong> 500 - 5,000 SAR depending on cause and extent</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with st.expander("Electrical Issues / مشاكل كهربائية", expanded=False):
            st.markdown("""
            <div style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                <h4 style="margin-top: 0; color: #1e3c72;">Common Electrical Issues / المشاكل الكهربائية الشائعة</h4>
                
                <div style="margin-bottom: 15px;">
                    <h5 style="color: #9a86fe; margin-bottom: 5px;">Outdated Wiring / الأسلاك القديمة</h5>
                    <p style="margin-top: 0;">Older properties may have aluminum wiring or insufficient electrical capacity for modern needs.</p>
                    <p style="margin-top: 0;"><strong>Severity:</strong> <span style="color: #e74c3c;">High</span></p>
                    <p style="margin-top: 0;"><strong>Repair Cost:</strong> 10,000 - 40,000 SAR for complete rewiring</p>
                </div>
                
                <div style="margin-bottom: 15px;">
                    <h5 style="color: #9a86fe; margin-bottom: 5px;">Overloaded Circuits / الدوائر المحملة بشكل زائد</h5>
                    <p style="margin-top: 0;">Too many devices on a single circuit can lead to breaker trips and potential fire hazards.</p>
                    <p style="margin-top: 0;"><strong>Severity:</strong> <span style="color: #f39c12;">Medium</span></p>
                    <p style="margin-top: 0;"><strong>Repair Cost:</strong> 1,500 - 5,000 SAR to add circuits</p>
                </div>
                
                <div style="margin-bottom: 0;">
                    <h5 style="color: #9a86fe; margin-bottom: 5px;">Improper Grounding / التأريض غير الصحيح</h5>
                    <p style="margin-top: 0;">Inadequate grounding can lead to electric shock risks and damage to sensitive electronics.</p>
                    <p style="margin-top: 0;"><strong>Severity:</strong> <span style="color: #f39c12;">Medium</span></p>
                    <p style="margin-top: 0;"><strong>Repair Cost:</strong> 1,000 - 3,000 SAR</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with st.expander("Plumbing Issues / مشاكل السباكة", expanded=False):
            st.markdown("""
            <div style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                <h4 style="margin-top: 0; color: #1e3c72;">Common Plumbing Issues / مشاكل السباكة الشائعة</h4>
                
                <div style="margin-bottom: 15px;">
                    <h5 style="color: #9a86fe; margin-bottom: 5px;">Leaking Pipes / تسرب الأنابيب</h5>
                    <p style="margin-top: 0;">Water leaks can cause significant damage to the property and lead to mold growth.</p>
                    <p style="margin-top: 0;"><strong>Severity:</strong> <span style="color: #f39c12;">Medium to High</span></p>
                    <p style="margin-top: 0;"><strong>Repair Cost:</strong> 500 - 10,000 SAR depending on location and extent</p>
                </div>
                
                <div style="margin-bottom: 15px;">
                    <h5 style="color: #9a86fe; margin-bottom: 5px;">Water Pressure Issues / مشاكل ضغط الماء</h5>
                    <p style="margin-top: 0;">Low water pressure can be caused by clogged pipes, while high pressure can damage fixtures and appliances.</p>
                    <p style="margin-top: 0;"><strong>Severity:</strong> <span style="color: #2ecc71;">Low to Medium</span></p>
                    <p style="margin-top: 0;"><strong>Repair Cost:</strong> 300 - 3,000 SAR</p>
                </div>
                
                <div style="margin-bottom: 0;">
                    <h5 style="color: #9a86fe; margin-bottom: 5px;">Outdated Plumbing Materials / مواد السباكة القديمة</h5>
                    <p style="margin-top: 0;">Older properties may have lead or galvanized steel pipes that need replacement.</p>
                    <p style="margin-top: 0;"><strong>Severity:</strong> <span style="color: #f39c12;">Medium</span></p>
                    <p style="margin-top: 0;"><strong>Repair Cost:</strong> 8,000 - 30,000 SAR for complete repiping</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with st.expander("HVAC Issues / مشاكل التكييف والتهوية", expanded=False):
            st.markdown("""
            <div style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                <h4 style="margin-top: 0; color: #1e3c72;">Common HVAC Issues / مشاكل التكييف والتهوية الشائعة</h4>
                
                <div style="margin-bottom: 15px;">
                    <h5 style="color: #9a86fe; margin-bottom: 5px;">Aging HVAC System / نظام تكييف قديم</h5>
                    <p style="margin-top: 0;">Older HVAC systems are less efficient and may require frequent repairs.</p>
                    <p style="margin-top: 0;"><strong>Severity:</strong> <span style="color: #f39c12;">Medium</span></p>
                    <p style="margin-top: 0;"><strong>Repair Cost:</strong> 15,000 - 40,000 SAR for replacement</p>
                </div>
                
                <div style="margin-bottom: 15px;">
                    <h5 style="color: #9a86fe; margin-bottom: 5px;">Poor Ventilation / سوء التهوية</h5>
                    <p style="margin-top: 0;">Inadequate ventilation can lead to indoor air quality issues and moisture problems.</p>
                    <p style="margin-top: 0;"><strong>Severity:</strong> <span style="color: #2ecc71;">Low to Medium</span></p>
                    <p style="margin-top: 0;"><strong>Repair Cost:</strong> 1,000 - 8,000 SAR</p>
                </div>
                
                <div style="margin-bottom: 0;">
                    <h5 style="color: #9a86fe; margin-bottom: 5px;">Refrigerant Leaks / تسرب غاز التبريد</h5>
                    <p style="margin-top: 0;">Refrigerant leaks can reduce cooling efficiency and damage the compressor.</p>
                    <p style="margin-top: 0;"><strong>Severity:</strong> <span style="color: #f39c12;">Medium</span></p>
                    <p style="margin-top: 0;"><strong>Repair Cost:</strong> 800 - 3,000 SAR</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Tips for buyers
        st.subheader("Tips for Buyers / نصائح للمشترين")
        
        st.markdown("""
        <div style="background-color: #f0f8ff; padding: 20px; border-radius: 10px; margin-top: 20px;">
            <h4 style="margin-top: 0; color: #1e3c72;">Tips for Property Buyers / نصائح لمشتري العقارات</h4>
            <ul style="margin-bottom: 0;">
                <li><strong>Always get a professional inspection:</strong> Even if a property looks perfect, a professional inspector can identify hidden issues.</li>
                <li><strong>Attend the inspection:</strong> Being present during the inspection allows you to see issues firsthand and ask questions.</li>
                <li><strong>Don't skip on specialized inspections:</strong> If the general inspection reveals concerns about a specific system, consider a specialized inspection.</li>
                <li><strong>Use the inspection report for negotiation:</strong> Significant issues can be grounds for price adjustments or repair requests.</li>
                <li><strong>Budget for repairs:</strong> No property is perfect. Set aside funds for repairs based on the inspection findings.</li>
                <li><strong>Prioritize safety issues:</strong> Address any safety concerns immediately after purchase.</li>
                <li><strong>Consider long-term maintenance:</strong> The inspection report can help you plan for future maintenance needs.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# Real estate consultants page
def show_consultants_page():
    st.markdown("<h1>Real Estate Consultants / مستشارو العقارات</h1>", unsafe_allow_html=True)
    
    # Introduction
    st.markdown("""
    Our network of certified real estate consultants provides expert guidance throughout your property journey.
    From finding the perfect property to navigating complex negotiations and paperwork, our consultants are here to help.
    
    شبكتنا من مستشاري العقارات المعتمدين تقدم توجيهات خبيرة طوال رحلة العقار الخاصة بك.
    من العثور على العقار المثالي إلى التنقل عبر المفاوضات المعقدة والأوراق، مستشارونا هنا للمساعدة.
    """)
    
    # Tabs for different sections
    tabs = st.tabs(["Find a Consultant", "Services", "Why Use a Consultant", "Success Stories"])
    
    with tabs[0]:
        st.subheader("Find a Real Estate Consultant / ابحث عن مستشار عقاري")
        
        # Search filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            specialty = st.selectbox("Specialty / التخصص", ["All", "Luxury Properties", "Family Homes", "Investment Properties", "First-time Buyers"])
        
        with col2:
            area = st.multiselect("Area / المنطقة", ["Al Olaya", "Al Nakheel", "Hittin", "Al Malaz", "Al Naseem", "All Riyadh Areas"])
        
        with col3:
            language = st.multiselect("Language / اللغة", ["Arabic", "English", "French", "Urdu"])
        
        # Load consultants data
        consultants = load_consultants()
        
        # Filter consultants based on selection
        filtered_consultants = consultants.copy()
        
        if specialty != "All":
            filtered_consultants = [c for c in filtered_consultants if c["specialty"] == specialty]
        
        if area:
            filtered_consultants = [c for c in filtered_consultants if "All Riyadh Areas" in c["areas"] or any(a in c["areas"] for a in area)]
        
        if language:
            filtered_consultants = [c for c in filtered_consultants if any(l in c["languages"] for l in language)]
        
        # Display consultants
        if filtered_consultants:
            st.markdown(f"<h3>Found {len(filtered_consultants)} consultants / تم العثور على {len(filtered_consultants)} مستشار</h3>", unsafe_allow_html=True)
            
            for consultant in filtered_consultants:
                st.markdown(f"""
                <div style="background-color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                        <h3 style="margin: 0;">{consultant['name']} / {consultant['name_ar']}</h3>
                        <span style="background-color: {'#e6f4ff' if consultant['availability'] == 'Available' else '#fff2e6'}; color: {'#1e3c72' if consultant['availability'] == 'Available' else '#ff9933'}; padding: 5px 10px; border-radius: 4px; font-size: 14px;">
                            {consultant['availability']}
                        </span>
                    </div>
                    
                    <div style="display: flex; flex-wrap: wrap; gap: 20px; margin-bottom: 15px;">
                        <div>
                            <span style="color: #666;">Specialty / التخصص</span>
                            <h4 style="margin: 5px 0; color: #1e3c72;">{consultant['specialty']} / {consultant['specialty_ar']}</h4>
                        </div>
                        <div>
                            <span style="color: #666;">Experience / الخبرة</span>
                            <h4 style="margin: 5px 0; color: #1e3c72;">{consultant['experience']} years</h4>
                        </div>
                        <div>
                            <span style="color: #666;">Rating / التقييم</span>
                            <h4 style="margin: 5px 0; color: #1e3c72;">{consultant['rating']} <small>({consultant['reviews']} reviews)</small></h4>
                        </div>
                        <div>
                            <span style="color: #666;">Fee / الرسوم</span>
                            <h4 style="margin: 5px 0; color: #1e3c72;">{consultant['fee']}</h4>
                        </div>
                    </div>
                    
                    <div style="margin-bottom: 15px;">
                        <h4 style="margin-bottom: 10px;">Areas / المناطق</h4>
                        <div style="display: flex; flex-wrap: wrap; gap: 10px;">
                """, unsafe_allow_html=True)
                
                for area_name in consultant['areas']:
                    st.markdown(f"""
                    <span style="background-color: #f0f2f5; padding: 5px 10px; border-radius: 20px;">
                        <i class="fas fa-map-marker-alt" style="color: #9a86fe; margin-right: 5px;"></i> {area_name}
                    </span>
                    """, unsafe_allow_html=True)
                
                st.markdown("</div></div>", unsafe_allow_html=True)
                
                # Languages
                st.markdown("""
                <div style="margin-bottom: 15px;">
                    <h4 style="margin-bottom: 10px;">Languages / اللغات</h4>
                    <div style="display: flex; flex-wrap: wrap; gap: 10px;">
                """, unsafe_allow_html=True)
                
                for lang in consultant['languages']:
                    st.markdown(f"""
                    <span style="background-color: #f0f2f5; padding: 5px 10px; border-radius: 20px;">
                        <i class="fas fa-language" style="color: #9a86fe; margin-right: 5px;"></i> {lang}
                    </span>
                    """, unsafe_allow_html=True)
                
                st.markdown("</div></div>", unsafe_allow_html=True)
                
                # Certifications
                st.markdown("""
                <div style="margin-bottom: 15px;">
                    <h4 style="margin-bottom: 10px;">Certifications / الشهادات</h4>
                    <div style="display: flex; flex-wrap: wrap; gap: 10px;">
                """, unsafe_allow_html=True)
                
                for cert in consultant['certifications']:
                    st.markdown(f"""
                    <span style="background-color: #e6f4ff; color: #1e3c72; padding: 5px 10px; border-radius: 20px;">
                        <i class="fas fa-certificate" style="margin-right: 5px;"></i> {cert}
                    </span>
                    """, unsafe_allow_html=True)
                
                st.markdown("</div></div>", unsafe_allow_html=True)
                
                # Action buttons
                st.markdown("""
                <div style="display: flex; gap: 10px;">
                    <button style="background-color: #9a86fe; color: white; border: none; padding: 8px 15px; border-radius: 5px; cursor: pointer; flex: 1;">Contact Consultant</button>
                    <button style="background-color: white; color: #1e3c72; border: 1px solid #1e3c72; padding: 8px 15px; border-radius: 5px; cursor: pointer; flex: 1;">View Reviews</button>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("No consultants match your search criteria. Try adjusting your filters.")
        
        # Request consultant form
        st.subheader("Request a Consultant / طلب مستشار")
        
        with st.form("consultant_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Your Name / اسمك")
                phone = st.text_input("Phone Number / رقم الهاتف")
                email = st.text_input("Email / البريد الإلكتروني")
            
            with col2:
                property_interest = st.selectbox("Property Interest / اهتمام العقار", ["Buying", "Selling", "Investing", "Renting"])
                preferred_specialty = st.selectbox("Preferred Consultant Specialty / تخصص المستشار المفضل", ["Luxury Properties", "Family Homes", "Investment Properties", "First-time Buyers", "No Preference"])
                notes = st.text_area("Additional Notes / ملاحظات إضافية", height=100)
            
            submit_button = st.form_submit_button("Submit Request / إرسال الطلب")
            
            if submit_button:
                st.success("Your consultant request has been submitted! One of our consultants will contact you within 24 hours.")
    
    with tabs[1]:
        st.subheader("Services / الخدمات")
        
        # Service categories
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style="background-color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                <div style="text-align: center; margin-bottom: 15px;">
                    <i class="fas fa-search" style="font-size: 36px; color: #9a86fe;"></i>
                </div>
                <h3 style="text-align: center; margin-bottom: 15px;">Property Search / البحث عن العقار</h3>
                <p>Our consultants help you find properties that match your criteria, saving you time and effort.</p>
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-top: 15px;">
                    <h4 style="margin-top: 0;">Services Include:</h4>
                    <ul style="margin-bottom: 0;">
                        <li>Understanding your requirements</li>
                        <li>Curated property recommendations</li>
                        <li>Off-market property access</li>
                        <li>Property viewing coordination</li>
                        <li>Neighborhood insights</li>
                    </ul>
                </div>
                <div style="text-align: center; margin-top: 15px;">
                    <span style="background-color: #e6f4ff; color: #1e3c72; padding: 5px 10px; border-radius: 5px; display: inline-block;">
                        Starting from 3,000 SAR
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style="background-color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                <div style="text-align: center; margin-bottom: 15px;">
                    <i class="fas fa-handshake" style="font-size: 36px; color: #9a86fe;"></i>
                </div>
                <h3 style="text-align: center; margin-bottom: 15px;">Negotiation Support / دعم التفاوض</h3>
                <p>Skilled negotiation can save you thousands. Our consultants represent your interests and help secure the best possible deal.</p>
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-top: 15px;">
                    <h4 style="margin-top: 0;">Services Include:</h4>
                    <ul style="margin-bottom: 0;">
                        <li>Market value assessment</li>
                        <li>Offer preparation and presentation</li>
                        <li>Counter-offer advice</li>
                        <li>Price negotiation</li>
                        <li>Contract terms negotiation</li>
                    </ul>
                </div>
                <div style="text-align: center; margin-top: 15px;">
                    <span style="background-color: #e6f4ff; color: #1e3c72; padding: 5px 10px; border-radius: 5px; display: inline-block;">
                        Starting from 2,000 SAR
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background-color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                <div style="text-align: center; margin-bottom: 15px;">
                    <i class="fas fa-file-contract" style="font-size: 36px; color: #9a86fe;"></i>
                </div>
                <h3 style="text-align: center; margin-bottom: 15px;">Transaction Management / إدارة المعاملات</h3>
                <p>Our consultants guide you through the entire transaction process, ensuring everything goes smoothly from offer to closing.</p>
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-top: 15px;">
                    <h4 style="margin-top: 0;">Services Include:</h4>
                    <ul style="margin-bottom: 0;">
                        <li>Contract review and explanation</li>
                        <li>Required document preparation</li>
                        <li>Coordination with all parties</li>
                        <li>Due diligence oversight</li>
                        <li>Closing process management</li>
                    </ul>
                </div>
                <div style="text-align: center; margin-top: 15px;">
                    <span style="background-color: #e6f4ff; color: #1e3c72; padding: 5px 10px; border-radius: 5px; display: inline-block;">
                        Starting from 4,000 SAR
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style="background-color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                <div style="text-align: center; margin-bottom: 15px;">
                    <i class="fas fa-chart-line" style="font-size: 36px; color: #9a86fe;"></i>
                </div>
                <h3 style="text-align: center; margin-bottom: 15px;">Investment Advisory / استشارات الاستثمار</h3>
                <p>For investors, our consultants provide market analysis, ROI calculations, and strategic advice to maximize your investment returns.</p>
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-top: 15px;">
                    <h4 style="margin-top: 0;">Services Include:</h4>
                    <ul style="margin-bottom: 0;">
                        <li>Market trend analysis</li>
                        <li>Rental yield calculations</li>
                        <li>Capital growth projections</li>
                        <li>Investment property sourcing</li>
                        <li>Portfolio diversification advice</li>
                    </ul>
                </div>
                <div style="text-align: center; margin-top: 15px;">
                    <span style="background-color: #e6f4ff; color: #1e3c72; padding: 5px 10px; border-radius: 5px; display: inline-block;">
                        Starting from 5,000 SAR
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Full-service packages
        st.subheader("Full-Service Packages / حزم الخدمة الكاملة")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style="background-color: white; padding: 20px; border-radius: 10px; height: 450px; position: relative; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                <div style="text-align: center;">
                    <h3 style="color: #9a86fe;">Essential Package</h3>
                    <div style="font-size: 28px; font-weight: bold; margin: 15px 0;">8,000 SAR</div>
                    <p>Perfect for first-time buyers</p>
                </div>
                <div style="margin: 20px 0;">
                    <ul>
                        <li>Property search assistance</li>
                        <li>3 property viewings</li>
                        <li>Basic negotiation support</li>
                        <li>Standard contract review</li>
                        <li>Basic closing support</li>
                    </ul>
                </div>
                <div style="position: absolute; bottom: 20px; left: 0; right: 0; text-align: center;">
                    <button style="background-color: #9a86fe; color: white; border: none; padding: 8px 15px; border-radius: 5px; cursor: pointer; width: 80%;">Select Package</button>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background-color: #1e3c72; color: white; padding: 20px; border-radius: 10px; height: 450px; position: relative; box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);">
                <div style="position: absolute; top: -10px; left: 0; right: 0; text-align: center;">
                    <span style="background-color: #9a86fe; color: white; padding: 5px 15px; border-radius: 20px; font-weight: bold;">Most Popular</span>
                </div>
                <div style="text-align: center; margin-top: 15px;">
                    <h3 style="color: #9a86fe;">Premium Package</h3>
                    <div style="font-size: 28px; font-weight: bold; margin: 15px 0;">15,000 SAR</div>
                    <p>Comprehensive support for buyers</p>
                </div>
                <div style="margin: 20px 0;">
                    <ul>
                        <li>All Essential Package services</li>
                        <li>Unlimited property viewings</li>
                        <li>Advanced negotiation strategy</li>
                        <li>Detailed contract review</li>
                        <li>Full closing management</li>
                        <li>Inspector coordination</li>
                        <li>Financing assistance</li>
                    </ul>
                </div>
                <div style="position: absolute; bottom: 20px; left: 0; right: 0; text-align: center;">
                    <button style="background-color: #9a86fe; color: white; border: none; padding: 8px 15px; border-radius: 5px; cursor: pointer; width: 80%;">Select Package</button>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="background-color: white; padding: 20px; border-radius: 10px; height: 450px; position: relative; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                <div style="text-align: center;">
                    <h3 style="color: #9a86fe;">Investor Package</h3>
                    <div style="font-size: 28px; font-weight: bold; margin: 15px 0;">25,000 SAR</div>
                    <p>Specialized for property investors</p>
                </div>
                <div style="margin: 20px 0;">
                    <ul>
                        <li>All Premium Package services</li>
                        <li>Market analysis report</li>
                        <li>Investment property sourcing</li>
                        <li>ROI calculations</li>
                        <li>Future growth projections</li>
                        <li>Rental management setup</li>
                        <li>Tax optimization advice</li>
                        <li>Investment portfolio review</li>
                    </ul>
                </div>
                <div style="position: absolute; bottom: 20px; left: 0; right: 0; text-align: center;">
                    <button style="background-color: #9a86fe; color: white; border: none; padding: 8px 15px; border-radius: 5px; cursor: pointer; width: 80%;">Select Package</button>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with tabs[2]:
        st.subheader("Why Use a Real Estate Consultant / لماذا تستخدم مستشار عقاري")
        
        # Benefits of using a consultant
        st.markdown("""
        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin-bottom: 30px;">
            <div style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                <div style="display: flex; align-items: center; margin-bottom: 15px;">
                    <i class="fas fa-clock" style="font-size: 24px; color: #9a86fe; margin-right: 15px;"></i>
                    <h4 style="margin: 0; color: #1e3c72;">Save Time / توفير الوقت</h4>
                </div>
                <p style="margin: 0;">Our consultants handle property searching, viewings, and paperwork, saving you countless hours. Focus on your priorities while we manage the details.</p>
            </div>
            
            <div style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                <div style="display: flex; align-items: center; margin-bottom: 15px;">
                    <i class="fas fa-money-bill-wave" style="font-size: 24px; color: #9a86fe; margin-right: 15px;"></i>
                    <h4 style="margin: 0; color: #1e3c72;">Save Money / توفير المال</h4>
                </div>
                <p style="margin: 0;">Skilled negotiation often saves more than the consultant's fee. Our experts know market values and can help you avoid overpriced properties.</p>
            </div>
            
            <div style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                <div style="display: flex; align-items: center; margin-bottom: 15px;">
                    <i class="fas fa-database" style="font-size: 24px; color: #9a86fe; margin-right: 15px;"></i>
                    <h4 style="margin: 0; color: #1e3c72;">Market Knowledge / معرفة السوق</h4>
                </div>
                <p style="margin: 0;">Our consultants have deep knowledge of the local market, pricing trends, and neighborhood insights that aren't available through online searches.</p>
            </div>
            
            <div style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                <div style="display: flex; align-items: center; margin-bottom: 15px;">
                    <i class="fas fa-shield-alt" style="font-size: 24px; color: #9a86fe; margin-right: 15px;"></i>
                    <h4 style="margin: 0; color: #1e3c72;">Avoid Pitfalls / تجنب المشاكل</h4>
                </div>
                <p style="margin: 0;">Property transactions involve complex legal and financial considerations. Our consultants help you navigate potential risks and avoid costly mistakes.</p>
            </div>
            
            <div style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                <div style="display: flex; align-items: center; margin-bottom: 15px;">
                    <i class="fas fa-door-open" style="font-size: 24px; color: #9a86fe; margin-right: 15px;"></i>
                    <h4 style="margin: 0; color: #1e3c72;">Access to Off-Market Properties / الوصول إلى العقارات غير المعلنة</h4>
                </div>
                <p style="margin: 0;">Our consultants have access to exclusive listings and off-market properties not available to the general public, expanding your options.</p>
            </div>
            
            <div style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                <div style="display: flex; align-items: center; margin-bottom: 15px;">
                    <i class="fas fa-users" style="font-size: 24px; color: #9a86fe; margin-right: 15px;"></i>
                    <h4 style="margin: 0; color: #1e3c72;">Professional Network / شبكة مهنية</h4>
                </div>
                <p style="margin: 0;">Our consultants provide connections to trusted inspectors, mortgage brokers, attorneys, and other professionals needed throughout the transaction.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Statistics
        st.subheader("The Value of Professional Representation / قيمة التمثيل المهني")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style="background-color: #f0f8ff; padding: 30px; border-radius: 10px; text-align: center;">
                <h1 style="color: #9a86fe; font-size: 48px; margin-bottom: 10px;">12%</h1>
                <p style="margin: 0; font-size: 16px;">Average savings on purchase price when using a consultant</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background-color: #f0f8ff; padding: 30px; border-radius: 10px; text-align: center;">
                <h1 style="color: #9a86fe; font-size: 48px; margin-bottom: 10px;">65%</h1>
                <p style="margin: 0; font-size: 16px;">Faster closing time compared to unrepresented buyers</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="background-color: #f0f8ff; padding: 30px; border-radius: 10px; text-align: center;">
                <h1 style="color: #9a86fe; font-size: 48px; margin-bottom: 10px;">93%</h1>
                <p style="margin: 0; font-size: 16px;">Client satisfaction rate with our consultants</p>
            </div>
            """, unsafe_allow_html=True)
        
        # FAQ
        st.subheader("Frequently Asked Questions / الأسئلة الشائعة")
        
        with st.expander("How are consultant fees structured? / كيف يتم هيكلة رسوم المستشار؟", expanded=True):
            st.markdown("""
            Our consultants typically operate under two fee structures:
            
            1. **Percentage-based Fee**: A percentage of the property price, typically 1-2% depending on the consultant and services provided.
            
            2. **Fixed Fee**: A predetermined amount based on the service package selected, ranging from 3,000 to 25,000 SAR.
            
            The fee structure is always transparent and agreed upon before any services begin.
            """)
        
        with st.expander("What's the difference between a real estate agent and a consultant? / ما هو الفرق بين وكيل العقارات والمستشار؟", expanded=False):
            st.markdown("""
            While there is some overlap in services, there are key differences:
            
            - **Real Estate Agents** typically represent either buyers or sellers in transactions, and are compensated through commissions paid by the seller.
            
            - **Real Estate Consultants** work exclusively for you and provide more comprehensive advisory services. They are paid directly by you, ensuring their loyalty is solely to your interests.
            
            Our consultants provide strategic advice, market analysis, and guidance throughout the entire property journey, beyond just the transaction itself.
            """)
        
        with st.expander("How long does it typically take to find a property? / كم من الوقت يستغرق عادة للعثور على عقار؟", expanded=False):
            st.markdown("""
            The timeframe varies based on your requirements and market conditions. On average:
            
            - **Standard Requirements**: 2-4 weeks to find suitable options
            - **Specialized Requirements**: 4-8 weeks for more unique property needs
            - **Luxury or High-End Properties**: Sometimes 1-3 months to find the perfect match
            
            Our consultants work efficiently to find properties matching your criteria as quickly as possible, while ensuring quality options.
            """)
        
        with st.expander("Can consultants help with investment properties? / هل يمكن للمستشارين المساعدة في عقارات الاستثمار؟", expanded=False):
            st.markdown("""
            Yes, many of our consultants specialize in investment properties. They can:
            
            - Analyze potential ROI and rental yields
            - Identify up-and-coming areas with growth potential
            - Advise on property types that match your investment goals
            - Help create an investment strategy
            - Connect you with property management services
            
            We recommend our Investor Package for clients focused on investment properties.
            """)
    
    with tabs[3]:
        st.subheader("Success Stories / قصص النجاح")
        
        # Customer testimonials
        st.markdown("""
        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin-bottom: 30px;">
            <div style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                <div style="color: #9a86fe; margin-bottom: 10px;">
                    <i class="fas fa-star"></i>
                    <i class="fas fa-star"></i>
                    <i class="fas fa-star"></i>
                    <i class="fas fa-star"></i>
                    <i class="fas fa-star"></i>
                </div>
                <p style="font-style: italic; margin-bottom: 20px;">"Ahmed helped us find our dream home in Al Nakheel. His knowledge of the area was invaluable, and he negotiated a price 8% below the asking price. We wouldn't have found this property without him."</p>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <p style="font-weight: bold; margin: 0;">Mohammed & Sara Al-Otaibi</p>
                        <p style="font-size: 14px; color: #666; margin: 0;">First-time homebuyers</p>
                    </div>
                    <div>
                        <p style="font-size: 14px; color: #666; margin: 0;">Consultant: Ahmed Al-Qahtani</p>
                    </div>
                </div>
            </div>
            
            <div style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                <div style="color: #9a86fe; margin-bottom: 10px;">
                    <i class="fas fa-star"></i>
                    <i class="fas fa-star"></i>
                    <i class="fas fa-star"></i>
                    <i class="fas fa-star"></i>
                    <i class="fas fa-star"></i>
                </div>
                <p style="font-style: italic; margin-bottom: 20px;">"As an investor from outside Riyadh, I needed someone with local knowledge. Khalid's investment advice was spot-on. My rental property is generating 15% higher returns than I expected."</p>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <p style="font-weight: bold; margin: 0;">Fahad Al-Ahmadi</p>
                        <p style="font-size: 14px; color: #666; margin: 0;">Property Investor</p>
                    </div>
                    <div>
                        <p style="font-size: 14px; color: #666; margin: 0;">Consultant: Khalid Alsudairi</p>
                    </div>
                </div>
            </div>
            
            <div style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                <div style="color: #9a86fe; margin-bottom: 10px;">
                    <i class="fas fa-star"></i>
                    <i class="fas fa-star"></i>
                    <i class="fas fa-star"></i>
                    <i class="fas fa-star"></i>
                    <i class="fas fa-star-half-alt"></i>
                </div>
                <p style="font-style: italic; margin-bottom: 20px;">"Noura made the home buying process so much easier. As first-time buyers, we were overwhelmed by the paperwork and process. She guided us every step of the way and found us a beautiful home in our budget."</p>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <p style="font-weight: bold; margin: 0;">Abdullah & Hana Al-Ghamdi</p>
                        <p style="font-size: 14px; color: #666; margin: 0;">Newlywed Couple</p>
                    </div>
                    <div>
                        <p style="font-size: 14px; color: #666; margin: 0;">Consultant: Noura Al-Dossary</p>
                    </div>
                </div>
            </div>
            
            <div style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                <div style="color: #9a86fe; margin-bottom: 10px;">
                    <i class="fas fa-star"></i>
                    <i class="fas fa-star"></i>
                    <i class="fas fa-star"></i>
                    <i class="fas fa-star"></i>
                    <i class="fas fa-star"></i>
                </div>
                <p style="font-style: italic; margin-bottom: 20px;">"Fatima helped us find the perfect family home. Her knowledge of schools and family-friendly neighborhoods was exceptional. She negotiated several repairs before closing, saving us thousands."</p>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <p style="font-weight: bold; margin: 0;">Saleh & Norah Al-Mansour</p>
                        <p style="font-size: 14px; color: #666; margin: 0;">Family of Five</p>
                    </div>
                    <div>
                        <p style="font-size: 14px; color: #666; margin: 0;">Consultant: Fatima Al-Harbi</p>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Case studies
        st.subheader("Featured Case Studies / دراسات الحالة المميزة")
        
        with st.expander("Luxury Villa in Al Nakheel - 15% Below Market", expanded=True):
            st.markdown("""
            <div style="display: flex; gap: 20px; margin-bottom: 20px;">
                <div style="flex: 1;">
                    <h4 style="color: #1e3c72; margin-top: 0;">The Challenge</h4>
                    <p>An expatriate family moving to Riyadh needed a luxury villa in Al Nakheel district. They had specific requirements for school proximity, security features, and modern design. With limited time in the country for viewings, they needed efficient, focused assistance.</p>
                    
                    <h4 style="color: #1e3c72;">Our Approach</h4>
                    <p>Consultant Ahmed Al-Qahtani:</p>
                    <ul>
                        <li>Pre-screened 27 properties to identify the 7 best matches</li>
                        <li>Conducted video tours for remote assessment</li>
                        <li>Researched neighborhood amenities and school ratings</li>
                        <li>Discovered the seller was relocating internationally and motivated to sell quickly</li>
                        <li>Negotiated pricing based on comparative market analysis</li>
                        <li>Coordinated building inspections and follow-up negotiations</li>
                    </ul>
                </div>
                
                <div style="flex: 1;">
                    <h4 style="color: #1e3c72; margin-top: 0;">The Results</h4>
                    <ul>
                        <li>Secured a 5-bedroom villa in prime location</li>
                        <li>Negotiated price 15% below initial asking price</li>
                        <li>Included high-end appliances and custom furnishings</li>
                        <li>Arranged all paperwork remotely before client's arrival</li>
                        <li>Closed the transaction within 3 weeks</li>
                        <li>Total client savings: 525,000 SAR</li>
                    </ul>
                    
                    <div style="background-color: #f0f8ff; padding: 15px; border-radius: 10px; margin-top: 20px;">
                        <h4 style="color: #1e3c72; margin-top: 0;">Client Testimonial</h4>
                        <p style="font-style: italic; margin-bottom: 10px;">"Ahmed's expertise saved us not just money but time and stress. He understood exactly what we needed and negotiated brilliantly on our behalf. We couldn't have managed this transition so smoothly without him."</p>
                        <p style="margin: 0;">— James & Layla Thompson</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with st.expander("First-Time Buyer Journey - From Apartment to Townhouse", expanded=False):
            st.markdown("""
            <div style="display: flex; gap: 20px; margin-bottom: 20px;">
                <div style="flex: 1;">
                    <h4 style="color: #1e3c72; margin-top: 0;">The Challenge</h4>
                    <p>A young Saudi couple with a baby on the way was looking to buy their first home. They initially thought they could only afford an apartment but wanted outdoor space for their growing family. With limited understanding of the buying process and financing options, they needed comprehensive guidance.</p>
                    
                    <h4 style="color: #1e3c72;">Our Approach</h4>
                    <p>Consultant Noura Al-Dossary:</p>
                    <ul>
                        <li>Provided education on the entire buying process</li>
                        <li>Connected them with mortgage specialists to maximize their budget</li>
                        <li>Identified an up-and-coming neighborhood with good value</li>
                        <li>Found a townhouse option they hadn't considered</li>
                        <li>Negotiated favorable terms including extended closing</li>
                        <li>Coordinated inspections and supervised repairs</li>
                    </ul>
                </div>
                
                <div style="flex: 1;">
                    <h4 style="color: #1e3c72; margin-top: 0;">The Results</h4>
                    <ul>
                        <li>Secured a 3-bedroom townhouse instead of a 2-bedroom apartment</li>
                        <li>Found a property with a private garden</li>
                        <li>Obtained a 3.4% interest rate through lender recommendations</li>
                        <li>Negotiated 50,000 SAR in necessary repairs</li>
                        <li>Closed the transaction before baby's arrival</li>
                        <li>Property has appreciated 12% in the year since purchase</li>
                    </ul>
                    
                    <div style="background-color: #f0f8ff; padding: 15px; border-radius: 10px; margin-top: 20px;">
                        <h4 style="color: #1e3c72; margin-top: 0;">Client Testimonial</h4>
                        <p style="font-style: italic; margin-bottom: 10px;">"Noura expanded our vision of what was possible. We never thought we could afford a townhouse with a garden. She didn't just find us a home; she educated us throughout the process and gave us confidence in our investment."</p>
                        <p style="margin: 0;">— Saad & Reema Al-Zahrani</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with st.expander("Investment Portfolio Growth - 22% Return in 18 Months", expanded=False):
            st.markdown("""
            <div style="display: flex; gap: 20px; margin-bottom: 20px;">
                <div style="flex: 1;">
                    <h4 style="color: #1e3c72; margin-top: 0;">The Challenge</h4>
                    <p>A Saudi investor had 5 million SAR to invest in real estate but wanted to diversify across property types and locations. He needed strategic advice on maximizing returns while balancing risk, with a focus on both rental income and capital appreciation.</p>
                    
                    <h4 style="color: #1e3c72;">Our Approach</h4>
                    <p>Consultant Khalid Alsudairi:</p>
                    <ul>
                        <li>Conducted comprehensive market analysis across Riyadh</li>
                        <li>Identified emerging districts with growth potential</li>
                        <li>Created a diversified investment strategy</li>
                        <li>Sourced off-market properties with value-add potential</li>
                        <li>Negotiated bulk purchase discounts</li>
                        <li>Connected client with property management services</li>
                    </ul>
                </div>
                
                <div style="flex: 1;">
                    <h4 style="color: #1e3c72; margin-top: 0;">The Results</h4>
                    <ul>
                        <li>Acquired portfolio of 5 properties across 3 districts</li>
                        <li>Mix of apartments, townhomes, and commercial space</li>
                        <li>Average initial rental yield of 8.2%</li>
                        <li>Capital appreciation of 14% in first 18 months</li>
                        <li>Total ROI of 22% in 18 months</li>
                        <li>Established efficient property management system</li>
                    </ul>
                    
                    <div style="background-color: #f0f8ff; padding: 15px; border-radius: 10px; margin-top: 20px;">
                        <h4 style="color: #1e3c72; margin-top: 0;">Client Testimonial</h4>
                        <p style="font-style: italic; margin-bottom: 10px;">"Khalid's investment strategy was brilliant. His knowledge of emerging areas and ability to find off-market deals gave me a significant advantage. The portfolio is performing even better than projected, and I've since allocated additional funds for him to invest."</p>
                        <p style="margin: 0;">— Ibrahim Al-Saud</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# AI chat page
def show_ai_chat():
    st.markdown("<h1>Chat with SUHAIL AI / الدردشة مع الذكاء الاصطناعي سُهيل</h1>", unsafe_allow_html=True)
    
    # Introduction
    st.markdown("""
    Our AI assistant specializes in Saudi real estate and can answer your questions about properties, 
    neighborhoods, financing options, and transaction processes. Ask anything to get instant expertise!
    
    يتخصص مساعدنا الذكي في العقارات السعودية ويمكنه الإجابة على أسئلتك حول العقارات،
    الأحياء، خيارات التمويل، وعمليات المعاملات. اسأل أي شيء للحصول على خبرة فورية!
    """)
    
    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Display chat history
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="chat-message chat-message-user">
                <p>{message["content"]}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message chat-message-bot">
                <p>{message["content"]}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Chat input
    user_input = st.text_input("Type your question here...", key="user_input")
    
    if user_input:
        # Check if this exact question was asked before
        if any(msg["role"] == "user" and msg["content"] == user_input for msg in st.session_state.chat_history[:-1]):
            # User is repeating the exact same question
            repeat_response = """
            أعتقد أنني أجبت بالفعل على هذا السؤال. هل تود معرفة المزيد من التفاصيل أو لديك سؤال آخر؟
            
            I believe I've already answered this question. Would you like more specific details or do you have a different question?
            """
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            st.session_state.chat_history.append({"role": "assistant", "content": repeat_response})
            st.rerun()
            return
        
        # Get AI response
        with st.spinner("Thinking..."):
            try:
                ai_response = get_ai_response(user_input, st.session_state.chat_history)
            except Exception as e:
                ai_response = """
                مرحبا! أنا سُهيل، مساعدك الذكي المتخصص في العقارات السعودية. كيف يمكنني مساعدتك اليوم؟ يمكنني تقديم معلومات حول العقارات، الأحياء، خيارات التمويل، وعمليات الشراء.
                
                Hello! I'm Suhail, your AI assistant specializing in Saudi real estate. How can I help you today? I can provide information about properties, neighborhoods, financing options, and buying processes.
                """
        
        # Add AI response to chat history
        st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
        
        # Rerun to display the updated chat
        st.rerun()
    
    # Suggested questions
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h4>Suggested Questions / أسئلة مقترحة</h4>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.button("What are the best neighborhoods for families in Riyadh?", key="q1", on_click=lambda: st.session_state.update({"user_input": "What are the best neighborhoods for families in Riyadh?"}))
        st.button("How does Islamic financing work for home purchases?", key="q2", on_click=lambda: st.session_state.update({"user_input": "How does Islamic financing work for home purchases?"}))
        st.button("What documents do I need to buy a property in Saudi Arabia?", key="q3", on_click=lambda: st.session_state.update({"user_input": "What documents do I need to buy a property in Saudi Arabia?"}))
    
    with col2:
        st.button("What is the average price per square meter in Al Olaya?", key="q4", on_click=lambda: st.session_state.update({"user_input": "What is the average price per square meter in Al Olaya?"}))
        st.button("How do I qualify for a mortgage as an expatriate?", key="q5", on_click=lambda: st.session_state.update({"user_input": "How do I qualify for a mortgage as an expatriate?"}))
        st.button("What should I check during a property inspection?", key="q6", on_click=lambda: st.session_state.update({"user_input": "What should I check during a property inspection?"}))
    
    # Related resources
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h4>Related Resources / موارد ذات صلة</h4>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
            <h5 style="margin-top: 0; color: #1e3c72;">Saudi Real Estate Guide 2025</h5>
            <p style="font-size: 14px;">Comprehensive guide to buying, selling, and investing in Saudi real estate.</p>
            <button style="background-color: #9a86fe; color: white; border: none; padding: 5px 10px; border-radius: 5px; font-size: 14px; cursor: pointer;">Download Guide</button>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
            <h5 style="margin-top: 0; color: #1e3c72;">Riyadh Neighborhood Reports</h5>
            <p style="font-size: 14px;">Detailed market reports for major Riyadh neighborhoods, including pricing trends.</p>
            <button style="background-color: #9a86fe; color: white; border: none; padding: 5px 10px; border-radius: 5px; font-size: 14px; cursor: pointer;">View Reports</button>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
            <h5 style="margin-top: 0; color: #1e3c72;">Financing Calculator</h5>
            <p style="font-size: 14px;">Advanced calculator to estimate mortgage payments and financing options.</p>
            <button style="background-color: #9a86fe; color: white; border: none; padding: 5px 10px; border-radius: 5px; font-size: 14px; cursor: pointer;">Open Calculator</button>
        </div>
        """, unsafe_allow_html=True)

# Buying journey page
def show_buying_journey():
    st.markdown("<h1>Home Buying Journey / رحلة شراء المنزل</h1>", unsafe_allow_html=True)
    
    # Introduction
    st.markdown("""
    Purchasing a home in Saudi Arabia involves several steps. Our platform guides you through each stage
    of the process, from initial search to final closing. Follow our structured approach to make your home buying journey smooth and successful.
    
    يتضمن شراء منزل في المملكة العربية السعودية عدة خطوات. تساعدك منصتنا من خلال كل مرحلة
    من العملية، من البحث الأولي إلى الإغلاق النهائي. اتبع نهجنا المنظم لجعل رحلة شراء منزلك سلسة وناجحة.
    """)
    
    # Progress tracker
    st.subheader("Your Journey Progress / تقدم رحلتك")
    
    # Set current stage (this would normally be saved in the user's profile)
    current_stage = 2  # Example: Financing stage
    
    # Define stages
    stages = [
        {"number": 1, "title": "Property Search", "active": current_stage >= 1, "completed": current_stage > 1},
        {"number": 2, "title": "Financing", "active": current_stage >= 2, "completed": current_stage > 2},
        {"number": 3, "title": "Inspection", "active": current_stage >= 3, "completed": current_stage > 3},
        {"number": 4, "title": "Legal Verification", "active": current_stage >= 4, "completed": current_stage > 4},
        {"number": 5, "title": "Closing", "active": current_stage >= 5, "completed": current_stage > 5}
    ]
    
    # Create custom progress bar
    progress_html = """
    <div style="position: relative; margin: 30px 0; height: 6px; background-color: #eee; border-radius: 3px;">
        <div style="position: absolute; top: 0; left: 0; height: 6px; width: {}%; background-color: #9a86fe; border-radius: 3px;"></div>
    """.format((current_stage - 1) * 25)
    
    for i, stage in enumerate(stages):
        position = i * 25
        progress_html += f"""
        <div style="position: absolute; top: -10px; left: {position}%; transform: translateX(-50%);">
            <div style="width: 25px; height: 25px; border-radius: 50%; background-color: {'#9a86fe' if stage['active'] else '#eee'}; color: {'white' if stage['active'] else '#666'}; display: flex; justify-content: center; align-items: center; font-weight: bold; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                {stage['number'] if not stage['completed'] else '<i class="fas fa-check"></i>'}
            </div>
            <div style="position: absolute; top: 30px; left: 50%; transform: translateX(-50%); width: max-content; font-size: 12px; color: {'#1e3c72' if stage['active'] else '#666'}; font-weight: {'bold' if stage['active'] else 'normal'};">
                {stage['title']}
            </div>
        </div>
        """
    
    progress_html += "</div><div style='height: 40px;'></div>"
    st.markdown(progress_html, unsafe_allow_html=True)
    
    # Current stage information
    st.subheader(f"Stage {current_stage}: {stages[current_stage-1]['title']} / المرحلة {current_stage}: {stages[current_stage-1]['title']}")
    
    if current_stage == 1:  # Property Search
        st.markdown("""
        <div style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); margin-bottom: 20px;">
            <h3 style="color: #1e3c72; margin-top: 0;">Property Search Stage</h3>
            <p>The first step in your home buying journey is finding the right property. Here's what to focus on during this stage:</p>
            
            <div style="margin: 20px 0;">
                <h4>Your Tasks:</h4>
                <ul>
                    <li><input type="checkbox"> Define your property requirements and budget</li>
                    <li><input type="checkbox"> Explore neighborhoods that match your lifestyle</li>
                    <li><input type="checkbox"> View multiple properties (aim for at least 5-7)</li>
                    <li><input type="checkbox"> Shortlist your top choices</li>
                    <li><input type="checkbox"> Make an offer on your preferred property</li>
                </ul>
            </div>
            
            <div style="background-color: #f0f8ff; padding: 15px; border-radius: 5px; margin-top: 20px;">
                <h4 style="margin-top: 0;">SUHAIL Tools for This Stage:</h4>
                <ul style="margin-bottom: 0;">
                    <li><strong>Property Search:</strong> Use our advanced filters to find properties matching your criteria</li>
                    <li><strong>Neighborhood Comparison:</strong> Compare different areas based on your priorities</li>
                    <li><strong>Real Estate Consultants:</strong> Connect with experts who can guide your search</li>
                    <li><strong>AI Assistant:</strong> Get instant answers to your property questions</li>
                </ul>
            </div>
        </div>
        
        <div style="text-align: center; margin: 30px 0;">
            <button style="background-color: #9a86fe; color: white; border: none; padding: 10px 20px; border-radius: 5px; font-size: 16px; cursor: pointer;">Get Started with Property Search</button>
        </div>
        """, unsafe_allow_html=True)
        
        # Featured properties for this stage
        st.subheader("Recommended Properties Based on Your Preferences")
        
        properties = load_properties()[:3]  # Just use the first 3 for demo
        
        cols = st.columns(3)
        for i, prop in enumerate(properties):
            with cols[i]:
                display_property_card(prop)
    
    elif current_stage == 2:  # Financing
        st.markdown("""
        <div style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); margin-bottom: 20px;">
            <h3 style="color: #1e3c72; margin-top: 0;">Financing Stage</h3>
            <p>Now that you've found a property, it's time to secure financing. Here's what to focus on during this stage:</p>
            
            <div style="margin: 20px 0;">
                <h4>Your Tasks:</h4>
                <ul>
                    <li><input type="checkbox" checked> Compare financing options from different banks</li>
                    <li><input type="checkbox" checked> Gather necessary financial documents</li>
                    <li><input type="checkbox"> Apply for pre-approval</li>
                    <li><input type="checkbox"> Review and accept financing offer</li>
                    <li><input type="checkbox"> Make down payment</li>
                </ul>
            </div>
            
            <div style="background-color: #f0f8ff; padding: 15px; border-radius: 5px; margin-top: 20px;">
                <h4 style="margin-top: 0;">SUHAIL Tools for This Stage:</h4>
                <ul style="margin-bottom: 0;">
                    <li><strong>Financing Hub:</strong> Compare rates and terms from our partner banks</li>
                    <li><strong>Mortgage Calculator:</strong> Estimate your monthly payments and total costs</li>
                    <li><strong>Document Checklist:</strong> Ensure you have all required paperwork</li>
                    <li><strong>Financing Assistant:</strong> Get personalized recommendations based on your financial profile</li>
                </ul>
            </div>
        </div>
        
        <div style="text-align: center; margin: 30px 0;">
            <button style="background-color: #9a86fe; color: white; border: none; padding: 10px 20px; border-radius: 5px; font-size: 16px; cursor: pointer;">Continue Financing Process</button>
        </div>
        """, unsafe_allow_html=True)
        
        # Bank recommendations for this stage
        st.subheader("Recommended Financing Options")
        
        banks = load_banks()[:3]  # Just use the first 3 for demo
        
        for bank in banks:
            st.markdown(f"""
            <div style="background-color: white; padding: 20px; border-radius: 10px; margin-bottom: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                    <h3 style="margin: 0;">{bank['name']} <span style="font-size: 16px; color: #666; font-weight: normal;"> / {bank['name_ar']}</span></h3>
                    <button style="background-color: #9a86fe; color: white; border: none; padding: 8px 15px; border-radius: 5px; cursor: pointer;">Apply Now</button>
                </div>
                <div style="display: flex; flex-wrap: wrap; gap: 20px; margin-bottom: 15px;">
                    <div>
                        <span style="color: #666;">Interest Rate</span>
                        <h4 style="margin: 5px 0; color: #1e3c72;">{bank['interest_rate']}%</h4>
                    </div>
                    <div>
                        <span style="color: #666;">Max Loan Term</span>
                        <h4 style="margin: 5px 0; color: #1e3c72;">{bank['max_loan_term']} years</h4>
                    </div>
                    <div>
                        <span style="color: #666;">Min Down Payment</span>
                        <h4 style="margin: 5px 0; color: #1e3c72;">{bank['min_down_payment']}%</h4>
                    </div>
                    <div>
                        <span style="color: #666;">Processing Fee</span>
                        <h4 style="margin: 5px 0; color: #1e3c72;">{bank['processing_fee']}%</h4>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    elif current_stage == 3:  # Inspection
        st.markdown("""
        <div style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); margin-bottom: 20px;">
            <h3 style="color: #1e3c72; margin-top: 0;">Inspection Stage</h3>
            <p>Before finalizing your purchase, it's important to have the property thoroughly inspected. Here's what to focus on during this stage:</p>
            
            <div style="margin: 20px 0;">
                <h4>Your Tasks:</h4>
                <ul>
                    <li><input type="checkbox"> Select a certified building inspector</li>
                    <li><input type="checkbox"> Schedule and attend the inspection</li>
                    <li><input type="checkbox"> Review detailed inspection report</li>
                    <li><input type="checkbox"> Negotiate repairs or price adjustments (if needed)</li>
                    <li><input type="checkbox"> Get final approval to proceed</li>
                </ul>
            </div>
            
            <div style="background-color: #f0f8ff; padding: 15px; border-radius: 5px; margin-top: 20px;">
                <h4 style="margin-top: 0;">SUHAIL Tools for This Stage:</h4>
                <ul style="margin-bottom: 0;">
                    <li><strong>Building Inspection:</strong> Connect with certified inspectors</li>
                    <li><strong>Inspection Checklist:</strong> Know what to look for during the inspection</li>
                    <li><strong>Common Issues Guide:</strong> Understand potential problem areas</li>
                    <li><strong>Negotiation Support:</strong> Get help addressing issues found during inspection</li>
                </ul>
            </div>
        </div>
        
        <div style="text-align: center; margin: 30px 0;">
            <button style="background-color: #9a86fe; color: white; border: none; padding: 10px 20px; border-radius: 5px; font-size: 16px; cursor: pointer;">Schedule an Inspection</button>
        </div>
        """, unsafe_allow_html=True)
        
        # Inspector recommendations for this stage
        st.subheader("Recommended Building Inspectors")
        
        inspectors = load_inspectors()  # Just use all for demo
        
        cols = st.columns(len(inspectors))
        for i, inspector in enumerate(inspectors):
            with cols[i]:
                st.markdown(f"""
                <div style="background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                    <h4 style="text-align: center; margin-top: 0; color: #1e3c72;">{inspector['name']}</h4>
                    <p style="text-align: center; font-size: 14px; margin-bottom: 15px;">{inspector['specialty']}</p>
                    <p style="text-align: center; margin-bottom: 5px;"><strong>Rating:</strong> {inspector['rating']} ({inspector['reviews']} reviews)</p>
                    <p style="text-align: center; margin-bottom: 15px;"><strong>Fee:</strong> {inspector['fee_range']}</p>
                    <div style="text-align: center;">
                        <button style="background-color: #9a86fe; color: white; border: none; padding: 5px 10px; border-radius: 5px; font-size: 14px; cursor: pointer; width: 100%;">Book Now</button>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    elif current_stage == 4:  # Legal Verification
        st.markdown("""
        <div style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); margin-bottom: 20px;">
            <h3 style="color: #1e3c72; margin-top: 0;">Legal Verification Stage</h3>
            <p>This stage ensures the property has clear title and complies with all legal requirements. Here's what to focus on during this stage:</p>
            
            <div style="margin: 20px 0;">
                <h4>Your Tasks:</h4>
                <ul>
                    <li><input type="checkbox"> Verify property ownership and title</li>
                    <li><input type="checkbox"> Check for any legal claims or disputes</li>
                    <li><input type="checkbox"> Ensure compliance with building regulations</li>
                    <li><input type="checkbox"> Review all legal documents</li>
                    <li><input type="checkbox"> Prepare for ownership transfer</li>
                </ul>
            </div>
            
            <div style="background-color: #f0f8ff; padding: 15px; border-radius: 5px; margin-top: 20px;">
                <h4 style="margin-top: 0;">SUHAIL Tools for This Stage:</h4>
                <ul style="margin-bottom: 0;">
                    <li><strong>Legal Verification:</strong> Integrated checks with government systems</li>
                    <li><strong>Document Review:</strong> Expert analysis of all legal documents</li>
                    <li><strong>Legal Advisor:</strong> Connect with real estate legal specialists</li>
                    <li><strong>Compliance Check:</strong> Ensure all regulatory requirements are met</li>
                </ul>
            </div>
        </div>
        
        <div style="text-align: center; margin: 30px 0;">
            <button style="background-color: #9a86fe; color: white; border: none; padding: 10px 20px; border-radius: 5px; font-size: 16px; cursor: pointer;">Start Legal Verification</button>
        </div>
        """, unsafe_allow_html=True)
        
        # Legal verification info
        st.subheader("Legal Verification Process")
        
        st.markdown("""
        <div style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
            <h4 style="color: #1e3c72; margin-top: 0;">Required Documents</h4>
            <ul>
                <li>Property Title Deed (صك الملكية)</li>
                <li>Building Permit (رخصة البناء)</li>
                <li>Seller's National ID (هوية البائع)</li>
                <li>Buyer's National ID (هوية المشتري)</li>
                <li>Sales Contract (عقد البيع)</li>
                <li>Property Survey Document (مخطط العقار)</li>
                <li>Tax Clearance Certificate (شهادة خلو من الضرائب)</li>
                <li>Utilities Payment Proof (إثبات سداد المرافق)</li>
            </ul>
            
            <h4 style="color: #1e3c72;">Verification Checks</h4>
            <ol>
                <li>Title verification through Ministry of Justice portal</li>
                <li>Ownership history check</li>
                <li>Property boundaries confirmation</li>
                <li>Encumbrances and liens check</li>
                <li>Building code compliance verification</li>
                <li>Utility connections confirmation</li>
            </ol>
            
            <div style="background-color: #fff2e6; padding: 15px; border-radius: 5px; margin-top: 15px;">
                <p style="margin: 0;"><strong>Note:</strong> SUHAIL's integrated verification system connects directly with government databases to ensure all information is current and accurate.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    elif current_stage == 5:  # Closing
        st.markdown("""
        <div style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); margin-bottom: 20px;">
            <h3 style="color: #1e3c72; margin-top: 0;">Closing Stage</h3>
            <p>The final step in your home buying journey is closing the transaction. Here's what to focus on during this stage:</p>
            
            <div style="margin: 20px 0;">
                <h4>Your Tasks:</h4>
                <ul>
                    <li><input type="checkbox"> Review and sign final purchase agreement</li>
                    <li><input type="checkbox"> Complete financing documentation</li>
                    <li><input type="checkbox"> Pay closing costs and fees</li>
                    <li><input type="checkbox"> Transfer ownership through Najiz system</li>
                    <li><input type="checkbox"> Receive property keys and documentation</li>
                </ul>
            </div>
            
            <div style="background-color: #f0f8ff; padding: 15px; border-radius: 5px; margin-top: 20px;">
                <h4 style="margin-top: 0;">SUHAIL Tools for This Stage:</h4>
                <ul style="margin-bottom: 0;">
                    <li><strong>Closing Coordinator:</strong> Expert guidance through the final steps</li>
                    <li><strong>Document Preparation:</strong> Ensure all paperwork is complete and accurate</li>
                    <li><strong>Fee Calculator:</strong> Know exactly what you'll pay at closing</li>
                    <li><strong>Digital Signing:</strong> Secure electronic signature for required documents</li>
                </ul>
            </div>
        </div>
        
        <div style="text-align: center; margin: 30px 0;">
            <button style="background-color: #9a86fe; color: white; border: none; padding: 10px 20px; border-radius: 5px; font-size: 16px; cursor: pointer;">Schedule Closing</button>
        </div>
        """, unsafe_allow_html=True)
        
        # Closing info
        st.subheader("Closing Process Overview")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                <h4 style="color: #1e3c72; margin-top: 0;">Closing Costs</h4>
                <table style="width: 100%; border-collapse: collapse;">
                    <tr>
                        <th style="padding: 8px; border: 1px solid #ddd; text-align: left;">Fee Type</th>
                        <th style="padding: 8px; border: 1px solid #ddd; text-align: right;">Amount</th>
                    </tr>
                    <tr>
                        <td style="padding: 8px; border: 1px solid #ddd;">Real Estate Transaction Tax</td>
                        <td style="padding: 8px; border: 1px solid #ddd; text-align: right;">5% of property value</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px; border: 1px solid #ddd;">Loan Processing Fee</td>
                        <td style="padding: 8px; border: 1px solid #ddd; text-align: right;">1% of loan amount</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px; border: 1px solid #ddd;">Title Transfer Fee</td>
                        <td style="padding: 8px; border: 1px solid #ddd; text-align: right;">500 SAR</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px; border: 1px solid #ddd;">Notary Services</td>
                        <td style="padding: 8px; border: 1px solid #ddd; text-align: right;">1,000 - 2,000 SAR</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px; border: 1px solid #ddd;">Registration Fee</td>
                        <td style="padding: 8px; border: 1px solid #ddd; text-align: right;">1,000 SAR</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px; border: 1px solid #ddd; font-weight: bold;">Total Estimated Closing Costs</td>
                        <td style="padding: 8px; border: 1px solid #ddd; text-align: right; font-weight: bold;">Varies by property value</td>
                    </tr>
                </table>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                <h4 style="color: #1e3c72; margin-top: 0;">Closing Day Checklist</h4>
                <ul>
                    <li><strong>Bring Photo ID:</strong> Original national ID or passport</li>
                    <li><strong>Payment Method:</strong> Certified bank check or wire transfer confirmation</li>
                    <li><strong>Review Documents:</strong> Carefully read all papers before signing</li>
                    <li><strong>Property Walkthrough:</strong> Complete final inspection before closing</li>
                    <li><strong>Insurance Proof:</strong> Bring confirmation of home insurance</li>
                    <li><strong>Contact Information:</strong> Exchange details with seller</li>
                </ul>
                
                <div style="background-color: #e6f4ff; padding: 15px; border-radius: 5px; margin-top: 15px;">
                    <p style="margin: 0;"><strong>Pro Tip:</strong> Schedule your closing early in the day to allow time for resolving any last-minute issues that might arise.</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Next steps and support
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Support & Resources / الدعم والموارد")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
            <div style="text-align: center; margin-bottom: 15px;">
                <i class="fas fa-headset" style="font-size: 36px; color: #9a86fe;"></i>
            </div>
            <h4 style="text-align: center; margin-bottom: 15px;">Personal Support</h4>
            <p style="text-align: center;">Need assistance with your journey? Our experts are here to help.</p>
            <div style="text-align: center; margin-top: 15px;">
                <button style="background-color: #9a86fe; color: white; border: none; padding: 8px 15px; border-radius: 5px; cursor: pointer;">Contact Support</button>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
            <div style="text-align: center; margin-bottom: 15px;">
                <i class="fas fa-book" style="font-size: 36px; color: #9a86fe;"></i>
            </div>
            <h4 style="text-align: center; margin-bottom: 15px;">Buyer's Guide</h4>
            <p style="text-align: center;">Download our comprehensive guide to buying property in Saudi Arabia.</p>
            <div style="text-align: center; margin-top: 15px;">
                <button style="background-color: #9a86fe; color: white; border: none; padding: 8px 15px; border-radius: 5px; cursor: pointer;">Download Guide</button>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
            <div style="text-align: center; margin-bottom: 15px;">
                <i class="fas fa-calendar-alt" style="font-size: 36px; color: #9a86fe;"></i>
            </div>
            <h4 style="text-align: center; margin-bottom: 15px;">Schedule Consultation</h4>
            <p style="text-align: center;">Book a one-on-one consultation with a real estate expert.</p>
            <div style="text-align: center; margin-top: 15px;">
                <button style="background-color: #9a86fe; color: white; border: none; padding: 8px 15px; border-radius: 5px; cursor: pointer;">Book Appointment</button>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Main execution
if __name__ == "__main__":
    main()
