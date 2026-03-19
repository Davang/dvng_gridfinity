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


def draw_background(t_stdscr, t_color, t_title):
    t_stdscr.clear()
    t_stdscr.bkgd(t_color)
    t_stdscr.border()
    t_stdscr.addstr(1, 2, t_title, t_color | curses.A_BOLD | curses.A_UNDERLINE)


def ask_from_list(t_stdscr, t_color, t_list, t_position = 0):
    t_list.insert(CANCEL, "cancel")
    position = t_position
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

    return selection, position


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

# ele name Label in
# get value {t_var_set.getPropertyByName(ele)}
# hidden or not {t_var_set.getPropertyStatus(ele)}
# property type {t_var_set.getTypeOfProperty(ele)}


def draw_export_menu( t_stdscr , t_color, t_out_dir, t_cad_file, t_var_set, t_file_name, t_label ):
    pass

def draw_obj_menu( t_stdscr , t_color, t_out_dir, t_cad_file, t_var_set, t_file_name, t_label ):
    def not_label( t_ele ):
        return "Label" not in t_ele
    
    def not_hidden( t_var_set, t_ele ):
        return "Hidden" not in t_var_set.getPropertyStatus(t_ele) and "Hidden" not in t_var_set.getTypeOfProperty(t_ele)

    var_label = "holder"
    last_postion = 0
    while var_label:
        draw_background( t_stdscr , t_color, f"{t_file_name[:-len(EXTENSTION)]}::{t_label}")
        var_labels = [ i for i in t_var_set.PropertiesList if not_label(i) and not_hidden(t_var_set, i ) ]
        var_labels.append( "generate stl file" )

        user_input, last_postion = ask_from_list( t_stdscr, t_color, var_labels, last_postion)
        
        if CANCEL == user_input:
            var_label = None
        elif user_input == len(var_labels)-1:
            t_stdscr.addstr(10, 2, f"handle stl generation", t_color)
            t_stdscr.getch()
            pass
        else:
            t_stdscr.addstr(12, 2, f"handle modification", t_color)
            t_stdscr.getch()
            pass


def draw_file_menu( t_stdscr , t_color, t_error_color, t_file_name, t_out_dir ):
    cad_file = FreeCAD.open(t_file_name)
    title = t_file_name[:-len(EXTENSTION)]
    var_set = cad_file.getObjectsByLabel("user_input")[0]
    if var_set:
        obj_label = "holder"
        while obj_label:
            draw_background( t_stdscr , t_color, title )
            obj_labels = [ obj.Label for obj in cad_file.RootObjects ]
            
            user_input,_ = ask_from_list( t_stdscr, t_color, obj_labels )
            if CANCEL == user_input:
                obj_label = None
            else:
                obj_label = obj_labels[ user_input ]
                draw_obj_menu( t_stdscr, t_color, t_out_dir, cad_file, var_set, t_file_name, obj_label )
    else:
        draw_background(t_stdscr , t_error_color | curses.A_REVERSE )
        t_stdscr.addstr(1, 2, f"ERROR, {t_file_name} has no varSet labeled user_input, press any key to return", t_error_color | curses.A_BOLD )
        t_stdscr.getch()

    FreeCAD.closeDocument(cad_file.Name)

    return os.path.dirname( t_file_name )  + "/"



def draw_folder_menu( t_stdscr , t_color, t_dir, t_base_dir ):
    dir_list = list_dir(t_dir)
    
    draw_background(t_stdscr, t_color, t_dir )
    
    user_input,_ = ask_from_list(stdscr, curses.color_pair(1), dir_list )
    
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
    
    target = draw_folder_menu( stdscr, curses.color_pair(1), os.getcwd(), mec_dir)
    while target:
        
        if target.endswith("/"):
            os.chdir(target)
            target = draw_folder_menu( stdscr, curses.color_pair(1), os.getcwd(), mec_dir)
        else:
            target = draw_file_menu( stdscr, curses.color_pair(1), curses.color_pair(2), target, out_dir )

    curses.nocbreak()
    win.keypad(False)
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()
