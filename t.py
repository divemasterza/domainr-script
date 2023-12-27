def test_file_creation():
    try:
        with open('testfile.txt', 'w') as file:
            file.write('This is a test.')
        print("Test file created successfully.")
    except Exception as e:
        print(f"Error creating test file: {e}")


test_file_creation()
