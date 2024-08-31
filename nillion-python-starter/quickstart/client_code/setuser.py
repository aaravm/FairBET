import sys

def set_user():
    if len(sys.argv) != 2:
        print("Usage: python verify_id.py <param1> <param2>")
        sys.exit(1)

    param1 = sys.argv[1]
    print(f"{param1}")
    return param1


if __name__ == "__main__":
    set_user()
