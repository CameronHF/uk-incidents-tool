import logging
import pandas as pd
from retry import retry


def read_sql_file(path_to_file: str) -> str:
    """
    Loading an SQL query from a file

    :param path_to_file: str, path to the file
    :return: str, SQL query as string
    """

    try:
        return open(path_to_file).read()
    except FileNotFoundError:
        logging.debug(f'FileNotFoundError: No such sql file {path_to_file}')
        raise FileNotFoundError(f'No such sql file {path_to_file}')


def prepare_sql_template(sql_template: str, test_parameters: dict) -> str:
    """
    Preparing SQL query containing parameters

    :param sql_template: str, SQL query
    :param test_parameters: dict, parameters to be parsed
    :return: str, query with parsed parameters
    """

    query = sql_template.format(**test_parameters).strip()

    return query


def run_query(query: str, limit: int = None, conn=None, **kwargs) -> pd.DataFrame:
    """
    Run a query with query and return the result as a pandas.DataFrame

    :param query: the query as a string.
    :param limit: add a limit parameter to the query.
    :param conn: the connection to be used.
    :param kwargs: a dictionary to attach any additional parameters to pd.read_sql (for example: parameters)
    :return a pd.DataFrame with the result of the query.
    """

    if conn is None:
        logging.debug('Exception: database connection is not established')
        raise Exception('database connection is not established')

    if limit:
        query += f' LIMIT {limit}'

    if kwargs:
        return pd.read_sql(query, conn, **kwargs)
    else:
        return pd.read_sql(query, conn)


@retry(tries=10)
def get_df_from_query(query_path: str, limit: int = None, conn=None, **kwargs) -> pd.DataFrame:
    """
    Run a query from an SQL file specified by query_path and return the result as a pandas.DataFrame

    :param query_path: the path to the SQL file containing the query
    :param limit: add a limit parameter to the query.
    :param conn: the connection to be used.
    :param kwargs: a dictionary to attach any additional parameters to pd.read_sql (for example: parameters)
    :return a pd.DataFrame with the result of the query.
    """

    query = read_sql_file(query_path)

    return run_query(query, limit=limit, conn=conn)