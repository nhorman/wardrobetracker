import binascii
import pandas as pd
import io
import streamlit as st
import mysql.connector
from PIL import Image

#Set up db connection
@st.experimental_singleton
def init_connection():
    print("INITALIZING DB CONNECTION")
    return mysql.connector.connect(**st.secrets["mysql"])

dbcon = init_connection()

def intro():
    import streamlit as st

    st.write("Welcome to the wardrobe manager" )
    st.sidebar.success("Select an operation above.")

def create_piece():
    st.markdown(f'# {list(page_names_to_funcs.keys())[1]}')
    with st.form("NewArticleForm", clear_on_submit=True):
        name = st.text_input("Article Name")
        atype = st.selectbox("Type of Article", ('Top', 'Bottom', 'Dress', 'Shoes', 'Accessory', 'Other'))
        cost = st.number_input("Cost Of Article", format="%f")
        photo = st.file_uploader("ArticleImage", accept_multiple_files=False)
        submit = st.form_submit_button("Submit")
        cursor = dbcon.cursor()
        query = ""
        if submit:
            if photo != None:
                hexvalue = binascii.b2a_base64(photo.getvalue(),newline=False).decode('utf-8')
                query = "INSERT INTO articles(Name, Type, Image, Cost, Retired) VALUES ('%s', '%s', '%s', %f, %d)" % (name, atype, hexvalue, cost, 0)
            else:
                query = "INSERT INTO articles(Name, Type, Cost, Retired) VALUES ('%s', '%s', %f, %d)" % (name, atype, cost, 0)
            cursor.execute(query)
            dbcon.commit()
            cursor.close()
            st.write("Article added")

def view_pieces():
    st.markdown(f'# {list(page_names_to_funcs.keys())[2]}')
    cursor = dbcon.cursor()
    query = "SELECT Name, Type, Image, Cost From articles where Retired = 0"
    cursor.execute(query)

    page = st.container()
    for (name, atype, imagestr, cost) in cursor:
        row = page.container()
        namec, typec, imagec = row.columns(3)
        namec.text(name)
        typec.text(atype)
        binvalue = binascii.a2b_base64(imagestr)
        try:
            imagec.image(Image.open(io.BytesIO(binvalue)))
        except e:
            imagec.image(Image.new(mode="RGBA", size(100,100), color=255)
    cursor.close()

   
page_names_to_funcs = {
    "Home": intro,
    "Add Clothing": create_piece,
    "View Clothing": view_pieces,
}

page_name = st.sidebar.selectbox("Choose an operation", page_names_to_funcs.keys())
page_names_to_funcs[page_name]()
