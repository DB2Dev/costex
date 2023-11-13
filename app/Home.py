import streamlit as st
import pandas as pd
import numpy as np
from models.metadata.attrs_constraints import Constraints
from models.metadata.distributions import Distributions
from models.metadata.tables_info import TablesDetails
from models.metadata.indexes import Indexes

# from pathlib import Path

# path = Path(__file__).parent.resolve()


def main():
     
    constraint = Constraints()
    distribution = Distributions()
    table_details = TablesDetails()    
    index = Indexes()
    
   

    
    
     
    #     print(path)
    st.title("Meta Data")
    # Sample data
    # Create DataFrames
    # df1 = pd.DataFrame(data1, columns=[f"Column {i+1}" for i in range(5)])
    # df2 = pd.DataFrame(data2, columns=[f"Column {i+1}" for i in range(5)])
    # df3 = pd.DataFrame(data3, columns=[f"Column {i+1}" for i in range(5)])
    # df4 = pd.DataFrame(data4, columns=[f"Column {i+1}" for i in range(5)])

    # Display tables
    # st.table(df1)
    # st.table(df2)
    # st.table(df3)
    # st.table(df4)


if __name__ == "__main__":
    main()

# omar el far5 TODO: make a query object and pass it to the cost estimator
