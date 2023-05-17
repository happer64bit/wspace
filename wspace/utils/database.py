import os
import sys
import json

class Initialize:
    def __init__(self) -> None:
        pass

    def __create__(self) -> None:
        isExist = os.path.exists(".wspace")
        
        if not isExist:
            os.mkdir(".wspace/")
            with open(".wspace/keys.json", "w") as f:
                f.write("{")
                f.write('"maps": []')
                f.write("}")
                f.close()
            return True
        
        return False