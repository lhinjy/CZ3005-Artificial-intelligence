import hug
from pyswip import Prolog
import random

prolog = Prolog()
prolog.consult('subway.pl')

main_counter = 0
item_counter = 0


@hug.get('/', output=hug.output_format.html)
def root():
    with open('index.html', 'r', encoding='utf-8') as HTMLFile:
        return HTMLFile.read()


def next_step(item_title):
    return (
        "Alright! {} has been taken note of. \nPlease tell us 'Next' when you are ready for the next step"
        .format(item_title))


def error_input():
    return "Sorry. I don not understand.\n Please reply with 'yes', 'no', or 'next'"


def global_counter():
    global main_counter
    main_counter = main_counter + 1


def second_counter():
    global item_counter
    item_counter = item_counter + 1


def reset_second():
    global item_counter
    item_counter = 0


def order_set(msg, item_title):
    item_list = list(prolog.query('ask_{}s(X)'.format(item_title)))

    try:
        item = item_list[item_counter]['X']
    except:
        global_counter()
        reset_second()
        prolog.assertz('{}_chosen(null)'.format(item_title))
        return (
            "no {} is available/chosen. \nPlease tell us 'Next' when you are ready for the next step"
            .format(item_title))

    new_item = item.replace('_', ' ')
    if (msg == 'n' or msg == 'no'):
        second_counter()
        return new_item

    elif (msg == 'yes'):
        item = item_list[item_counter - 1]['X']
        prolog.assertz('{}_chosen({})'.format(item_title, item))
        global_counter()
        reset_second()
        item = ''
        return next_step(item_title)

    else:
        return error_input()


@hug.get()
def get(msg: hug.types.text):
    if (main_counter == 0):  #if subway
        if (msg == 'yes'):  #yes to subway #ask for first meal
            global_counter()
            return next_step('order')
        else:
            return error_input()

    elif (main_counter == 1):  #ask for meal
        return order_set(msg, 'meal')
    # return list(prolog.query('meal_chosen(X)'))[0]['X']

    elif (main_counter == 2):  #ask for bread
        # return list(prolog.query('meal_chosen(X)'))[0]['X']
        return order_set(msg, 'bread')
    #meal
    elif (main_counter == 3):  #ask for meat
        return order_set(msg, 'meat')
    #veggie
    elif (main_counter == 4):
        return order_set(msg, 'veggie')

    #sauce
    elif (main_counter == 5):
        return order_set(msg, 'sauce')

    #top ups
    elif (main_counter == 6):
        return order_set(msg, 'topup')

    #side
    elif (main_counter == 7):
        return order_set(msg, 'side')

    elif (main_counter == 8):
        return (
            'meal chosen = {}\n bread chosen = {}\nmeat chosen = {}\nveggie chosen = {}\nsauce chosen = {}\n top up chosen = {} \n side chosen = {}\n Thank you and have a nice day \n Restart the server for a new order'
            .format(
                list(prolog.query('meal_chosen(X)'))[0]['X'],
                list(prolog.query('bread_chosen(X)'))[0]['X'],
                list(prolog.query('meat_chosen(X)'))[0]['X'],
                list(prolog.query('veggie_chosen(X)'))[0]['X'],
                list(prolog.query('sauce_chosen(X)'))[0]['X'],
                list(prolog.query('topup_chosen(X)'))[0]['X'],
                list(prolog.query('side_chosen(X)'))[0]['X']))
