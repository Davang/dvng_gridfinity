import sys
import os
import argparse
import curses


CANCEL = 0


def update_path(t_modules):
    for module in t_modules:
        if module not in sys.path and module:
            sys.path.append(module)


def parse_args():
    parser = argparse.ArgumentParser(
        prog="dvng_gridfinity.py",
        description="python script to mana	 dvng_gridfinity from the cli without opening FreeCAD",
        epilog="https://github.com/Davang/dvng_gridfinity",
    )
    parser.add_argument("-m", "--modules-file")
    parser.add_argument("-b", "--build-dir")
    parser.add_argument("-d", "--mec-dir")
    return vars(parser.parse_args())


def draw_background(t_stdscr, t_color):
    t_stdscr.clear()
    t_stdscr.bkgd(t_color)
    t_stdscr.border()


def ask_from_list(t_stdscr, t_color, t_list, t_title):
    t_list.insert(CANCEL, "cancel")
    position = 0
    selection = -1
    draw_background(t_stdscr, t_color)
    t_stdscr.addstr(1, 2, t_title, t_color | curses.A_BOLD | curses.A_UNDERLINE)
    while selection == -1:
        for i, ele in enumerate(t_list):
            color = t_color if not i == position else t_color | curses.A_REVERSE
            t_stdscr.addstr(i + 2, 2, f"{i}. {ele}", color)
            t_stdscr.move(position + 1, 2)

        user_input = t_stdscr.getch()
        if curses.KEY_UP == user_input:
            position = max(0, position - 1)
        elif curses.KEY_DOWN == user_input:
            position = min(len(t_list) - 1, position + 1)
        elif ord("\n") == user_input:
            selection = position
        else:
            pass

        t_stdscr.refresh()
    return selection


def list_dir(t_path):
    content_list = []
    for ele in os.listdir(t_path):
        if os.path.isdir(os.path.join(t_path, ele)):
            content_list.append(ele + "/")
        elif ".FCStd" in ele:
            content_list.append(ele)
        else:
            pass

    return content_list


def print_error(t_stdscr, t_color):
    draw_background(t_stdscr, t_color)
    t_stdscr.addstr(1, 1, "INVALID INPUT", t_color | curses.A_REVERSE)


if __name__ == "__main__":
    args = parse_args()
    mod_file = args["modules_file"]
    out_dir = args["build_dir"]
    mec_dir = args["mec_dir"]

    with open(mod_file, "r") as f:
        update_path(f.read().split(","))

    # import FreeCAD

    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    curses.start_color()
    curses.use_default_colors()
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_CYAN)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_CYAN)

    win = curses.newwin(10, 50)
    win.keypad(True)

    os.chdir(mec_dir)
    user_input = -1
    cur_file = None

    while True:
        cur_dir = os.getcwd()
        dir_list = list_dir(cur_dir)

        if cur_file:
            user_input = CANCEL
        else:
            user_input = ask_from_list(stdscr, curses.color_pair(1), dir_list, cur_dir)

        if cur_file:
            if CANCEL == user_input:
                cur_file = None
                # todo close file
            else:
                pass  # manage file
        else:
            if CANCEL == user_input:
                if cur_dir == mec_dir:
                    break
                else:
                    os.chdir("..")
            else:
                target = os.path.join(cur_dir, dir_list[user_input])
                if "/" in dir_list[user_input]:
                    os.chdir(target)
                else:
                    cur_file = target

    curses.nocbreak()
    win.keypad(False)
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()
