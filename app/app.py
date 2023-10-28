import streamlit as st

def main():
    st.set_page_config(page_title="Costex", page_icon="📊", layout="wide", initial_sidebar_state="auto")
    
    st.title("Costex: Query Cost Estimator 📊")
    st.write(
        """
        Welcome to Costex, the premier solution for estimating the cost of your database queries!
        Just input your query and let us do the magic. 🚀
        """
    )

    query_input = st.text_area("Enter your SQL query here:", "")
    if st.button("Estimate Cost"):
        # cost estimation process to be handled here
        st.success("Estimated cost: xx blocks")  

    st.sidebar.header("Quick Links")
    st.sidebar.text("Home\nDatabase Stats")

    st.markdown(
        """
        <hr>
        <p style="font-size:0.75em">© 2023, Costex - All Rights Reserved</p>
        """, unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()