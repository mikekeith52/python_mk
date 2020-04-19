import configparser
import pyperclip

def main():
    config = configparser.ConfigParser()

    config.read('config.ini',encoding='UTF-8')

    go = True
    while go:
        shortkey = input('select a HotKey : ')
        if shortkey.lower() == 'stop':
            go = False
        else:
            try:
                string = config[shortkey.lower()]['comment']
                print(string)
                loop_through = string.count('[')
                l = 0
                while l < loop_through:
                    for i, val in enumerate(string):
                        if val == '[':
                            replace_start = i
                        elif val == ']':
                            replace_end = i
                            break
                    replace = input('replace: ' + string[replace_start:replace_end+1])
                    string = string.replace(string[replace_start:replace_end+1],replace)
                    l+=1
                pyperclip.copy(string)
            except KeyError as e:
                print(f'key not found: {e}')
main()