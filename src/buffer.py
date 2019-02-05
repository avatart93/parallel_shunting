
import select


class BufferHandler:

    def __init__(self):

        self._in_buffer = ''.encode()
        self._out_buffer = ''.encode()

    def receive(self, channel):
        """ Receives data over the socket 'channel', append it to previous data that was incomplete.
        Returns data received as a list of lines. Will perform such operation only if the socket is
         ready for reading. """

        # Verify if the socket is ready for reading.
        ready_to_read, _, _ = select.select([channel], [], [], 0)
        if channel not in ready_to_read:
            return []

        self._in_buffer += channel.recv(4096)  # Append to previous data.

        # Separate data into lines.
        lines = self._in_buffer.split('\n'.encode())
        self._in_buffer = ''.encode()

        # Re-store incomplete data.
        if len(lines[-1]) > 0:
            self._in_buffer += lines[-1]

        return list(map(lambda x: x.decode(), lines[:-1]))

    def send(self, channel, data):
        """ Sends data over the socket 'channel', it takes into account previous data that couldn't
         be sent. Will perform such operation only if the socket is ready for writing. """

        self._out_buffer += data.encode()  # Append to previous data.

        # Verify if the socket is ready for writing.
        _, ready_to_write, _ = select.select([], [channel], [], 0)
        if channel in ready_to_write:

            sent = channel.send(self._out_buffer)
            self._out_buffer = self._out_buffer[sent:]
