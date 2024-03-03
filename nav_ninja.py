from os           import *
from configparser import ConfigParser
from webbrowser   import open    as open_url
from cutie        import select  as select
from re           import compile as compile_regex

def read_config(computer):
    filenames = ConfigParser()
    filenames.optionxform=str
    filenames.read(f"{computer}_config.ini")
    return filenames

def is_valid_website(url):
    pattern = compile_regex(r'^(?:https?://|www)')
    match = pattern.match(url)
    return bool(match)

computer = getenv('COMPUTERNAME').lower()
filenames = read_config(computer)
sections = filenames.sections()

i = 0
stylish_items : list[str] = [] # for terminal
raw_paths : list[str] = []     # for process
captions : list[int] = []
for section in sections:
    # add config.ini sections as menu items, but captions will make them unselectable
    captions += [i]
    stylish_items += [section + ":"]
    raw_paths += [None]
    i += 1
    for k,v in filenames.items(section):
        # add menu items and their non-styled equivalent in parallel
        stylish_items += [f"\033[{33}m{k}\033[0m : {v}"]
        raw_paths += [v]
        i += 1

# This is a shortcut to the config file responsible for this menu
stylish_items += ['',f"Add to this list: {computer}_config.ini"]
raw_paths += [None, f"{getcwd()}/{computer}_config.ini"]
captions += [i]

position = 1 # set cursor at first non-section item
while True:
    system('cls')
    print("Hello " + computer.upper() + "\n")
    position = select(
            stylish_items,
            caption_indices=captions,
            deselected_prefix="   ",
            selected_prefix=" \033[92m>\033[0m ",
            selected_index=position
        )
    
    file = raw_paths[position]
    prefix = '' if is_valid_website(file) else 'file:///' # if it's not a website, add prefix
    open_url(prefix + file)