import json, socket, time, typing

class CGMinerAPI:
    """Thin wrapper around cgminer JSON API on localhost:4028."""

    def __init__(self, host: str = "127.0.0.1", port: int = 4028, timeout: float = 2.0):
        self.host = host
        self.port = port
        self.timeout = timeout

    def _query(self, payload: dict) -> typing.Any:
        line = json.dumps(payload) + "\n"
        with socket.create_connection((self.host, self.port), self.timeout) as sock:
            sock.sendall(line.encode())
            sock.shutdown(socket.SHUT_WR)
            data = sock.recv(4096)
        # cgminer sometimes sends multiple JSON dicts concatenated; split at }{ edge.
        if b"}{" in data:
            data = b"[" + data.replace(b"}{", b"},{") + b"]"
            return json.loads(data.decode())
        return json.loads(data.decode())

    def summary(self):
        return self._query({"command": "summary"})

    def get_work(self):
        """Ask cgminer for a work template (80-byte header + target).
        Only available when cgminer is connected to a pool."""
        return self._query({"command": "getwork"})

    def notify(self):
        return self._query({"command": "notify"}) 