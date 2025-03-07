import json


def create_user(filename, user_name, user_designation):
    with open(filename, 'r+') as file:
        data = json.load(file)
        new_user_id = str(max(map(int, data.keys())) + 1)
        data[new_user_id] = {
            "user_name": user_name,
            "user_designation": user_designation
        }
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()
    print(f"User ID: {new_user_id}, User Name: {user_name}, User Designation: {user_designation} - Successfully created.")

def update_user(filename, user_id, user_name, user_designation):
    with open(filename, 'r+') as file:
        data = json.load(file)
        user_id_str = str(user_id)
        if user_id_str in data:
            data[user_id_str]['user_name'] = user_name
            data[user_id_str]['user_designation'] = user_designation
        else:
            data[user_id_str] = {
                "user_name": user_name,
                "user_designation": user_designation
            }
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()
    print(f"User with user_id {user_id} updated successfully in '{filename}'.")

def delete_user(filename, user_id):
    with open(filename, 'r+') as file:
        data = json.load(file)
        user_id_str = str(user_id)
        if user_id_str in data:
            del data[user_id_str]
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()
    print(f"User with user_id {user_id} deleted successfully from '{filename}'.")


filename = 'users.json'

#create_user(filename, user_name= "Jane black", user_designation= "Senior manager") 
update_user(filename, user_id = 4, user_name= "Jane white", user_designation= "Senior Developer")
#delete_user(filename, 3)
