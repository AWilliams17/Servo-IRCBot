from inspect import getargspec


class CommandHandler(object):
    def __init__(self):
        """
        This dictionary contains the following:
        A command string, which is the key, the values of which are:
            command_description - An optional description describing what the command does. If no description is given
            during registration of the command, then it defaults to "No description given."

            arg_type - An optional parameter which is used to determine how to treat incoming command calls.
            If the arg_type is set to "multi string", then it will assume that everything after the
            command_string in the message is the argument to be used in the registered function, and it
            passes it as such to the function. If the argument type is default, then it treats everything
            after the command string as separate parameters, and passes them into the function as such.

            EG, assume !test is of arg_type default, and takes a single argument. If the call were
                !test param1 param2
            Then the function paired to !test will have param1 and param2 passed to it, resulting in
            an error message being returned due to the function not being able to accept the
            extra parameter in the function call.

            But, if !test is of arg_type multi string, and takes a single argument, then if the call were
                !test double dundee ducker
            Then the function associated with !test will have "double dundee ducker" passed into the
            command call.
        """
        self.registeredcommands = {}

    def registercommand(self, command_string, command_description="No description given.", arg_type="default"):
        """
        This function takes the desired command string, description, and arg type, and then if it is
        a valid command string, the information is paired with a decorated function, via the registeredcommands
        dictionary.

        :param command_string: The desired string used to call the command. EG: !test will execute the function
        which is associated with !test in the dictionary.
        :param command_description: An optional value used to describe the command's actions.
        :param arg_type: An optional value used to figure out how to pass arguments to a decorated function.
        :return: Returns the decorated function.
        """
        if command_string is "":
            raise ValueError("Can't define a command with no command string")

        def decorator(f):
            """
            Take the function being decorated, and pair it with the information gathered above. Store the
            result in the registeredcommands dictionary.
            :param f: The function being paired with the command call.
            :return: Return the function.
            """
            self.registeredcommands[str(command_string).lower()] = [f, command_description, arg_type]
            return f
        return decorator

    def serve(self, link):
        """
        This function is used to check potential incoming command calls for any valid registered command strings.
        If a command string is found, then it attempts to execute the function paired with it, passing in
        arguments as needed.

        Anything trailing the command string in the message is to be assumed to be arguments, and are treated as such,
        with how they are passed into the function being determined by the arg_type parameter.
        :param link:
        :return:
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
                if len(link_list) < args and arg_type is not "optional":
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
