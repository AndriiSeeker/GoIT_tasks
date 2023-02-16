def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "This note doesnt exist, please try again."
        except ValueError as exception:
            if exception.args:
                return exception.args[0]
            else:
                return "Value error"
        except IndexError:
            return "Wrong note number."
        except TypeError:
            return "Unknown command or parametrs, please try again."

    return inner
