import warnings
from datetime import datetime

import pandas as pd
import streamlit as st
from db_functions.dwh_connection import dwh_connect
from db_functions.functionforDownloadButtons import download_button

warnings.filterwarnings('ignore')

current_date = datetime.today().strftime('%Y-%m-%d')
current_date_2 = datetime.today()

year, week_num, day_of_week = current_date_2.isocalendar()
week_num = str(week_num)

df_error_dimensions = pd.read_csv(r'input/compensation_dimensions.csv', usecols=[
    'Category', 'error category', 'error sub category', 'complaint', 'additional detail 1', 'additional detail 2'])
df_error_dimensions_list = df_error_dimensions['Category'].to_list()

st.set_page_config(page_title='Bulk Upload Tool',
                   page_icon=':lemon:',
                   layout='centered'
                   )
hide_menu_style = '<style> footer {visibility: hidden;} </style>'
st.markdown(hide_menu_style, unsafe_allow_html=True)

gsheet_error_category = ['Incorrect', 'Missing', 'Delivery +1Day', 'Delivery +2Days', 'Delivery -1Day', 'No delivery',
                         'Other', 'Presumed rolled',
                         'Brand Change - Too little', 'Brand Change - Too much', 'Incorrect too little',
                         'Incorrect too much',
                         'Brand Change', 'Pres > Delivered']

if 'SKU_list' and 'cul_sku' not in st.session_state:
    st.session_state['SKU_list'] = []
    st.session_state['cul_sku'] = ''

if 'df' not in st.session_state:
    st.session_state['df'] = False

if 'bu_dp' not in st.session_state:
    st.session_state['bu_dp'] = False


def change_df():
    df = st.session_state['df']


def change_budf():
    df_gsheet = st.session_state['bu_dp']


def change_sku_list():
    ingredient_list = st.session_state['SKU_list']
    culinary_sku = st.session_state['cul_sku']


st.title("🛠 Bulk Upload Tool")

st.info('Ensure your VPN is active. Select "Multiple Recipes Impacted" when processing for multiple recipes', icon="ℹ️")
bulk_upload_file = st.file_uploader('Upload production data', type=['csv', 'xlsx'])

st.write('Incident Parameters')
cols = st.columns((1, 1, 1))
brand_select = cols[1].radio('Brand', ['HelloFresh', 'Green Chef'])
incident_type_select = cols[0].radio('Incident Type', ['Recipe', 'Addons'])
multiple_recipes_impacted = cols[2].checkbox('Multiple Recipes Impacted', False)
week_number = cols[2].text_input('Week Number', value=str(week_num))

# sku_searcher_form = st.form(key='sku_searcher_form')

# with sku_searcher_form:
st.write('Culinary SKU searcher')
cols_2 = st.columns((1, 1))
sku_searcher_input = cols_2[0].text_input('Search for SKU')
sku_searcher_submit = cols_2[0].button('Search', key='sku_searcher_submit')

if sku_searcher_submit:
    try:
        sql = open('sql/SKU_searcher.sql').read()
        sql = sql.replace('REPLACE_ME', str(sku_searcher_input).lower())
        sql = sql.replace('COUNTRY', str(brand_select))

        with st.spinner('Searching for SKU...'):
            df = pd.read_sql(sql=sql, con=dwh_connect('DWH-CDP'))
            # if df is None:
            #     st.success('No results found')
            ingredient_list = df['ingredient_name'].tolist()

            # setting sessions for the ingredient list and dataframe
            st.session_state.SKU_list = ingredient_list
            st.session_state.df = df


    except Exception as e:
        st.error('Error: ' + str(e))

sku_list = cols_2[1].selectbox('Ingredient list:', st.session_state.SKU_list, on_change=change_sku_list)

if sku_list in st.session_state.SKU_list:
    df = st.session_state.df
    culinary_sku = df.loc[df['ingredient_name'] == str(sku_list), 'culinary_sku'].iloc[0]
    print(culinary_sku)
    st.session_state.cul_sku = culinary_sku

incident_sku = cols_2[1].text_input('Culinary SKU', st.session_state.cul_sku, on_change=change_sku_list)

incidents_form = st.form(key='incidents_form')

with incidents_form:
    st.write('Incidents form')
    incident_ingredient_name = incidents_form.text_input('Ingredient name')
    incident_recipe_number = incidents_form.text_input('Recipe number (Separate multiple by a comma)')
    incident_comment = incidents_form.text_input('Error comment')
    incident_error_category = incidents_form.selectbox('Error category', df_error_dimensions_list)

    cols_3 = st.columns((1, 1))
    incident_compensation_type = cols_3[0].radio('Compensation Type', ['Refund', 'Credit'])
    incident_compensation_value = cols_3[1].radio(label=' ', options=['Flat Rate', 'Percentage'])
    incident_compensation_amount = cols_3[0].number_input('Compensation amount/ Percentage')

    incident_submit = incidents_form.form_submit_button('Submit')

