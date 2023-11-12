import streamlit as st
from utils.qstore import retrieve_object


def query_report_page(dictionary):
    st.write("### Displaying Dictionary:")
    for key, value in dictionary.items():
        st.write(f"**{key}:** {value}")


def main():
    st.title("Streamlit Dictionary Display")

    # Example dictionary (replace this with your own)
    costs = retrieve_object().cost

    # Display the dictionary
    query_report_page(costs)


if __name__ == "__main__":
    main()
