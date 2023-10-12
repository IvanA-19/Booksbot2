import json


data = json.load(open('config.json'))

api_token = data['api_token']
main_menu_buttons = data['main_menu_buttons']
novels = data['novels']
contacts = data['contacts']
info = data['info']
helpList = data['helpList']
hello = data['hello']

novels_callback_id = [str(i) for i in range(len(novels))]
about_callback_id = [f'about {str(i)}' for i in range(len(novels_callback_id))]
characters_callback_id = [f'characters {str(i)}' for i in range(len(novels_callback_id))]
