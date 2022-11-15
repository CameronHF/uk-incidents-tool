import pandas as pd
import streamlit as st
from datetime import datetime

from db_functions.functionforDownloadButtons import download_button
from db_functions.dwh_connection import dwh_connect

current_date = datetime.today().strftime('%Y-%m-%d')
st.set_page_config(page_title='Production Data',
                   page_icon=':lemon:',
                   layout='wide'
                   )

hide_menu_style = '<style> footer {visibility: hidden;} </style>'
st.markdown(hide_menu_style, unsafe_allow_html=True)


st.title("⚙️ Production Data")

production_query_form = st.form(key='production_query_form')
with production_query_form:
    st.write('Select a date range (format: YYYY-MM-DD)')
    cols = st.columns((1, 1))
    start_date = cols[0].date_input('Start Date')
    end_date = cols[1].date_input('End Date')
    recipe_addon_select = cols[0].radio('Production Type', ['Recipe', 'Addon'])
    recipe_number_error = cols[1].text_input("Recipe Number (Separate multiple by a comma)")
    submit_button = production_query_form.form_submit_button(label='Run Query')

    if submit_button:
        str_start_date = str(start_date)
        str_end_date = str(end_date)
        str_recipe_number_error = str(recipe_number_error)
        sql = open('sql/recipe_production_query.sql').read()
        if recipe_addon_select == 'Recipe':
            sql = sql.replace('REPLACE_ADDON_OR_RECIPE', 'recipe1,recipe2,recipe3,recipe4,recipe5,recipe6,recipe7')
            sql = sql.replace('REPLACE_WHERE', 'WHERE  recipe1 IN (REPLACE_RECIPE) OR recipe2 IN (REPLACE_RECIPE) OR '
                                               'recipe3 IN (REPLACE_RECIPE) OR recipe4 IN (REPLACE_RECIPE) OR recipe5 '
                                               'IN (REPLACE_RECIPE) OR recipe6 IN (REPLACE_RECIPE) OR recipe7 IN ('
                                               'REPLACE_RECIPE)')
            save_file_name = f'recipes_({str_recipe_number_error})({str_end_date}).csv'

        elif recipe_addon_select == 'Addon':
            sql = sql.replace('REPLACE_ADDON_OR_RECIPE', 'addons_1,addons_2,addons_3,addons_4,addons_5,addons_6,'
                                                         'addons_7,addons_8,addons_9')
            sql = sql.replace('REPLACE_WHERE', 'WHERE addons_1 IN (REPLACE_RECIPE) OR addons_2 IN (REPLACE_RECIPE) OR '
                                               'addons_3 IN (REPLACE_RECIPE) OR addons_4 IN (REPLACE_RECIPE) OR '
                                               'addons_5 IN (REPLACE_RECIPE) OR addons_6 IN (REPLACE_RECIPE) OR '
                                               'addons_7 IN (REPLACE_RECIPE) OR addons_8 IN (REPLACE_RECIPE) OR '
                                               'addons_9 IN (REPLACE_RECIPE)')
            save_file_name = f'addons_({str_recipe_number_error})({str_end_date}).csv'

        sql = sql.replace('REPLACE_START', str(start_date))
        sql = sql.replace('REPLACE_END', str(end_date))
        sql = sql.replace('REPLACE_RECIPE', str(recipe_number_error))
        with st.spinner('Querying Data...'):
            df = pd.read_sql(sql=sql, con=dwh_connect('DWH-CDP'))
            df.drop_duplicates(subset=['box_id'], keep='last', inplace=True)

            print(df)
            print(sql)

        st.success(
            f"""
                Production data loaded {str_start_date} to {str_end_date}
                """
        )
        c29, c30, c31 = st.columns([1, 1, 2])
        with c29:

            CSVButton = download_button(
                df,
                f"{save_file_name}",
                "Download to CSV",
            )
