from bs4 import BeautifulSoup
import requests
import time
import random
import json

# persons_url_list = []
#
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
# }
#
# for i in range(0, 749, 12):
#     url = f'https://www.bundestag.de/ajax/filterlist/en/members/863330-863330?limit=12&noFilterSet=true&offset={i}'
#
#     q = requests.get(url, headers=headers)
#     result = q.content
#
#     soup = BeautifulSoup(result, 'lxml')
#     persons = soup.find_all('a')
#
#     for person in persons:
#         person_page_url = person.get('href')
#         persons_url_list.append(person_page_url)
#
#     with open('persons_url_list.txt', 'a', encoding='utf-8') as file:
#         for line in persons_url_list:
#             file.write(f'{line}\n')
#     time.sleep(random.randrange(1, 2))

with open('persons_url_list.txt') as file:

    lines = [line.strip() for line in file.readlines()]

    data_dict = []

    count = 0

    for line in lines:
        q = requests.get(line)
        result = q.content        # CONTENT - это весь код html, доступный по ссылке
        soup = BeautifulSoup(result, 'lxml')

        person = soup.find(class_='col-xs-8').find('h3').text
        person_name_company = person.strip().split(',')
        name = person_name_company[0]
        party = person_name_company[1].strip()

        social_networks = soup.find_all(class_='bt-link-extern')

        social_networks_urls = []
        social_networks_name = []

        for item in social_networks:
            social_networks_urls.append(item.get('href'))


        data = {
            'persons_name': name,
            'persons_party': party,
            'social_networks': social_networks_urls

        }
        count += 1

        print(f'Член парламента №{count} записан...')

        data_dict.append(data)

        with open('all_members', 'w', encoding='utf-8') as json_file:
            json.dump(data_dict, json_file, indent=4)



