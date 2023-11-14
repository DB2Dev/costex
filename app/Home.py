import streamlit as st
import pandas as pd

# import numpy as np
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
    attrs = pd.DataFrame.from_records([c.to_dict() for c in constraint])
    dist_cols = [
        "table_name",
        "attr name",
        "attr width",
        "NDV",
        "most common vals",
        "most common freq",
        "histogram",
        "correlation",
    ]
    dist = pd.DataFrame(distribution, columns=dist_cols)
    tables_cols = [
        "table_name",
        "no. of Blocks",
        "no. of Records",
    ]
    tables = pd.DataFrame(table_details, columns=tables_cols)
    indexes = pd.DataFrame.from_records([i.to_dict() for i in index])

    # Display tables
    st.subheader("Attributes Details:")
    # st.table(attrs)
    st.data_editor(
        attrs,
        hide_index=True,
        disabled=True,
    )

    st.subheader("Statistics:")
    # st.table(dist)
    st.data_editor(
        dist,
        column_config={
            "table_name": st.column_config.Column(width="small"),
            "attr name": st.column_config.Column(width="small"),
            "attr width": st.column_config.Column(width="small"),
            "NDV": st.column_config.Column(width="small"),
            "most common vals": st.column_config.Column(width="small"),
            "most common freq": st.column_config.BarChartColumn(
                width="large",
                y_max=0.001,
                y_min=0
            ),
            "histogram": st.column_config.Column(width="small"),
            "correlation": st.column_config.Column(width="small"),
        },
        hide_index=True,
        disabled=True,
    )

    st.subheader("Tables Details:")
    # st.table(tables)
    st.data_editor(
        tables,
        hide_index=True,
        disabled=True,
    )

    st.subheader("Indexes Details:")
    # st.table(indexes)
    st.data_editor(
        indexes,
        hide_index=True,
        disabled=True,
    )


if __name__ == "__main__":
    main()

# omar el far5 TODO: make a query object and pass it to the cost estimator
