import requests
import time
import json

def spy_game():  
    TOKEN = '243c61ecee26cb868893bb23b4b101005aa63f63e2ab90db203ebf93c54a3346daebc78e6aa3c73cee32c'
    params = {
        'access_token': TOKEN,
        'order': 'hints',
        'v': '5.52'
    }
    
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
    c = 0
    for i in ids_user_friends:
        c += (1/len(ids_user_friends))*100
        print('Выполнено: ', round(c, 1), '%')
        friends_get_params['user_id'] = i
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
    for i in groups:
        friends_get_params['group_id'] = i
        friends_get_params['extended'] = 1
        friends_get_params['fields'] = 'members_count'    
        response = requests.get('https://api.vk.com/method/groups.getById', params=friends_get_params)
        id_groups = response.json()['response'][0]['id']
        name_groups = response.json()['response'][0]['name']
        member_count_groups = response.json()['response'][0]['members_count']
        file_dict = {'name': name_groups, 'id': id_groups, 'members_count': member_count_groups}
        file_list.append(file_dict)
        time.sleep(pause)

    with open('groups.json', 'w', encoding='UTF-8') as x:
        json.dump(file_list, x, ensure_ascii=False)

if __name__ == "__main__":
    spy_game()