import argparse
from modules import find_bicimad as find


# argument parser
def argument_parser():
    parser = argparse.ArgumentParser(description= 'App allows to find the nearest BiciMAD station to a set of places of interest.')
    help_message ='Option 1: "1" get nearest BiciMAD for every place of interest. Option 2: "2" get nearest BiciMAD for a specific place of interest.' 
    parser.add_argument('-o', '--option', help=help_message, type=str)
    args = parser.parse_args()
    return args

def main():
    if argument_parser().option == '1':
        print("Calculate bicimad nearest for every place")
        # get BiciMAD nearest for every place
        find.every_place_bicimad()
    elif argument_parser().option == '2':
        name_place = input("Please, type a name of interest place: ")
        print(f"Calculate bicimad nearest for {name_place}")
        # get BiciMAD nearest for specific place
        find.specific_place_bicimad(name_place)        
    else:
        print("FATAL ERROR. You need to select the correct option.")
        print('Option 1: "1" get nearest BiciMAD for every place of interest. Option 2: "2" get nearest BiciMAD for a specific place of interest.')
    
if __name__ == '__main__':
    main()
