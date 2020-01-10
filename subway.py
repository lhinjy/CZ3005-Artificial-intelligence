import hug
from pyswip import Prolog

prolog = Prolog()
prolog.consult('subway.pl')

# Initialize counter
main_counter = 0
item_counter = 0


# Requirement for framework
@hug.get('/', output=hug.output_format.html)
def root():
    with open('index.html', 'r', encoding='utf-8') as HTMLFile:
        return HTMLFile.read()


# Main counter used to keep track of order step( Start -> Meal -> Bread -> Meat -> Veggie -> Sauce -> Topup -> Side)
def global_counter():
    global main_counter
    main_counter = main_counter + 1


# Secondary counter to keep track of the items in one step
def second_counter():
    global item_counter
    item_counter = item_counter + 1


# Reset the secondary counter when each step is done
def reset_second():
    global item_counter
    item_counter = 0

#text
def item_text(item_title, item):
    return ('{} : Do you want {} ?'.format(item_title,item))

# Text
def next_step(item_title):
    return (
        "Alright! {} has been taken note of. \nPlease tell us 'next' when you are ready for the next step"
        .format(item_title))


# Text
def error_input():
    return "Sorry. I don not understand.\n Please reply with 'yes', 'no', or 'next'"


# Per order step
def order_set(msg, item_title):
    # Retrieve prolog item and save all items into a list
    item_list = list(prolog.query('ask_{}s(X)'.format(item_title)))

    try:
        item = item_list[item_counter]['X']

    # List is empty due to the condition of the meal OR User said no to all items in the list OR Unknown error :(
    except:
        global_counter()
        reset_second()
        prolog.assertz('{}_chosen(null)'.format(item_title))
        return (
            "no {} is available/chosen. \nPlease tell us 'Next' when you are ready for the next step"
            .format(item_title))

    # Prolog file doesnt allow the assert(ion) of phrases with space. Replacing the _ for aesthetic purposes(to print out without _)
    new_item = item.replace('_', ' ')

    if (msg == 'next' or msg == 'no'):
        second_counter()
        return item_text(item_title,new_item)

    elif (msg == 'yes'):
        # Due to the structure of this python file
        item = item_list[item_counter - 1]['X']
        prolog.assertz('{}_chosen({})'.format(item_title, item))
        global_counter()
        reset_second()
        return next_step(item_title)

    else:
        return error_input()


# Input from HTML is saved under 'msg'
@hug.get()
def get(msg: hug.types.text):
    # Start ordering process
    if (main_counter == 0):
        if (msg == 'yes'):
            global_counter()
            return next_step('order')
        elif (msg == 'no'):
            return "Good bye"
        else:
            return "error_input()"

    # Start meal order
    elif (main_counter == 1):
        return order_set(msg, 'meal')

    # Start bread order
    elif (main_counter == 2):
        return order_set(msg, 'bread')

    # Start meat order
    elif (main_counter == 3):
        return order_set(msg, 'meat')

    # Start veggie order
    elif (main_counter == 4):
        return order_set(msg, 'veggie')

    # Start sauce ordder
    elif (main_counter == 5):
        return order_set(msg, 'sauce')

    # Start topup order
    elif (main_counter == 6):
        return order_set(msg, 'topup')

    # Start side order
    elif (main_counter == 7):
        return order_set(msg, 'side')

    # Print all items chosen
    elif (main_counter == 8):
        return (
            'meal chosen = {}\n bread chosen = {}\nmeat chosen = {}\nveggie chosen = {}\nsauce chosen = {}\n top up chosen = {} \n side chosen = {}\n Thank you and have a nice day \n Restart the server for a new order'
            .format(
                list(prolog.query('show_meal(X)'))[0]['X'],
                list(prolog.query('show_bread(X)'))[0]['X'],
                list(prolog.query('show_meat(X)'))[0]['X'],
                list(prolog.query('show_veggie(X)'))[0]['X'],
                list(prolog.query('show_sauce(X)'))[0]['X'],
                list(prolog.query('show_topup(X)'))[0]['X'],
                list(prolog.query('show_side(X)'))[0]['X']))

    else:
        return error_input()






# There is a logic error here :> all the best for your assignment 
