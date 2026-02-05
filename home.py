import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
from query import *
import time

st.set_page_config(page_title="Dashoboard", page_icon="📊", layout="wide")

# Aplicando modificações na insterface da aplicação
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

st.subheader("🔔 Insurance Descriptive Analytics")
st.markdown("##")

result = view_all_data()
df = pd.DataFrame(result, columns=["id","Location","State","Region","Investment","Construction","BusinessType","Earthquake","Flood","Rating"])
# st.dataframe(df)

st.sidebar.image("./resourses/logo-genesis.png", caption="Online Analytics")

st.sidebar.header("Please filter")
region = st.sidebar.multiselect("Select Region",
                                options=df["Region"].unique(),
                                default=df["Region"].unique())

location = st.sidebar.multiselect("Select Location",
                                options=df["Location"].unique(),
                                default=df["Location"].unique())

construction = st.sidebar.multiselect("Select Construction",
                                options=df["Construction"].unique(),
                                default=df["Construction"].unique())

df_selection = df.query("Region == @region & Location == @location & Construction == @construction")

# st.dataframe(df_selection)

def home():
    with st.expander("Tabular"):
        showData = st.multiselect("Filter: ", df_selection.columns, default=[])
        st.write(df_selection[showData])

    # Compute top analytics
    total_investment = float(df_selection["Investment"].sum())
    investment_mode = float(df_selection["Investment"].mode())
    investment_mean = float(df_selection["Investment"].mean())
    invstment_median = float(df_selection["Investment"].median())
    rating = float(df_selection["Investment"].median())
    
    total1, total2, total3, total4, total5 = st.columns(5, gap="medium")
    with total1:
        st.info("Total Investment", icon="📌")
        st.metric(label="sum USD", value=f"{total_investment:,.0f}")

    with total2:
        st.info("Most Frequent", icon="📌")
        st.metric(label="mode USD", value=f"{investment_mode:,.0f}")

    with total3:
        st.info("Average", icon="📌")
        st.metric(label="average USD", value=f"{investment_mean:,.0f}")

    with total4:
        st.info("Central Earnings", icon="📌")
        st.metric(label="median USD", value=f"{invstment_median:,.0f}")

    with total5:
        st.info("Ratings", icon="📌")
        st.metric(label="Rating", value=numerize(rating), help=f""" Total Rating: {rating:,.0f} """)

    st.markdown("""---""")

# Gráficos
def graphs():
    total_investment = int(df_selection["Investment"].sum())
    average_rating = int(round(df_selection["Rating"].mean(),2))

    # Gráfico de barras simples
    investment_by_business_type = df_selection.groupby(by=["BusinessType"]).count()[["Investment"]].sort_values(by="Investment")

    fig_investment = px.bar(investment_by_business_type,
                            x="Investment",
                            y=investment_by_business_type.index,
                            orientation="h",
                            title="<b> Investment by Businesss Type </b>",
                            color_discrete_sequence=["#0083b8"]*len(investment_by_business_type),
                            template="plotly_white")
    
    fig_investment.update_layout(plot_bgcolor="rgba(0,0,0,0)",
                                 xaxis=dict(showgrid=False))

    # Gráfico de linhas simples
    investment_by_state = df_selection.groupby(by=["State"]).count()[["Investment"]]

    fig_state = px.line(investment_by_state,
                            x=investment_by_state.index,
                            y="Investment",
                            orientation="v",
                            title="<b> Investment by State </b>",
                            color_discrete_sequence=["#0083b8"]*len(investment_by_state),
                            template="plotly_white")
    
    fig_state.update_layout(plot_bgcolor="rgba(0,0,0,0)",
                            xaxis=dict(tickmode="linear"),
                            yaxis=dict(showgrid=False))
    
    left, right = st.columns(2)
    left.plotly_chart(fig_state, use_container_width=True)
    right.plotly_chart(fig_investment, use_container_width=True)

def progressBar():
    st.markdown("""<style>.stProgress > div > div > div > div> {background: linear-gradien(to right, #99ff99, #FFFF00)}</style>""", unsafe_allow_html=True)
    target = 3000000000
    current = df_selection["Investment"].sum()
    percent = round((current/target)*100)
    myBar = st.progress(0)

    if percent > 100:
        st.subheader("Target done!!")
    
    else:
        st.write("you have ", percent, r"% of", format(target, "d"), "USD")

        for percent_complete in range(percent):
            time.sleep(0.1)
            myBar.progress(percent_complete+1, text=" Target Percentage")

def sideBar():
    with st.sidebar:
        selected = option_menu(menu_title="Main menu",
                               options=["Home", "Progress"],
                               icons=["house", "eye"],
                               menu_icon="cast",
                               default_index=0)
        
    if selected == "Home":
        st.subheader(f"Page: {selected}")
        home()
        graphs()

    if selected == "Progress":
        st.subheader(f"Page: {selected}")
        progressBar()
        graphs()

sideBar()
