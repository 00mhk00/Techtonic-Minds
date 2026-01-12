"""
Airline Data Warehouse - Streamlit Web Application
Interactive dashboard for analyzing airline data and creating customer segments
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import re

# Page configuration
st.set_page_config(
    page_title="Airline Data Warehouse",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Data loading functions
@st.cache_data
def load_data():
    """Load all CSV files"""
    data_dir = Path('data')
    data = {}
    
    files = [
        'dim_date', 'dim_time', 'dim_airport', 'dim_aircraft', 
        'dim_airline', 'dim_customer', 'dim_route',
        'fact_flight', 'fact_booking', 'fact_passenger_journey'
    ]
    
    for file in files:
        csv_path = data_dir / f'{file}.csv'
        if csv_path.exists():
            data[file] = pd.read_csv(csv_path)
    
    return data

def parse_segment_prompt(prompt, customers_df, bookings_df):
    """Parse natural language prompt to create customer segment"""
    prompt_lower = prompt.lower()
    filtered_customers = customers_df.copy()
    
    conditions = []
    
    # Loyalty tier
    loyalty_tiers = ['diamond', 'platinum', 'gold', 'silver', 'none']
    for tier in loyalty_tiers:
        if tier in prompt_lower:
            filtered_customers = filtered_customers[
                filtered_customers['loyalty_tier'].str.lower() == tier
            ]
            conditions.append(f"Loyalty tier: {tier.capitalize()}")
            break
    
    # Country
    if 'from' in prompt_lower or 'in' in prompt_lower or 'country' in prompt_lower:
        words = prompt.split()
        countries = filtered_customers['country'].unique()
        for country in countries:
            if country.lower() in prompt_lower:
                filtered_customers = filtered_customers[
                    filtered_customers['country'].str.lower() == country.lower()
                ]
                conditions.append(f"Country: {country}")
                break
    
    # Total flights (high-value, frequent, etc.)
    if 'frequent' in prompt_lower or 'high' in prompt_lower or 'many' in prompt_lower:
        threshold = filtered_customers['total_flights'].quantile(0.75)
        filtered_customers = filtered_customers[
            filtered_customers['total_flights'] >= threshold
        ]
        conditions.append(f"Frequent flyers (≥{int(threshold)} flights)")
    
    if 'inactive' in prompt_lower or 'churned' in prompt_lower:
        filtered_customers = filtered_customers[
            filtered_customers['is_active'] == False
        ]
        conditions.append("Status: Inactive")
    
    if 'active' in prompt_lower and 'inactive' not in prompt_lower:
        filtered_customers = filtered_customers[
            filtered_customers['is_active'] == True
        ]
        conditions.append("Status: Active")
    
    # Cabin class preference
    cabin_classes = ['economy', 'business', 'first', 'premium']
    for cabin in cabin_classes:
        if cabin in prompt_lower:
            filtered_customers = filtered_customers[
                filtered_customers['preferred_class'].str.lower().str.contains(cabin)
            ]
            conditions.append(f"Preferred class: {cabin.capitalize()}")
            break
    
    # Age-based (if date of birth available)
    if 'young' in prompt_lower or 'millennial' in prompt_lower:
        filtered_customers['age'] = 2026 - pd.to_datetime(
            filtered_customers['date_of_birth']
        ).dt.year
        filtered_customers = filtered_customers[
            (filtered_customers['age'] >= 25) & (filtered_customers['age'] <= 40)
        ]
        conditions.append("Age: 25-40")
    
    if 'senior' in prompt_lower:
        filtered_customers['age'] = 2026 - pd.to_datetime(
            filtered_customers['date_of_birth']
        ).dt.year
        filtered_customers = filtered_customers[filtered_customers['age'] >= 65]
        conditions.append("Age: 65+")
    
    # Booking behavior
    if bookings_df is not None and 'spend' in prompt_lower:
        customer_spend = bookings_df[
            bookings_df['booking_status'] == 'Completed'
        ].groupby('customer_id')['total_amount'].sum()
        
        high_spenders = customer_spend[
            customer_spend >= customer_spend.quantile(0.75)
        ].index
        
        filtered_customers = filtered_customers[
            filtered_customers['customer_id'].isin(high_spenders)
        ]
        conditions.append("High spenders (top 25%)")
    
    if not conditions:
        conditions.append("All customers (no filters applied)")
    
    return filtered_customers, conditions

# Main application
def main():
    # Header
    st.markdown('<h1 class="main-header">✈️ Airline Data Warehouse</h1>', 
                unsafe_allow_html=True)
    
    # Load data
    try:
        data = load_data()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.info("Please run `python scripts/generate_data.py` first to generate data.")
        return
    
    # Sidebar navigation
    st.sidebar.title("🧭 Navigation")
    page = st.sidebar.radio(
        "Select Page",
        ["📊 Dashboard", "🔍 Customer Segmentation", "✈️ Flight Analysis", 
         "💰 Revenue Analysis", "📈 Data Explorer"]
    )
    
    # PAGE 1: Dashboard
    if page == "📊 Dashboard":
        st.header("Executive Dashboard")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        if 'fact_flight' in data:
            flights = data['fact_flight']
            with col1:
                st.metric("Total Flights", f"{len(flights):,}")
            with col2:
                on_time_pct = (flights['flight_status'] == 'On-Time').mean() * 100
                st.metric("On-Time %", f"{on_time_pct:.1f}%")
            with col3:
                avg_load = flights['load_factor'].mean()
                st.metric("Avg Load Factor", f"{avg_load:.1f}%")
            with col4:
                cancelled = (flights['is_cancelled'] == True).sum()
                st.metric("Cancellations", f"{cancelled:,}")
        
        col1, col2, col3, col4 = st.columns(4)
        
        if 'fact_booking' in data:
            bookings = data['fact_booking']
            completed = bookings[bookings['booking_status'] == 'Completed']
            with col1:
                st.metric("Total Bookings", f"{len(bookings):,}")
            with col2:
                revenue = completed['total_amount'].sum()
                st.metric("Total Revenue", f"${revenue:,.0f}")
            with col3:
                avg_fare = completed['total_amount'].mean()
                st.metric("Avg Booking Value", f"${avg_fare:.2f}")
            with col4:
                customers = bookings['customer_id'].nunique()
                st.metric("Unique Customers", f"{customers:,}")
        
        # Visualizations
        st.subheader("📊 Key Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if 'fact_flight' in data:
                st.write("**Flight Status Distribution**")
                status_counts = flights['flight_status'].value_counts()
                fig = px.pie(
                    values=status_counts.values,
                    names=status_counts.index,
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            if 'dim_customer' in data:
                st.write("**Customer Loyalty Distribution**")
                loyalty_counts = data['dim_customer']['loyalty_tier'].value_counts()
                fig = px.bar(
                    x=loyalty_counts.index,
                    y=loyalty_counts.values,
                    labels={'x': 'Loyalty Tier', 'y': 'Number of Customers'},
                    color=loyalty_counts.values,
                    color_continuous_scale='Blues'
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Top routes
        if 'fact_flight' in data and 'dim_route' in data:
            st.subheader("🌍 Top Routes by Passengers")
            flights_with_route = flights.merge(
                data['dim_route'][['route_id', 'route_code']],
                on='route_id'
            )
            top_routes = flights_with_route.groupby('route_code')['total_passengers'].sum()
            top_routes = top_routes.nlargest(10).sort_values()
            
            fig = px.bar(
                x=top_routes.values,
                y=top_routes.index,
                orientation='h',
                labels={'x': 'Total Passengers', 'y': 'Route'},
                color=top_routes.values,
                color_continuous_scale='Viridis'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # PAGE 2: Customer Segmentation
    elif page == "🔍 Customer Segmentation":
        st.header("Customer Segmentation with Natural Language")
        
        st.write("""
        **Create custom customer segments using natural language!**
        
        Try prompts like:
        - "Show me all diamond loyalty customers"
        - "Find frequent flyers from USA"
        - "Show inactive customers who prefer business class"
        - "Find young customers who are high spenders"
        """)
        
        # Input prompt
        prompt = st.text_input(
            "📝 Enter your segmentation criteria:",
            placeholder="e.g., Show me platinum customers from USA who fly frequently"
        )
        
        if prompt and 'dim_customer' in data:
            with st.spinner("Creating segment..."):
                bookings_df = data.get('fact_booking')
                segment, conditions = parse_segment_prompt(
                    prompt, 
                    data['dim_customer'],
                    bookings_df
                )
                
                st.success(f"✅ Segment created! Found {len(segment)} customers")
                
                # Show conditions
                st.write("**Applied Filters:**")
                for condition in conditions:
                    st.write(f"- {condition}")
                
                # Segment metrics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Customers", len(segment))
                with col2:
                    avg_flights = segment['total_flights'].mean()
                    st.metric("Avg Flights", f"{avg_flights:.1f}")
                with col3:
                    avg_points = segment['loyalty_points'].mean()
                    st.metric("Avg Loyalty Points", f"{avg_points:,.0f}")
                with col4:
                    active_pct = (segment['is_active'] == True).mean() * 100
                    st.metric("Active %", f"{active_pct:.1f}%")
                
                # Segment details
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Loyalty Tier Distribution**")
                    tier_dist = segment['loyalty_tier'].value_counts()
                    fig = px.pie(values=tier_dist.values, names=tier_dist.index)
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    st.write("**Top Countries**")
                    country_dist = segment['country'].value_counts().head(10)
                    fig = px.bar(x=country_dist.values, y=country_dist.index, orientation='h')
                    st.plotly_chart(fig, use_container_width=True)
                
                # Show sample data
                st.subheader("📋 Segment Preview")
                display_cols = [
                    'customer_code', 'first_name', 'last_name', 'email',
                    'country', 'loyalty_tier', 'total_flights', 'loyalty_points', 'is_active'
                ]
                st.dataframe(segment[display_cols].head(50), use_container_width=True)
                
                # Export option
                csv = segment.to_csv(index=False)
                st.download_button(
                    label="📥 Download Segment as CSV",
                    data=csv,
                    file_name=f"customer_segment_{len(segment)}_customers.csv",
                    mime="text/csv"
                )
    
    # PAGE 3: Flight Analysis
    elif page == "✈️ Flight Analysis":
        st.header("Flight Performance Analysis")
        
        if 'fact_flight' not in data:
            st.error("Flight data not available")
            return
        
        flights = data['fact_flight']
        
        # Filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            airlines = data.get('dim_airline')
            if airlines is not None:
                airline_options = ['All'] + sorted(airlines['airline_name'].unique().tolist())
                selected_airline = st.selectbox("Select Airline", airline_options)
        
        with col2:
            status_options = ['All'] + sorted(flights['flight_status'].unique().tolist())
            selected_status = st.selectbox("Flight Status", status_options)
        
        with col3:
            cancelled_only = st.checkbox("Show cancelled flights only")
        
        # Filter data
        filtered_flights = flights.copy()
        
        if selected_airline != 'All' and airlines is not None:
            airline_id = airlines[airlines['airline_name'] == selected_airline]['airline_id'].iloc[0]
            filtered_flights = filtered_flights[filtered_flights['airline_id'] == airline_id]
        
        if selected_status != 'All':
            filtered_flights = filtered_flights[filtered_flights['flight_status'] == selected_status]
        
        if cancelled_only:
            filtered_flights = filtered_flights[filtered_flights['is_cancelled'] == True]
        
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Flights", len(filtered_flights))
        with col2:
            avg_delay = filtered_flights['arrival_delay_minutes'].mean()
            st.metric("Avg Delay (min)", f"{avg_delay:.1f}")
        with col3:
            avg_load = filtered_flights['load_factor'].mean()
            st.metric("Avg Load Factor", f"{avg_load:.1f}%")
        with col4:
            avg_revenue = filtered_flights['total_revenue'].mean()
            st.metric("Avg Revenue", f"${avg_revenue:,.0f}")
        
        # Visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Load Factor Distribution**")
            fig = px.histogram(
                filtered_flights,
                x='load_factor',
                nbins=30,
                labels={'load_factor': 'Load Factor (%)'},
                color_discrete_sequence=['#1f77b4']
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.write("**Delay Distribution**")
            non_cancelled = filtered_flights[filtered_flights['is_cancelled'] == False]
            fig = px.histogram(
                non_cancelled,
                x='arrival_delay_minutes',
                nbins=40,
                labels={'arrival_delay_minutes': 'Arrival Delay (minutes)'},
                color_discrete_sequence=['#ff7f0e']
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Detailed table
        st.subheader("📋 Flight Details")
        display_cols = [
            'flight_id', 'flight_number', 'flight_status', 'total_passengers',
            'load_factor', 'departure_delay_minutes', 'arrival_delay_minutes',
            'total_revenue'
        ]
        st.dataframe(filtered_flights[display_cols].head(100), use_container_width=True)
    
    # PAGE 4: Revenue Analysis
    elif page == "💰 Revenue Analysis":
        st.header("Revenue & Booking Analysis")
        
        if 'fact_booking' not in data:
            st.error("Booking data not available")
            return
        
        bookings = data['fact_booking']
        completed = bookings[bookings['booking_status'] == 'Completed']
        
        # Revenue metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_revenue = completed['total_amount'].sum()
            st.metric("Total Revenue", f"${total_revenue:,.0f}")
        with col2:
            avg_booking = completed['total_amount'].mean()
            st.metric("Avg Booking Value", f"${avg_booking:.2f}")
        with col3:
            conversion_rate = (len(completed) / len(bookings)) * 100
            st.metric("Conversion Rate", f"{conversion_rate:.1f}%")
        with col4:
            avg_advance = completed['days_before_departure'].mean()
            st.metric("Avg Booking Window", f"{avg_advance:.0f} days")
        
        # Visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Revenue by Cabin Class**")
            class_revenue = completed.groupby('cabin_class')['total_amount'].sum().sort_values(ascending=False)
            fig = px.bar(
                x=class_revenue.index,
                y=class_revenue.values,
                labels={'x': 'Cabin Class', 'y': 'Revenue ($)'},
                color=class_revenue.values,
                color_continuous_scale='Greens'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.write("**Revenue by Booking Channel**")
            channel_revenue = completed.groupby('booking_channel')['total_amount'].sum().sort_values(ascending=False)
            fig = px.bar(
                x=channel_revenue.index,
                y=channel_revenue.values,
                labels={'x': 'Booking Channel', 'y': 'Revenue ($)'},
                color=channel_revenue.values,
                color_continuous_scale='Blues'
            )
            fig.update_xaxis(tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
        
        # Booking window analysis
        st.subheader("📅 Booking Window Analysis")
        completed['booking_window_category'] = pd.cut(
            completed['days_before_departure'],
            bins=[0, 7, 14, 30, 60, 365],
            labels=['0-7 days', '7-14 days', '14-30 days', '30-60 days', '60+ days']
        )
        
        window_analysis = completed.groupby('booking_window_category').agg({
            'booking_id': 'count',
            'total_amount': ['mean', 'sum']
        }).reset_index()
        window_analysis.columns = ['Window', 'Bookings', 'Avg Fare', 'Total Revenue']
        
        st.dataframe(window_analysis, use_container_width=True)
        
        fig = px.scatter(
            completed,
            x='days_before_departure',
            y='total_amount',
            color='cabin_class',
            opacity=0.5,
            labels={'days_before_departure': 'Days Before Departure', 'total_amount': 'Fare ($)'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # PAGE 5: Data Explorer
    else:
        st.header("Data Explorer")
        
        st.write("Explore the raw data tables")
        
        table_names = {
            'Flights': 'fact_flight',
            'Bookings': 'fact_booking',
            'Passenger Journeys': 'fact_passenger_journey',
            'Customers': 'dim_customer',
            'Airlines': 'dim_airline',
            'Airports': 'dim_airport',
            'Aircraft': 'dim_aircraft',
            'Routes': 'dim_route',
            'Dates': 'dim_date',
            'Times': 'dim_time'
        }
        
        selected_table = st.selectbox("Select Table", list(table_names.keys()))
        
        table_key = table_names[selected_table]
        if table_key in data:
            df = data[table_key]
            
            st.write(f"**{selected_table}** - {len(df):,} rows")
            
            # Show sample
            num_rows = st.slider("Number of rows to display", 10, 100, 50)
            st.dataframe(df.head(num_rows), use_container_width=True)
            
            # Download button
            csv = df.to_csv(index=False)
            st.download_button(
                label=f"📥 Download {selected_table}",
                data=csv,
                file_name=f"{table_key}.csv",
                mime="text/csv"
            )
        else:
            st.error(f"Table {selected_table} not found")

if __name__ == '__main__':
    main()
