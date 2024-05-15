import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
import json
import folder_processor
import os 
import yaml
from final_json_output import process_json_output

process_json_output()
data_json_current = folder_processor.current_month()

data_json_prev = folder_processor.last_month()
#{'Month': '2024-04-01', 'Expenses': {'E-commerce': 12499.0, 'Food': 6007.62, 'Investment': 100000.0, 'EMI': 313.21, 'Maintenance': 3660.0, 'Rent': 18000.0}, 'Miscellaneous': 49867.0, 'Credit': '220320.08', 'Debit': '190346.83', 'Opening Balance': '681989.58', 'Closing Balance': '711962.83'}

# Assume you have some variables representing prices
debit_bal = float(data_json_current['Debit'])
credit_price = float(data_json_current['Credit'])
zerodha_price = 0 #Will configure later
totbal_price = float(data_json_current['Closing Balance'])
startbal_price = float(data_json_current['Opening Balance'])

# You can calculate trends based on previous values
debit_previous_bal = float(data_json_prev['Debit'])
credit_previous_price = float(data_json_prev['Credit'])
zerodha_previous_price = 0
totbal_previous_price = float(data_json_prev['Closing Balance'])
startbal_previous_price = float(data_json_prev['Opening Balance'])

json_data = folder_processor.last_six_month()
# Iterate over the keys in the JSON data and enumerate them to get index
for idx, (key, value) in enumerate(json_data.items(), start=1):
    # Dynamically create variables based on the index
    globals()[f"month{idx}"] = value





# Calculate trend for each cryptocurrency
debit_trend = "🔼" if debit_bal > debit_previous_bal else "🔽" if debit_bal < debit_previous_bal else ""
credit_trend = "🔼" if credit_price > credit_previous_price else "🔽" if credit_price < credit_previous_price else ""
zerodha_trend = "🔼" if zerodha_price > zerodha_previous_price else "🔽" if zerodha_price < zerodha_previous_price else ""
totbal_trend = "🔼" if totbal_price > totbal_previous_price else "🔽" if totbal_price < totbal_previous_price else ""
startbal_trend = "🔼" if startbal_price > startbal_previous_price else "🔽" if startbal_price < startbal_previous_price else ""

# Calculate percentage change for each cryptocurrency
debit_percentage_change = ((debit_bal - debit_previous_bal) / debit_previous_bal) * 100 if debit_previous_bal != 0 else 0
credit_percentage_change = ((credit_price - credit_previous_price) / credit_previous_price) * 100 if credit_previous_price != 0 else 0
zerodha_percentage_change = ((zerodha_price - zerodha_previous_price) / zerodha_previous_price) * 100 if zerodha_previous_price != 0 else 0
totbal_percentage_change = ((totbal_price - totbal_previous_price) / totbal_previous_price) * 100 if totbal_previous_price != 0 else 0
startbal_percentage_change = ((startbal_price - startbal_previous_price) / startbal_previous_price) * 100 if startbal_previous_price != 0 else 0

# Set up the Streamlit page configuration
st.set_page_config(
    layout='wide',
    page_title='Dashboard'
)

# Hide Streamlit header and footer
st.markdown(
    """
    <style>
        footer {display: none}
        [data-testid="stHeader"] {display: none}
    </style>
    """, unsafe_allow_html=True
)

# Load custom CSS styles
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Define layout columns
title_col, emp_col, debit_col, credit_col, zerodha_col, totbal_col, startbal_col = st.columns([1, 0.2, 1, 1, 1, 1, 1])

# Title section
with title_col:
    st.markdown('<p class="dashboard_title">Personal<br>money</p>', unsafe_allow_html=True)

#DEBIT
with debit_col:
    with st.container():
        debit_color = "green" if debit_trend == "🔽" else "red" if debit_trend == "🔼" else "black"
        debit_percentage_change_text = f" ({debit_percentage_change:.2f}%)" if debit_percentage_change != 0 else ""
        st.markdown(f'<p class="debit_text">Debit<br></p><p class="price_details" style="color: {debit_color}">{debit_bal} {debit_trend}<sub>{debit_percentage_change_text}</sub></p>', unsafe_allow_html=True)

# credit section
with credit_col:
    with st.container():
        credit_color = "red" if credit_trend == "🔽" else "green" if credit_trend == "🔼" else "black"
        credit_percentage_change_text = f" ({credit_percentage_change:.2f}%)" if credit_percentage_change != 0 else ""
        st.markdown(f'<p class="credit_text">Credit<br></p><p class="price_details" style="color: {credit_color}">{credit_price} {credit_trend}<sub>{credit_percentage_change_text}</sub></p>', unsafe_allow_html=True)

# zerodha section
with zerodha_col:
    with st.container():
        zerodha_color = "red" if zerodha_trend == "🔽" else "green" if zerodha_trend == "🔼" else "black"
        zerodha_percentage_change_text = f" ({zerodha_percentage_change:.2f}%)" if zerodha_percentage_change != 0 else ""
        st.markdown(f'<p class="zerodha_text">Zerodha<br></p><p class="price_details" style="color: {zerodha_color}">{zerodha_price} {zerodha_trend}<sub>{zerodha_percentage_change_text}</sub></p>', unsafe_allow_html=True)

