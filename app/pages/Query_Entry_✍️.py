import streamlit as st
from models.query import Query
from models.enums.queryOperation import QueryOperation
from models.enums.filterOperator import FilterOperator
from models.enums.queryType import QueryType
from models.enums.tableType import TableType
from models.condition import Condition
from models.enums.logicalOperator import LogicalOperator
from utils.qstore import store_object
from models.metadata.attrs_constraints import Constraints
from controller.main import pipeline


def query_builder():
    data = {
        "EMPLOYEE": [
            row.attribute_name for row in Constraints.get_columns(TableType.EMPLOYEE)
        ],
        "PROJECT": [
            row.attribute_name for row in Constraints.get_columns(TableType.PROJECT)
        ],
    }

    conditions = []
    logical_operators = []

    filter_operators = {
        "=": FilterOperator.EQ,
        ">": FilterOperator.GT,
        "<": FilterOperator.LT,
        ">=": FilterOperator.GE,
        "<=": FilterOperator.LE,
        "!=": FilterOperator.NE,
        "BETWEEN": FilterOperator.BETWEEN,
    }

    # Dropdown for selecting table
    st.subheader("SELECT")
    selected_table = st.selectbox("Select Table", list(data.keys()))

    # Select columns for the SELECT clause
    st.subheader("COLUMNS")
    select_all_columns = st.checkbox(f"Select All Columns from {selected_table}")
    if select_all_columns:
        selected_columns = data[selected_table]
    else:
        selected_columns = st.multiselect(
            f"Select Columns from {selected_table}", data[selected_table]
        )

    st.subheader("JOIN")
    # Checkbox for join
    join_checkbox = st.checkbox("Use EQUI JOIN")
    join_table = None
    if join_checkbox:
        # Dropdown for selecting table to join
        join_table = st.selectbox("Select Table to INNER JOIN", list(data.keys()))

        row1_columns = st.columns(3)
        # Condition for INNER JOIN
        condition_col1 = row1_columns[0].selectbox(
            f"Select Column from {selected_table}", data[selected_table]
        )
        condition_sign = row1_columns[1].selectbox("Equal Sign", ["="])
        condition_col2 = row1_columns[2].selectbox(
            f"Select Column from {join_table}",
            data[join_table],
            key="join_condition_col2",
        )

        join_condition = f"INNER JOIN {join_table} ON {selected_table}.{condition_col1} {condition_sign} {join_table}.{condition_col2}"  # noqa: E501

        join_col_names = [condition_col1, condition_col2]
    else:
        join_condition = ""

    # WHERE clause
    st.subheader("WHERE")
    row1_columns = st.columns(4)
    condition_col_main = row1_columns[0].selectbox(
        f" {selected_table}",
        data[selected_table],
        key="where_condition_col",
    )
    condition_sign_main = row1_columns[1].selectbox(
        "Select Sign",
        ["=", ">", "<", ">=", "<=", "!=", "BETWEEN"],
        key="where_condition_sign",
    )

    if condition_sign_main != "BETWEEN":
        condition_value_main = row1_columns[2].text_input(
            "Enter Value", "", key="where_condition_value"
        )
        where_clause = f"WHERE ({selected_table}.{condition_col_main} {condition_sign_main} '{condition_value_main}'"  # noqa: E501
    else:
        condition_value_main1 = row1_columns[2].text_input(
            "Enter First Value", key="between_condition_value1"
        )
        condition_value_main2 = row1_columns[3].text_input(
            "Enter Second Value", key="between_condition_value2"
        )
        where_clause = f"WHERE ({selected_table}.{condition_col_main} {condition_sign_main} '{condition_value_main1}' AND '{condition_value_main2}'"  # noqa: E501

    # Additional conditions
    i = 1
    st.subheader("CONDITIONS")

    while st.checkbox("EXTRA CONDITION", key=f"extra_condition_{i}"):
        st.write(f"Condition {i}")
        row1_columns = st.columns(5)
        condition_logic = row1_columns[0].selectbox(
            "Logic", ["AND", "OR"], key=f"condition_logic_{i}"
        )
        condition_col = row1_columns[1].selectbox(
            "Column", data[selected_table], key=f"extra_condition_col_{i}"
        )
        condition_sign = row1_columns[2].selectbox(
            "Sign",
            ["=", ">", "<", ">=", "<=", "!=", "BETWEEN"],
            key=f"extra_condition_sign_{i}",
        )

        if condition_logic == "OR":
            if condition_sign != "BETWEEN":
                condition_value = row1_columns[3].text_input(
                    "Value", "", key=f"extra_condition_value_{i}"
                )
                where_clause += f") {condition_logic} ({selected_table}.{condition_col} {condition_sign} '{condition_value}'"  # noqa: E501
            else:
                condition_value1 = row1_columns[3].text_input(
                    "Enter First Value", key=f"extra_condition_value1_{i}"
                )
                condition_value2 = row1_columns[4].text_input(
                    "Enter Second Value", key=f"extra_condition_value2_{i}"
                )
                where_clause += f") {condition_logic} ({selected_table}.{condition_col} BETWEEN '{condition_value1}' AND '{condition_value2}'"  # noqa: E501
        else:
            if condition_sign != "BETWEEN":
                condition_value = row1_columns[3].text_input(
                    "Value", "", key=f"extra_condition_value_{i}"
                )
                where_clause += f" {condition_logic} {selected_table}.{condition_col} {condition_sign} '{condition_value}'"  # noqa: E501
            else:
                condition_value1 = row1_columns[3].text_input(
                    "Enter First Value", key=f"extra_condition_value1_{i}"
                )
                condition_value2 = row1_columns[4].text_input(
                    "Enter Second Value", key=f"extra_condition_value2_{i}"
                )
                where_clause += f" {condition_logic} {selected_table}.{condition_col} BETWEEN '{condition_value1}' AND '{condition_value2}'"  # noqa: E501

        conditions.append(
            Condition(
                column_name=condition_col,
                operator=filter_operators[condition_sign],
                condition_type=QueryType.EQUALITY
                if condition_sign == "="
                else QueryType.RANGE,
                values=[condition_value1, condition_value2]
                if condition_sign == "BETWEEN"
                else [condition_value],
            )
        )
        logical_operators.append(
            LogicalOperator.OR if condition_logic == "OR" else LogicalOperator.AND
        )

        i += 1

    # Close the last parenthesis if there are additional conditions
    if i > 1:
        where_clause += ")"

    # Display the final query
    if join_checkbox:
        final_query = f"SELECT {', '.join(selected_columns)} FROM {selected_table} {join_condition} {where_clause}"  # noqa: E501
        f_final_query = f"SELECT {', '.join(selected_columns)}\nFROM {selected_table}\n{join_condition}\n{where_clause}"  # noqa: E501
    else:
        final_query = (  # noqa: F841
            f"SELECT {', '.join(selected_columns)} FROM {selected_table}{where_clause}"
        )
        f_final_query = f"SELECT {', '.join(selected_columns)}\nFROM {selected_table}\n{where_clause}"  # noqa: E501
    st.subheader("Final Query:")
    st.code(f_final_query)

    if st.button("Generate Query Report"):
        conditions.append(
            Condition(
                column_name=condition_col_main,
                operator=filter_operators[condition_sign_main],
                condition_type=QueryType.EQUALITY
                if condition_sign_main == "="
                else QueryType.RANGE,
                values=[condition_value_main1, condition_value_main2]
                if condition_sign_main == "BETWEEN"
                else [condition_value_main],
            )
        )
        query = Query(
            operation=QueryOperation.SELECT
            if (join_checkbox is False)
            else QueryOperation.JOIN,
            table_name=TableType.EMPLOYEE
            if (selected_table == "EMPLOYEE")
            else TableType.PROJECT,
            select_columns_names=selected_columns,
            filters=conditions,
            filters_operators=logical_operators,
            join_column_names=join_col_names if (join_checkbox is True) else [],
            join_table_name=
            # None if (join_checkbox == False)
            # else (
            TableType.EMPLOYEE if (join_table == "EMPLOYEE") else TableType.PROJECT
            # ),
        )
        pipeline(query)
        store_object(query)

        st.success("Query report generated!")
        st.write("Go to Query Report page to access the Statistics 📊.")

    # Query = Query(
    #     operation=QueryOperation.SELECT,
    #     table_name=TableType.EMPLOYEE,
    #     select_columns_names=["ssn", "middle_name"],
    #     filters=[
    #         Condition(
    #             column_name="ssn",
    #             operator=FilterOperator.BETWEEN,
    #             condition_type=QueryType.RANGE,
    #             values=["EM100000", "EM100010"],
    #         ),
    #         Condition(
    #             column_name="middle_name",
    #             operator=FilterOperator.GT,
    #             condition_type=QueryType.RANGE,
    #             values=["C"],
    #         ),
    #     ],
    #     filters_operators=[LogicalOperator.AND],
    # )


def main():
    st.title("Query Entry ✍️")
    query_builder()


if __name__ == "__main__":
    main()
