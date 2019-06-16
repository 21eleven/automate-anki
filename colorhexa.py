import sys
if __name__ == "__main__":
    if len(sys.argv) == 2:
        color = sys.argv[1]
        print(color)
    else:
        print(sys.argv)