with st.expander('Googe Sheet uploader'):
    gsheet_issue = st.selectbox('Issue', gsheet_error_category)
    gsheet_original_sku = st.text_input('Orginal SKU')
    gsheet_new_sku = st.text_input('New SKU')
    gsheet_additional_notes = st.text_input('Additional notes')

    cols_3 = st.columns((1, 1, 1))
    gsheet_copy = cols_3[0].button('Copy incident data')
    gsheet_upload = cols_3[1].button('Upload to DWH')

if incident_submit:
    brand_selected = str(brand_select)
    incident_type_selected = str(incident_type_select)
    incident_compensation_type = str(incident_compensation_type).lower()

    with st.spinner('Processing incident...'):

        if incident_type_selected == 'Recipe':
            sql_recipe_incident = open('sql/recipes_in_menu.sql').read()
            sql_recipe_incident = sql_recipe_incident.replace('week_number', str(week_number))

        elif incident_type_selected == 'Addons':
            print('Addons')
            sql_recipe_incident = open('sql/addons_in_menu.sql').read()
            sql_recipe_incident = sql_recipe_incident.replace('week_number', str(week_number))

        if brand_selected == 'HelloFresh':
            sql_recipe_incident = sql_recipe_incident.replace('MARKET', 'GB')

        elif brand_selected == 'Green Chef':
            sql_recipe_incident = sql_recipe_incident.replace('MARKET', 'GN')

        if multiple_recipes_impacted == True:
            df_recipe_matcher = pd.read_sql(sql=sql_recipe_incident, con=dwh_connect('DWH-CDP'))

            print('Multiple recipes impacted....')
            # incident_recipe_number = incident_recipe_number.split(',')
            # print(incident_recipe_number)
            if incident_type_selected == 'Addons':
                st.error('Multiple addons impacted not yet supported')

            elif incident_type_selected == 'Recipe':

                bulk_upload_file = pd.read_csv(bulk_upload_file, usecols=[
                    'customer_id', 'clean_box_id', 'box_value', 'courier', 'delivery_day', 'site', 'recipe1', 'recipe2',
                    'recipe3', 'recipe4', 'recipe5', 'recipe6', 'recipe7'])
                bulk_upload_file = bulk_upload_file.rename(
                    columns={'clean_box_id': 'box id', 'customer_id': 'customer id'})

                recipe_index = str(incident_recipe_number).split(',')
                print(recipe_index)

                for i in range(0, len(recipe_index)):
                    recipe_index[i] = int(recipe_index[i])
                number_of_recipes_impacted = len(recipe_index)
                df_names = ['df_' + str(i) for i in range(0, number_of_recipes_impacted)]
                df_names_saves = df_names

                cols = bulk_upload_file.columns.tolist()

                df = []
                # creates a dataframe for each recipe index
                for d, r, s in zip(df_names, recipe_index, df_names_saves):
                    bulk_upload_file['recipeCounter'] = ''
                    globals()[d] = d = bulk_upload_file[
                        (bulk_upload_file['recipe1'] == r) |
                        (bulk_upload_file['recipe2'] == r) |
                        (bulk_upload_file['recipe3'] == r) |
                        (bulk_upload_file['recipe4'] == r) |
                        (bulk_upload_file['recipe5'] == r) |
                        (bulk_upload_file['recipe6'] == r) |
                        (bulk_upload_file['recipe7'] == r)]
                    d['recipeCounter'] = d[['recipe1', 'recipe2', 'recipe3', 'recipe4',
                                            'recipe5', 'recipe6', 'recipe7']].apply(
                        lambda s: (s == r).sum(),
                        axis=1)
                    # todo: link recipe numbers to recipe names

                    r_name = df_recipe_matcher[df_recipe_matcher['recipe_index'] == r]['recipe']
                    d['recipe'] = r_name.iloc[0]
                    r_index = r
                    d['recipe index'] = r_index
                    df.append(d)

                bulk_upload_file = pd.concat(df)
                bulk_upload_file = bulk_upload_file.reset_index(level=None, drop=False)

        elif multiple_recipes_impacted == False:
            df_recipe_matcher = pd.read_sql(sql=sql_recipe_incident, con=dwh_connect('DWH-CDP'))
            incident_recipe_number = int(incident_recipe_number)

            recipe_name = \
                df_recipe_matcher.loc[df_recipe_matcher['recipe_index'] == int(incident_recipe_number), 'recipe'].iloc[
                    0]

            if incident_type_select == 'Recipe':
                bulk_upload_file = pd.read_csv(bulk_upload_file, usecols=[
                    'customer_id', 'clean_box_id', 'box_value', 'courier', 'delivery_day', 'site', 'recipe1', 'recipe2',
                    'recipe3',
                    'recipe4', 'recipe5', 'recipe6', 'recipe7'])
                bulk_upload_file = bulk_upload_file.rename(
                    columns={'clean_box_id': 'box id', 'customer_id': 'customer id'})
                bulk_upload_file['recipeCounter'] = bulk_upload_file[['recipe1', 'recipe2', 'recipe3', 'recipe4',
                                                                      'recipe5', 'recipe6', 'recipe7']].apply(
                    lambda s: (s == incident_recipe_number).sum(), axis=1)
            elif incident_type_select == 'Addons':
                bulk_upload_file = pd.read_csv(bulk_upload_file,
                                               usecols=['customer_id', 'clean_box_id', 'box_value', 'courier',
                                                        'delivery_day',
                                                        'site', 'addons_1', 'addons_2', 'addons_3', 'addons_4',
                                                        'addons_5', 'addons_6', 'addons_7', 'addons_8',
                                                        'addons_9'])
                bulk_upload_file = bulk_upload_file.rename(
                    columns={'clean_box_id': 'box id', 'customer_id': 'customer id'})
                bulk_upload_file['recipeCounter'] = bulk_upload_file[['addons_1', 'addons_2', 'addons_3', 'addons_4',
                                                                      'addons_5', 'addons_6', 'addons_7', 'addons_8',
                                                                      'addons_9']].apply(
                    lambda s: (s == incident_recipe_number).sum(), axis=1)

            bulk_upload_file['recipe index'] = incident_recipe_number
            bulk_upload_file['recipe'] = recipe_name

        if incident_compensation_value == 'Flat Rate':
            bulk_upload_file['compensation amount'] = (
                                                          float(incident_compensation_amount)) * (
                                                          bulk_upload_file["recipeCounter"])

        elif incident_compensation_value == 'Percentage':
            bulk_upload_file['compensation amount'] = bulk_upload_file.box_value * \
                                                      (incident_compensation_amount * bulk_upload_file['recipeCounter'])
            bulk_upload_file['compensation amount'] = bulk_upload_file['compensation amount'].round(
                decimals=2)

        bulk_upload_file['compensation type'] = incident_compensation_type
        bulk_upload_file['comment'] = incident_comment
        bulk_upload_file['culinary sku'] = culinary_sku
        bulk_upload_file['ingredient'] = incident_ingredient_name

        if incident_error_category is not None:
            df_errors = df_error_dimensions[df_error_dimensions['Category'] == incident_error_category]
            df_gsheet = bulk_upload_file
            st.session_state.bu_dp = df_gsheet

            df_merg_2 = pd.concat([df_errors, bulk_upload_file], axis=1)
            df_merg_2['error category'] = df_merg_2['error category'].ffill()
            df_merg_2['error sub category'] = df_merg_2['error sub category'].ffill()
            df_merg_2['complaint'] = df_merg_2['complaint'].ffill()
            df_merg_2['additional detail 1'] = df_merg_2['additional detail 1'].ffill()
            df_merg_2['additional detail 2'] = df_merg_2['additional detail 2'].ffill()
            df_merg_2.drop(columns=['Category'], inplace=True)

            cols = ['customer id', 'box id', 'error category', 'error sub category', 'complaint',
                    'additional detail 1', 'additional detail 2',
                    'ingredient', 'recipe', 'compensation type', 'compensation amount', 'recipe index',
                    'culinary sku', 'comment']

            df_final = df_merg_2[cols]

            try:
                st.success(f'Incident for {recipe_name} has been processed')
                save_file_name = ('WK' + str(week_num) + '-' +
                                  str(incident_ingredient_name) + '-R' + str(incident_recipe_number) + '.csv')
            except:
                st.success(f'Incident for {incident_recipe_number} has been processed')
                save_file_name = ('WK' + str(week_num) + '-' +
                                  'multiple' + '-R' + str(incident_recipe_number) + '.csv')

            c29, c30, c31 = st.columns([1, 1, 2])
            with c29:
                CSVButton = download_button(
                    df_final,
                    f"{save_file_name}",
                    "Download to CSV",
                )

