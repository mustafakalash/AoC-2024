import math

def is_safe(report, dampened = False):
    sign = None
    safe = True
    for i in range(len(report) - 1):
        a = int(report[i])
        b = int(report[i + 1])
        diff = a - b

        if sign is not None and sign != math.copysign(1, diff):
            safe = False

        sign = math.copysign(1, diff) 
        diff = abs(diff)

        if diff < 1 or diff > 3:
            safe = False
        
    if dampened and not safe:
        for i in range(len(report)):
            dampened_report = report.copy()
            dampened_report.pop(i)
            if is_safe(dampened_report):
                return True

    return safe

with open("2/input") as f:
    reports = f.readlines()
    
    safe_reports = 0
    dampened_safe_reports = 0
    for report in reports:
        report = report.strip().split(" ")
        if is_safe(report):
            safe_reports += 1
        if is_safe(report, True):
            dampened_safe_reports += 1

    print(f"Part 1: {safe_reports}\nPart 2: {dampened_safe_reports}")
