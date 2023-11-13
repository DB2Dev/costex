from streamlit_echarts import st_echarts
import streamlit as st
from utils.qstore import retrieve_object
from models.enums.algoChoice import AlgoChoice
import pandas as pd


def query_report_page(dictionary):
    st.write("### Query:")
    query = retrieve_object("sqlstr.dat")
    st.code(f"{query}")

    algo_choices = {
        AlgoChoice.NESTED_LOOP_JOIN: "Nested Loop Join",
        AlgoChoice.SORT_MERGE_JOIN: "Sort Merge Join",
        AlgoChoice.BINARY_SEARCH: "Binary Search",
        AlgoChoice.FILE_SCAN: "File Scan",
        AlgoChoice.PRIMARY_INDEX: "Primary Index",
        AlgoChoice.SECONDARY_INDEX: "Secondary Index",
        AlgoChoice.CLUSTERED_INDEX: "Clustered Index",
        AlgoChoice.INDEXED_NESTED_LOOP_JOIN: "Indexed Nested Loop Join",
    }

    data_keys = []
    data_values = []

    dictionary = dict(sorted(dictionary.items(), key=lambda item: item[1]))

    new_dictionary = {}

    for key, value in dictionary.items():
        new_dictionary[algo_choices[key]] = value
        data_keys.append(algo_choices[key])
        data_values.append(value)

    if len(data_values) >= 2:
        min_value = min(data_values)
        data_values.remove(min_value)
        max_value = max(data_values)
        data_values.remove(max_value)

        options = {
            "xAxis": {
                "type": "category",
                "data": data_keys,
            },
            "yAxis": {"type": "value", "max": max_value},
            "series": [
                {
                    # add data_values to the chart and make sure to style the min and max values to be different # noqa: E501
                    "data": [
                        {"value": min_value, "itemStyle": {"color": "#03a900"}},
                        *data_values,
                        {"value": max_value, "itemStyle": {"color": "#d91600"}},
                    ],
                    "type": "bar",
                    "barMinHeight": "10",
                }
            ],
        }
    else:
        options = {
            "xAxis": {
                "type": "category",
                "data": data_keys,
            },
            "yAxis": {"type": "value"},
            "series": [
                {
                    # add data_values to the chart and make sure to style the min and max values to be different # noqa: E501
                    "data": [
                        {"value": data_values[0], "itemStyle": {"color": "#03a900"}},
                    ],
                    "type": "bar",
                    "barMinHeight": "10",
                }
            ],
        }
    st_echarts(
        options=options,
        height="600px",
    )

    st.table(pd.DataFrame.from_dict(new_dictionary, orient="index", columns=["Cost"]))


def main():
    st.title("Query Cost Statistics 📊")

    # Example dictionary (replace this with your own)
    costs = retrieve_object().cost

    # Display the dictionary
    query_report_page(costs)


if __name__ == "__main__":
    main()
