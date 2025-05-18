import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import altair as alt
import random
import os
from openai import OpenAI

# Page configuration
st.set_page_config(
    page_title="Suhail - AI Real Estate Assistant",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize OpenAI client with API key from Streamlit secrets
@st.cache_resource
def get_openai_client():
    # Get the API key from Streamlit secrets
    api_key = st.secrets["OPENAI_API_KEY"]
    # Create the client without the proxies parameter
    return OpenAI(api_key=api_key)

# Custom CSS styling
custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;800&display=swap');
    
    * {
        font-family: 'Tajawal', sans-serif;
    }
    
    .property-card {
        border-radius: 10px;
        border: 1px solid #eee;
        padding: 10px;
        margin-bottom: 15px;
        transition: all 0.3s ease;
    }
    
    .property-card:hover {
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        transform: translateY(-5px);
    }
    
    .risk-low {
        color: green;
        font-weight: bold;
    }
    
    .risk-medium {
        color: orange;
        font-weight: bold;
    }
    
    .risk-high {
        color: red;
        font-weight: bold;
    }
    
    .section-header {
        color: #0056b3;
        border-bottom: 2px solid #0056b3;
        padding-bottom: 10px;
    }
    
    .chat-message {
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    
    .chat-message-user {
        background-color: #e6f7ff;
        text-align: right;
    }
    
    .chat-message-bot {
        background-color: #f0f0f0;
    }
    
    .hero-section {
        background: linear-gradient(45deg, #0056b3, #00326e);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 20px;
        text-align: center;
    }
    
    .feature-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        background-color: #e6f7ff;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

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
            "location": {"lat": 24.758913, "lng": 46.637417}
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
            "location": {"lat": 24.690595, "lng": 46.685419}
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
            "location": {"lat": 24.711667, "lng": 46.674167}
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
            "location": {"lat": 24.774772, "lng": 46.831479}
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
            "location": {"lat": 24.790107, "lng": 46.694477}
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
            "location": {"lat": 24.674667, "lng": 46.751472}
        }
    ]
    return properties

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

# Enhanced AI response function using OpenAI
def get_ai_response(prompt, history=None):
    try:
        client = get_openai_client()
        
        # Create the system message for real estate context
        messages = [{"role": "system", "content": "You are Suhail, an AI assistant specialized in Saudi Arabian real estate. You provide detailed information about properties, neighborhoods, and environmental factors. Always respond in both Arabic (first) and English (second). Be helpful, detailed, and concise. Include real estate expertise in your answers about the Saudi market, particularly for Riyadh. Provide balanced views of properties and neighborhoods."}]
        
        # Add chat history if available
        if history:
            # Only include the last 10 messages to avoid token limits
            for msg in history[-10:]:
                if msg["role"] in ["user", "assistant"]:
                    messages.append(msg)
        
        # Add the current user prompt
        messages.append({"role": "user", "content": prompt})
        
        # Call the OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Use "gpt-4" for better responses if available
            messages=messages,
            max_tokens=800,
            temperature=0.7,
        )
        
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error with OpenAI: {str(e)}")
        # Fallback message if OpenAI fails
        return "عذراً، حدث خطأ في الاتصال بقاعدة المعرفة. يرجى المحاولة مرة أخرى لاحقاً.\n\nSorry, there was an error connecting to my knowledge base. Please try again later."

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
            colors.append('green')
        elif v < 60:
            colors.append('orange')
        else:
            colors.append('red')
    
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
    ax.plot(angles, values, linewidth=2, linestyle='solid')
    ax.fill(angles, values, alpha=0.25)
    
    # Set y-limits
    ax.set_ylim(0, 100)
    
    # Add title
    plt.title(f'Neighborhood Quality: {area}', size=15, y=1.1)
    
    return fig

