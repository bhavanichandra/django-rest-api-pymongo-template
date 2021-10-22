def get_query_param_value(query_param, key):
    """
    Get query param based on provided key
    :param query_param: Query params from request
    :param key: query param key
    :return: query param value
    """
    query_param_dict = dict(query_param)
    return query_param_dict.get(key)
