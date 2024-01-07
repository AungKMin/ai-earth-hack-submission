#---PIP PACKAGES---#
import streamlit as st
from streamlit_option_menu import option_menu

#---IMPORT PYTHON FILE IN SAME DIR---#
import db as db
import api as api
import pandas as pd

# ---STREAMLIT SETTINGS---#
page_title = "Welcome to AI Chef! Let's create something delicious and sustainable"
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

#---NAV BARS---#
nav_menu = option_menu(
    menu_title = None,
    options = ["Shopping list", "Instructions"],
    icons = ["bag-heart-fill", "list-task"],
    orientation = "horizontal"
) 

image = []

def update_shopping_list(item, checked):
    if checked and item not in st.session_state['selected_items']:
        st.session_state['selected_items'].append(item)
    elif not checked and item in st.session_state['selected_items']:
        st.session_state['selected_items'].remove(item)

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


if nav_menu == "Shopping list":
    col1, col2, col3 = st.columns([ 2, 2, 2])
    if 'selected_items' not in st.session_state:
        st.session_state['selected_items'] = []
    if st.checkbox("Show pictures"):
        for i, t in enumerate(st.session_state["item_list"]):
            columns = [col1, col2, col3]
            for index, col in enumerate(columns):
                if i % 3 == index:
                    with col:
                        st.write("\n\n")
                        url = st.session_state["images"][i]
                        st.image(f"{url}",width=150)
                        add_to_list = st.checkbox(f"{i + 1}. {t}")
                        update_shopping_list(t, add_to_list)
    else:
        for i, t in enumerate(st.session_state["item_list"]):
            add_to_list = st.checkbox(f"{i + 1}. {t}")
            update_shopping_list(t, add_to_list)


    if st.session_state["item_list"]:
        st.write("## My Cart 🛒")
        if not st.session_state['selected_items']:
            st.write("Empty Cart")
        else:
            selected_items = st.session_state.get('selected_items', [])

            df = pd.DataFrame({'Item': selected_items})
            df.index=df.index+1 
            st.table(df)
        button_clicked = st.button('Go Shopping')


if nav_menu == "Instructions":
    ordered_list_html = "<ul>" 
    for t in st.session_state["instructions"]:
        ordered_list_html += f"<li> {t}</li>"
    ordered_list_html += "</ul>"

    container_content = f"""
        <div style='margin-top: 20px; background-color: #282434; border-radius: 10px; padding: 20px;  '>
            <h3>Instructions: 📜</h3>
            {ordered_list_html}
        </div>
    """

    # Clear previous content before displaying new content
    st.empty()
    st.markdown(container_content, unsafe_allow_html=True)


