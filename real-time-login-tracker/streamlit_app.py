import streamlit as st
import pandas as pd
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client.userlogs
collection = db.logs

st.set_page_config(page_title="User Activity Dashboard", layout="wide")
st.title("📈 Real-Time User Login Dashboard")

data = list(collection.find({}, {'_id': 0}))
df = pd.DataFrame(data)

if not df.empty:
    st.dataframe(df.tail(50), use_container_width=True)
else:
    st.warning("No login events found.")
