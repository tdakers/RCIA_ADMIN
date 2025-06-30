from supabase import create_client, Client
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import streamlit as st
import pandas as pd
import numpy as np

url = "https://dptslvjsbhmxposqarwj.supabase.co"
key = st.secrets["api"]["key"]

supabase: Client = create_client(url, key)

# Centered title using HTML
st.set_page_config(page_title="St Matthews RCIA", layout='wide')

st.session_state.setdefault("base_df", None)

if st.session_state.base_df is None:
    # Replace 'your_table' with your actual table name
    response = supabase.table("Candidates").select("*").execute()

# Convert to DataFrame
df = pd.DataFrame(response.data)

st.markdown(
    """
    <h1 style='text-align: center; font-family: "Helvetica", sans-serif; font-size: 32px;'>
        RCIA Alert Roster
    </h1>
    """,
    unsafe_allow_html=True
)

df['Name'] = df['first_name'] + ' ' + df['last_name']
df['Address'] = df['mailing_address'].fillna('') + ' ' + df['app_number'].fillna('') + ', ' + df['city'].fillna('') + ', ' + df['state'].fillna('')

df_alert_roster = df[['Name', 'Address', 'phone_day', 'phone_evening', 'cell_phone', 'email', 'other']]
st.write(df_alert_roster)

st.markdown(
    """
    <h1 style='text-align: center; font-family: "Helvetica", sans-serif; font-size: 32px;'>
        Candidate have been married before
    </h1>
    """,
    unsafe_allow_html=True
)

candidate_has_been_married_before_col_1, candidate_has_been_married_before_col_2 = st.columns([1, 2])
with candidate_has_been_married_before_col_1:
    df_my_previous_marriage = df[(df['spouse_my_previous_marriage_status'] == 'I have been married before') | (df['fiance_my_previous_mariage'] == 'I have been married before')][['id', 'first_name', 'last_name', 'marriage_status']]
    df_my_previous_marriage['Name'] = df_my_previous_marriage['first_name'] + ' ' + df_my_previous_marriage['last_name']

    df_my_previous_marriage = df_my_previous_marriage.rename(columns={
        'marriage_status': 'Current Marriage Status'
    })

    df_my_previous_marriage = df_my_previous_marriage[['id', 'Name', 'Current Marriage Status']]

    # Set up AgGrid with row selection
    gb = GridOptionsBuilder.from_dataframe(df_my_previous_marriage)
    gb.configure_selection("single")  # 'multiple' for multi-row selection
    gb.configure_column("id", hide=True) # Hide ID column, but still allows the data to be stored
    grid_options = gb.build()

    # Display interactive grid
    grid_response = AgGrid(
        df_my_previous_marriage,
        gridOptions=grid_options,
        update_mode=GridUpdateMode.SELECTION_CHANGED,
        height=200,
        width='100%',
        fit_columns_on_grid_load=True
    )

    # Get selected row
    my_previous_marrige_selected = grid_response["selected_rows"]

