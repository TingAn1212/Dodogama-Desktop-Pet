from cx_Freeze import setup, Executable

target = Executable("pet.py",icon = "assets/icon.ico",base = "Win32GUI")

setup(name = "Dodogama" ,
      version = "0.3" ,
      description = "" ,
      options = {"build_exe": {"packages": ["tkinter","random","PIL","threading","pystray"]}},
      executables = [target])
