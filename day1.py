def day1():
    sum_calibration_values = 0
    with open("input1_day1") as file:
        for line in file:
            line = line.rstrip()
            numbers = [int(s) for s in line if s.isdigit()]
            if len(numbers):
                calibration_value = numbers[0] * 10 + numbers[-1]
                sum_calibration_values = sum_calibration_values + calibration_value
    return sum_calibration_values


result = day1()
print(result)
