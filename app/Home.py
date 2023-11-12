import streamlit as st
import pandas as pd
import numpy as np

# from pathlib import Path

# path = Path(__file__).parent.resolve()


def main():
    #     print(path)
    st.title("Meta Data")
    # Sample data
    data1 = np.random.randn(5, 5)
    data2 = np.random.randn(5, 5)
    data3 = np.random.randn(5, 5)
    data4 = np.random.randn(5, 5)

    # Create DataFrames
    df1 = pd.DataFrame(data1, columns=[f"Column {i+1}" for i in range(5)])
    df2 = pd.DataFrame(data2, columns=[f"Column {i+1}" for i in range(5)])
    df3 = pd.DataFrame(data3, columns=[f"Column {i+1}" for i in range(5)])
    df4 = pd.DataFrame(data4, columns=[f"Column {i+1}" for i in range(5)])

    # Display tables
    st.table(df1)
    st.table(df2)
    st.table(df3)
    st.table(df4)


if __name__ == "__main__":
    main()

# omar el far5 TODO: make a query object and pass it to the cost estimator
