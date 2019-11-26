

class Debug:

    def log(self, string):
        G = "\033[1;32;40m"
        W = "\033[1;37;40m"
        N = "\033[0;37;40m"
        class_name = str(self.__class__.__name__)
        intro = '['+class_name+']'
        msg = G + intro + W + string + N

        print(msg)