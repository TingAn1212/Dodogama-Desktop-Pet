from win32api import GetMonitorInfo, MonitorFromPoint

def screen_size():
    monitor_info = GetMonitorInfo(MonitorFromPoint((0,0)))
    work_area = monitor_info.get("Work")
    return (work_area[2],work_area[3])

print(screen_size())