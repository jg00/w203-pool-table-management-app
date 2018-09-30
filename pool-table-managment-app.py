# version 11 working version but need to upate daily reports file

import json
import datetime
import math


class Table:
    def __init__(self,table_number):
        self.table_number = table_number
        self.start_date_time = ""
        self.end_date_time = ""
        self.total_time_played = 0
        # self.cost = 0
    
    def as_dictionary(self):
        return self.__dict__


# For pool table states
def persist_to_file(table_list, file_name):
    with open(file_name,"w") as file_object:
        json.dump(table_list, file_object, indent=2)


def read_from_file(file_name):
    with open(file_name,"r") as file_object:
        pool_table_states_obj = json.load(file_object)
        return pool_table_states_obj


def update_pool_table_state_json_file(table_object_as_dictionary, file_name):
    new_table_object_as_dictionary = table_object_as_dictionary

    table_list = []
    
    try:
        # If exists capture full list and append
        table_list = read_from_file(file_name)

        table_list.append(new_table_object_as_dictionary)

        # Dump new list
        persist_to_file(table_list,file_name)

        print("Message: Pool table states updated")
    
    except FileNotFoundError:
        table_list.append(new_table_object_as_dictionary)

        persist_to_file(table_list,file_name)

        print("Message: New file created and table added")


def update_pool_table_history_json_file(table_object_as_dictionary, file_name):
    new_table_object_as_dictionary = table_object_as_dictionary

    table_list = []
    
    try:
        # If exists capture full list and append
        table_list = read_from_file(file_name)

        table_list.append(new_table_object_as_dictionary)

        # Dump new list
        persist_to_file(table_list, file_name)

        print("Message: History table updated")
    
    except FileNotFoundError:
        table_list.append(new_table_object_as_dictionary)

        persist_to_file(table_list, file_name)

        print("Message: New history file {} created and table added".format(file_name))


