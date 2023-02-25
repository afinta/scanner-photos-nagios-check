import sys


def main(args):
    if len(sys.argv) == 2:
        name = sys.argv[1]
        print("Bye", name)
    else:
        print('wrong amount of arguments')
    
            
        

if __name__ == '__main__':
    main(sys.argv)