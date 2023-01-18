import binascii
import time
import pandas as pd
import io
import streamlit as st
import mysql.connector
from PIL import Image
from PIL import ImageOps

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

TypeTuple=('Active Top', 'Regular Long Sleeve Top', 'Regular Short Sleeve Top', 'Tank Top', 'Active Bottom', 'Regular Bottom', 'Active Sports Bra', 'Long Bottoms', 'Short Bottoms', 'Dress/Jumpsuit')
FilterTuple=('All', 'Active Top', 'Regular Long Sleeve Top', 'Regular Short Sleeve Top', 'Tank Top', 'Active Bottom', 'Regular Bottom', 'Active Sports Bra', 'Long Bottoms', 'Short Bottoms', 'Dress/Jumpsuit')
def create_piece():
    st.markdown(f'# {list(page_names_to_funcs.keys())[1]}')
    with st.form("NewArticleForm", clear_on_submit=True):
        name = st.text_input("Article Name")
        atype = st.selectbox("Type of Article", TypeTuple)
        cost = st.number_input("Cost Of Article", format="%f")
        photo = st.file_uploader("ArticleImage", accept_multiple_files=False)
        submit = st.form_submit_button("Submit")
        cursor = dbcon.cursor()
        query = ""
        if submit:
            if photo != None:
                tphoto = Image.open(io.BytesIO(photo.getvalue()))
                tphoto.thumbnail((200,200))
                tphoto = ImageOps.exif_transpose(tphoto)
                toutput = io.BytesIO()
                tphoto.save(toutput, format='JPEG')
                hexvalue = binascii.b2a_base64(toutput.getvalue(),newline=False).decode('utf-8')
                query = "INSERT INTO articles(Name, Type, Image, Cost, TimesWorn, Retired) VALUES ('%s', '%s', '%s', %f, %d, %d)" % (name, atype, hexvalue, cost, 1, 0)
            else:
                query = "INSERT INTO articles(Name, Type, Cost, TimesWorn, Retired) VALUES ('%s', '%s', %f, %d, %d)" % (name, atype, cost, 1, 0)
            cursor.execute(query)
            dbcon.commit()
            cursor.close()
            st.write("Article added")

def view_pieces():
    st.markdown(f'# {list(page_names_to_funcs.keys())[2]}')
    viewpage = None
    filterc = st.container()
    filterform = filterc.form("Filter Articles", clear_on_submit=True)
    filterselect = filterform.selectbox("Filter by Type", FilterTuple)
    submit = filterform.form_submit_button("Update Filter")

    viewc = st.container()
    if submit:
        if (viewpage != None):
            viewpage.empty()
        query = "SELECT Name, Type, Image, Cost, TimesWorn From articles where Retired = 0"
        if filterselect != 'All':
            query = query + " and Type = '" + str(filterselect) + "'"

        cursor = dbcon.cursor()
        cursor.execute(query)
        viewpage = st.container()
        row = viewpage.container()
        namec, typec, unitcostc, imagec = row.columns(4)
        namec.text("Article Name")
        typec.text("Article Type")
        unitcostc.text("Cost Per Wearing")
        imagec.text("Picture")
        for (name, atype, imagestr, cost, timesworn) in cursor:
            row = viewpage.container()
            namec, typec, unitcostc, imagec = row.columns(4)
            namec.text(name)
            typec.text(atype)
            costperwear = (float(cost)/int(timesworn))
            unitcostc.text(str(costperwear))
            binvalue = binascii.a2b_base64(imagestr)
            try:
                imagec.image(Image.open(io.BytesIO(binvalue)))
            except e:
                imagec.image(Image.new(mode="RGBA", size=(100,100), color=255))
        cursor.close()

def get_dressed():
    st.markdown(f'# {list(page_names_to_funcs.keys())[3]}')

    filterc = st.container()
    filterform = filterc.form("Filter Articles", clear_on_submit=True)
    filterselect = filterform.selectbox("Filter by Type", FilterTuple)
    submit = filterform.form_submit_button("Update Filter")
    query = "SELECT Name, Type, Image From articles where Retired = 0"
    try:
        if st.session_state['filterkey'] != 'All':
            query = query + " and Type = '" + str(st.session_state['filterkey']) + "'"
    except:
        st.session_state['filterkey'] = 'All'

    cursor = dbcon.cursor()
    cursor.execute(query)
    viewpage = st.container()
    viewform = viewpage.form("Select Clothes", clear_on_submit=True)
    wsubmit = viewform.form_submit_button("Wear Clothes")
    row = viewform.container()
    wearc, namec, typec, imagec = row.columns(4)
    wearc.text("Wear Me")
    namec.text("Article Name")
    typec.text("Article Type")
    imagec.text("Picture")
    pressed = {}
    for (name, atype, imagestr) in cursor:
        row = viewform.container()
        wearc, namec, typec, imagec = row.columns(4)
        pressed[name] = wearc.checkbox("Wear Me", key=name)
        namec.text(name)
        typec.text(atype)
        binvalue = binascii.a2b_base64(imagestr)
    try:
        imagec.image(Image.open(io.BytesIO(binvalue)))
    except:
        imagec.image(Image.new(mode="RGBA", size=(100,100), color=255))
    cursor.close()

    if submit:
        st.session_state['filterkey'] = filterselect
        st.experimental_rerun()
    elif  wsubmit:
        cursor = dbcon.cursor()
        for k in pressed.keys():
            if pressed[k] == True:
                query="UPDATE articles SET TimesWorn = TimesWorn + 1 WHERE Name = '" + name + "'"
                cursor.execute(query)
        cursor.close()

page_names_to_funcs = {
    "Home": intro,
    "Add Clothing": create_piece,
    "View Clothing": view_pieces,
    "Get Dressed": get_dressed,
}

page_name = st.sidebar.selectbox("Choose an operation", page_names_to_funcs.keys())
page_names_to_funcs[page_name]()
