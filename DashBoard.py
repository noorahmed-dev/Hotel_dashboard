import streamlit as st
import pandas as pd
import plotly.express as px

# --------- Load Data ---------
@st.cache_data
def load_data():
    return pd.read_csv("hotels.csv")

df = load_data()

# --------- Sidebar ---------
st.set_page_config(layout="wide")
st.sidebar.title("Hotel Bookings Dashboard")
st.sidebar.image("informational-poster-on-building-written-260nw-1493986589.webp", width=120)
selected_hotel = st.sidebar.selectbox("Filter by Hotel Type:", df['hotel'].unique())

# --------- Filtered Data ---------
filtered_df = df[df['hotel'] == selected_hotel]

# --------- Top KPIs ---------
total_bookings = len(filtered_df)
avg_lead_time = round(filtered_df['lead_time'].mean(), 1)
cancel_rate = round((filtered_df['is_canceled'].sum() / total_bookings) * 100, 2)

st.title("🏨 Hotel Booking Dashboard")
st.markdown("## Key Metrics")
kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("Total Bookings", f"{total_bookings:,}")
kpi2.metric("Average Lead Time", f"{avg_lead_time} days")
kpi3.metric("Cancellation Rate", f"{cancel_rate}%")

# --------- Main Tabs ---------
tab1, tab2, tab3 = st.tabs(["📌 Booking", "💰 ADR", "❌ Cancellation"])

# --------- TAB 1: Booking ---------
with tab1:
    st.subheader("📌 Booking Insights")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("1️⃣ Bookings per Arrival Month (Line Chart)")
        month_counts = filtered_df['arrival_date_month'].value_counts().reset_index()
        month_counts.columns = ['Month', 'Bookings']
        month_order = ['January','February','March','April','May','June','July','August','September','October','November','December']
        month_counts['Month'] = pd.Categorical(month_counts['Month'], categories=month_order, ordered=True)
        fig1 = px.line(month_counts.sort_values('Month'), x='Month', y='Bookings', markers=True)
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.markdown("2️⃣ Bookings by Room Type (Bar Chart)")
        room_counts = filtered_df['reserved_room_type'].value_counts().reset_index()
        room_counts.columns = ['Room Type', 'Bookings']
        fig2 = px.bar(room_counts, x='Room Type', y='Bookings', color='Room Type')
        st.plotly_chart(fig2, use_container_width=True)

# --------- TAB 2: ADR ---------
with tab2:
    st.subheader("💰 ADR (Average Daily Rate) Insights")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("1️⃣ ADR vs Lead Time (Scatter Plot)")
        fig3 = px.scatter(filtered_df, x='lead_time', y='adr', color='reserved_room_type',
                          title="ADR vs Lead Time by Room Type")
        st.plotly_chart(fig3, use_container_width=True)

    with col2:
        st.markdown("2️⃣ ADR Distribution by Room Type (Box Plot)")
        fig4 = px.box(filtered_df, x='reserved_room_type', y='adr', color='reserved_room_type')
        st.plotly_chart(fig4, use_container_width=True)

# --------- TAB 3: Cancellation ---------
with tab3:
    st.subheader("❌ Cancellation Insights")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("1️⃣ Cancellation Rate by Deposit Type (Pie Chart)")
        cancel_deposit = filtered_df[filtered_df['is_canceled'] == 1]['deposit_type'].value_counts().reset_index()
        cancel_deposit.columns = ['Deposit Type', 'Count']
        fig5 = px.pie(cancel_deposit, names='Deposit Type', values='Count', hole=0.4)
        st.plotly_chart(fig5, use_container_width=True)

    with col2:
        st.markdown("2️⃣ Cancellations by Market Segment (Bar Chart)")
        cancel_market = filtered_df[filtered_df['is_canceled'] == 1]['market_segment'].value_counts().reset_index()
        cancel_market.columns = ['Market Segment', 'Cancellations']
        fig6 = px.bar(cancel_market, x='Market Segment', y='Cancellations', color='Market Segment')
        st.plotly_chart(fig6, use_container_width=True)