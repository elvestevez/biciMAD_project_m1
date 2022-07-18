import argparse
from modules import find_bicimad_OLD as find


# argument parser
def argument_parser():
    parser = argparse.ArgumentParser(description= "App allows to find the nearest BiciMAD station to a set of places of interest.")
    help_message_o ='Option 1: "1" get nearest BiciMAD for every place of interest. Option 2: "2" get nearest BiciMAD for a specific place of interest.'
    parser.add_argument("-o", "--option", help=help_message_o, type=str)
    help_message_a ='Option 1: "T" take a bike. Option 2: "L" leave a bike.' 
    parser.add_argument("-a", "--action", help=help_message_a, type=str)
    args = parser.parse_args()
    return args

def main():
    if argument_parser().option == '1':
        if argument_parser().action == 'T':
            print("Calculate bicimad nearest for every place to take a bike")
            # get BiciMAD nearest for every place to take a bike
            find.every_place_take_bicimad()
        elif argument_parser().action == 'L':
            print("Calculate bicimad nearest for every place to leave a bike")
            # get BiciMAD nearest for every place to leave a bike
            find.every_place_leave_bicimad()
        else:
            # error argument 2 (action)
            print("FATAL ERROR. You need to select the correct option.")
            print('Option 1: "T" take a bike. Option 2: "L" leave a bike.')
    elif argument_parser().option == '2':
        if argument_parser().action == 'T':
            name_place = input("Please, type a name of interest place: ")
            if name_place == "":
                # error specific place
                print("FATAL ERROR. You need type a name of a place.")                
            else:
                print(f"Calculate bicimad nearest for {name_place} to take a bike")
                # get BiciMAD nearest for specific place to take a bike
                find.specific_place_take_bicimad(name_place)
        elif argument_parser().action == 'L':
            name_place = input("Please, type a name of interest place: ")
            if name_place == "":
                # error specific place
                print("FATAL ERROR. You need type a name of a place.")                
            else:
                print(f"Calculate bicimad nearest for {name_place} to leave a bike")
                # get BiciMAD nearest for specific place to leave a bike
                find.specific_place_leave_bicimad(name_place)
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
