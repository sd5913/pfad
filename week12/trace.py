# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Local simulation of a host's permission check; NOT an MCP connection."""


def add(a: int, b: int) -> int:
    """Add exactly two integers, with no side effects."""
    if type(a) is not int or type(b) is not int:
        raise TypeError("a and b must be integers (not booleans)")
    return a + b


def check_call(name: str, arguments: object) -> str | None:
    """Return a refusal reason, or None if this host may dispatch the call."""
    if name != "add":
        return "blocked by host: only add is allowed; nothing dispatched"
    if not isinstance(arguments, dict) or set(arguments) != {"a", "b"}:
        return "invalid input: add needs exactly a and b; nothing dispatched"
    if any(type(arguments[key]) is not int for key in ("a", "b")):
        return "invalid input: a and b must be integers; nothing dispatched"
    return None


def simulate(name: str, arguments: object) -> str:
    """Apply host policy and call the local function, without any MCP server."""
    refusal = check_call(name, arguments)
    if refusal:
        return refusal
    return f"local function result: {add(arguments['a'], arguments['b'])}"


if __name__ == "__main__":
    for name, arguments in (
        ("add", {"a": 3, "b": 4}),
        ("overwrite", {"path": "work.txt"}),
        ("add", {"a": 3}),
        ("add", {"a": "3", "b": 4}),
    ):
        print(f"proposed {name}({arguments}) -> {simulate(name, arguments)}")
