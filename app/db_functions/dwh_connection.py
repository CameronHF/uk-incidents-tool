import logging
import json
import os
import jaydebeapi
from dotenv import load_dotenv
import streamlit as st


def get_local_configuration(database: str):
    """
    get credentials to connect to DWH
    Parameters
    ----------
    database : string
        key under which the required database connection credentials are kept in the file
    Returns
    -------
    json_conf : dictionary
        dictionary of credentials for selected database key
    """

    load_dotenv()

    try:
        with open(os.getenv('CREDENTIALS')) as cred_file:
            json_conf = json.load(cred_file)
    except TypeError:
        logging.debug('TypeError: Unable to load credentials')
        raise TypeError('Unable to load credentials')

    return json_conf[database]


def dwh_connect(database: str):
    """
    creates a DWH connection object
    Parameters
    -------
    database: string
        key under which the required database connection credentials are kept in the file
    Returns
    -------
    dwh_conn : pyodbc connection object
        the connection object used to execute DWH queries
    """

    # logging.info('Creating DWH connection')

    # dwh_conf = get_local_configuration(database)
    dwh_conn = jaydebeapi.connect(jclassname=st.secrets['DWH-CDP-JCLASSNAME'],
                              url=st.secrets['DWH-CDP-URL'],
                                  driver_args={'UID': st.secrets['DWH-CDP-USER'], 'PWD': st.secrets['DWH-CDP-PASSWORD']},
                                 jars=st.secrets['DWH-CDP-JARPATH'])
    return dwh_conn
