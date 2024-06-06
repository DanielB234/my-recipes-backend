from collections import Counter
from board.regex import get_word_count, tabulate_instructions_data

INSTRUCTIONS_AVERAGE_LENGTH = 31.17241379310345
INSTRUCTIIONS_AVERAGE_LENGTH_STANDARD_DEVIATION = 26.391920958406047
FREQUENT_WORD_COEFFICIENTS = [('bring', 2.1666666666666665), ('two', 2.2), ('bake', 2.2857142857142856), ('rise', 2.5), ('garnish', 2.5), ('cake', 2.5555555555555554), ('milk', 2.75), ('f', 2.75), ('set', 2.888888888888889), ('egg', 3.0), ('step', 3.0), ('plastic', 3.0), 
                              ('nearly', 3.0), ('choice', 3.0), ('cast', 3.0), ('iron', 3.0), ('heavy', 3.0), ('refrigerator', 3.2), ('brush', 3.3333333333333335), ('small', 3.4285714285714284), ('necessary', 3.5), ('slightly', 3.5), ('offset', 3.5), ('temperature', 3.6666666666666665), 
                              ('fry', 3.75), ('cool', 3.8), ('green', 4.0), ('pieces', 4.0), ('45', 4.0), ('spray', 4.0), ('softened', 4.0), ('serve', 4.2), ('add', 4.21875), ('vegetable', 4.333333333333333), ('surface', 4.5), ('pepperoni', 4.5), ('buttercream', 4.5), ('paper', 4.666666666666667), 
                              ('spices', 5.0), ('edges', 5.0), ('saucepan', 5.0), ('large', 5.3), ('mascarpone', 5.333333333333333), ('parchment', 5.5), ('speed', 5.5), ('sauce', 6.0), ('layer', 6.0), ('marinade', 6.0), ('continue', 6.0), ('excess', 6.0), ('reaches', 6.0), ('meanwhile', 6.0), 
                              ('510', 6.0), ('frequently', 6.0), ('tray', 6.0), ('drain', 6.0), ('aluminum', 6.0), ('stretch', 6.0), ('thin', 6.0), ('nonstick', 6.0), ('prepared', 6.0), ('begin', 6.0), ('beginning', 6.0), ('center', 6.0), ('cook', 6.444444444444445), ('ready', 6.5), 
                              ('bottom', 6.5), ('yolks', 6.5), ('mixture', 7.0), ('gently', 7.0), ('seasoning', 7.0), ('clean', 7.0), ('carefully', 7.0), ('internal', 7.0), ('rimmed', 7.0), ('roll', 7.0), ('metal', 7.0), ('divide', 7.0), ('sprinkle', 7.0), ('12inch', 7.0), ('swirl', 7.0), 
                              ('grand', 7.0), ('dip', 7.0), ('lid', 7.5), ('stir', 7.8), ('pour', 8.0), ('soy', 8.0), ('fire', 8.0), ('stone', 8.0), ('floured', 8.0), ('return', 8.0), ('melted', 8.0), ('color', 8.0), ('bun', 8.0), ('peaks', 8.0), ('tier', 8.0), ('remove', 9.0), ('golden', 9.0), 
                              ('mediumhigh', 9.0), ('½f', 9.0), ('preheated', 9.0), ('prepare', 9.0), ('attachment', 9.0), ('fully', 9.0), ('ladyfingers', 9.5), ('minutes', 9.636363636363637), ('simmer', 10.0), ('fold', 10.0), ('evenly', 10.0), ('immediately', 10.0), ('patty', 10.0), ('allow', 10.5), 
                              ('remaining', 11.0), ('browned', 11.0), ('ï', 11.0), ('refrigerate', 11.0), ('rack', 11.0), ('completely', 11.0), ('stand', 11.0), ('mixer', 11.0), ('seconds', 11.0), ('aside', 11.5), ('stirring', 12.0), ('sausage', 12.0), ('beat', 12.0), ('espresso', 12.0), ('bowl', 12.4), 
                              ('onto', 13.0), ('toss', 13.0), ('wok', 13.0), ('boil', 14.0), ('plate', 14.0), ('medium', 14.333333333333334), ('skillet', 14.5), ('optionally', 15.0), ('mixing', 15.0), ('heat', 16.0), ('top', 16.0), ('coat', 16.0), ('combined', 16.0), 
                              ('spatula', 16.0), ('season', 17.0), ('dog', 17.0), ('together', 18.0), ('preheat', 22.0), ('lightly', 22.0), ('transfer', 25.0), ('½', 13.0), ('whisk', 30.0), ('cover', 33.0), ('place', 45.0), ('combine', 59.0)]

def get_lower_bound(): # Instructions are likely to be reasonably long, 
    return INSTRUCTIONS_AVERAGE_LENGTH - INSTRUCTIIONS_AVERAGE_LENGTH_STANDARD_DEVIATION

def get_instruction_coefficient(list_set):
    list_set_without_steps = tabulate_instructions_data(list_set)
    joined_list_set = " ".join(list_set_without_steps)
    words = joined_list_set.split()
    unformatted_coefficient = 0
    for x in FREQUENT_WORD_COEFFICIENTS:
        for word in words:
            if word == x[0]:
                unformatted_coefficient += x[1]
    return (list_set_without_steps, unformatted_coefficient/(len(words)+1))

def exclude_instruction_outliers(list_set): # we can rule out very short lists for instructions
    list_element_word_counts = []
    for list_element in list_set:
        list_element_word_counts.append(get_word_count(list_element))
    return ((sum(list_element_word_counts))/(len(list_element_word_counts)+1)) > get_lower_bound()

def get_ingredient_coefficient(ingredient_list):
    ingredient_amount_counter = 0
    ingredient_unit_counter = 0
    for ingredient in ingredient_list:      
        if ingredient[0] is not None : ingredient_amount_counter += 1
        if ingredient[1] is not None : ingredient_unit_counter += 1
    return (ingredient_unit_counter+ingredient_amount_counter)/(len(ingredient_list)+1)
