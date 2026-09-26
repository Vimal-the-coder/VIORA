from commands.desktop import execute_command


result = execute_command("open notepad")

if result:
    print(f"VIORA: {result}")
else:
    print("VIORA: Command not recognized.")