age_to_flower = 7
age_to_fruit = 23
target_tuber = 15

for age in range(25):
    if age_to_flower <= age <= age_to_fruit:
        current_tuber = target_tuber * ( (age - age_to_flower) / 
                                        (age_to_fruit - age_to_flower) )
        #print((age - age_to_flower) / (age_to_fruit - age_to_flower) )
        print(current_tuber)