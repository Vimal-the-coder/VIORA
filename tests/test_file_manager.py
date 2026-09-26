from commands.file_manager import rename_path


result = rename_path(
    "VIORA_TEST_FOLDER/test.txt",
    "hello.txt"
)

print(f"VIORA: {result}")