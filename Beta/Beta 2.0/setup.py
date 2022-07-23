from cx_Freeze import setup, Executable

tar = Executable("pet.py",icon = "assets/icon.ico")

setup(name = "Dodogama" ,
      version = "0.2" ,
      description = "" ,
      options = {"build_exe": {"packages": ["tkinter","random","PIL"]}},
      executables = [tar])