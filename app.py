import streamlit as st 
import os
import datetime
import time
import hashlib
import pycountry
import shutil

st.set_page_config(
    page_title='Combo Cleaner',layout="centered",page_icon=":bloom:",
    menu_items={'Get Help': None,'Report a bug': None,'About': None},initial_sidebar_state="auto")
title = st.title('Combo Cleaner 🧹')
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """            
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

def check_passwd(passwd):
    lenn=False
    num,maj,min,=0,0,0
    if len(passwd)>=8:
        lenn=True
    for i in passwd:
        if i.isnumeric():
            num = num+1
        if i.isupper():
            maj=maj+1
        if i.islower():
            min=min+1
    return True if (maj!=0 and min!=0 and num!=0 and lenn) else False

def gen_filename():
    return datetime.datetime.fromtimestamp(time.time()).strftime('[%H-%M]')+'.txt'
fname = gen_filename()

def better_line(line):
    line = line.rstrip('\n\r')
    return line

try:
    os.mkdir("results")
except:
    pass

f = open(os.path.join("results",fname), "w")
uploaded = st.file_uploader("Enter file",type=["txt"])
if uploaded:
    st.success("File uploaded successfully :ok:")
    para = uploaded.getvalue()
    para = para.decode('utf-8')
    options = st.radio("Choose an option : ",["🧹","Clean","Enhance","Filter by Domain","Filter by Country"])
    completed_lines_hash = set()
    if options == "Clean":
        st.caption("1. Removing weak combos")
        for line in uploaded:
            line = line.decode('utf8')
            line = line.split(':')
            try:
                email = line[0]
                passwd = line[1]
                if check_passwd(passwd):
                    f.write(f"{email}:{passwd}\n")
            except:
                pass
        st.success("Combo Cleaned Successfully 🧹")
    
    elif options == "Enhance":
        completed_lines_hash = set()
        st.caption("2. Adding desired charcter(s) to combos")
        char = st.text_input("Enter character(s) to add :")
        for line in para.splitlines():
            hashValue = hashlib.md5(line.rstrip().encode('utf-8')).hexdigest()
            line = line.rstrip('\n')
            line = line + char
            f.write(f"{line}\n")
        f.close()
        st.success("Combo Enhanced   Successfully 🧹")
    elif options == "Filter by Domain":
        try:
            folder = 'results'
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path) and file_path.contains('Domain'):
                        os.unlink(file_path)
                except Exception as e:
                    print('Failed to delete %s. Reason: %s' % (file_path, e))
        except:
            pass
        domains = []
        completed_lines_hash = set()
        st.caption("3. Filtering by domain")
        #TODO : Add domain filtering
        for line in uploaded:
            line = line.decode('utf-8')
            line = better_line(line)
            hashValue = hashlib.md5(line.rstrip().encode('utf-8')).hexdigest()
            email = line.split(':')[0]
            domain = email.split('@')[1]
            domains.append(domain)
            domains = list(set(domains))
            f = open(os.path.join("results",f"Domain-[{domain}].txt"), "a+")
            if domain in email and hashValue not in completed_lines_hash:
                completed_lines_hash.add(hashValue)
                f.write(f"{line}\n")
        f.close()

        st.success("Combo Filtered by Domain Successfully 🧹")
    elif options == "Filter by Country":
        st.caption("4. Filtering by country")
        try:
            folder = 'results'
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path) and file_path.contains('Country'):
                        os.unlink(file_path)
                except Exception as e:
                    print('Failed to delete %s. Reason: %s' % (file_path, e))
        except:
            pass
        for line in uploaded:
                line = line.decode('utf-8')
                line = line.rstrip('\n')
                email = line.split(':')[0]
                if email[-3] == '.':
                    cc = email[-2:]
                    cc1 = pycountry.countries.get(alpha_2=cc)
                    if cc1 != None:
                        country = cc1.name
                        f = open(os.path.join("results",f"Country-[{country}].txt"), "a")
                        f.write(f"{line}\n")
                    elif cc1 ==None:
                        f = open(os.path.join("results","Country-[International].txt"), "a")
                        f.write(f"{line}\n")
                elif email[-4] == '.':
                    cc = email[-3:]
                    cc1 = pycountry.countries.get(alpha_2=cc)
                    if cc1 != None:
                        country = cc1.name
                        f = open(os.path.join("results",f"Country-[{country}].txt"), "a")
                        f.write(country)
                        f.write(f"{line}\n")
                    elif cc1 ==None:
                        f = open(os.path.join("results","Country-[International].txt"), "a")
                        f.write(f"{line}\n")
                f.close()
        st.success("Combo Filtered by Country Successfully 🧹")
    elif options == "🧹":
        st.caption("0. Choose the option that fits You.")