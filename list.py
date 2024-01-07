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

image = []

#---INPUT FORM---#
if "item_list" not in st.session_state:
    st.session_state["item_list"] = []
if "instructions" not in st.session_state:
    st.session_state["instructions"] = []
if "images" not in st.session_state:
    st.session_state["images"] = []

item_enter = st.text_input("What do you want to cook?", " ")

if st.button("Generate recipe"):
    result = api.get_json(item_enter)
    st.session_state["item_list"] = result["ingredients"]
    st.session_state["instructions"] = result["instructions"]
    for item in st.session_state["item_list"]:
        st.session_state["images"].append(api.imageURL(item))


col1, col2, col3 = st.columns([ 1, 1, 1])
if nav_menu == "Shopping list":
    for i, t in enumerate(st.session_state["item_list"]):
        if i % 3 == 0:
            with col1:
                st.write("\n\n")
                url = st.session_state["images"][i]
                st.image(f"{url}",width =150)
                st.checkbox(f"{i + 1}. {t}")


        elif i % 3 == 1:
            with col2:
                st.write("\n\n")
                url = st.session_state["images"][i]
                st.image(f"{url}",width =150)
                st.checkbox(f"{i + 1}. {t}")

        else:
            with col3:
                st.write("\n\n")
                url = st.session_state["images"][i]
                st.image(f"{url}",width =150)
                st.checkbox(f"{i + 1}. {t}")

if nav_menu == "Instructions":
    ordered_list_html = "<ol>" 
    for t in st.session_state["instructions"]:
        ordered_list_html += f"<li> {t}</li>"
    ordered_list_html += "</ol>"

    container_content = f"""
        <div style='margin-top: 20px; background-color: #282434; border-radius: 10px; padding: 20px;  '>
            <h3>Instructions: 📜</h3>
            {ordered_list_html}
        </div>
    """

    # Clear previous content before displaying new content
    st.empty()
    st.markdown(container_content, unsafe_allow_html=True)

    