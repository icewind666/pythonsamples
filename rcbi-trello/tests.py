import os
import json
from trello import TrelloClient
from trello.trellolist import List
from rocketchat import RocketChatClient
from telegrambot import TelegramBot

# ======== CONSTANTS =============================
STATE_FILE = 'state.json'
ROCKETCHAT_URL = 'https://chat.rcbi.company/'
ROCKETCHAT_USERNAME = 'trello_bot'
ROCKETCHAT_PASSWORD = 'trellobot2017'
# Current sprint's board id
SPRINT_BOARD_ID = '57e8fca727f213bf96619288'
# predefined id keys of SCRUM lists
TODO_LIST_ID = '57e8fcbefab90979abcf459b'
INPROGRESS_LIST_ID = '57e8fcc3f27f310cdbe6fd83'
DONE_LIST_ID = '57e8fcc77dc35584ace008e5'
TESTED_ON_DEV_LIST_ID = '57e8fcce5f5786f5a65a3f95'

telegrambot = TelegramBot()


# ================================================
# ================================================

def rocket_chat_print_status(done_count, inprogress_count, todo_count):
    """
    Printing stats to trellobot chat room
    :return:
    """
    # getting done percent
    all_cards_count = done_count + inprogress_count + todo_count
    done_percent = (done_count / all_cards_count) * 100

    strings = [
        'Sprint status -> Done: {} card(s). Progress: {} card(s). TODO: {} card(s). '
        'Sprint percent ready: {:05.1f} %'.format(done_count,
                                                  inprogress_count,
                                                  todo_count, done_percent)
    ]

    rclient = RocketChatClient(ROCKETCHAT_URL)
    rclient.login(ROCKETCHAT_USERNAME, ROCKETCHAT_PASSWORD)

    for x in strings:
        rclient.send_room("#trellobot", x)
        telegrambot.echo(x)


def serialize_card(card):
    """
    Serializing Trello card to json format.
    Using only name, id, and member_id
    :return:
    """
    result = {'name': card.name, 'id': card.id, 'member_id': card.member_id}
    return result


def serialize_card_list(card_list):
    """
    Serializing list of Trello cards ro JSON
    :param card_list:
    :return:
    """
    result = []
    for x in card_list:
        result.append(serialize_card(x))
    return result

def save_state_file(done, inprogress, todo):
    """
    Saving state to json file
    :param done:
    :param inprogress:
    :param todo:
    :return:
    """
    with open(STATE_FILE, 'w') as state_file:
        state = dict(done=done, progress=inprogress, todo=todo)
        json.dump(state, state_file)


def states_equals(done_was, done_now):
    pass

"""
MAIN PART GOES BELOW
"""
# Starting trello api client wrapper
client = TrelloClient(
    api_key='7f3198f11e4fb333b00f687914cde2ad',
    token='ebcb4f16f128639a01bbafaddc785fb7816f0aac70f82d402653426b5572f5e4'
)

board = None

for b in client.list_boards():
    if b.id == SPRINT_BOARD_ID:
        board = b

# fetch card from To do list
todo_list_obj = List(board, TODO_LIST_ID)
todo_cards = todo_list_obj.list_cards()

# fetch card from In progress list
inprogress_list_obj = List(board, INPROGRESS_LIST_ID)
inprogress_cards = inprogress_list_obj.list_cards()

# fetch card from Done list
done_list_obj = List(board, DONE_LIST_ID)
done_cards = done_list_obj.list_cards()
total_sprint_cards = len(done_cards) + len(inprogress_cards) + len(todo_cards)
previous_state = None

# Getting saved state.
if os.path.exists(STATE_FILE):
    with open(STATE_FILE) as state_file_obj:
        previous_state = json.load(state_file_obj)

# Comparing states
if previous_state:
    done_cards_was = previous_state['done']
    progress_cards_was = previous_state['progress']
    todo_cards_was = previous_state['todo']

    if not states_equals(done_now=done_list_obj, done_was=done_cards_was):
        save_state_file(done_list_obj, inprogress_list_obj, todo_list_obj)
        rocket_chat_print_status(len(done_cards), len(inprogress_cards), len(todo_cards))

else:
    save_state_file(done_cards, inprogress_cards, todo_cards)
