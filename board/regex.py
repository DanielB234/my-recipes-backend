import re
import unicodedata
from fractions import Fraction

# These expressions will detect any numerical expression including decimals and fractions
PLURALS_REGEX = '(?:\'s|s)?[^a-zA-Z]'
NUMBER_REGEX = '\d+(?:\.\d+)?'
SLASHED_FRACTION_REGEX = "(?:\d+\/\d+)"
VULGAR_FRACTION_REGEX = "[\u00BC-\u00BE\u2150-\u215E]"
FRACTION_REGEX = "(?:" + SLASHED_FRACTION_REGEX + "|" + VULGAR_FRACTION_REGEX +  ")"
FULL_NUMBER_REGEX = "((?:"+ NUMBER_REGEX + " *(?:\/ *(?:" + NUMBER_REGEX +"))? *" + FRACTION_REGEX + "?)|(?:" + FRACTION_REGEX + "?))"
START_REGEX = "(?:[^0-9\u00BC-\u00BE\u2150-\u215Ea-zA-Z])"

# we will optionally grab miscellaneous data with these expressions
PREPARATION_TIME_REGEX = "prep[A-Z: ]*(\d+)"
COOK_TIME_REGEX = "cook[ time]?[: ]*(\d+)"
SERVES_REGEX = "(serv(es|e|ing)?|makes|yield)[A-Z: ]*(\d+)( (cups?))?"

INSTRUCTIONS_REGEX = "(?:STEP \d+)(.*)"

def get_word_count(list_element): 
    return len(re.findall(r'\w+', list_element))

def get_recipe_data(html): # Here we grab the misc data
    preparation_time = re.findall(PREPARATION_TIME_REGEX,html.get_text(),re.IGNORECASE)
    cook_time = re.findall(COOK_TIME_REGEX, html.get_text(), re.IGNORECASE)
    serves = re.findall(SERVES_REGEX,html.get_text(), re.IGNORECASE)
    return preparation_time[0]if len(preparation_time) > 0 else None, cook_time[0] if len(cook_time) > 0 else None,serves[0][0] if len(serves) > 0 else "Serves", serves[0][2] if len(serves) > 0 else 1, serves[0][3] if len(serves) > 0 else ""

# Our database should contain 
def get_permutation_data(permutations):
    return [i[0] for i in permutations]

def process_regex(regex,context): # All regular expressions use this function
    return re.findall(regex,context,re.IGNORECASE)

# Here we are constructing the regular expression for interpreting ingredients
# This shall be comprised of: an amount (optional) an upper amount (optional)
# the units (optional) and the name of the ingredient (this is simply the rest of the expression)
# the ingredient '2-3 teaspoons sugar' contains all 4 of these
def get_regex(list_result): 
    perms_plural = [x + PLURALS_REGEX for x in list_result]
    perms_regex =  '(?:% s)' % '|'.join(perms_plural)
    return START_REGEX + "? *" + FULL_NUMBER_REGEX + " *(?:- *" + FULL_NUMBER_REGEX + ")? *(" + perms_regex + "?) *([^!]*)"

def numberify(i): # Here we will convert numbers detected by the Regex into floats
    number_string = "".join(i.rstrip().lstrip())
    if len(number_string) == 1: # Detect and convert unicode fractions (vulgar fractions) to floats
        v = float(number_string) if number_string.isdigit() else unicodedata.numeric(number_string)
    elif len(number_string) == 0:
        v=None
    elif "/" in number_string: # Convert fractions to floats
        v = float(sum(Fraction(s) for s in number_string.split()))
    elif number_string[-1].isdigit(): # A normal number, ending in [0-9]
        v = float(number_string)
    else: # Assume the last character is a unicode fraction
        v = float(number_string[:-1]) + unicodedata.numeric(number_string[-1])
    return v

# Where we process each ingredient
def process_raw_ingredients_data(ingredients_data,regex):
    captured_ingredients = []
    for ingredient in ingredients_data:
        capture = process_regex(regex,ingredient)
        # Some ingredients will be presented as something like '1 cup + 2 teaspoons'
        # this logic will extract both amounts and units
        if capture[0][-1].startswith("+"): 
            new_capture = re.findall(regex,capture[0][-1][1:],re.IGNORECASE)
            capture[0] = capture[0][:-1] + (new_capture[0][-1],)
            captured_ingredients.append(capture[0])
            captured_ingredients.append(new_capture[0])
        else:
            captured_ingredients.append(capture[0])
    return captured_ingredients

# This function is broadly responsible for detecting ingredients
def tabulate_ingredients_data(ingredients_data, permutations):
    # The database should contain a tables with every all possible units of ingredients,
    # such as tablespoon or gram or teaspoon, in all permutations like tbsp, g and tsp
    list_result = get_permutation_data(permutations)
    ingredients = []
    # We create a regular expression to capture the units
    final_params = [x + "[^\'s ]*" for x in list_result]
    last_params = '(?:% s)' % '|'.join(final_params)
    regex = get_regex(list_result)
    captured_ingredients = process_raw_ingredients_data(ingredients_data,regex)
    for list_element in captured_ingredients:
        measurement = numberify(list_element[0])
        upper_measurement = numberify(list_element[1]) if list_element[1]!='' else None
        unit_raw = list_element[2]
        unit = process_regex(last_params,unit_raw)[0] if unit_raw != '' else unit_raw
        # We arrange each ingredient into a tuple of (amount,amount_upper,unit,name)
        ingredients.append((measurement,upper_measurement,unit,list_element[-1]))
    return ingredients

def tabulate_instructions_data(list_set): # Remove any redundant ordering from the instructions
    list_set_without_steps = []
    try:
        for element in list_set:
            list_set_without_steps.append(re.findall(INSTRUCTIONS_REGEX,element,re.IGNORECASE)[0])
        return list_set_without_steps
    except IndexError:
        return list_set
    