with candidate_has_been_married_before_col_2:
    # Use selected row as a trigger
    if my_previous_marrige_selected is not None and len(my_previous_marrige_selected) > 0:
        selected_row = my_previous_marrige_selected.iloc[0]
        df_first_prev_marriage = df[df['id'] == selected_row['id']][[
            'my_first_former_spouse_first_name',
            'my_first_former_spouse_last_name',
            'my_first_former_spouse_date_of_marriage',
            'my_first_former_spouse_annulment',
            'my_first_former_spouse_annulment_case_nbr',
            'my_first_former_spouse_annulment_nullity_date',
            'my_first_former_spouse_annulment_petition_'
            ]]
        
        df_first_prev_marriage['Name'] = df_first_prev_marriage['my_first_former_spouse_first_name'] + ' ' + df_first_prev_marriage['my_first_former_spouse_last_name']

        df_first_prev_marriage = df_first_prev_marriage.rename(columns={
            'my_first_former_spouse_date_of_marriage' : 'Marriage_Date',
            'my_first_former_spouse_annulment' : 'Annulment',
            'my_first_former_spouse_annulment_case_nbr' : 'Case_Number',
            'my_first_former_spouse_annulment_nullity_date' : 'Nullity_Date',
            'my_first_former_spouse_annulment_petition_' : 'Petitioned'
        })

        df_first_prev_marriage = df_first_prev_marriage[[
            'Name',
            'Marriage_Date',
            'Petitioned',
            'Annulment',
            'Case_Number',
            'Nullity_Date'
        ]]

        df_second_prev_marriage = df[df['id'] == selected_row['id']][[
            'my_second_former_spouse_first_name',
            'my_second_former_spouse_last_name',
            'my_second_former_spouse_date_of_marriage',
            'my_second_former_spouse_annulment',
            'my_second_former_spouse_annulment_case_nbr',
            'my_second_former_spouse_annulment_nullity_date',
            'my_second_former_spouse_annulment_petition_'
            ]]
        
        df_second_prev_marriage['Name'] = df_second_prev_marriage['my_second_former_spouse_first_name'] + ' ' + df_second_prev_marriage['my_second_former_spouse_last_name']

        df_second_prev_marriage = df_second_prev_marriage.rename(columns={
            'my_second_former_spouse_date_of_marriage' : 'Marriage_Date',
            'my_second_former_spouse_annulment' : 'Annulment',
            'my_second_former_spouse_annulment_case_nbr' : 'Case_Number',
            'my_second_former_spouse_annulment_nullity_date' : 'Nullity_Date',
            'my_second_former_spouse_annulment_petition_' : 'Petitioned'
        })

        df_second_prev_marriage = df_second_prev_marriage[[
            'Name',
            'Marriage_Date',
            'Petitioned',
            'Annulment',
            'Case_Number',
            'Nullity_Date'
        ]]

        df_third_prev_marriage = df[df['id'] == selected_row['id']][[
            'my_third_former_spouse_first_name',
            'my_third_former_spouse_last_name',
            'my_third_former_spouse_date_of_marriage',
            'my_third_former_spouse_annulment',
            'my_third_former_spouse_annulment_case_nbr',
            'my_third_former_spouse_annulment_nullity_date',
            'my_third_former_spouse_annulment_petition_'
            ]]
        
        df_third_prev_marriage['Name'] = df_third_prev_marriage['my_third_former_spouse_first_name'] + ' ' + df_third_prev_marriage['my_third_former_spouse_last_name']

        df_third_prev_marriage = df_third_prev_marriage.rename(columns={
            'my_third_former_spouse_date_of_marriage' : 'Marriage_Date',
            'my_third_former_spouse_annulment' : 'Annulment',
            'my_third_former_spouse_annulment_case_nbr' : 'Case_Number',
            'my_third_former_spouse_annulment_nullity_date' : 'Nullity_Date',
            'my_third_former_spouse_annulment_petition_' : 'Petitioned'
        })

        df_third_prev_marriage = df_third_prev_marriage[[
            'Name',
            'Marriage_Date',
            'Petitioned',
            'Annulment',
            'Case_Number',
            'Nullity_Date'
        ]]

        df_first_prev_marriage = pd.concat([df_first_prev_marriage, df_second_prev_marriage, df_third_prev_marriage], ignore_index=True)

        df_first_prev_marriage = df_first_prev_marriage.replace({'None': None})

        df_first_prev_marriage = df_first_prev_marriage.dropna(how="all")

        st.write(df_first_prev_marriage)
    else:
        st.write("<----------------- Click candidate to see details")

st.markdown(
    """
    <h1 style='text-align: center; font-family: "Helvetica", sans-serif; font-size: 32px;'>
        Candidate Significant Other has been married before
    </h1>
    """,
    unsafe_allow_html=True
)
candidate_so_been_married_before_col_1, candidate_so_been_married_before_col_2 = st.columns([1, 2])
with candidate_so_been_married_before_col_1:
    df_so_previous_marriage = df[(df['fiance_fiance_previous_mariage'] == 'My fiancé(e) has been married before ') | (df['spouse_spouses_previous_marriage_status'] == 'My spouse has been married before')][['id', 'first_name', 'last_name', 'marriage_status', 'spouse_name', 'fiance_name']]
    df_so_previous_marriage['Name'] = df_so_previous_marriage['first_name'] + ' ' + df_so_previous_marriage['last_name']
    df_so_previous_marriage['SO_Name'] = np.where(~df_so_previous_marriage['spouse_name'].isna(), df_so_previous_marriage['spouse_name'], df_so_previous_marriage['fiance_name'])
    df_so_previous_marriage['SO_Name'] = df_so_previous_marriage['SO_Name'].str.strip()

    df_so_previous_marriage = df_so_previous_marriage.rename(columns={
        'marriage_status': 'Current Marriage Status'
    })

    df_so_previous_marriage = df_so_previous_marriage[['id', 'Name', 'Current Marriage Status', 'SO_Name']]

    # Set up AgGrid with row selection
    gb = GridOptionsBuilder.from_dataframe(df_so_previous_marriage)
    gb.configure_selection("single")  # 'multiple' for multi-row selection
    gb.configure_column("id", hide=True) # Hide ID column, but still allows the data to be stored
    grid_options = gb.build()

    # Display interactive grid
    grid_response = AgGrid(
        df_so_previous_marriage,
        gridOptions=grid_options,
        update_mode=GridUpdateMode.SELECTION_CHANGED,
        height=200,
        width='100%',
        fit_columns_on_grid_load=True
    )

    # Get selected row
    my_previous_marrige_selected = grid_response["selected_rows"]

