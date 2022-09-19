#!/usr/bin/env python3

import platform, os

if platform.system() == "Windows":
    os.system("make.bat html")
else:
    # Assume Unix-based
    os.system("make html")
