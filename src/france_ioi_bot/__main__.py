from france_ioi.Account import *

def main():
    phpSessId: str = input("Please enter your PHPSESSID token: ")
    account = Account(phpSessId)
    if not account.hasSuccessfullyInitialized:
        print("Authentication failed!")
        exit(1)

    print(f"Continuing with user @{account.username}!")
    print(f"Enumerating tests...")
    levels = account.queryLevels()
    if levels is None:
        print("Failed to query levels!")
        exit(1)

    print(levels)



if __name__ == "__main__":
    main()
