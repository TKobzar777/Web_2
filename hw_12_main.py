from collections import UserDict
import functions_bot 
from classes_book import Name, Phone, Record, Birthday, BotView, AddressBook, ATTENTION, OK


class BotCommands:
    def __init__(self, command_bot:str, function_bot:None, help_bot:str):
        self.command_bot = command_bot
        self.function_bot = function_bot
        self.help_bot = help_bot

    def __str__(self):
        return f'\t{self.command_bot} - {self.help_bot}'
    

class Commands(UserDict):
    def add_command(self, bot_conand:BotCommands)->str:
        self.data[bot_conand.command_bot] = bot_conand
        # return f'Add new record to Address Book'

    def print_halp(self):
        BotView.display_content('Command Line Interface\n'\
        'I will help you with your phone book\n'\
        'List of commands you can use:', ATTENTION)
        for _, i in self.items():
            BotView.display_content(i, ATTENTION)


def create_bot(bot_commands:Commands)->Commands:
    bot_commands.add_command(BotCommands(command_bot = 'HELLO', function_bot = functions_bot.hello, help_bot ='greeting'))
    bot_commands.add_command(BotCommands(command_bot = 'ADD', function_bot = functions_bot.add_contact, help_bot ='(name and phone) - add a phonebook entry'))
    bot_commands.add_command(BotCommands(command_bot = 'EDIT', function_bot = functions_bot.edit_contact, help_bot ='(name or phone) - edit contact'))
    bot_commands.add_command(BotCommands(command_bot = 'SEARCH', function_bot = functions_bot.search, help_bot ='(name or phone) - search contact by name or phone number'))
    bot_commands.add_command(BotCommands(command_bot = 'FIND MATCHES', function_bot = functions_bot.search_for_matches, help_bot ='(part of the name or phone) - find matches by part of the name or phone number'))
    bot_commands.add_command(BotCommands(command_bot = 'SHOW ALL', function_bot = functions_bot.show_all, help_bot ='(part of the name or phone) - find matches by part of the name or phone number'))
    bot_commands.add_command(BotCommands(command_bot = 'EXIT', function_bot = functions_bot.finish_work, help_bot =' finish work'))
    return bot_commands


def main():
    bot_commands = Commands()
    bot_commands = create_bot(bot_commands)
    bot_commands.print_halp()
    functions_bot.address_book = functions_bot.start_work()

    while True:
        stp_user_input = BotView.input_content()
        if stp_user_input.upper().startswith('EXIT'):
            temp = bot_commands['EXIT'].function_bot('EXIT')                
            BotView.display_content(*temp)
            break
        fl = True
        for cw in bot_commands:
            if stp_user_input.upper().startswith(cw):
                input_args = stp_user_input[len(cw)::]
                list_user_input = input_args.split()
                temp = bot_commands[cw].function_bot(cw,*list_user_input)                
                BotView.display_content(*temp)
                fl = False
                break
        if fl:
            BotView.display_content('Wrong command. Try again', False)                 
    


if __name__ == "__main__":
    main()    




