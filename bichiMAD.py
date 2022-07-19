import argparse
import time
import re
from modules import find_bicimad as find


# check email address
def validate_email(email):
    pattern = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
    if(re.fullmatch(pattern, email)):
        return True
    else:
        return False

# ask email
def input_email():
    dir_email = input("Please, type your e-mail: ")
    if dir_email == "":
        print("FATAL ERROR. You need type an email.")
    else:
        if not validate_email(dir_email):
            dir_email = ""
            print("FATAL ERROR. You need type a correct email address.")
    return dir_email

# ask name of place
def input_place():
    place = input("Please, type a name of interest place: ")
    if place == "":
        print("FATAL ERROR. You need type a name of place.")
    return place

# get bicimad nearest every place to take a bike
def every_place_take_bicimad():
    # get email
    dir_email = input_email()
    if dir_email != "":
        start = time.time()
        # get BiciMAD nearest for every place to take a bike
        find.every_place_bicimad("TAKE", dir_email)
        end = time.time()
        print(f"every_place_take_bicimad time: {end-start}")

# get bicimad nearest every place to leave a bike
def every_place_leave_bicimad():
    # get email
    dir_email = input_email()
    if dir_email != "":
        start = time.time()
        # get BiciMAD nearest for every place to leave a bike
        find.every_place_bicimad("LEAVE", dir_email)
        end = time.time()
        print(f"every_place_leave_bicimad time: {end-start}")

# get bicimad nearest specific place to take a bike
def specific_place_take_bicimad():
    # get email
    dir_email = input_email()
    if dir_email != "":
        name_place = input_place()
        if name_place != "":
            start = time.time()
            # get BiciMAD nearest for specific place to take a bike
            find.specific_place_bicimad("TAKE", name_place, dir_email)
            end = time.time()
            print(f"specific_place_bicimad time: {end-start}")

# get bicimad nearest specific place to leave a bike
def specific_place_leave_bicimad():
    # get email
    dir_email = input_email()
    if dir_email != "":
        name_place = input_place()
        if name_place != "":
            start = time.time()
            # get BiciMAD nearest for specific place to leave a bike
            find.specific_place_bicimad("LEAVE", name_place, dir_email)
            end = time.time()
            print(f"specific_place_bicimad time: {end-start}")

# argument parser
def argument_parser():
    # OPTION: 1 - every place. 2 - specific place
    # ACTION: T - Take bike. L - Leave bike
    parser = argparse.ArgumentParser(description= "App allows to find the nearest BiciMAD station to a set of places of interest.")
    help_message_o ='Option 1: "1" get nearest BiciMAD for every place of interest. Option 2: "2" get nearest BiciMAD for a specific place of interest.'
    parser.add_argument("-o", "--option", help=help_message_o, type=str)
    help_message_a ='Option 1: "T" take a bike. Option 2: "L" leave a bike.' 
    parser.add_argument("-a", "--action", help=help_message_a, type=str)
    args = parser.parse_args()
    return args

def main():
    # validate args
    if argument_parser().option == '1':
        if argument_parser().action == 'T':
            # get bicimad nearest every place to take a bike
            ###print("Calculate bicimad nearest for every place to take a bike")
            every_place_take_bicimad()
        elif argument_parser().action == 'L':
            # get bicimad nearest every place to leave a bike
            ###print("Calculate bicimad nearest for every place to leave a bike")
            every_place_leave_bicimad()
        else:
            # error argument 2 (action)
            print("FATAL ERROR. You need to select the correct option.")
            print('Option 1: "T" take a bike. Option 2: "L" leave a bike.')
    elif argument_parser().option == '2':
        if argument_parser().action == 'T':
            # get bicimad nearest specific place to take a bike
            ###print(f"Calculate bicimad nearest specifici place to take a bike")
            specific_place_take_bicimad()
        elif argument_parser().action == 'L':
            # get bicimad nearest specific place to leave a bike
            ###print(f"Calculate bicimad nearest specifici place to leave a bike")
            specific_place_leave_bicimad()
        else:
            # error argument 2 (action)
            print("FATAL ERROR. You need to select the correct option.")
            print('Option 1: "T" take a bike. Option 2: "L" leave a bike.')
    else:
        # error argument 1 (option)
        print("FATAL ERROR. You need to select the correct option.")
        print('Option 1: "1" get nearest BiciMAD for every place of interest. Option 2: "2" get nearest BiciMAD for a specific place of interest.')            


if __name__ == '__main__':
    main()
