
import os
import time


def verify_dir(path, like='dir', append=''):
    """ Verifies that 'path' points to an existing directory regardless its pointing an existing file
    or not. """

    if path is not None:

        folder = os.path.split(path)[0] if like is 'file' else path

        if not os.path.isdir(folder):
            return "Invalid path."

        return path + append


def manage_message(logs_fd, verbose, text, timestamp=True):
    """ Writes 'text' to a log if 'log_fd' was provided and prints it out if 'verbose'.
     Also adds a timestamp. """

    message = text if not timestamp else "{0}: {1}".format(time.asctime(), text)

    if logs_fd is not None:
        logs_fd.write(message + '\n')

    if verbose:
        print(message)
