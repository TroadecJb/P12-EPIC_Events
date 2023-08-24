from views.display import View

view = View()


def ask_values():
    new_values_dict = {}
    adding = True
    while adding:
        field = view.user_input(detail="name of the field to modify")
        new_values_dict[field] = view.user_input(detail="new value")
        keep = view.confirm(detail="modify any other field?")
        if keep:
            adding = False
        else:
            pass
    return new_values_dict


def select_obj_from_list(list):
    choice = view.select_obj_from_list(list)
    return choice
