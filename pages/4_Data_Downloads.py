import io
import pandas as pd
import streamlit as st

st.title("⬇️ Data Downloads")

st.write("Select your preferred data format. Downloads are generated on the fly.")

# Sample dataset for download
sample_df = pd.DataFrame({
    "id": range(1, 11),
    "lat": [10.1, 11.2, 9.9, -2.3, 5.6, -12.2, 21.3, 2.9, -0.2, 14.4],
    "lon": [120.2, -45.1, 33.8, 140.3, -80.3, 12.5, -160.0, 88.2, -9.1, 60.7],
    "temp": [18.2, 17.9, 19.1, 16.5, 20.0, 14.8, 22.1, 19.5, 18.0, 21.2],
})

col1, col2, col3 = st.columns(3)

with col1:
    with st.container():
        st.markdown("<div class='ocean-card fade-in download-option'><div><div class='format'>CSV</div><div class='desc'>Comma-separated, easy for spreadsheets</div></div></div>", unsafe_allow_html=True)
        csv_buf = io.StringIO()
        sample_df.to_csv(csv_buf, index=False)
        with st.container():
            st.download_button("Download CSV", csv_buf.getvalue(), file_name="floats.csv", mime="text/csv", type="primary")

with col2:
    with st.container():
        st.markdown("<div class='ocean-card fade-in download-option'><div><div class='format'>NetCDF</div><div class='desc'>Binary scientific format for arrays</div></div></div>", unsafe_allow_html=True)
        # Placeholder NetCDF bytes
        nc_bytes = b"NetCDF placeholder content"
        with st.container():
            st.download_button("Download NetCDF", nc_bytes, file_name="floats.nc", mime="application/octet-stream", type="primary")

with col3:
    with st.container():
        st.markdown("<div class='ocean-card fade-in download-option'><div><div class='format'>ASCII</div><div class='desc'>Plain text for quick inspection</div></div></div>", unsafe_allow_html=True)
        ascii_buf = io.StringIO()
        ascii_buf.write(sample_df.to_string(index=False))
        with st.container():
            st.download_button("Download ASCII", ascii_buf.getvalue(), file_name="floats.txt", mime="text/plain", type="primary")

st.caption("Buttons include a neon glow hover animation via the global stylesheet.") 