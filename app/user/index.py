from app.user.user_first_name_query import userFirstName


def get_user_first_name():
    result = userFirstName.execute()
    if result.data is not None:
        return result.data.me.firstName
    return None
