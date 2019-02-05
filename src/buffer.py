
import select


class BufferHandler:

    def __init__(self):

        self._in_buffer = ''.encode()
        self._out_buffer = ''.encode()

    def receive(self, channel):

        ready_to_read, _, _ = select.select([channel], [], [], 0)
        if channel not in ready_to_read:
            return []

        self._in_buffer += channel.recv(4096)

        lines = self._in_buffer.split('\n'.encode())
        self._in_buffer = ''.encode()

        if len(lines[-1]) > 0:
            self._in_buffer += lines[-1]

        return list(map(lambda x: x.decode(), lines[:-1]))

    def send(self, channel, data):
        self._out_buffer += data.encode()

        _, ready_to_write, _ = select.select([], [channel], [], 0)
        if channel in ready_to_write:

            sent = channel.send(self._out_buffer)
            self._out_buffer = self._out_buffer[sent:]
