import streamlit as st
import pandas as pd
import pymongo
import time
from datetime import datetime, timedelta
client = pymongo.MongoClient("mongodb+srv://suriya315:12345678s@cluster0.kbh9v.mongodb.net/?retryWrites=true&w=majority")
db = client.data_learn
pc=db.values_finals
current_date = pd.Timestamp(datetime.now().date())
def adding():
    subject=st.selectbox("subject",["Mathematics","Statistics","English","Computational Thinking"])
    describe=st.text_input("describe")
    topic=st.text_input("topics")
    link=st.text_input("links")
    date_only = st.date_input("Select a date")

    if st.button("add data"):
        
        

# Extract the date part from the current date
        
        df=pd.DataFrame()
        df1=pd.DataFrame()
        for i in [1,4,7,14,30,60,90]:
            dates=date_only+timedelta(days=i)
            if i==1:
                df["subject"]=[subject]
                df["describe"]=[describe]
                df["youtube"]=[link]
                df["topic"]=[topic]
                df["date_to_study"]=[dates]
                df["day"]=[i]
            else:
                df1["subject"]=[subject]
                df1["describe"]=[describe]
                df1["youtube"]=[link]
                df1["topic"]=[topic]
                df1["date_to_study"]=[dates]
                df1["day"]=[i]
                df = pd.concat([df, df1], axis=0)
        df['date_to_study'] = df['date_to_study'].astype(str)
        data_dict = df.to_dict(orient='records')
        pc.insert_many(data_dict)
        st.success("data added successfully")
        
def view():
    retrieved_data = pd.DataFrame(list(pc.find()))
    retrieved_data["date_to_study"]=pd.to_datetime(retrieved_data["date_to_study"])
    filtered_df = retrieved_data[retrieved_data['date_to_study'] <= pd.Timestamp(st.date_input("date"))]
    
    a=st.selectbox("what to search subject >>>",["no","yes"])
    if a =="yes":
        sub=st.selectbox("subject >>>",["Mathematics","Statistics","English","Computational Thinking"])
        dfs=filtered_df[filtered_df["subject"]==sub]
        dfs["days to go"]=(dfs["date_to_study"]-current_date).dt.days
        dfs=dfs.sort_values(by="days to go", ascending=True)
        st.dataframe(dfs)
        st.text("done----:")
        nod=["None"]
        id_list = dfs["_id"].tolist()
        id_list=nod+id_list
        selected=st.selectbox("id select",id_list)
        if selected=="None":
            pass
        else:
            finalsdata=dfs[dfs["_id"]==selected]
            st.dataframe(finalsdata)
            st.text("are you completed this ...")
        
    else:
        filtered_df["days to go"]=(filtered_df["date_to_study"]-current_date).dt.days
        filtered_df=filtered_df.sort_values(by="days to go", ascending=True)
        st.dataframe(filtered_df)
        st.text("done----:")
        nod=["None"]
        id_list = filtered_df["_id"].tolist()
        id_list=nod+id_list
        selected=st.selectbox("id select",id_list)
        if selected=="None":
            pass
        else:
            finalsdata=filtered_df[filtered_df["_id"]==selected]
            st.dataframe(finalsdata)
            st.text("are you completed this ...")
    if st.button("remove"):
        if len(finalsdata)==0:
            pass
        else:
            result = pc.delete_one({"_id": finalsdata["_id"].values[0]})
    
            # Check if the document was successfully deleted
            if result.deleted_count == 1:
                st.success("Document deleted successfully.")
                time.sleep(1)
                st.experimental_rerun()
            else:
                st.error("Document not found or not deleted.")
page_names_to_funcs = {
    "adding": adding,
    "search":view
}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()
    
    