with candidate_so_been_married_before_col_2:
    # Use selected row as a trigger
    if my_previous_marrige_selected is not None and len(my_previous_marrige_selected) > 0:
        selected_row = my_previous_marrige_selected.iloc[0]
        df_so_first_prev_marriage = df[df['id'] == selected_row['id']][[
            'so_first_former_spouse_first_name',
            'so_first_former_spouse_last_name',
            'so_first_former_spouse_date_of_marriage',
            'so_first_former_spouse_annulment',
            'so_first_former_spouse_annulment_case_nbr',
            'so_first_former_spouse_annulment_nullity_date',
            'so_first_former_spouse_annulment_petition_'
            ]]
        
        df_so_first_prev_marriage['Name'] = df_so_first_prev_marriage['so_first_former_spouse_first_name'] + ' ' + df_so_first_prev_marriage['so_first_former_spouse_last_name']

        df_so_first_prev_marriage = df_so_first_prev_marriage.rename(columns={
            'so_first_former_spouse_date_of_marriage' : 'Marriage_Date',
            'so_first_former_spouse_annulment' : 'Annulment',
            'so_first_former_spouse_annulment_case_nbr' : 'Case_Number',
            'so_first_former_spouse_annulment_nullity_date' : 'Nullity_Date',
            'so_first_former_spouse_annulment_petition_' : 'Petitioned'
        })

        df_so_first_prev_marriage = df_so_first_prev_marriage[[
            'Name',
            'Marriage_Date',
            'Petitioned',
            'Annulment',
            'Case_Number',
            'Nullity_Date'
        ]]

        df_so_second_prev_marriage = df[df['id'] == selected_row['id']][[
            'so_second_former_spouse_first_name',
            'so_second_former_spouse_last_name',
            'so_second_former_spouse_date_of_marriage',
            'so_second_former_spouse_annulment',
            'so_second_former_spouse_annulment_case_nbr',
            'so_second_former_spouse_annulment_nullity_date',
            'so_second_former_spouse_annulment_petition_'
            ]]
        
        df_so_second_prev_marriage['Name'] = df_so_second_prev_marriage['so_second_former_spouse_first_name'] + ' ' + df_so_second_prev_marriage['so_second_former_spouse_last_name']

        df_so_second_prev_marriage = df_so_second_prev_marriage.rename(columns={
            'so_second_former_spouse_date_of_marriage' : 'Marriage_Date',
            'so_second_former_spouse_annulment' : 'Annulment',
            'so_second_former_spouse_annulment_case_nbr' : 'Case_Number',
            'so_second_former_spouse_annulment_nullity_date' : 'Nullity_Date',
            'so_second_former_spouse_annulment_petition_' : 'Petitioned'
        })

        df_so_second_prev_marriage = df_so_second_prev_marriage[[
            'Name',
            'Marriage_Date',
            'Petitioned',
            'Annulment',
            'Case_Number',
            'Nullity_Date'
        ]]

        df_so_third_prev_marriage = df[df['id'] == selected_row['id']][[
            'so_third_former_spouse_first_name',
            'so_third_former_spouse_last_name',
            'so_third_former_spouse_date_of_marriage',
            'so_third_former_spouse_annulment',
            'so_third_former_spouse_annulment_case_nbr',
            'so_third_former_spouse_annulment_nullity_date',
            'so_third_former_spouse_annulment_petition_'
            ]]
        
        df_so_third_prev_marriage['Name'] = df_so_third_prev_marriage['so_third_former_spouse_first_name'] + ' ' + df_so_third_prev_marriage['so_third_former_spouse_last_name']

        df_so_third_prev_marriage = df_so_third_prev_marriage.rename(columns={
            'so_third_former_spouse_date_of_marriage' : 'Marriage_Date',
            'so_third_former_spouse_annulment' : 'Annulment',
            'so_third_former_spouse_annulment_case_nbr' : 'Case_Number',
            'so_third_former_spouse_annulment_nullity_date' : 'Nullity_Date',
            'so_third_former_spouse_annulment_petition_' : 'Petitioned'
        })

        df_so_third_prev_marriage = df_so_third_prev_marriage[[
            'Name',
            'Marriage_Date',
            'Petitioned',
            'Annulment',
            'Case_Number',
            'Nullity_Date'
        ]]

        df_first_prev_marriage = pd.concat([df_so_first_prev_marriage, df_so_second_prev_marriage, df_so_third_prev_marriage], ignore_index=True)

        df_first_prev_marriage = df_first_prev_marriage.replace({'None': None})

        df_first_prev_marriage = df_first_prev_marriage.dropna(how="all")

        st.write(df_first_prev_marriage)
    else:
        st.write("<----------------- Click candidate to see details")

