
import streamlit as st


def intro():
    import streamlit as st

    st.write("Welcome to the wardrobe manager" )
    st.sidebar.success("Select an operation above.")

def create_piece():
    st.write("Create a new Article of Clothing")
    with st.form("NewArticleForm"):
        name = st.text_input("ArticleName")
        atype = st.selectbox("Type of Article", ('Top', 'Bottom', 'Dress', 'Shoes', 'Accessory', 'Other'))
        photo = st.file_uploader("ArticleImage", accept_multiple_files=False)
        submit = st.form_submit_button("Submit")
        if submit:
            print("Add clothing to database here")



def manage_outfits():
    import streamlit as st

    st.markdown(f'# {list(page_names_to_funcs.keys())[2]}')

page_names_to_funcs = {
    "Home": intro,
    "Add Clothing": create_piece,
}

page_name = st.sidebar.selectbox("Choose an operation", page_names_to_funcs.keys())
page_names_to_funcs[page_name]()