# totbal section
with totbal_col:
    with st.container():
        totbal_color = "red" if totbal_trend == "🔽" else "green" if totbal_trend == "🔼" else "black"
        totbal_percentage_change_text = f" ({totbal_percentage_change:.2f}%)" if totbal_percentage_change != 0 else ""
        st.markdown(f'<p class="totbal_text">Total Balance<br></p><p class="price_details" style="color: {totbal_color}">{totbal_price} {totbal_trend}<sub>{totbal_percentage_change_text}</sub></p>', unsafe_allow_html=True)

# startbal section
with startbal_col:
    with st.container():
        startbal_color = "red" if startbal_trend == "🔽" else "green" if startbal_trend == "🔼" else "black"
        startbal_percentage_change_text = f" ({startbal_percentage_change:.2f}%)" if startbal_percentage_change != 0 else ""
        st.markdown(f'<p class="startbal_text">Starting Balance<br></p><p class="price_details" style="color: {startbal_color}">{startbal_price} {startbal_trend}<sub>{startbal_percentage_change_text}</sub></p>', unsafe_allow_html=True)



params_col, chart_col = st.columns([1,1.2])

with params_col:


    #data = json.loads(data_json_current) #currentmonth
    data = data_json_current
    # Extract "Expenses" data for visualization
    expenses_data = data["Expenses"]

    # Convert expenses data to DataFrame for visualization
    expenses_df = pd.DataFrame(expenses_data.items(), columns=["Category", "Amount"])

    # Create Altair chart
    bars = alt.Chart(expenses_df).mark_bar().encode(
        x='Amount:Q',
        y="Category:O"
    )

    text = bars.mark_text(
        align='left',
        baseline='middle',
        dx=3  # Nudges text to right so it doesn't appear on top of the bar
    ).encode(
        text='Amount:Q'
    )

    chart = (bars + text).properties()

    # Display Altair chart
    st.altair_chart(chart, use_container_width=True)

    with chart_col:

        miscellaneous_data = data_json_current["Misc_set"]["Miscellaneous"]

        # Create DataFrame
        miscellaneous_df = pd.DataFrame(miscellaneous_data, columns=["Miscellaneous"])

        # Set width to 100% for the DataFrame
        st.write(miscellaneous_df)

#ZERODHA Integration
# fot1, fot3, fot4 = st.columns([1, 5, 1])

# with fot1:
#     with st.container():
#         credit_color = "red" if credit_trend == "🔽" else "green" if credit_trend == "🔼" else "black"
#         credit_percentage_change_text = f" ({credit_percentage_change:.2f}%)" if credit_percentage_change != 0 else ""
#         st.markdown(f'<p class="credit_text">Dividends<br></p><p class="price_details" style="color: {credit_color}">{credit_price} {credit_trend}<sub>{credit_percentage_change_text}</sub></p>', unsafe_allow_html=True)

# # with fot2:
# #     with st.container():
# #         credit_color = "red" if credit_trend == "🔽" else "green" if credit_trend == "🔼" else "black"
# #         credit_percentage_change_text = f" ({credit_percentage_change:.2f}%)" if credit_percentage_change != 0 else ""
# #         st.markdown(f'<p class="credit_text">Credit<br></p><p class="price_details" style="color: {credit_color}">{credit_price} {credit_trend}<sub>{credit_percentage_change_text}</sub></p>', unsafe_allow_html=True)

# with fot3:
#     st.markdown("""
#     <style>
#     .stProgress .st-bo {
#         background-color: green;
#     }
#     </style>
#     """, unsafe_allow_html=True)

#     #st.text(progress_text)
#     # Define the current and final financial goals
#     current_net = 3000000
#     final_goal = 10000000

#     # Calculate the percentage progress towards the financial goal
#     percent = round((current_net / final_goal) * 100, 2)

#     percent = percent / 100

#     st.progress(float(percent))
#     goal_text = f'<p class="credit_text">Goal: {final_goal}/{current_net}</p>'
#     st.markdown(goal_text, unsafe_allow_html=True)

# with fot4:
#     previous_percent = 25  # For demonstration, replace it with your actual previous percentage
#     percent = percent * 100

#     # Define the financial goal text with subscript for the percentage change from the previous state
    
#     progress_text = f"Financial Goal: {percent}%"
#     if percent > previous_percent:
#         credit_color = "green"
#     else:
#         credit_color = "red"
#     credit_color = "red" if credit_trend == "🔽" else "green" if credit_trend == "🔼" else "black"
#     credit_percentage_change_text = f"{percent - previous_percent}%"
#     progress_text = f'<p class="credit_text">Percent<p class="price_details" style="color: {credit_color}">{credit_price} {credit_trend}<sub>{credit_percentage_change_text}</sub></p>'
#     st.markdown(progress_text, unsafe_allow_html=True)




