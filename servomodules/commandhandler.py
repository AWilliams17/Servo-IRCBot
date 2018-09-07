from inspect import getargspec


class CommandHandler(object):
    def __init__(self):
        self.registered_commands = {}

    def register_command(self, command_string, command_description="No description given.", arg_type="default"):
        if command_string == "":
            raise ValueError("Can't define a command with no command string")

        def decorator(f):
            self.registered_commands[str(command_string).lower()] = [f, command_description, arg_type]
            return f
        return decorator

    def serve(self, link):
        if link == '':
            return None
        link_list = filter(None, link.split(" "))
        key_length = len(link_list[0]) + 1
        if link_list[0] in self.registered_commands:
            arg_type = self.registered_commands.get(str(link_list[0]).lower())[2]
            linked_function = self.registered_commands.get(str(link_list.pop(0)).lower())[0]
            if linked_function:
                args = len(getargspec(linked_function).args)
                if len(link_list) < args and arg_type is not "optional":
                    return "Too few parameters (%s given, %s needed)" % (len(link_list), args)
                elif len(link_list) > args and arg_type is not "multi string" and arg_type is "default":
                    return "Too many parameters (%s given, %s needed)" % (len(link_list), args)
                else:
                    if args == 0:
                        return linked_function()
                    elif args == 1:
                        return linked_function(str(link[key_length:]))
                    else:
                        return linked_function(*link_list)
