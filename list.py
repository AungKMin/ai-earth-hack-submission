#---PIP PACKAGES---#
import streamlit as st
from streamlit_option_menu import option_menu

#---IMPORT PYTHON FILE IN SAME DIR---#
import db as db
import api as api

# ---STREAMLIT SETTINGS---#
page_title = "Create something delicious and sustainable"
page_icon = ":evergreen_tree:"
layout  = "centered"

#---PAGE CONFIG---#
st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(f"{page_title} {page_icon}")

# #---STREAMLIT CONFIG HIDE---#
# hide_st_style = """<style>
#                 #MainMenu {visibility : hidden;}
#                 footer {visibility : hidden;}
#                 header {visibility : hidden;}
#                 </style>
#                 """
# st.markdown(hide_st_style, unsafe_allow_html=True)

#---FUNCTIONS---#


#---NAV BARS---#
nav_menu = option_menu(
    menu_title = None,
    options = ["Shopping list", "Instructions"],
    icons = ["list-task", "cup-straw"],
    orientation = "horizontal"
) 

#---INPUT FORM---#
if "item_list" not in st.session_state:
    st.session_state["item_list"] = []
if "instructions" not in st.session_state:
    st.session_state["instructions"] = []

item_enter = st.text_input("What do you want to cook?", " ")

if st.button("Generate recipe"):
    result = api.get_json(item_enter)
    st.session_state["item_list"] = result["ingredients"]
    st.session_state["instructions"] = result["instructions"]

if nav_menu == "Shopping list":
    for i, t in enumerate(st.session_state["item_list"]):
        st.checkbox(f"{i + 1}\. {t}")
        if st.button("delete", key=i):
            del st.session_state["item_list"][i]
            st.rerun()

if nav_menu == "Instructions":
    for i, t in enumerate(st.session_state["instructions"]):
        st.checkbox(f"{i + 1}\. {t}")
    

    