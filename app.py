import pandas as pd, altair as alt, streamlit as st

@st.cache_data(ttl=3600)
def load_data():
    anpp = pd.read_csv(
        "https://pasta.lternet.edu/package/data/eml/knb-lter-nwk/1/1/annual_net_primary_production.csv"
    )
    ppt = pd.read_csv(
        "https://pasta.lternet.edu/package/data/eml/knb-lter-nwk/1/1/annual_precipitation.csv"
    )
    return anpp.merge(ppt, on=["site","year"])

df = load_data()
st.title("ANPP ↔ Precipitation Explorer")
site = st.selectbox("Choose a site", sorted(df.site.unique()))
sub = df[df.site == site]

st.altair_chart(
    alt.Chart(sub).mark_line(point=True)
     .encode(x="year:O", y="anpp_g_m2:Q")
     .properties(height=300),
    use_container_width=True
)

st.line_chart(sub.set_index("year")["precip_mm"])
