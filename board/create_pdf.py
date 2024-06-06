# importing modules 
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from board.send_email import send_email
from board.data import commit_and_close, connect, get_recipes, get_ingredients, get_ingredients_by_name, get_instructions, get_instructions_by_name, get_shopping_list
import math

ACCEPTABLE_DENOMINATORS = [9, 8, 7, 6, 5, 4, 3, 2, 1]
MAX_DISTANCE_TO_NUMERATOR = 0.0001

def get_recipe_data(recipe_id):
    conn, cur = connect()
    recipe = get_recipes(cur,recipe_id)
    ingredients_names = get_ingredients(cur,recipe_id)
    ingredients = []
    for ingredient_name in ingredients_names:
        ingredients.append(get_ingredients_by_name(cur,recipe_id,ingredient_name[2]))
    instructions_names = get_instructions(cur,recipe_id)
    instructions = []
    for instruction_name in instructions_names:
        instructions.append(get_instructions_by_name(cur,recipe_id,instruction_name[2]))
    commit_and_close(conn,cur)
    return recipe, ingredients_names, instructions_names, ingredients, instructions

def create_pdf(recipe_id):
    recipe, ingredient_names, instruction_names, ingredients, instructions = get_recipe_data(recipe_id)
    flowables = []
    sample_style_sheet = getSampleStyleSheet()
    custom_style = sample_style_sheet['BodyText']
    custom_style.fontSize = 15
    title_style = sample_style_sheet['Heading1']
    title_style.fontSize = 28
    title_style2 = sample_style_sheet['Heading2']
    title_style2.fontSize = 22
    new = Paragraph(recipe[0][0],title_style)
    flowables.append(new)
    new = Paragraph("",custom_style)
    flowables.append(new)
    new = Paragraph("Ingredients:",title_style2)
    flowables.append(new)
    for list_set, ingredient_set in enumerate(ingredients):
        new = Paragraph("",custom_style)
        flowables.append(new)
        if len(str(ingredient_names[list_set][0])) > 4:
            new = Paragraph("<b>"+str(ingredient_names[list_set][0])+"</b>",custom_style)
            flowables.append(new)
        for ingredient in ingredient_set:
            if ingredient[3] is not None:
                scaled_ingredient = ingredient[3]*recipe[0][1]
            else: scaled_ingredient = None
            new = Paragraph(number_to_fraction_string(scaled_ingredient) + space_if_exists(ingredient[2]) + ingredient[0],custom_style)
            flowables.append(new)
    new = Paragraph("",custom_style)
    flowables.append(new)
    new = Paragraph("Instructions:",title_style2)
    flowables.append(new)
    for list_set, instructions_set in enumerate(instructions):
        new = Paragraph("",custom_style)
        flowables.append(new)
        if len(str(instruction_names[list_set][0])) > 4:
            new = Paragraph(str("<b>"+str(instruction_names[list_set][0])+"</b>"),custom_style)
            flowables.append(new)
        for instructions in instructions_set:
            new = Paragraph(str(instructions[1]) + ". " + instructions[0],custom_style)
            flowables.append(new)

    document = SimpleDocTemplate(recipe[0][0] + '.pdf')
    document.build(flowables)
    send_email(recipe[0][0] + '.pdf')

def create__shopping_list_pdf():
    conn, cur = connect()
    ingredients = get_shopping_list(cur)
    commit_and_close(conn,cur)
    flowables = []
    sample_style_sheet = getSampleStyleSheet()
    custom_style = sample_style_sheet['BodyText']
    custom_style.fontSize = 13
    title_style = sample_style_sheet['Heading2']
    title_style.fontSize = 18
   
    new = Paragraph("Shopping List",title_style)
    flowables.append(new)
    new = Paragraph("",custom_style)
    flowables.append(new)
    for ingredient in ingredients:
        new = Paragraph(ingredient[0].title(),custom_style)
        flowables.append(new)

    document = SimpleDocTemplate('Shopping List.pdf')
    document.build(flowables)
    send_email('Shopping List.pdf')


# Convert float values to presentable fractions, 
def number_to_fraction_string(n):
    if n == None:
      return ""
    if n == 0:
        return ""
    negative = (n < 0)
    if negative:
        n = -n
    whole_part = math.floor(n)
    n -= whole_part
    denom = 1
    if n == 0:
        return str(whole_part) + " "
    for d in ACCEPTABLE_DENOMINATORS:
        if abs(d*n - round(d*n)) <= MAX_DISTANCE_TO_NUMERATOR:
            denom = d
    numer = round(denom * n)
    if (denom == 1):
        return "" + str((whole_part + numer) * ( -1 if negative else 1)) + " "
    return ( "-" if negative else  "") + (str(whole_part) + " " if whole_part > 0 else "") + str(numer) + "/" + str(denom) + " "

def space_if_exists(s):
  if (s == ""):
    return ""
  else:
    return s + " "
  