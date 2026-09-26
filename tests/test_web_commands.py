from commands.web_commands import execute_web_command


result = execute_web_command("search for python programming")

if result:
    print(f"VIORA: {result}")
else:
    print("VIORA: Web command not recognized.")