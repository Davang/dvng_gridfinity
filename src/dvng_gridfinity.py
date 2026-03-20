import sys
import os
import argparse
import curses


CANCEL = 0
EXTENSTION = ".FCStd"


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


def list_dir(t_path):
    content_list = []
    for ele in os.listdir(t_path):
        if os.path.isdir(os.path.join(t_path, ele)):
            content_list.append(ele + "/")
        elif EXTENSTION in ele:
            content_list.append(ele)
        else:
            pass
    return content_list


def is_int(s):
    try:
        int(s)
    except ValueError:
        return False
    else:
        return True


def clear_line_till_end(t_stdscr, t_x, t_y, t_len):
    t_stdscr.addstr(t_x, t_y, (" " * t_len)[0:t_len])


def draw_background(t_stdscr, t_color, t_title):
    t_stdscr.clear()
    t_stdscr.bkgd(t_color)
    t_stdscr.border()
    t_stdscr.addstr(1, 2, t_title, t_color | curses.A_BOLD | curses.A_UNDERLINE)


def ask_from_list(t_stdscr, t_color, t_list):
    t_list.insert(CANCEL, "cancel")
    position = 0
    selection = -1
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

    return selection


def edit_line_integer(t_stdscr, t_color, t_position, t_index, t_name, t_val):
    fixed_text = f"{t_index}. {t_name} = "
    t_stdscr.addstr(t_position, 2, fixed_text, t_color)

    curses.echo()
    user_input = ""
    while not is_int(user_input):
        clear_line_till_end(t_stdscr, t_position, 2 + len(fixed_text), len(user_input))
        user_input = t_stdscr.getstr()

    curses.noecho()
    return str(user_input, "ASCII")


def draw_obj_menu(t_stdscr, t_color, t_out_dir, t_cad_file, t_obj_label, t_var_set):
    def not_label(t_ele):
        return "Label" not in t_ele

    def not_hidden(t_var_set, t_ele):
        return "Hidden" not in t_var_set.getPropertyStatus(t_ele) and "Hidden" not in t_var_set.getTypeOfProperty(t_ele)

    def generate_name(t_out_dir, t_label, t_values, t_extension=".step"):
        values_str = ""
        for i, val in enumerate(t_values):
            values_str += "_" + str(val)

        return os.path.join(t_out_dir, t_label + values_str + t_extension)

    var_label = "holder"

    while var_label:
        draw_background(t_stdscr, t_color, f"{t_cad_file.FileName[: -len(EXTENSTION)]}::{t_obj_label}")

        text_list = []
        var_labels = [f"{i}" for i in t_var_set.PropertiesList if not_label(i) and not_hidden(t_var_set, i)]
        var_values = [f"{t_var_set.getPropertyByName(i)}" for i in var_labels]
        var_labels.append("generate stl file")
        var_values.append("")

        for ele, val in zip(var_labels, var_values):
            if val:
                text_list.append(f"{ele} = {val}")
            else:
                text_list.append(f"{ele}")

        user_input = ask_from_list(t_stdscr, t_color, text_list)

        if CANCEL == user_input:
            var_label = None
        elif user_input == len(var_labels):
            t_cad_file.recompute()

            labels = [f"{i}" for i in t_var_set.PropertiesList if not_label(i) and not_hidden(t_var_set, i)]
            obj = t_cad_file.getObjectsByLabel(t_obj_label)[0]

            file_name = generate_name(t_out_dir, obj.Label, [f"{t_var_set.getPropertyByName(i)}" for i in labels])
            obj.Shape.exportStep(file_name)

            t_stdscr.addstr(20, 2, f"export done {file_name}, press any key to continue", t_color | curses.A_BOLD | curses.A_REVERSE)
            t_stdscr.getch()

            # pending generation
        else:
            var_index = user_input - 1
            new_value = edit_line_integer(t_stdscr, t_color, user_input + 2, user_input, var_labels[var_index], var_values[var_index])
            exec(f"t_var_set.{var_labels[var_index]} = {new_value}")


def draw_file_menu(t_stdscr, t_color, t_error_color, t_file_name, t_out_dir):
    cad_file = FreeCAD.open(t_file_name)
    var_set = cad_file.getObjectsByLabel("user_input")[0]
    if var_set:
        obj_label = "holder"
        while obj_label:
            draw_background(t_stdscr, t_color, t_file_name[: -len(EXTENSTION)])
            obj_labels = [obj.Label for obj in cad_file.RootObjects]

            user_input = ask_from_list(t_stdscr, t_color, obj_labels)

            if CANCEL == user_input:
                obj_label = None
            else:
                obj_label = obj_labels[user_input]
                draw_obj_menu(t_stdscr, t_color, t_out_dir, cad_file, obj_label, var_set)
    else:
        draw_background(t_stdscr, t_error_color | curses.A_REVERSE)
        t_stdscr.addstr(1, 2, f"ERROR, {t_file_name} has no varSet labeled user_input, press any key to return", t_error_color | curses.A_BOLD)
        t_stdscr.getch()

    FreeCAD.closeDocument(cad_file.Name)

    return os.path.dirname(t_file_name) + "/"


def draw_folder_menu(t_stdscr, t_color, t_dir, t_base_dir):
    dir_list = list_dir(t_dir)

    draw_background(t_stdscr, t_color, t_dir)

    user_input = ask_from_list(stdscr, curses.color_pair(1), dir_list)

    target = None
    if CANCEL == user_input:
        if t_dir != t_base_dir:
            target = "../"
    else:
        target = os.path.join(t_dir, dir_list[user_input])

    return target


if __name__ == "__main__":
    args = parse_args()
    mod_file = args["modules_file"]
    out_dir = args["build_dir"]
    mec_dir = args["mec_dir"]

    with open(mod_file, "r") as f:
        update_path(f.read().split(","))

    import FreeCAD

    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    curses.start_color()
    curses.use_default_colors()
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_CYAN)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_WHITE)

    win = curses.newwin(10, 50)
    win.keypad(True)

    os.chdir(mec_dir)
    user_input = -1

    target = draw_folder_menu(stdscr, curses.color_pair(1), os.getcwd(), mec_dir)
    while target:
        if target.endswith("/"):
            os.chdir(target)
            target = draw_folder_menu(stdscr, curses.color_pair(1), os.getcwd(), mec_dir)
        else:
            target = draw_file_menu(stdscr, curses.color_pair(1), curses.color_pair(2), target, out_dir)

    curses.nocbreak()
    win.keypad(False)
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()
