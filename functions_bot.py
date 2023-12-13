from classes_book import Name, Phone, Record, Birthday, AddressBook, DateValueError, NameValError, BotView, ALARM, OK, ATTENTION, PhoneValueError
import copy

class ChoiceError(Exception):
    pass

# import string
global file_name
file_name= 'new_file.bin'

global address_book
address_book = AddressBook()


def input_error(func):
    def inner(*args):
        try:
            return func(*args)
        except IndexError:
            return 'Not enough params. Try again', ALARM
        except ValueError:
            return 'Phon nomber is not correct. Try again', ALARM
        except KeyError:
            return 'There is no entry in the phone book that contains that parameter.', ALARM
        except DateValueError:
            return 'Format date wrong', ALARM
        except ChoiceError:
            return 'Wrong choice.Try again', ALARM
        except PhoneValueError:
            return 'Phone number most be 10 didgit', ALARM
        except NameValError:
            return 'Name most only letters', ALARM
        
    return inner


def start_work()->str:    
    book = AddressBook()
    return book.unpack_address_book(file_name)  


def hello(*args)->str:
    return 'Hello How can I help you?', OK


def finish_work(*args)->str:
    str_result = address_book.save_address_book(file_name)
    return 'Good bay - ' + str_result, OK


@input_error
def add_contact(*args)->str:
    record = address_book.get(args[1])
    if not record:
        record = Record(Name(args[1]))
    record.add_phone(Phone(args[2]))
    len_args = len(args)
    if len_args > 3:
        record.add_birthday(Birthday(args[3]))
    return address_book.add_record(record), OK
    

@input_error
def search(*args) ->Record|str:
    if (len(args))<2:
        raise IndexError
    i=1
    while i < len(args):
        record = address_book.serch_on_param(args[i])
        i+=1
        if record:
            return record, OK     
    return 'Contact with the specified parameter was not found', OK


def search_for_matches_by_name(part_name:str)->AddressBook|None:
    book_temp = AddressBook()
    for key, value in address_book.items():
        if str(key).lower().find(part_name.lower()) < 0:
            continue
        book_temp.add_record(value)
    if len(book_temp):
        return book_temp
    return None


def search_for_matches_by_phone(part_name:str)->AddressBook|None:
    book_temp = AddressBook()
    for _, value in address_book.items():
        for ph in value.list_phones:
            if ph.value_of().find(part_name) < 0:
                continue
            book_temp.add_record(value)
    if len(book_temp):
        return book_temp
    return None


@input_error
def search_for_matches(*args)-> AddressBook|None:
    if args[1].isdigit():
        book_resalt = search_for_matches_by_phone(args[1])
    else:
        book_resalt = search_for_matches_by_name(args[1])
    if show_book:
        return show_book(book_resalt, 2)
    return f'No match found!', ALARM
    
    

@input_error
def edit_contact(*args) -> str:

    records:list
    records = search(*args)
    BotView.display_content(*records)
    
    if not type(records[0])==Record:
        return 'There is no entry in the phone book that contains that parameter', ALARM
    #BotView.display_content(f'Entry for editing:\n{records[0]}', OK)
    BotView.display_content('Select a command from the list:\n'\
            '\tedit phone - 1\n'\
            '\tdelete phone -2\n'\
            '\tchange name - 3\n'\
            '\tdelete contact - 4\n'\
            '\texit - 5', ATTENTION)
    while True:
        user_input= int(BotView.input_content())
        if user_input == 1:
            phone = Phone(BotView.input_content('input phone '))
            new_phone = Phone(BotView.input_content('input new phone '))
            return records[0].edit_phone(phone, new_phone), OK
        elif user_input == 2:
            phone = Phone(BotView.input_content('input phone '))
            return records[0].delete_phone(phone)
        elif user_input == 3:
            new_name = Name(BotView.input_content('input new name '))
            record_temp = copy.deepcopy(records[0])
            BotView.display_content((address_book.delete_record(records[0])))
            record_temp.name.value = new_name.value
            BotView.display_content((address_book.add_record(record_temp)))
            return 'Name is changed', OK
        elif user_input == 5:
            return 'Exiting edit mode', OK
        elif user_input == 4:
            return address_book.delete_record(records[0])
        else:
            raise ChoiceError
        
def show_book(book:AddressBook, stap:int = 3) -> str:    
    for i in book.iterator(stap):
        BotView.display_content(i, OK)
    return 'Thet ALL', ATTENTION

def show_all(*args):
    BotView.display_content('SHOW ALL:', ATTENTION)
    er = show_book(address_book,5)
    return er


  



        
