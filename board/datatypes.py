import time
import uuid
from board.html_processing import get_path_base, get_html, get_soup
from board.regex import get_recipe_data

class Datatype:
    def __init__(self):
        self.id = str(uuid.uuid4())



class Recipe(Datatype):
    def __init__(self,id):
        self.id = id
        self.todo_list = False
        self.date = time.strftime('%Y-%m-%d %H:%M:%S')
    
    def set_name(self, url):
        self.name = get_path_base(url)
        self.name = self.name.replace("-"," ").title()

    def set_values(self,url):
        self.preparation_time, self.cook_time, self.serving, self.serving_amount, self.serving_units = get_recipe_data(get_soup(get_html(url)))


class Ingredient(Datatype):
    def __init__(self, data, list_reference, recipe_id):
        Datatype.__init__(self)
        self.name = data[3][:255]
        self.amount = data[0]
        self.amount_upper = data[1]
        self.units = data[2]
        self.shopping_list = False
        self.list_reference = list_reference
        self.recipe_id = recipe_id

class Instruction(Datatype):
    def __init__(self,position,context, list_reference, recipe_id):
        Datatype.__init__(self)
        self.position = position
        self.context = context
        self.list_reference = list_reference
        self.recipe_id = recipe_id

# List references bind together sets of instructions or ingredients, 
# as recipes may have several of each
class Reference(Datatype):
    def __init__(self, word_coefficient, name, position, recipe_id):
        Datatype.__init__(self)
        self.word_coefficient = word_coefficient
        self.name = name
        self.position = position
        self.recipe_id = recipe_id
