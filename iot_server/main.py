import os, sys
path = os.path.dirname(os.path.realpath(__file__))


'''
Main method
Checks what commnand line arg was passed and starts testing or server
'''
def main(args):
    if len(args) > 1 and args[1]=='--testing':
        import lib.testing
    else:
        command = 'python3 '+path+'/lib/server.py'
        os.system(command)

if __name__ == '__main__':
    main(sys.argv)