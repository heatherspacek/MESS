from src.messlib.interfaces.host import Host
from src.messlib.interfaces.situation import goto

host = Host()
host.setup()

for _ in range(500):
    _ = host.console.step()

goto(0, 0, False, False, host)