botom = st.columns(1)
with botom[0]:
    data_month1 = month1
    data_month2 = month2
    data_month3 = month3
    data_month4 = month4
    data_month5 = month5
    data_month6 = month6

    # Create a DataFrame for each month
    df_month1 = pd.DataFrame(data_month1['Expenses'].items(), columns=['Category', 'Amount'])
    #month1 = pd.to_datetime(month1["Month"]).strftime('%B')
    month1 =  pd.to_datetime(month1["Month"]).strftime('%B')
    df_month1['Month'] = month1

    df_month2 = pd.DataFrame(data_month2['Expenses'].items(), columns=['Category', 'Amount'])
    month2 = pd.to_datetime(month2["Month"]).strftime('%B')
    df_month2['Month'] = month2

    df_month3 = pd.DataFrame(data_month3['Expenses'].items(), columns=['Category', 'Amount'])
    month3 = pd.to_datetime(month3["Month"]).strftime('%B')
    df_month3['Month'] = month3

    df_month4 = pd.DataFrame(data_month4['Expenses'].items(), columns=['Category', 'Amount'])
    month4 = pd.to_datetime(month4["Month"]).strftime('%B')
    df_month4['Month'] = month4

    df_month5 = pd.DataFrame(data_month5['Expenses'].items(), columns=['Category', 'Amount'])
    month5 = pd.to_datetime(month5["Month"]).strftime('%B')
    df_month5['Month'] = month5

    df_month6 = pd.DataFrame(data_month6['Expenses'].items(), columns=['Category', 'Amount'])
    month6 = pd.to_datetime(month6["Month"]).strftime('%B')
    df_month6['Month'] = month6

    # Concatenate all DataFrames
    df = pd.concat([df_month1, df_month2, df_month3, df_month4, df_month5, df_month6], ignore_index=True)

    # chart = alt.Chart(df).mark_area().encode(
    #     x='Month:N',
    #     y='Amount:Q',
    #     color='Category:N',
    #     row=alt.Row('Category:N')
    # ).properties(height=50, width=700)

    # st.altair_chart(chart, theme="streamlit", use_container_width=False)

    monthly_sum = df.groupby('Month')['Amount'].sum().reset_index()
    df_merged = pd.merge(df, monthly_sum, on='Month', suffixes=('', '_sum'))


    chart = alt.Chart(df_merged).mark_bar(
        cornerRadiusTopLeft=3,
        cornerRadiusTopRight=3
    ).encode(
        x=alt.X('Amount:Q', stack="normalize"),
        y='Month:O',
        color='Category:N',
        tooltip=['Month', 'Category', 'Amount:Q', 'Amount_sum']
    )


    st.altair_chart(chart, theme="streamlit", use_container_width=True)



@st.experimental_dialog("Add pattern to category")
def vote():
    # Step 1: Recursively go through all .yaml files from directory and get category values
    cat_yaml = "cat_yaml"
    categories = []
    for root, dirs, files in os.walk(cat_yaml):
        for file in files:
            if file.endswith(".yaml"):
                yaml_file = os.path.join(root, file)
                with open(yaml_file, 'r') as f:
                    yaml_data = yaml.safe_load(f)
                    if 'category' in yaml_data:
                        categories.append(yaml_data['category'])

    # Step 2: Display dropdown select options
    selected_category = st.selectbox("Select Category", categories)

    # Step 3: Display contents of the selected file
    if selected_category:
        selected_file = None
        for root, dirs, files in os.walk(cat_yaml):
            for file in files:
                if file.endswith(".yaml"):
                    yaml_file = os.path.join(root, file)
                    with open(yaml_file, 'r') as f:
                        yaml_data = yaml.safe_load(f)
                        if 'category' in yaml_data and yaml_data['category'] == selected_category:
                            selected_file = yaml_file
                            break
            if selected_file:
                break
        if selected_file:
            with open(selected_file, 'r') as f:
                st.write(f"Contents of {selected_category} file:")
                st.code(f.read())

    # Step 4: Add text input to append to the file
    new_regex = st.text_input("Enter new regex")
    if new_regex and selected_file:
        with open(selected_file, 'r') as f:
            yaml_data = yaml.safe_load(f)

        # Check if the new regex already exists in the list
        if 'regex' in yaml_data and new_regex not in yaml_data['regex']:
            yaml_data['regex'].append(new_regex)
        elif 'regex' not in yaml_data:
            yaml_data['regex'] = [new_regex]

        # Write updated YAML data back to the file
        with open(selected_file, 'w') as f:
            yaml.dump(yaml_data, f)

    if st.button("Submit"):
        st.session_state.vote = {"item": new_regex, "reason": f"Added to category {selected_category}"}
        st.rerun()


if "vote" not in st.session_state:
    col1 = st.columns(1)
    # with text_col:
    #     st.markdown(
    #         f'<p class="debit_text" style="text-align: center;">Create/Modify category<br></p>',
    #         unsafe_allow_html=True
    #     )
   # col1 = st.columns(1)  # Create two columns
    with col1[0]:
        if st.button("Modify category", key="button_A", use_container_width=True):
            vote()
else:
    f"You voted for {st.session_state.vote['item']} because {st.session_state.vote['reason']}"
