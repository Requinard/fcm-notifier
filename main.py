import json

def main():
    try:
        configs = json.load(open("config.json"))
    except FileNotFoundError:
        print("There are no configs yet!")
        return 1

if __name__ == "__main__":
    main()