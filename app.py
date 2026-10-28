import streamlit as st
import pandas as pd
import datetime
import time

st.title("My Practice App")
name = st.text_input("Enter your name")
if name:
 st.write("Hello,", name)

st.divider()

marks = st.slider("Select your marks", 0,100,35)
st.write("Marks:", marks)
st.divider()

st.header("Columns and Metrics")
col1, col2, col3 = st.columns(3)

col1.metric("Sales", "50K", "+5%")
col2.metric("Profit", "12K", "+2%")
col3.metric("Orders", "340", "-8")

st.sidebar.header("Settings")
city = st.sidebar.selectbox("Select city",["Chennai","Madurai", "Trichy","Coimbatore"])
st.sidebar.write("You chose:",city)

st.divider()
st.header("Date,Time and Color")
dob = st.date_input( "Select your date of birth",
value=datetime.date(2000, 1, 1),
min_value=datetime.date(1950, 1, 1),
max_value=datetime.date.today())

st.write("Date of Birth:", dob)

meeting = st.time_input("Select meeting time")
st.write("Meeting time:", meeting)

color = st.color_picker("Pick a color", "#00FFFF")
st.write("Color code:",color)

st.divider()
st.header("Progress")
if st.button("Start loading"):
    bar = st.progress(0)
    for i in range(100):
        time.sleep(0.02)
        bar.progress(i + 1)
    st.success("Done!")

st.divider()
st.header("Tabs and Expander")
tab1,tab2=st.tabs(["About","Skills"])
with tab1:
    st.write("I'm learning Streamlit.")
    with tab2:
        st.write("Python","SQL","Pandas")
    with st.expander("Click to see more"):
        st.write("This text is hidden until you click.")
 
st.divider()
st.header("Data and Charts")
data = {"Month":["Jan","Feb","Mar","Apr","May"],
"Sales":[200,400,350,150,500],
"Profit":[50,80,60,150,120]}
df=pd.DataFrame(data)
st.dataframe(df)
st.subheader("Bar chart")
st.bar_chart(df.set_index("Month"))
st.subheader("Line chart")
st.line_chart(df.set_index("Month")[["Sales"]])

st.write("Total Sales:", df["Sales"].sum())
st.write("Average profit:",df["Profit"].mean())

st.divider()
st.header("Download and Upload")
csv = df.to_csv(index=False)

st.download_button(
    label="Download table as CSV",
    data=csv,
    file_name="sales.csv",
    mime="text/csv"
)

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    uploaded_df = pd.read_csv(uploaded_file)

    st.write("Rows and columns:", uploaded_df.shape)
    st.write("Preview of the data:")
    st.dataframe(uploaded_df)
else:
    st.info("Please upload a CSV file.")

st.divider()
st.header("Character limit")
bio = st.text_area("Write about yourself",max_chars=250,height=150)
st.write("Characters used:", len(bio), "/ 250")

st.divider()

st.header("Sign Up")
username = st.text_input("Username (letters only)", max_chars=20)
if username:
    if username.isalpha():
        st.success("Username is valid")
    else:
        st.error("Only letters are allowed. No numbers, spaces or symbols.")

password = st.text_input("Password", type="password", max_chars=30)

if password:
    if len(password) < 8:
        st.warning("Password must be at least 8 characters.")
    else:
        st.success("Password length is fine")

st.divider()

st.header("Registration Form")

with st.form("register_form"):
    new_user = st.text_input("Username (letters only)", max_chars=20)
    new_pass = st.text_input("Password", type="password", max_chars=30)
    submit = st.form_submit_button("Register")

if submit:
    if not new_user.isalpha():
        st.error("Username must contain letters only.")
    elif len(new_pass) < 8:
        st.warning("Password must be at least 8 characters.")
    else:
        st.success("Registered successfully!")

st.divider()
st.header("Counter")
if "count" not in st.session_state:
    st.session_state["count"]=0
if st.button("Add 1"):
    st.session_state["count"]+=1
st.write("Count:", st.session_state["count"])                        