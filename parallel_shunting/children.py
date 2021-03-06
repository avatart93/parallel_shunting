
import multiprocessing


class ChildrenHandler:
    """ This class will handle all children processes that run the target function. Will maintain all
     children organized according with their availability. """

    def __init__(self, children_count, func):

        self._pipes_for_send = []
        self._pipes_working = []
        self._pipes_for_receive = []

        # Launch children processes with one end of a pipe.
        for number_id in range(children_count):

            pipe_a, pipe_b = multiprocessing.Pipe()
            self._pipes_for_send.append(pipe_a)  # Store the other ends.

            child = multiprocessing.Process(name="child_{0}".format(number_id),
                                            target=ChildrenHandler._child_process,
                                            args=[func, pipe_b])
            child.start()

    @staticmethod
    def _child_process(func, pipe, answer_rule="{0}={1}\n"):
        """ Child process of the serve that will process all data received through 'func'. """

        while True:
            try:
                data = pipe.recv()
                result = func(data)
                pipe.send(answer_rule.format(data, result))
            except EOFError:
                # Server closed and leave expecting data.
                break

    def can_send(self):
        """ Says if at least one of the children is waiting for data. """

        return len(self._pipes_for_send) > 0

    def working(self):
        """ Says if at least one of the children is still working. """

        return len(self._pipes_working) > 0

    def can_receive(self):
        """ Says if at least one of the children is waiting to deliver an answer. """

        return len(self._pipes_for_receive) > 0

    def send(self, data):
        """ Sends 'data' to be processed by one of the idle children. """

        pipe = self._pipes_for_send.pop(0)
        pipe.send(data)
        self._pipes_working.append(pipe)

    def receive(self):
        """ Receives an answer from one of the children that finished its work. """

        pipe = self._pipes_for_receive.pop(0)
        result = pipe.recv()
        self._pipes_for_send.append(pipe)
        return result

    def update_receiving(self):
        """ Detects when a children is ready to give an answer. """

        ready = multiprocessing.connection.wait(self._pipes_working, 0)
        for pipe in ready:
            self._pipes_working.remove(pipe)
            self._pipes_for_receive.append(pipe)
