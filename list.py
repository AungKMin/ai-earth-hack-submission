#---PIP PACKAGES---#
import streamlit as st
from streamlit_option_menu import option_menu
from isoweek import Week

#---BUILT-IN PYTHON MODULES
from datetime import datetime, date
import calendar
from pprint import pprint
import uuid

#---IMPORT PYTHON FILE IN SAME DIR---#
import db as db

# ---STREAMLIT SETTINGS---#
page_title = "Your sustainable shopping list"
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
    options = ["Sustainable shopping list", "Other"],
    icons = ["list-task", "cup-straw" ],
    orientation = "horizontal"
) 

#---INPUT FORM---#
if nav_menu == "Sustainable shopping list":
    if "item_list" not in st.session_state:
        st.session_state["item_list"] = []
    if "item_key" not in st.session_state:
        st.session_state["item_key"] = 0

    item_enter = st.text_input("Enter your item", " ")

    if st.button("Add Item"):
        if item_enter: 
            st.session_state["item_list"].append(item_enter)
            st.session_state["item_key"] += 1

    for i, t in enumerate(st.session_state["item_list"]):
        st.checkbox(f"{i + 1}\. {t}")
        if st.button("delete", key=i):
            del st.session_state["item_list"][i]
            st.rerun()

    