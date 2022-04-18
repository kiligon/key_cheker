from multiprocessing import Pool,Process,Value
from multiprocessing import current_process
from multiprocessing.dummy import Pool as ThreadPool
from functools import partial
from config import *
import time
import os
from gooey import Gooey
from gooey import GooeyParser
from skqrper import key_checker
from tqdm.contrib.concurrent import process_map


@Gooey(program_name="Key validator",
        required_cols=2,
        body_bg_color=body_bg_color,
        header_bg_color=header_bg_color,
        footer_bg_color=footer_bg_color,
        terminal_panel_color=terminal_panel_color,
        terminal_font_color=terminal_font_color)
def arbitrary_function():

    my_cool_parser = GooeyParser(description="first version of key validator")

    my_cool_parser.add_argument(
        'foo',
        metavar="File selector",
        help='File with keys for processing',
        widget="FileChooser")

    my_cool_parser.add_argument(
        'proc',
        default = len(os.sched_getaffinity(0))*2 - 2,
        metavar="Number of proc",
        type = int)

    my_cool_parser.add_argument(
        'bar',
        metavar="Dir chooser",
        help="Select the directory where the processed keys will be saved",
        widget="DirChooser")


    args = my_cool_parser.parse_args()
    main(args)


def yield_keys(key_file):
    arr = []
    for key in key_file:
        arr.append(key[:-1])
    return arr


def main(args):
    with open(args.foo,"r") as key_file, open(args.bar+"/valid_keys","w") as valid_keys, open(args.bar+"/no_valid_keys","w+") as no_valid_keys:    
        keys = yield_keys(key_file)
        proc = args.proc
        keys_arr = []
        for i in range(proc):
            keys_arr.append(keys[(len(keys)//proc)*i:(len(keys)//proc)*(i+1)])
             
        if len(keys)%proc!=0:
            keys_arr.append(keys[(len(keys)//proc)*proc:])
            proc+=1
        global key_len
        num = Value('i',0)
        p = ThreadPool(4)
        p.imap(partial(key_checker, valid_file = valid_keys, no_valid_file = no_valid_keys, counter=num, our_len=len(keys_arr)), keys_arr)
        p.close()
        p.join()


if __name__ == '__main__':
    arbitrary_function()
