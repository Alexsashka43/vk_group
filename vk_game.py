import requests
import time
import json



def оutput_data(od):
    output_dict = {}
    output_dict['name'] = od['name']
    output_dict['gid'] = od['id']
    output_dict['members_count'] = od['members_count']
    return output_dict

def friend_in_my_groups(id):

    params = {
        'group_id': str(id),
        'access_token': Token,
        'v' : 5.89,
        'filter': 'friends'
    }
    return params


class Groups_without_friends:
    def __init__(self,user_id,token):
        self.user_id = user_id
        self.v = 5.89
        self.token = token

    def get_groups(self):
        params = {
            'user_id': self.user_id,
            'access_token': self.token,
            'extended': 1,
            'fields': 'id,name,members_count',
            'v': self.v,
        }
        response = requests.get('https://api.vk.com/method/groups.get',params)

        answer_get = response.json()['response']
        counter = 0
        data_list1 = []

        for i in answer_get['items']:
            data_list1.append(оutput_data(i))
            counter += 1
        self.data_list1 = data_list1
        self.counter = counter
        return data_list1

    def get_Members(self):

        data_list = []

        for ind in self.data_list1:

            i = (requests.get('https://api.vk.com/method/groups.getMembers', friend_in_my_groups(ind['gid'])))

            if self.counter != 1:
                print(f'До конца анализа осталось  {self.counter - 1} групп ')
                self.counter -= 1
            else:
                print('Проверьте результат')

            time.sleep(0.4)

            count_friends_in_groups = i.json()['response']['count']

            if count_friends_in_groups == 0:
                data_list.append(ind['gid'])

        return data_list

    def get_groups_without_friends(self,data_list1,data_list):
        data_list2 = []

        for id_without_friends in data_list:
            for i in data_list1:
                if i['gid'] == id_without_friends:
                    data_list2.append(i)
                    break

        return data_list2

Token = 'e8a677cf963590ae4fce6e2d23e0ee33c04ba5a9280120ad940ca05f5ad60c0d4fbfb46f4318ccb740753'

id = input('введите id пользователя:') #344671718
only_user = Groups_without_friends(id,Token)
data_list = only_user.get_Members()
data_list1 = only_user.get_groups()



with open('groups.json', 'w', encoding='utf-8') as file:
    json.dump(only_user.get_groups_without_friends(data_list1,data_list), file, ensure_ascii=False, indent=2)