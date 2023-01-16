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
    counter=0
    rowdata = []
    cursor = dbcon.cursor()
    query = "SELECT Name, Type, Image, Cost From articles where Retired = 0 ORDER BY Type, Name ASC"
    cursor.execute(query)
   
    formcontainer = st.container()
    wearform = formcontainer.form("Pick Clothes", clear_on_submit=True)
    tablecont = wearform.container()
    for (name, atype, imagestr, cost) in cursor:
        row = tablecont.container()
        opsc, namec, typec, imagec = row.columns(4)
        keyname = "wearme"+str(counter)
        counter=counter+1
        checkbox = opsc.checkbox("Wear Me", key=keyname)
        namec.text(name)
        typec.text(atype)
        binvalue = binascii.a2b_base64(imagestr)
        try:
            imagec.image(Image.open(io.BytesIO(binvalue)))
        except e:
            imagec.image(Image.new(mode="RGBA", size=(100,100), color=255))
        rowdata.append(name)
    submit = tablecont.form_submit_button("Submit")
    cursor.close()

    if (submit):
        cursor = dbcon.cursor()
        counter=0
        for name in rowdata:
            keyname = "wearme"+str(counter)
            counter=counter+1
            query="UPDATE articles SET TimesWorn = TimesWorn + 1 WHERE Name = '" + name + "'"
            if (st.session_state[keyname] == True):
                cursor.execute(query)
        dbcon.commit()
        cursor.close()
        
        


page_names_to_funcs = {
    "Home": intro,
    "Add Clothing": create_piece,
    "View Clothing": view_pieces,
    "Get Dressed": get_dressed,
}

page_name = st.sidebar.selectbox("Choose an operation", page_names_to_funcs.keys())
page_names_to_funcs[page_name]()
