import numpy as np

"""Parses a text file into pitchers and a goal"""
class Parser:
    def parse(self, path):
        """Main parse argument"""
        file = open(path, "r")
        lines = file.readlines()

        pitchers = np.array(list(map(int, self.formatter(lines[0], [" ", "\n"]))))
        target = int(lines[1])

        file.close()

        print(f"Pitchers: {pitchers}, Target volume: {target}")

        return (pitchers, target)
    
    def formatter(self,string, chars):   
        """Formats a string of pitchers by splitting them at the ','"""
        for c in chars:
            string.replace(c, "")
        return string.split(",")
