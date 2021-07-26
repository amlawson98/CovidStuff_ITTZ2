"""Defines all the functions related to the database"""
from app import db

def fetch_StateSafetyIndex() -> dict:
    """Reads all states listed in the state table

    Returns:
        A list of dictionaries
    """

    conn = db.connect()
    query_results = conn.execute("Select * from State Order By State_FIPS;").fetchall()
    conn.close()
    StateSafetyIndex_list = []
    for result in query_results:
        item = {
            "State_FIPS": result[0],
            "State_Name": result[1],
            "Safety_Index": result[2]
        }
        StateSafetyIndex_list.append(item)
    # StateSafetyIndex_list = [
    #     {
    #         "State_FIPS": "22",
    #         "State_Name": "AA",
    #         "Safety_Index": 33.0
    #     },
    #     {
    #         "State_FIPS": "33",
    #         "State_Name": "BB",
    #         "Safety_Index": 44.0
    #     }
    # ]

    return StateSafetyIndex_list

def Generic_Select(sqlselect_code_string) -> dict:
    """Runs a select command and returns the result

    Returns:
        A list of dictionaries
    """

    conn = db.connect()
    query_results = conn.execute(sqlselect_code_string).fetchall()
    conn.close()
    return query_results

# def update_statename_entry(State_FIPS: str, State_Name: str) -> None:
#     """Updates state name based on given `State_FIPS`

#     Args:
#         State_FIPS (str): State FIPS
#         State_Name (str): State Name

#     Returns:
#         None
#     """

#     conn = db.connect()
#     query = 'Update State set State_Name = "{}" where State_FIPS = {};'.format(State_Name, State_FIPS)
#     conn.execute(query)
#     conn.close()


def update_safetyindex_entry(State_FIPS: str, Safety_Index: float) -> None:
    """Updates safty index based on given `State_FIPS`

    Args:
        State_FIPS (str): Targeted State FIPS
        Safety_Index (float): Updated safety index

    Returns:
        None
    """

    conn = db.connect()
    query = 'Update State set Safety_Index = "{}" where State_FIPS = {};'.format(Safety_Index, State_FIPS)
    conn.execute(query)
    conn.close()


def insert_new_state(text: str) ->  str:
    """Insert new state to state table.

    Args:
        text (str): state name

    Returns: The task ID for the inserted entry
    """

    conn = db.connect()
    query = 'Insert Into State (State_Name, Safety_Index) VALUES ("{}", "{}");'.format(
        text, 0.0)
    conn.execute(query)
    query_results = conn.execute("Select LAST_INSERT_ID();")
    query_results = [x for x in query_results]
    State_FIPS = str(query_results[0][0])
    conn.close()

    return State_FIPS


def remove_state_by_fips(State_FIPS: str) -> None:
    """ remove entries based on State_FIPS """
    conn = db.connect()
    query = 'Delete From State where State_FIPS={};'.format(State_FIPS)
    conn.execute(query)
    conn.close()
