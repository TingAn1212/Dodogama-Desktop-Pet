from cx_Freeze import setup, Executable

target = Executable("Dodogama.py",icon = "assets/icon.ico",base = "Win32GUI")

setup(name = "Dodogama" ,
      version = "1.3" ,
      description = "A windows dodogama pet made with python " ,
      options = {"build_exe": {"packages": ["tkinter","random","PIL","threading","pystray","playsound","win32api"]}},
      executables = [target])
