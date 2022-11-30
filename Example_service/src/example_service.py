import os;

if __name__ == '__main__':
    print("Starting waitress")
    os.system("waitress-serve --port=3466 app2:app2")
    # Add code here
