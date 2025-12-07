import streamlit as st
import pandas as pd
from kafka import KafkaConsumer
import json
import time

# Page Configuration
st.set_page_config(page_title="Kafka Fraud Detector", page_icon="🛡️", layout="wide")

st.title("🛡️ Real-Time Fraud Detection Dashboard")
st.markdown("Monitoring real-time transaction data flowing through **Apache Kafka**...")

# Layout: Metrics on top
kpi1, kpi2, kpi3 = st.columns(3)
col1, col2 = st.columns([2, 1])

# Placeholders for dynamic updates
with kpi1:
    metric_count = st.empty()
with kpi2:
    metric_fraud = st.empty()
with kpi3:
    metric_amount = st.empty()

with col1:
    st.subheader("Live Transaction Amounts")
    chart_placeholder = st.empty()

with col2:
    st.subheader("🚨 Detected Anomalies")
    alert_placeholder = st.empty()

# Initialize Kafka Consumer
try:
    consumer = KafkaConsumer(
        'transactions',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='latest',
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        consumer_timeout_ms=1000  # Stop iteration if no message after 1 sec to prevent blocking
    )
except Exception as e:
    st.error("Failed to connect to Kafka. Ensure Docker containers are running.")
    st.stop()

data_buffer = []
fraud_count = 0

# Main Loop
while True:
    msg_pack = consumer.poll(timeout_ms=500)
    
    for tp, messages in msg_pack.items():
        for message in messages:
            tx = message.value
            data_buffer.append(tx)
            
            # Keep only the last 100 records for chart stability
            if len(data_buffer) > 100:
                data_buffer.pop(0)
    
    if data_buffer:
        df = pd.DataFrame(data_buffer)
        
        # Metric Calculations
        total_tx = len(df) # Total transactions in buffer
        current_fraud = df[df['is_fraud'] == True]
        detected_fraud_count = len(current_fraud)
        avg_amt = df['amount'].mean()

        # Update KPIs
        metric_count.metric(label="Buffered Transactions", value=total_tx)
        metric_fraud.metric(label="Fraud Alerts (in Buffer)", value=detected_fraud_count, delta_color="inverse")
        metric_amount.metric(label="Average Transaction Amount", value=f"${avg_amt:.2f}")

        # Update Chart
        chart_placeholder.line_chart(df[['amount']])

        # Update Alert Panel
        if not current_fraud.empty:
            last_fraud = current_fraud.iloc[-1]
            alert_placeholder.error(
                f"⚠️ FRAUD DETECTED!\n\n"
                f"**Time:** {last_fraud['timestamp']}\n"
                f"**Amount:** ${last_fraud['amount']}\n"
                f"**Location:** {last_fraud['city']}"
            )
        else:
            alert_placeholder.success("✅ System Status: Secure")
            
    time.sleep(0.1) # UI Refresh rate