#st.markdown(
#    """
#    <h1 style='text-align: left; font-family: "Helvetica", sans-serif; font-size: 18px;'>
#        Married to a Catholic, but not married in the Church
#    </h1>
#    """,
#    unsafe_allow_html=True
#)

remarried_updates_col, baptism_cert_col = st.columns(2)
#Candidates who are married to a Catholic but not married in the Church
with remarried_updates_col:
    center_cols = st.columns(1)
    with center_cols[0]:
        st.markdown(
        """
        <h1 style='text-align: center; font-family: "Helvetica", sans-serif; font-size: 18px;, layout="wide"'>
            Married a Catholic, but not in the Church
        </h1>
        """,
        unsafe_allow_html=True
        )
    df_catholic_non_church_marriage = df[
        (df['spouse_baptised_catholic'].str.upper() == 'TRUE') & 
        (df['spouse_witnessed_by_ordination'].str.upper() == 'NO') & 
        (df['spouse_dispensation_for_ordination'].str.upper() == 'NO') & 
        (df['so_baptised_catholic_needs_church_wedding_resolved'] == False)
        ][['id', 'so_baptised_catholic_needs_church_wedding_resolved', 'first_name', 'last_name']]
    
    df_catholic_non_church_marriage['Name'] = df_catholic_non_church_marriage['first_name'] + ' ' + df_catholic_non_church_marriage['last_name']

    gb = GridOptionsBuilder.from_dataframe(df_catholic_non_church_marriage)

    df_catholic_non_church_marriage = df_catholic_non_church_marriage.rename(columns={'so_baptised_catholic_needs_church_wedding_resolved': 'Wedding_Resolved'})
    df_catholic_non_church_marriage = df_catholic_non_church_marriage[['id', 'Wedding_Resolved', 'first_name', 'last_name', 'Name']]

    gb.configure_column("Wedding_Resolved", editable=True, cellEditor="agCheckboxCellEditor")
    gb.configure_selection("multiple", use_checkbox=True)  # Use checkboxes for multi-select

    gb.configure_column("id", hide=True) # Hide ID column, but still allows the data to be stored
    gb.configure_column("so_baptised_catholic_needs_church_wedding_resolved", hide=True) # Hide ID column, but still allows the data to be stored
    gb.configure_column("first_name", hide=True) # Hide ID column, but still allows the data to be stored
    gb.configure_column("last_name", hide=True) # Hide ID column, but still allows the data to be stored

    # All other columns are implicitly non-editable unless specified
    grid_options = gb.build()

    # Display grid
    remarried_grid_response = AgGrid(
        df_catholic_non_church_marriage,
        gridOptions=grid_options,
        update_mode=GridUpdateMode.VALUE_CHANGED,
        height=200,
        fit_columns_on_grid_load=True
    )

    updated_remarried_df = pd.DataFrame(remarried_grid_response["data"])
    selected_remarried = updated_remarried_df[updated_remarried_df["Wedding_Resolved"] == True]

    update_list = selected_remarried['id'].tolist()

    remarried_submit_button = st.button("Update Remarried Records")

    if remarried_submit_button:
        # Define what to update
        update_data = {"so_baptised_catholic_needs_church_wedding_resolved": True}

        remarried_response = supabase.table("Candidates").update(update_data).in_("id", update_list).execute()
        st.success("Records updated successfully!")
        st.rerun()