def user_options():
    table_state_file_string = "./PoolTableStates.json"
    table_history_file_string = "./PlaceHolder-HISTORY.json"

    while True:
        
        option = input("MAIN MENU:\ta-add table\t v-view tables\t r-rent\t e-end rental\t q-exit app\t: ")

        if option == "q":
            return option
        

        elif option == "a":
            while True:
                table_id = input("Add new table number or 'x' to cancel ")

                if table_id == "x":
                    break

                # Check if file exists
                file_exists = -1
                try:
                    table_list = read_from_file(table_state_file_string)
                    file_exists = 1
                    
                except FileNotFoundError:
                    print("Message: File does not exists. ")

                # If file exists check if table id provided exists
                table_id_exists = -1
                if file_exists == 1:

                    while (table_id_exists == -1):

                        for table in table_list:
                            if table["table_number"] == table_id:
                                print("Message: Table number exists.  Try another.")
                                table_id_exists = 1

                        if table_id_exists == -1:
                            break

                # Add new pool table
                if (table_id_exists == -1):
                    try:
                        if int(table_id) >= 0:
                            table_object_as_dictionary = Table(table_id).as_dictionary()
                            update_pool_table_state_json_file(table_object_as_dictionary,table_state_file_string)
                            break

                    except ValueError:
                        print("Message: Enter number or 'x' to cancel ")


        elif option == "v":
            # Check if file exists
            file_exists = -1
            try:
                table_list = read_from_file(table_state_file_string)
                file_exists = 1

                # Show tables and status
                for table in table_list:

                    table_status = ""
                    table_start_datetime = ""

                    if table["start_date_time"] == "":
                        table_status = "NOT OCCUPIED"
                        print("Table {0} {1}".format(table["table_number"], table_status))

                    else:
                        number_of_minutes_played = 0
                        time_diff_intimedelta = ""
                        start_converted_to_dt = ""

                        table_status = "OCCUPIED"
                        table_start_datetime = table["start_date_time"]

                        # Number of minutes played
                        start_converted_to_dt = datetime.datetime.strptime(table_start_datetime,"%m/%d/%y %H:%M:%S")
                        time_diff_intimedelta = datetime.datetime.now() - start_converted_to_dt
                        number_of_minutes_played = math.floor(time_diff_intimedelta.total_seconds() / 60)
                        print("Table {0} {1}\t Start:{2}\t MinutesPlayed: {3}".format(table["table_number"], table_status, table_start_datetime, number_of_minutes_played))
                
            except FileNotFoundError:
                print("Message: File does not exists.  Add first table. ")


        elif option == "r":
            # Check if file exists
            file_exists = -1
            try:
                table_list = read_from_file(table_state_file_string)
                file_exists = 1

                # Show tables and status
                for table in table_list:

                    table_status = ""
                    table_start_datetime = ""

                    if table["start_date_time"] == "":
                        table_status = "NOT OCCUPIED"
                        print("Table {0} {1}".format(table["table_number"], table_status))

                    else:
                        number_of_minutes_played = 0
                        time_diff_intimedelta = ""
                        start_converted_to_dt = ""

                        table_status = "OCCUPIED"
                        table_start_datetime = table["start_date_time"]

                        # Number of minutes played
                        start_converted_to_dt = datetime.datetime.strptime(table_start_datetime,"%m/%d/%y %H:%M:%S")
                        time_diff_intimedelta = datetime.datetime.now() - start_converted_to_dt
                        number_of_minutes_played = math.floor(time_diff_intimedelta.total_seconds() / 60)
                        print("Table {0} {1}\t Start:{2}\t MinutesPlayed: {3}".format(table["table_number"], table_status, table_start_datetime, number_of_minutes_played))

                # Rent table
                rent_table_number = input("Select table to rent out or 'x' to cancel: ")

                if rent_table_number == "x":
                    break

                # Find specific table number in table list
                table_dictionary = {}
                for table in table_list:
                    if table["table_number"] == rent_table_number:
                        table_dictionary = table
                        # print("Table {0} {1}".format(table["table_number"], table["start_date_time"]))

                # If table number not found return to options menu
                if table_dictionary == {}:
                    print('Message: Table number does not exists.')
                    break

                # If table number found rent out the table if available
                if table_dictionary["start_date_time"] == "":
                    # table_dictionary["start_date_time"] = datetime.datetime.now().strftime("%D %T")
                    table_dictionary["start_date_time"] = datetime.datetime.now().strftime("%m/%d/%y %H:%M:%S")

                    print("Pool table {0} rented out".format(table_dictionary["table_number"]))
                else:
                    print("Pool table {0} is currently occupied".format(table_dictionary["table_number"]))

                persist_to_file(table_list, table_state_file_string)
                
            except FileNotFoundError:
                print("Message: File does not exists.  Add first table. ")


        elif option == "e":
            while True:
                
                # Check if pool table states file exists
                file_exists = -1
                try:
                    table_list = read_from_file(table_state_file_string)
                    file_exists = 1

                    # Show tables and status
                    for table in table_list:

                        table_status = ""
                        table_start_datetime = ""

                        if table["start_date_time"] == "":
                            table_status = "NOT OCCUPIED"
                            print("Table {0} {1}".format(table["table_number"], table_status))

                        else:
                            number_of_minutes_played = 0
                            time_diff_intimedelta = ""
                            start_converted_to_dt = ""

                            table_status = "OCCUPIED"
                            table_start_datetime = table["start_date_time"]

                            # Number of minutes played
                            start_converted_to_dt = datetime.datetime.strptime(table_start_datetime,"%m/%d/%y %H:%M:%S")
                            time_diff_intimedelta = datetime.datetime.now() - start_converted_to_dt
                            number_of_minutes_played = math.floor(time_diff_intimedelta.total_seconds() / 60)
                            print("Table {0} {1}\t Start:{2}\t MinutesPlayed: {3}".format(table["table_number"], table_status, table_start_datetime, number_of_minutes_played))

                except FileNotFoundError:
                    print("Message: File does not exists.  No data to update. ")
                    break

                rent_table_number = input("Enter table number to end rental or 'x' to cancel ")

                if rent_table_number == "x":
                    break

               # Find specific table number in table list
                table_dictionary = {}
                for table in table_list:
                    if table["table_number"] == rent_table_number:
                        table_dictionary = table

                # If table number not found return to options menu
                if table_dictionary == {}:
                    print('Message: Table number does not exists.')
                    break

                # If table number found document the end of the table rental, track the table rental info into separate file and reset the table rental state.
                if table_dictionary["start_date_time"] != "":       # ie Table is occupied

                    end_date_time = datetime.datetime.now()

                    # Calculate total minutes
                    number_of_minutes_played = 0
                    time_diff_intimedelta = ""
                    start_converted_to_dt = ""

                    table_status = "TABLE RENTAL ENDED"
                    table_start_datetime = table_dictionary["start_date_time"]

                    # Number of minutes played
                    start_converted_to_dt = datetime.datetime.strptime(table_start_datetime,"%m/%d/%y %H:%M:%S")
                    time_diff_intimedelta = datetime.datetime.now() - start_converted_to_dt
                    number_of_minutes_played = math.floor(time_diff_intimedelta.total_seconds() / 60)
                    print("Table {0} {1}\t Start:{2}\t MinutesPlayed: {3}".format(table_dictionary["table_number"], table_status, table_start_datetime, number_of_minutes_played))

                    # Temporarily prep table dictionary object with calculated values to save to history file
                    table_dictionary["end_date_time"] = end_date_time.strftime("%m/%d/%y %H:%M:%S")
                    table_dictionary["total_time_played"] = number_of_minutes_played

                    # Save to daily history file.  Create one if it does not exist for the day.
                    string_file_name = "./"
                    date_today = datetime.datetime.now().date().strftime("%m-%d-%Y")
                    string_file_name = string_file_name + date_today + ".json"
                    table_history_file_string = string_file_name

                    update_pool_table_history_json_file(table_dictionary,table_history_file_string)

                    # Reset pool table states file for the specific table
                    table_dictionary["start_date_time"] = ""
                    table_dictionary["end_date_time"] = ""
                    table_dictionary["total_time_played"] = ""

                    # Update the pool table states file
                    persist_to_file(table_list, table_state_file_string)

                    # Info on update
                    print("Table {0} {1}\t Start:{2}\t End:{3}\t MinutesPlayed: {4}".format(table_dictionary["table_number"], table_status, table_start_datetime, end_date_time, number_of_minutes_played))

                    break

                else:
                    print("Pool table {0} is not currently occupied".format(table_dictionary["table_number"]))

        else:
            print("Message: Enter valid option ")




while True:
    print("** POOL TABLE MANAGMENT APP STARTED **")
    option = user_options()

    if (option == "q"):
        break

print("** POOL TABLE MANAGMENT APP CLOSED **")