# Application layout
def main():
    # Sidebar for navigation
    with st.sidebar:
        st.markdown("""
                    <div style="background-color:#f0f0f0; height:200px; border-radius:10px; display:flex; 
                    justify-content:center; align-items:center; margin-bottom:10px;">
                    <p style="color:#505050;">Property Image</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Language selection
        language = st.radio("Language / اللغة", ["English", "العربية"])
        
        st.markdown("---")
        
        # Navigation
        st.subheader("Navigation")
        page = st.radio("Go to", ["Home", "Property Search", "Environmental Analysis", "Neighborhood Comparison", "Chat with AI"])
    
    # Main content
    if page == "Home":
        show_home()
    elif page == "Property Search":
        show_property_search()
    elif page == "Environmental Analysis":
        show_environmental_analysis()
    elif page == "Neighborhood Comparison":
        show_neighborhood_comparison()
    elif page == "Chat with AI":
        show_ai_chat()

# Home page
def show_home():
    # Hero section
    st.markdown("""
    <div class="hero-section">
        <h1>سهيل - مرشدك للعقار المثالي</h1>
        <h2>Suhail - Guiding You to Your Perfect Property</h2>
        <p>AI-powered real estate assistant with environmental analysis and neighborhood insights</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Introduction
    st.markdown("""
    <div style="direction: rtl; text-align: right; margin-bottom: 20px;">
        <h2>أهلاً بك في سهيل</h2>
        <p>سهيل هو تطبيق عقاري ذكي يساعدك في العثور على العقار المثالي باستخدام تحليلات بيئية وبيانات محدثة عن الأحياء.</p>
    </div>
    
    <div style="margin-bottom: 30px;">
        <h2>Welcome to Suhail</h2>
        <p>Suhail is an AI-powered real estate application that helps you find the perfect property using environmental analysis and up-to-date neighborhood data.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key features
    st.subheader("Key Features")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🏠 Property Search</h3>
            <p>Find properties matching your criteria with our powerful search tools.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3>🗣️ Bilingual Support</h3>
            <p>Full support for both Arabic and English languages.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>🌊 Environmental Analysis</h3>
            <p>Understand environmental risks like flooding, air quality, and heat effects.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3>🤖 AI Assistant</h3>
            <p>Get personalized guidance from our AI real estate assistant.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>🏫 Neighborhood Insights</h3>
            <p>Compare neighborhoods based on schools, healthcare, and more.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3>📈 Price Predictions</h3>
            <p>Get data-driven insights on property values and trends.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Featured properties
    st.subheader("Featured Properties")
    properties = load_properties()
    
    # Show top 3 properties
    cols = st.columns(3)
    for i, prop in enumerate(properties[:3]):
        with cols[i]:
            st.markdown("""
                        <div style="background-color:#f0f0f0; height:200px; border-radius:10px; display:flex; 
                        justify-content:center; align-items:center; margin-bottom:10px;">
                        <p style="color:#505050;">Property Image</p>
                        </div>
                        """, unsafe_allow_html=True)
            st.subheader(prop["title"])
            st.write(f"**Price:** {prop['price']:,} SAR")
            st.write(f"**Area:** {prop['area']}")
            st.write(f"**{prop['bedrooms']} bedrooms | {prop['bathrooms']} bathrooms | {prop['size_sqm']} sqm**")
            if st.button("View Details", key=f"home_view_{i}"):
                st.session_state.selected_property = prop["id"]
                st.session_state.page = "Property Search"
                st.rerun()

# Property search page
def show_property_search():
    st.subheader("Property Search / البحث عن العقار")
    
    # Search filters
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
    
    # Search results
    st.subheader(f"Found {len(filtered_properties)} properties / تم العثور على {len(filtered_properties)} عقار")
    
    # Property details view or search results
    if 'selected_property' in st.session_state:
        property_id = st.session_state.selected_property
        prop = next((p for p in properties if p['id'] == property_id), None)
        
        if prop:
            # Back button
            if st.button("← Back to Search Results"):
                del st.session_state.selected_property
                st.rerun()
            
            # Property details
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("""
                            <div style="background-color:#f0f0f0; height:200px; border-radius:10px; display:flex; 
                            justify-content:center; align-items:center; margin-bottom:10px;">
                            <p style="color:#505050;">Property Image</p>
                            </div>
                            """, unsafe_allow_html=True)
                
                # Property description
                st.subheader("Description / الوصف")
                st.write(prop['description'])
                st.write(prop['description_ar'])
                
                # Features
                st.subheader("Features / الميزات")
                features = ", ".join(prop['features'])
                features_ar = "، ".join(prop['features_ar'])
                st.write(features)
                st.write(features_ar)
            
            with col2:
                st.subheader(prop['title'])
                st.write(prop['title_ar'])
                st.markdown(f"**Price / السعر:** {prop['price']:,} SAR")
                st.markdown(f"**Area / المنطقة:** {prop['area']}")
                st.markdown(f"**Type / النوع:** {prop['type']}")
                st.markdown(f"**Size / المساحة:** {prop['size_sqm']} sqm")
                st.markdown(f"**Bedrooms / غرف النوم:** {prop['bedrooms']}")
                st.markdown(f"**Bathrooms / الحمامات:** {prop['bathrooms']}")
                
                st.button("Contact Agent / تواصل مع الوكيل", type="primary")
                st.button("Save Property / حفظ العقار")
            
            # Environmental risk analysis tab
            st.subheader("Environmental Risk Analysis / تحليل المخاطر البيئية")
            fig = plot_environmental_risks(prop['area'])
            if fig:
                st.pyplot(fig)
                
                # Risk recommendations
                st.subheader("Risk Recommendations / توصيات المخاطر")
                area_risks = next((r for r in load_risk_data() if r["name"] == prop['area']), None)
                
                if area_risks:
                    for risk_type, value in [
                        ("Flood Risk / مخاطر الفيضانات", area_risks['flood_risk']),
                        ("Air Pollution / تلوث الهواء", area_risks['air_pollution']),
                        ("Heat Island / الجزيرة الحرارية", area_risks['heat_island']),
                        ("Water Quality / جودة المياه", area_risks['water_quality'])
                    ]:
                        level, css_class = get_risk_level(value)
                        st.markdown(f"**{risk_type}:** <span class='{css_class}'>{level} ({value}%)</span>", unsafe_allow_html=True)
                        
                        # Simple recommendations based on risk level
                        if level == "Low":
                            st.markdown("✅ No special measures needed / لا حاجة لإجراءات خاصة")
                        elif level == "Medium":
                            st.markdown("⚠️ Consider basic precautions / النظر في اتخاذ احتياطات أساسية")
                        else:  # High
                            st.markdown("🚨 Special measures recommended / يوصى باتخاذ تدابير خاصة")
            
            # Neighborhood quality
            st.subheader("Neighborhood Quality / جودة الحي")
            fig = plot_neighborhood_quality(prop['area'])
            if fig:
                st.pyplot(fig)
                
                # Neighborhood metrics
                neighborhood = next((n for n in load_neighborhoods() if n["name"] == prop['area']), None)
                
                if neighborhood:
                    st.write("Detailed Ratings / تقييمات مفصلة:")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric("Safety / الأمان", f"{neighborhood['safety']}%")
                        st.metric("Schools / المدارس", f"{neighborhood['schools']}%")
                        st.metric("Healthcare / الرعاية الصحية", f"{neighborhood['healthcare']}%")
                    
                    with col2:
                        st.metric("Shopping / التسوق", f"{neighborhood['shopping']}%")
                        st.metric("Transportation / المواصلات", f"{neighborhood['transportation']}%")
                        overall = sum([neighborhood['safety'], neighborhood['schools'], 
                                      neighborhood['healthcare'], neighborhood['shopping'], 
                                      neighborhood['transportation']]) / 5
                        st.metric("Overall / التقييم العام", f"{overall:.1f}%")
        else:
            st.error("Property not found / لم يتم العثور على العقار")
            del st.session_state.selected_property
    else:
        # Show search results
        for prop in filtered_properties:
            col1, col2 = st.columns([1, 3])
            
            with col1:
                st.markdown("""
                            <div style="background-color:#f0f0f0; height:200px; border-radius:10px; display:flex; 
                            justify-content:center; align-items:center; margin-bottom:10px;">
                            <p style="color:#505050;">Property Image</p>
                            </div>
                            """, unsafe_allow_html=True)
            
            with col2:
                st.subheader(prop['title'])
                st.write(f"**Price / السعر:** {prop['price']:,} SAR")
                st.write(f"**Area / المنطقة:** {prop['area']}")
                st.write(f"**{prop['bedrooms']} bedrooms / غرف النوم | {prop['bathrooms']} bathrooms / حمامات | {prop['size_sqm']} sqm / متر مربع**")
                if st.button("View Details / عرض التفاصيل", key=f"search_view_{prop['id']}"):
                    st.session_state.selected_property = prop['id']
                    st.rerun()
            
            st.markdown("---")

# Environmental analysis page
def show_environmental_analysis():
    st.subheader("Environmental Risk Analysis / تحليل المخاطر البيئية")
    
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
            color=alt.Color('Risk:Q', scale=alt.Scale(scheme='redYellowGreen', reverse=True, domain=[0, 100])),
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
                recommendations = get_ai_response(risk_prompt)
                st.write(recommendations)

# Neighborhood comparison page
def show_neighborhood_comparison():
    st.subheader("Neighborhood Comparison / مقارنة الأحياء")
    
    # Select neighborhoods to compare
    neighborhoods_to_compare = st.multiselect(
        "Select Neighborhoods to Compare / اختر الأحياء للمقارنة",
        options=[n["name"] for n in load_neighborhoods()],
        default=[n["name"] for n in load_neighborhoods()][:2]
    )
    
    if not neighborhoods_to_compare:
        st.warning("Please select at least one neighborhood to analyze / يرجى اختيار حي واحد على الأقل للتحليل")
        return
    
    # Compare neighborhoods
    if len(neighborhoods_to_compare) == 1:
        # Single neighborhood analysis
        area = neighborhoods_to_compare[0]
        
        # Neighborhood quality
        st.subheader(f"Neighborhood Quality: {area} / جودة الحي: {area}")
        fig = plot_neighborhood_quality(area)
        if fig:
            st.pyplot(fig)
        
        # Neighborhood metrics
        neighborhood = next((n for n in load_neighborhoods() if n["name"] == area), None)
        
        if neighborhood:
            st.write("Detailed Ratings / تقييمات مفصلة:")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Safety / الأمان", f"{neighborhood['safety']}%")
                st.metric("Schools / المدارس", f"{neighborhood['schools']}%")
            
            with col2:
                st.metric("Healthcare / الرعاية الصحية", f"{neighborhood['healthcare']}%")
                st.metric("Shopping / التسوق", f"{neighborhood['shopping']}%")
            
            with col3:
                st.metric("Transportation / المواصلات", f"{neighborhood['transportation']}%")
                overall = sum([neighborhood['safety'], neighborhood['schools'], 
                              neighborhood['healthcare'], neighborhood['shopping'], 
                              neighborhood['transportation']]) / 5
                st.metric("Overall / التقييم العام", f"{overall:.1f}%")
        
        # Environmental risks
        st.subheader(f"Environmental Risks: {area} / المخاطر البيئية: {area}")
        fig = plot_environmental_risks(area)
        if fig:
            st.pyplot(fig)
            
        # AI neighborhood insights
        st.subheader("AI Neighborhood Insights / نظرة متعمقة للحي")
        
        insight_prompt = f"Give a detailed analysis of the {area} neighborhood in Riyadh for a potential property buyer or renter. Include information about the lifestyle, typical residents, nearby attractions, and investment potential. The neighborhood has safety rating of {neighborhood['safety']}%, schools rating of {neighborhood['schools']}%, healthcare rating of {neighborhood['healthcare']}%, shopping rating of {neighborhood['shopping']}%, and transportation rating of {neighborhood['transportation']}%. Be concise but specific."
        
        with st.spinner("Generating neighborhood insights..."):
            insights = get_ai_response(insight_prompt)
            st.write(insights)
    else:
        # Multiple neighborhood comparison
        st.subheader("Comparative Analysis / تحليل مقارن")
        
        # Create comparison data
        comparison_data = []
        
        for area in neighborhoods_to_compare:
            neighborhood = next((n for n in load_neighborhoods() if n["name"] == area), None)
            risks = next((r for r in load_risk_data() if r["name"] == area), None)
            
            if neighborhood and risks:
                # Calculate overall scores
                neighborhood_score = sum([
                    neighborhood['safety'],
                    neighborhood['schools'],
                    neighborhood['healthcare'],
                    neighborhood['shopping'],
                    neighborhood['transportation']
                ]) / 5
                
                risk_score = sum([
                    risks['flood_risk'],
                    risks['air_pollution'],
                    risks['heat_island'],
                    risks['water_quality']
                ]) / 4
                
                # Clean risk score (lower is better)
                clean_risk_score = 100 - risk_score
                
                comparison_data.append({
                    "Area": area,
                    "Neighborhood Quality": neighborhood_score,
                    "Environmental Safety": clean_risk_score,
                    "Overall Score": (neighborhood_score + clean_risk_score) / 2
                })
        
        comparison_df = pd.DataFrame(comparison_data)
        
        # Sort by overall score
        comparison_df = comparison_df.sort_values("Overall Score", ascending=False)
        
        # Show top neighborhood
        top_neighborhood = comparison_df.iloc[0]['Area']
        top_score = comparison_df.iloc[0]['Overall Score']
        
        st.success(f"**Best Neighborhood: {top_neighborhood}** with an overall score of {top_score:.1f}%")
        
        # Display comparison table
        st.table(comparison_df.style.format({
            "Neighborhood Quality": "{:.1f}%",
            "Environmental Safety": "{:.1f}%",
            "Overall Score": "{:.1f}%"
        }))
        
        # Create a more detailed comparison
        st.subheader("Detailed Comparison / مقارنة مفصلة")
        
        # Choose what to compare
        comparison_metric = st.selectbox(
            "Select Metric to Compare / اختر المقياس للمقارنة",
            options=[
                "safety", "schools", "healthcare", "shopping", "transportation",
                "flood_risk", "air_pollution", "heat_island", "water_quality"
            ],
            format_func=lambda x: {
                "safety": "Safety / الأمان",
                "schools": "Schools / المدارس",
                "healthcare": "Healthcare / الرعاية الصحية",
                "shopping": "Shopping / التسوق",
                "transportation": "Transportation / المواصلات",
                "flood_risk": "Flood Risk / مخاطر الفيضانات",
                "air_pollution": "Air Pollution / تلوث الهواء",
                "heat_island": "Heat Island / الجزيرة الحرارية",
                "water_quality": "Water Quality / جودة المياه"
            }[x]
        )
        
        # Determine which dataset to use
        if comparison_metric in ["safety", "schools", "healthcare", "shopping", "transportation"]:
            # Neighborhood metrics
            detail_data = [{"Area": n["name"], "Value": n[comparison_metric]} 
                          for n in load_neighborhoods() 
                          if n["name"] in neighborhoods_to_compare]
            # Higher is better
            color_scheme = 'greens'
            reverse = True
        else:
            # Risk metrics
            detail_data = [{"Area": r["name"], "Value": r[comparison_metric]} 
                          for r in load_risk_data() 
                          if r["name"] in neighborhoods_to_compare]
            # Lower is better
            color_scheme = 'reds'
            reverse = True
        
        detail_df = pd.DataFrame(detail_data)
        
        # Create comparison chart
        if not detail_df.empty:
            # Sort by value
            sort_ascending = comparison_metric in ["flood_risk", "air_pollution", "heat_island", "water_quality"]
            detail_df = detail_df.sort_values("Value", ascending=sort_ascending)
            
            chart = alt.Chart(detail_df).mark_bar().encode(
                x=alt.X('Value:Q', title='Value'),
                y=alt.Y('Area:N', title='Area', sort='-x'),
                color=alt.Color('Value:Q', scale=alt.Scale(scheme=color_scheme, reverse=reverse, domain=[0, 100])),
                tooltip=['Area', 'Value']
            ).properties(
                width=600,
                height=300,
                title=f"Comparison of {comparison_metric.replace('_', ' ').title()}"
            )
            
            st.altair_chart(chart, use_container_width=True)
        else:
            st.warning("No data available for comparison / لا توجد بيانات متاحة للمقارنة")
            
        # AI comparison analysis
        if len(neighborhoods_to_compare) >= 2:
            st.subheader("AI Neighborhood Comparison / المقارنة الذكية بين الأحياء")
            
            comparison_prompt = f"Compare these neighborhoods in Riyadh as potential areas to buy or rent property: {', '.join(neighborhoods_to_compare)}. Consider lifestyle differences, investment potential, and suitability for different types of residents (families, singles, professionals, etc.). Based on the data: {comparison_df.to_string()}. Be concise but specific."
            
            with st.spinner("Generating comparison analysis..."):
                comparison_analysis = get_ai_response(comparison_prompt)
                st.write(comparison_analysis)

# Enhanced AI Chat page using OpenAI
def show_ai_chat():
    st.subheader("Chat with Suhail / الدردشة مع سهيل")
    
    # Initialize chat history
    if "chat_history" not in st.session_state:
        welcome_message = "مرحباً! أنا سهيل، مساعدك العقاري الذكي. كيف يمكنني مساعدتك اليوم؟\n\nHello! I'm Suhail, your smart real estate assistant. How can I help you today?"
        st.session_state.chat_history = [
            {"role": "assistant", "content": welcome_message}
        ]
    
    # Display chat history
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f"""<div class="chat-message chat-message-user">{message["content"]}</div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""<div class="chat-message chat-message-bot">{message["content"]}</div>""", unsafe_allow_html=True)
    
    # Chat input
    user_message = st.text_input("Type your message / اكتب رسالتك", key="chat_input")
    
    # Submit button
    if st.button("Send / إرسال"):
        if user_message:  # Only process if there's a message
            # Add user message to chat history
            st.session_state.chat_history.append({"role": "user", "content": user_message})
            
            # Get AI response
            with st.spinner("Thinking... / جاري التفكير..."):
                # Pass the full conversation history for context
                response = get_ai_response(user_message, st.session_state.chat_history[:-1])
                
                # Add AI response to chat history
                st.session_state.chat_history.append({"role": "assistant", "content": response})
            
            # Rerun to update UI
            st.rerun()
    
    # Example queries
    st.subheader("Example Questions / أسئلة نموذجية")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("What areas have the best schools? / ما هي المناطق ذات أفضل المدارس؟"):
            question = "What areas have the best schools in Riyadh for families with children?"
            st.session_state.chat_history.append({"role": "user", "content": question})
            with st.spinner("Thinking... / جاري التفكير..."):
                response = get_ai_response(question, st.session_state.chat_history[:-1])
                st.session_state.chat_history.append({"role": "assistant", "content": response})
            st.rerun()
        
        if st.button("Tell me about flood risks in Al Naseem / أخبرني عن مخاطر الفيضانات في النسيم"):
            question = "Tell me about flood risks in Al Naseem neighborhood and how they might affect property values"
            st.session_state.chat_history.append({"role": "user", "content": question})
            with st.spinner("Thinking... / جاري التفكير..."):
                response = get_ai_response(question, st.session_state.chat_history[:-1])
                st.session_state.chat_history.append({"role": "assistant", "content": response})
            st.rerun()
    
    with col2:
        if st.button("Properties for a family of 4 near good schools / عقارات لعائلة من 4 أفراد بالقرب من مدارس جيدة"):
            question = "What types of properties would you recommend for a family of 4 with children looking to be near good schools in Riyadh?"
            st.session_state.chat_history.append({"role": "user", "content": question})
            with st.spinner("Thinking... / جاري التفكير..."):
                response = get_ai_response(question, st.session_state.chat_history[:-1])
                st.session_state.chat_history.append({"role": "assistant", "content": response})
            st.rerun()
        
        if st.button("Which area has the best air quality? / أي منطقة تتمتع بأفضل جودة هواء؟"):
            question = "Which neighborhoods in Riyadh have the best air quality? Why is this important for health and property value?"
            st.session_state.chat_history.append({"role": "user", "content": question})
            with st.spinner("Thinking... / جاري التفكير..."):
                response = get_ai_response(question, st.session_state.chat_history[:-1])
                st.session_state.chat_history.append({"role": "assistant", "content": response})
            st.rerun()

# Run the app
if __name__ == "__main__":
    main()