#Candidates who are not baptised
with baptism_cert_col:
    center_cols = st.columns(1)
    with center_cols[0]:
        st.markdown(
        """
        <h1 style='text-align: center; font-family: "Helvetica", sans-serif; font-size: 18px;, layout="wide"'>
            Outstanding Baptism Certificates
        </h1>
        """,
        unsafe_allow_html=True
        )
    
    df_outstanding_baptism_certs = df[
        (df['baptism_status'].str.upper() == 'NO') & 
        (df['received_baptism_cert'] == False)
        ][['id', 'received_baptism_cert', 'first_name', 'last_name']]
    
    df_outstanding_baptism_certs['Name'] = df_outstanding_baptism_certs['first_name'] + ' ' + df_outstanding_baptism_certs['last_name']

    gb = GridOptionsBuilder.from_dataframe(df_outstanding_baptism_certs)

    df_outstanding_baptism_certs = df_outstanding_baptism_certs.rename(columns={'received_baptism_cert': 'Received_Baptism_Cert'})
    df_outstanding_baptism_certs = df_outstanding_baptism_certs[['id', 'Received_Baptism_Cert', 'first_name', 'last_name', 'Name']]

    gb.configure_column("Received_Baptism_Cert", editable=True, cellEditor="agCheckboxCellEditor")
    gb.configure_selection("multiple", use_checkbox=True)  # Use checkboxes for multi-select

    gb.configure_column("id", hide=True) # Hide ID column, but still allows the data to be stored
    gb.configure_column("received_baptism_cert", hide=True) # Hide ID column, but still allows the data to be stored
    gb.configure_column("first_name", hide=True) # Hide ID column, but still allows the data to be stored
    gb.configure_column("last_name", hide=True) # Hide ID column, but still allows the data to be stored

    # All other columns are implicitly non-editable unless specified
    grid_options = gb.build()

    # Display grid
    baptism_cert_grid_response = AgGrid(
        df_outstanding_baptism_certs,
        gridOptions=grid_options,
        update_mode=GridUpdateMode.VALUE_CHANGED,
        height=200,
        fit_columns_on_grid_load=True
    )

    updated_baptism_cert_df = pd.DataFrame(baptism_cert_grid_response["data"])
    selected_baptism_cert = updated_baptism_cert_df[updated_baptism_cert_df["Received_Baptism_Cert"] == True]

    update_list = selected_baptism_cert['id'].tolist()

    remarried_submit_button = st.button("Update Baptism Records")

    if remarried_submit_button:
        # Define what to update
        update_data = {"received_baptism_cert": True}

        remarried_response = supabase.table("Candidates").update(update_data).in_("id", update_list).execute()
        st.success("Records updated successfully!")
        st.rerun()

unbaptised_col, engaged_col = st.columns(2)
with unbaptised_col:
    center_cols = st.columns(1)
    with center_cols[0]:
        st.markdown(
        """
        <h1 style='text-align: center; font-family: "Helvetica", sans-serif; font-size: 18px;, layout="wide"'>
            Unbaptised Candidates
        </h1>
        """,
        unsafe_allow_html=True
        )
    unbaptised_df = df[df['baptism_status'].str.upper().isin(['NO', 'I AM NOT SURE'])][['first_name', 'last_name', 'baptism_status']]
    st.write(unbaptised_df)

with engaged_col:
    center_cols = st.columns(1)
    with center_cols[0]:
        st.markdown(
        """
        <h1 style='text-align: center; font-family: "Helvetica", sans-serif; font-size: 18px;, layout="wide"'>
            Engaged Candidates
        </h1>
        """,
        unsafe_allow_html=True
        )
    engaged_df = df[df['marriage_status'] == 'Engaged'][['first_name', 'last_name', 'fiance_name']]
    st.write(engaged_df)