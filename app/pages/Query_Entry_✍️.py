import streamlit as st



# make a nonlocal variable to store the final query

def query_builder():
    # change the nonlocal variable to a global variable
    
    tables = {
        'table1': ['col1', 'col2', 'col3'],
        'table2': ['col1', 'col2', 'col3']
    }
    
    # Dropdown for selecting table
    st.subheader('SELECT')
    selected_table = st.selectbox('Select Table', ['table1', 'table2', 'table3'])
    
    # Select columns for the SELECT clause
    st.subheader('COLUMNS')
    select_all_columns = st.checkbox(f'Select All Columns from {selected_table}')
    if select_all_columns:
        selected_columns = ['*']
    else:
        selected_columns = st.multiselect(f'Select Columns from {selected_table}', ['col1', 'col2', 'col3'])

    st.subheader('JOIN')
    # Checkbox for join
    join_checkbox = st.checkbox('Use EQUI JOIN')

    if join_checkbox:
        # Dropdown for selecting table to join
        join_table = st.selectbox('Select Table to INNER JOIN', ['table1', 'table2', 'table3'])
        
        row1_columns = st.columns(3)
        # Condition for INNER JOIN
        condition_col1 =  row1_columns[0].selectbox(f'Select Column from {selected_table}', ['col1', 'col2', 'col3'])
        condition_sign =  row1_columns[1].selectbox('Equal Sign', ['='])
        condition_col2 =  row1_columns[2].selectbox(f'Select Column from {join_table}', ['col1', 'col2', 'col3'], key='join_condition_col2')

        join_condition = f"INNER JOIN {join_table} ON {selected_table}.{condition_col1} {condition_sign} {join_table}.{condition_col2}"
    else:
        join_condition = ''

   
    # WHERE clause
    st.subheader('WHERE')
    row1_columns = st.columns(3)
    condition_col = row1_columns[0].selectbox(f'Select Column from {selected_table}', ['col1', 'col2', 'col3'], key='where_condition_col')
    condition_sign = row1_columns[1].selectbox('Select Sign', ['=', '>', '<', '>=', '<='], key='where_condition_sign')
    condition_value = row1_columns[2].text_input('Enter Value', '', key='where_condition_value')
    where_clause = f"WHERE ({selected_table}.{condition_col} {condition_sign} '{condition_value}'"

      # Additional conditions
    i = 1
    st.subheader('CONDITIONS')
    
    while st.checkbox(f'EXTRA CONDITION', key=f'extra_condition_{i}'):
        
        st.write(f'Condition {i}')
        row1_columns = st.columns(3)
        row1_columns[0].selectbox('Column', ['col1', 'col2', 'col3'], key=f'extra_condition_col_{i}')
        row1_columns[1].selectbox('Sign', ['=', '>', '<', '>=', '<='], key=f'extra_condition_sign_{i}')
        row1_columns[2].text_input('Value', '', key=f'extra_condition_value_{i}')
        

        condition_logic = st.radio(f'Logic', ['AND', 'OR'], key=f'condition_logic_{i}')
        
        if condition_logic == 'OR':
            where_clause += f") {condition_logic} ({selected_table}.{condition_col} {condition_sign} '{condition_value}'"
        else:
            where_clause += f" {condition_logic} {selected_table}.{condition_col} {condition_sign} '{condition_value}'"
        
        i += 1

    # Close the last parenthesis if there are additional conditions
    if i > 1:
        where_clause += ")"

    # Display the final query
    if join_checkbox:
        final_query = f"SELECT {', '.join(selected_columns)} FROM {selected_table} {join_condition} {where_clause}"
        f_final_query = f"SELECT {', '.join(selected_columns)}\nFROM {selected_table}\n{join_condition}\n{where_clause}"
    else:
        final_query = f"SELECT {', '.join(selected_columns)} FROM {selected_table}{where_clause}"
        f_final_query = f"SELECT {', '.join(selected_columns)}\nFROM {selected_table}\n{where_clause}"
    st.subheader('Final Query:')
    st.code(f_final_query)
        
    if st.button('Generate Query Report'):
        st.success('Query report generated!')
        st.write("Go to Query Report page to access the Statistics 📊.")
    
    #omar el far5 TODO: make a query object and pass it to the cost estimator


def main():
    st.title('Query Entry ✍️')
    query_builder()

if __name__ == '__main__':
    main()


