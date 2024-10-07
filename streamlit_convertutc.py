import streamlit as st
import pytz
from datetime import datetime, date, timedelta

def convert_time(time, from_tz, to_tz):
    from_zone = pytz.timezone(from_tz)
    to_zone = pytz.timezone(to_tz)
    
    # Combine date and time
    today = date.today()
    dt = datetime.combine(today, time)
    
    # Localize the datetime to the 'from' timezone
    dt_with_tz = from_zone.localize(dt)
    
    # Convert to the 'to' timezone
    converted_time = dt_with_tz.astimezone(to_zone)
    
    # Check if the date has changed
    next_day = converted_time.date() > today
    
    time_str = converted_time.strftime("%I:%M %p %Z")
    if next_day:
        time_str += " (next day)"
    
    return time_str

st.title("Time Zone Converter")

# Define the time zones
time_zones = {
    "UTC": "UTC",
    "PST": "US/Pacific",
    "CDT": "US/Central",
    "MST": "US/Mountain",
    "EST": "US/Eastern"
}

# Create two columns
col1, col2 = st.columns(2)

with col1:
    st.header("Convert from UTC")
    utc_time = st.time_input("Enter UTC time", datetime.now().time())
    
    if st.button("Convert from UTC"):
        for tz_name, tz_string in time_zones.items():
            if tz_name != "UTC":
                converted = convert_time(utc_time, "UTC", tz_string)
                st.write(f"{tz_name}: {converted}")

with col2:
    st.header("Convert to UTC")
    local_time = st.time_input("Enter local time", datetime.now().time())
    from_tz = st.selectbox("Select source time zone", list(time_zones.keys())[1:])
    
    if st.button("Convert to UTC"):
        converted = convert_time(local_time, time_zones[from_tz], "UTC")
        st.write(f"UTC: {converted}")

st.info("Note: This app uses today's date for conversions. It uses standard time zones and does not account for daylight saving time changes.")
