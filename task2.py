file_name = "text_2_var_6"
with open(file_name) as file:
    lines = file.readlines()

average = list()
for line in lines:
    element_list = line.split(";")
    sum_element = 0

    for item in element_list:
        sum_element += int(item)

    average.append(sum_element)

with open('r_text_2_var_6.txt', 'w') as result:
    for value in average:
        result.write(str(value) + "\n")