if gsheet_copy:
    df_gsheet = st.session_state.bu_dp
    df_to_copy = df_gsheet

    # if multiple_recipes_impacted == False:

    if incident_type_select == 'Recipe':
        df_to_copy['Recipe n'] = '-' + df_gsheet['recipe index'].astype(str) + '-'

    elif incident_type_select == 'Addons':
        df_to_copy['Recipe n'] = '-' + df_gsheet['recipe index'].astype(str) + 'a-'

    if incident_compensation_type == 'Credit':
        df_to_copy['Credit'] = df_gsheet['compensation amount']
        df_to_copy['Refund'] = ''

    elif incident_compensation_type == 'Refund':
        df_to_copy['Refund'] = df_gsheet['compensation amount']
        df_to_copy['Credit'] = ''

    df_to_copy['issue'] = str(gsheet_issue)
    df_to_copy['Original sku'] = gsheet_original_sku
    df_to_copy['new sku'] = gsheet_new_sku
    df_to_copy['additional notes'] = gsheet_additional_notes

    df_to_copy.to_csv('gsheet_2.csv', index=False)
    copy_columns = ['delivery_day', 'box id', 'customer id', 'Recipe n', 'issue', 'Original sku', 'new sku',
                    'additional notes', 'Credit', 'Refund', 'courier', 'site']

    df_save = df_to_copy[copy_columns]
    df_save.to_clipboard(excel=True, index=False, header=True)

    st.success('Data copied to clipboard')

if gsheet_upload:
    st.error('This feature is not available yet')
