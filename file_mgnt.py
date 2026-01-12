class FileManager:
    def write_data(self, text):
        with open("data.txt", "a") as file:
            file.write(text + "\n")

    def read_data(self):
        with open("data.txt", "r") as file:
            print(file.read())

fm = FileManager()
fm.write_data("Hello File")
fm.read_data()
