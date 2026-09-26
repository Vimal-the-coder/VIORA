from commands.app_launcher import open_app


result = open_app("CMD")

if result:
    print(f"VIORA: {result}")
else:
    print("VIORA: Application not found.")