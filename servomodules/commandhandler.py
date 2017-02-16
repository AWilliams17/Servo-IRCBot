# ToDo: Refactor the docstrings and the serve function.
from inspect import getargspec


class CommandHandler(object):
    def __init__(self):
        """
        This is a list of commands currently registered.
        Example:
            ["!test": test_function]
        Basically, every 'command' in the dictionary should be just a string linked to a function.
        """
        self.registeredcommands = {}

    def registercommand(self, command_string, command_description="No description given.", arg_type="default"):
        """
        Take a given command string(EG: "!test"), and if one is supplied, a description, and place them both into
        the dictionary registerdcommands along with the decorated function.

        :param command_string: The string which is to be 'linked' to a function.
        :param command_description: The description which describes what the command does. Not required.
        :param arg_type: Either default or multi string. The only difference between default arguments and multi string
        ones are just how they are called, with multi string arguments treating string arguments as a single argument.
        Example:
            if !test were default, and it was called like so: "!test test test", then it would treat the two trailing
            tests as extra arguments and return an error.
            if !test were multi string, and it was called like so: "!test test test", then it would treat the two
            trailing tests as one argument, and pass them into the function as "test test".
        :return: If the command string is left empty, then raise a value error. Otherwise, take the decorated
        function, and 'link' it to the command string. Store both in the registerdcommands dictionary.
        """
        if command_string is "":
            raise ValueError("Can't define a command with no command string")

        def decorator(f):
            self.registeredcommands[str(command_string).lower()] = [f, command_description, arg_type]
            return f
        return decorator

    def serve(self, link):
        """
        Attempt to take a given command string(a 'link')and its function, and then call said function, passing in
        arguments from the command call to the function according to its type(default or multi string).

        :param link: The command call.
        Example: "!test testme" - Treat whitespace as trailing arguments, and split it accordingly, putting them
        into a list. Then, take the first element of that list, assume that its the command, and check and see
        if it exists in the registerdcommands. If it does, then depending on what type of command its registerd as,
        pass the contents of the list into the function as its arguments.

        :return: Attempt to return the result of executing the linked function. If the parameters in the command
        call are greater than or less than the function accepts, then return an error message. Otherwise, if
        the argument count of function is 0, assume the function takes no arguments, and simply execute the function
        and return its result. If it takes a single argument, then assume it is a multi string function and pass the
        rest of the list in as a single argument. Otherwise, pass in all the contents of the list into the function as
        its arguments.
        """
        if link is '':
            return None
        link_list = filter(None, link.split(" "))
        key_length = len(link_list[0]) + 1
        if link_list[0] in self.registeredcommands:
            arg_type = self.registeredcommands.get(str(link_list[0]).lower())[2]
            linked_function = self.registeredcommands.get(str(link_list.pop(0)).lower())[0]
            if linked_function:
                args = len(getargspec(linked_function).args)
                if len(link_list) < args:
                    return "Too few parameters (%s given, %s needed)" % (len(link_list), args)
                elif len(link_list) > args and arg_type is not "multi string" and arg_type is "default":
                    return "Too many parameters (%s given, %s needed)" % (len(link_list), args)
                else:
                    if args is 0:
                        return linked_function()
                    elif args is 1:
                        return linked_function(str(link[key_length:]))
                    else:
                        return linked_function(*link_list)
