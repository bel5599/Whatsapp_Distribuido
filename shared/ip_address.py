class IPAddress:
    def __init__(self, *numbers: int):
        assert len(numbers) == 4 and all(
            0 <= n < 256 for n in numbers), "Invalid IP address"

        self._numbers = numbers

    @classmethod
    def from_string(cls, ip: str):
        numbers = [int(n) for n in ip.split(".")]
        return cls(*numbers)

    def __repr__(self):
        return ".".join([str(n) for n in self._numbers])

    def to_string(self):
        return self.__repr__()

    def __and__(self, other: "IPAddress"):
        return IPAddress(*[a & b for a, b in zip(self._numbers, other._numbers)])

    def __or__(self, other: "IPAddress"):
        return IPAddress(*[a | b for a, b in zip(self._numbers, other._numbers)])

    def __invert__(self):
        return IPAddress(*[~n+256 for n in self._numbers])
