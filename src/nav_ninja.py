from os           import *
from configparser import ConfigParser
from webbrowser   import open    as open_url
from cutie        import select  as select
from re           import compile as compile_regex

CONFIGS = "configs" # path to folder

def read_config(computer):
    filenames = ConfigParser()
    filenames.optionxform=str
    filenames.read(f"{CONFIGS}/{computer}.ini")
    return filenames

def is_valid_website(url):
    pattern = compile_regex(r'^(?:https?://|www)')
    match = pattern.match(url)
    return bool(match)

chdir(path.dirname(path.abspath(__file__)))
computer = getenv('COMPUTERNAME').lower()
filenames = read_config(computer)
sections = filenames.sections()

i = 0
stylish_items : list[str] = [] # for terminal
raw_paths : list[str] = []     # for process
captions : list[int] = []
for section in sections:
    # add config.ini sections as menu items, but captions will make them unselectable
    captions += [i,i+1]
    stylish_items += [' ', f"\033[4m{section}\033[0m:"]
    raw_paths += [None, None]
    i += 2
    for k,v in filenames.items(section):
        # add menu items and their non-styled equivalent in parallel
        stylish_items += [f"\033[{33}m{k}\033[0m : {v}"]
        raw_paths += [v]
        i += 1

# This is a shortcut to the config file responsible for this menu
stylish_items += [
    '',
    "***********************",
    '',
    f"UPDATE THIS LIST: {computer}.ini",
    '',
    "EXIT\033[0m" # Exit is always last
]
raw_paths += [
    None, # i
    None, # i + 1
    None, # i + 2
    f"{getcwd()}/{CONFIGS}/{computer}.ini",
    None, # i + 4
    None  # i + 5
    ]
captions += [
    i,
    i+1,
    i+2,
    i+4
]

position = 2 # set cursor at first non-section item
exit_flag = 0
while exit_flag == 0:
    system('cls')
    print("Hello " + computer.upper())
    position = select(
            stylish_items,
            caption_indices=captions,
            deselected_prefix="\033[0m   ",
            selected_prefix=" \033[92m>\033[7m\033[0m \033[7m", # 92 = green, 7 = reverse
            selected_index=position
        )
    
    if position == len(stylish_items) - 1: # in other words, if selected position is last item
        exit_flag = 1
        # TODO git add .
        # TODO git commit -m "config"
        # TODO git push
    else:
        file = raw_paths[position]
        prefix = '' if is_valid_website(file) else 'file:///' # if it's not a website, add prefix
        open_url(prefix + file)
