

def intro():
    print("Welcome to the Travelling Salesman Problem")
    isPredefined = input("Do you want to use a predefined dataset? (y/n): ")
    if isPredefined == "y":
        dataset = input("What dataset do you want to use? (0 for Berlin52, 1 for KroA100, 2 for Pr1002): ")
        match dataset:
            case "0":
                return "dataset/berlin52.tsp"
            case "1":
                return "dataset/kroA100.tsp"
            case "2":
                return "dataset/pr100.tsp"
            case _:
                print("Invalid input. Please run the program again.")
                return -1
    elif isPredefined == "n":
        filepath = input("Please enter the FULL file path to you tsp file: ")
        return filepath
    else:
        print("Invalid input. Please run the program again.")
        return -1






if __name__ == '__main__':
    dataset_file = intro()
    if dataset_file == -1:
        quit()
