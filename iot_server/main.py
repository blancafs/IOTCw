import os, sys

'''
Main method
Checks what commnand line arg was passed and starts testing or server
'''
def main(args):
    if len(args) > 1 and args[1]=='--testing':
        # run testing
        os.system('python3 lib/testing.py')
        pass
    else:
        os.system('python3 server.py')

if __name__ == '__main__':
    main(sys.argv)