from cx_Freeze import setup, Executable



setup(name = 'MinutesToMidnight', 
      version='2.7', 
      description='',
      executables = [Executable('testing1.py',base="WIN32GUI")])
