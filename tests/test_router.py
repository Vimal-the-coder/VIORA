from commands.router import route_command


result = route_command("open notepad")

if result:
    print(f"VIORA: {result}")
else:
    print("VIORA: Command not recognized.")