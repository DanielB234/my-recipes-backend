import uuid
import json
from board.list_analysis import get_ingredient_coefficient, get_instruction_coefficient, exclude_instruction_outliers
from board.regex import tabulate_ingredients_data
from board.html_processing import MyHTMLParser, get_header, get_html, get_lists
from board.data import commit_and_close, connect, create_list_reference, delete_ingredient, get_list_reference_position, get_permutations, get_recipes, update_ingredient, update_list_reference
from board.datatypes import Recipe, Ingredient, Instruction, Reference
from board.data import create_recipe, create_ingredient, create_instruction, create_reference

def get_uuid():
    return str(uuid.uuid4())

def create_recipes(cur, url,recipe_id):
    recipe = Recipe(recipe_id)
    recipe.set_name(url)
    recipe.set_values(url)
    create_recipe(cur, recipe)
    return recipe.id

def create_instructions(cur, annotated_instructions, recipe_id, parser):
    
    sorted_instructions = sorted(annotated_instructions, key=lambda tup: tup[1])
    sorted_instructions.reverse()
    for default_name, (document_list, coefficient, index),  in enumerate(sorted_instructions):
        if coefficient > 0.5 or (default_name == 0):
            header = get_header(parser, document_list[0])
            header = "" if len(header) < 4 else header
            reference = Reference(coefficient, header, index, recipe_id)
            create_reference(cur,reference)
            for position,  list_element in enumerate(document_list):
                instruction = Instruction(position+1, list_element, reference.id, recipe_id)
                create_instruction(cur, instruction)
    

def create_ingredients(cur, annotated_ingredients, recipe_id, parser):
    selected_ingredients = []
    for default_name, (document_list, coefficient, element) in enumerate(annotated_ingredients):
        selected_ingredients.append(0)
        if coefficient > 0.3:
            selected_ingredients[-1] = 0.7
            header = get_header(parser, element[0])
            header = "" if len(header) < 4 else header
            reference = Reference(coefficient, header, default_name, recipe_id)
            create_reference(cur,reference)
            for list_element in document_list:
                ingredient = Ingredient(list_element, reference.id, recipe_id)
                create_ingredient(cur, ingredient, 1)
    return selected_ingredients

# Scrape data from the web url, 
def compile_data(url,recipe_id):
    conn, cur = connect()
    html = get_html(url)
    recipe_id = create_recipes(cur, url,recipe_id)
    unordered_lists = get_lists(html,'ul')
    parser = MyHTMLParser()
    parser.feed(html)
    permutations = get_permutations(cur)
    annotated_ingredients = []
    for element in unordered_lists:
        ingredients = tabulate_ingredients_data(element, permutations)
        annotated_ingredients.append((ingredients, get_ingredient_coefficient(ingredients),element))
    selected_ingredients = create_ingredients(cur, annotated_ingredients, recipe_id, parser)
    ordered_lists = get_lists(html,'ol')
    annotated_instructions = []
    index_ordered = 0
    for index, element in enumerate(ordered_lists):
        if exclude_instruction_outliers(element) == True:
            test = (get_instruction_coefficient(element)[0],get_instruction_coefficient(element)[1]+0.25,index)
            annotated_instructions.append(test)
            index_ordered = index
    for index, element in enumerate(unordered_lists):
        if exclude_instruction_outliers(element) == True:
            test = (get_instruction_coefficient(element)[0],get_instruction_coefficient(element)[1]-selected_ingredients[index],index+index_ordered)
            annotated_instructions.append(test)
    create_instructions(cur, annotated_instructions, recipe_id, parser)
    commit_and_close(conn,cur)
    return recipe_id

def save_ingredient_set(recipe_id,list_reference,ingredients_data):
    conn, cur = connect()
    modifier = get_recipes(cur,recipe_id)[0][1]
    ingredients = json.loads(ingredients_data)
    data = get_list_reference_position(cur,recipe_id)[0][0]
    print(data)
    print(ingredients_data)
    data = data+1 if data is not None else 1
    id_set = []
    ingredient_set = []
    for key, value in ingredients.items():
        if key == "name":
            if list_reference == "0":
                list_reference = get_uuid()
                create_list_reference(cur,list_reference,data+1,value,recipe_id)
            else:
                update_list_reference(cur,list_reference,value)
        else:
            id_set.append(key)
            ingredient_set.append(value)
    
    permutations = get_permutations(cur)
    tabulated_ingredients = tabulate_ingredients_data(ingredient_set,permutations)
    for index, ingredient in enumerate(tabulated_ingredients):
        if int(id_set[index]) <= 0:
            ingredient_new = Ingredient(ingredient,list_reference,recipe_id)
            create_ingredient(cur,ingredient_new,modifier)
        elif ingredient_set[index] == "":
            delete_ingredient(cur,id_set[index])
        else:
            update_ingredient(cur,id_set[index],ingredient,modifier)
    commit_and_close(conn,cur)

