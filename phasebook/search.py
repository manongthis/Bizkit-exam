from flask import Blueprint, request

from .data.search_data import USERS


bp = Blueprint("search", __name__, url_prefix="/search")


@bp.route("")
def search():
    return search_users(request.args.to_dict()), 200


def search_users(args):
    """Search users database

    Parameters:
        args: a dictionary containing the following search parameters:
            id: string
            name: string
            age: string
            occupation: string

    Returns:
        a list of users that match the search parameters
    """
    id = args.get('id')
    name = args.get('name')
    age = args.get('age')
    occupation = args.get('occupation')
    print(id, name, age, occupation)
    search_result = set()

    if id:
        for user in USERS:
            if user['id'] == id:
                search_result.add(tuple(user.items()))
                break
    if name:
        for user in USERS:
            if name.lower() in user['name'].lower():
                search_result.add(tuple(user.items()))
    if age:
        for user in USERS:
            user_age = int(user['age'])
            age = int(age)
            if age - 1 <= user_age <= age + 1:
                search_result.add(tuple(user.items()))

    if occupation:
        for user in USERS:
            if occupation.lower() in user['occupation'].lower():
                search_result.add(tuple(user.items()))

    new_search_result = [dict(user) for user in search_result]

    def sort_by_priority(user):
        id_match = 1 if id and user['id'] == id else 0
        name_match = 1 if name and name.lower() in user['name'].lower() else 0
        age_match = 1 if age and age - 1 <= int(user['age']) <= age + 1 else 0
        occupation_match = 1 if occupation and occupation.lower(
        ) in user['occupation'].lower() else 0

        priority_score = (id_match * 4) + (name_match * 3) + \
            (age_match * 2) + (occupation_match * 1)
        print(priority_score)

        return priority_score

    new_search_result.sort(key=sort_by_priority, reverse=True)

    # Implement search here!
    return new_search_result
    # return search_result
