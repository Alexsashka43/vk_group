import time
import json
import requests


def output_data(information):
    output_dict = {}
    output_dict['name'] = information['name']
    output_dict['gid'] = information['id']
    output_dict['members_count'] = information['members_count']
    return output_dict


def get_friend_in_groups(id):
    params = {
        'group_id': str(id),
        'access_token': Token,
        'v': '5.89',
        'filter': 'friends'  # будут возвращены только друзья в этом сообществе.
    }
    return params


class Groups_Without_Friends:
    def __init__(self, user_id, token):
        self.user_id = user_id
        self.v = '5.89'
        self.token = token


    def get_groups(self): #получить список групп
        params = {
            'user_id': self.user_id,
            'access_token': self.token,
            'extended': 1,
            'fields': 'id,name,members_count',
            'v': self.v,
        }
        response = requests.get('https://api.vk.com/method/groups.get', params)

        answer_get = response.json()['response']
        counter = 0
        groups_list = []

        for i in answer_get['items']:
            groups_list.append(output_data(i))
            counter += 1
            return groups_list


        def get_members(self): #Получить количество человек в моих группах
            member_list = []
            counter = 0
            for member in groups_list:
                try:
                    member = (requests.get('https://api.vk.com/method/groups.getMembers', get_friend_in_groups(member['group_id'])))
                except Exception as e:
                    print(e)

                member = (requests.get('https://api.vk.com/method/groups.getMembers', get_friend_in_groups(member['group_id'])))

                if counter != 1:
                    print(f'До конца анализа осталось  {counter - 1} групп ')
                    counter -= 1
                else:
                    print('Проверьте результат')

                time.sleep(0.4)

                count_friends_in_groups = member.json()['response']['count']

                if count_friends_in_groups == 0:
                    member_list.append(member['gid'])

                return member_list


            def get_groups_without_friends(self):#найти группы без друзей
                out_friend = []

                for id_out_friends in member_list:
                    for id in groups_list:
                        if id['gid'] == id_out_friends:
                            out_friend.append(id)
                            break

                return out_friend
            return get_groups_without_friends(self)
        return get_members(self)

Token = 'e8a677cf963590ae4fce6e2d23e0ee33c04ba5a9280120ad940ca05f5ad60c0d4fbfb46f4318ccb740753'

id = input('введите id пользователя:')  # 344671718
only_user = Groups_Without_Friends(id, Token)
member_list = only_user.get_members()
groups_list = only_user.get_groups()

with open('groups.json', 'w', encoding='utf-8') as file:
    json.dump(only_user.get_groups_without_friends(), file, ensure_ascii=False)


