import requests
import time
import json

TOKEN = '9ce54ca40727eee8ec3ddf39a1cc3d66abbcdfcd7734d9697aa169c2f98c665de4d48ae0453fa3dfb2264'
params = {
        'access_token': TOKEN,
        'order': 'hints',
        'v': '5.52'
        }

def spy_game():  
    
    friends_get_params = params.copy()
    friends_get_params['user_id'] = 171691064
    response = requests.get('https://api.vk.com/method/users.get', params=friends_get_params)
    print('Пользователь: ', response.json()['response'][0]['first_name'],  response.json()['response'][0]['last_name'])

    response = requests.get('https://api.vk.com/method/friends.get', params=friends_get_params)
    ids_user_friends = response.json()['response']['items']

    response = requests.get('https://api.vk.com/method/groups.get', params=friends_get_params)
    groups_user = response.json()['response']['items']

    pause = 0.34
    group_list = []
    progress_complete = 0

    for id_friend in ids_user_friends:
        
        progress_complete += (1/len(ids_user_friends))*100
        print('Выполнено: ', round(progress_complete, 1), '%')

        friends_get_params['user_id'] = id_friend
        response = requests.get('https://api.vk.com/method/users.get', params=friends_get_params)
        try:
            response = requests.get('https://api.vk.com/method/groups.get', params=friends_get_params)
            groups_user_friend = response.json()['response']['items']
        except KeyError:
            pass
        group_list += groups_user_friend
        time.sleep(pause)

    groups = set(groups_user).difference(set(group_list))

    file_list = []
    friends_get_params['extended'] = 1
    friends_get_params['fields'] = 'members_count'

    for id_group in groups:
        friends_get_params['group_id'] = id_group  
        response = requests.get('https://api.vk.com/method/groups.getById', params=friends_get_params)
        id_groups = response.json()['response'][0]['id']
        name_groups = response.json()['response'][0]['name']
        member_count_groups = response.json()['response'][0]['members_count']
        file_dict = {'name': name_groups, 'id': id_groups, 'members_count': member_count_groups}
        file_list.append(file_dict)
        time.sleep(pause)

    with open('groups.json', 'w', encoding='UTF-8') as file:
        json.dump(file_list, file, ensure_ascii=False)

if __name__ == "__main__":
    spy_game()