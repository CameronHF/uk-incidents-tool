import logging
import json
import os
import jaydebeapi
from dotenv import load_dotenv


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


# def dwh_connect(database: str):
#     """
#     creates a DWH connection object
#     Parameters
#     -------
#     database: string
#         key under which the required database connection credentials are kept in the file
#     Returns
#     -------
#     dwh_conn : pyodbc connection object
#         the connection object used to execute DWH queries
#     """

#     logging.info('Creating DWH connection')

#     dwh_conf = get_local_configuration(database)
#     print(dwh_conf)
#     dwh_conn = jaydebeapi.connect(jclassname=dwh_conf['jclassname'],
#                               url=dwh_conf['url'],
#                                   driver_args={'UID': dwh_conf['user'], 'PWD': dwh_conf['password']},
#                                  jars=dwh_conf['jar_path'])
#     print(dwh_conn)
    
#     return dwh_conn


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

    logging.info('Creating DWH connection...')

    # dwh_conf = get_local_configuration(database)
    # print(dwh_conf)
    dwh_conn = jaydebeapi.connect(jclassname="com.cloudera.impala.jdbc.DataSource",
                              url="jdbc:impala://coordinator-cdp-cdw-live.dw-aws-bi-live.vaxy-y10l.cloudera.site:443/default;AuthMech=3;transportMode=http;httpPath=cliservice;ssl=1;",
                                  driver_args={'UID': "cameron.jones", 'PWD': "CnJs@1921!"},
                                 jars="app/jars/ImpalaJDBC42.jar")
    print(dwh_conn)


    return dwh_conn

