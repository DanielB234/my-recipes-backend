import psycopg2
import os

def connect():
    conn = psycopg2.connect(database=os.environ.get("DATABASE"), 
                            user=os.environ.get("USER"),
                            password=os.environ.get("PASSWORD"),
                            host=os.environ.get("HOST"))
    cur = conn.cursor()
    return conn, cur

def get_permutations(cur):
    cur.execute('''SELECT name FROM measurement_perms''')
    return cur.fetchall() 

def get_recipes(cur, recipe_id):
    cur.execute('''SELECT name, modifier FROM recipes WHERE id = %s;''',(recipe_id,))
    return cur.fetchall() 

def get_recipes_all(cur, recipe_id):
    cur.execute('''SELECT * FROM recipes WHERE id = %s;''',(recipe_id,))
    return cur.fetchall() 

def get_list_reference_position(cur, recipe_id):
    cur.execute('''SELECT MAX(position) FROM list_references WHERE recipe_id = %s;''',(recipe_id,))
    return cur.fetchall()


def get_ingredients_by_name(cur, recipe_id, name):
    cur.execute('''SELECT 
        ingredients.name,
        ingredients.name_full,
        ingredients.units,
        ingredients.amount,
        ingredients.amount_upper,
        recipes.serving_amount,
        recipes.modifier
      FROM ingredients 
      INNER JOIN recipes on ingredients.recipe_id = recipes.id
      WHERE ingredients.recipe_id = %s and ingredients.list_reference = %s''',
      (recipe_id,name))
    return cur.fetchall() 

def get_shopping_list(cur):
    cur.execute('''SELECT 
        ingredients.name
      FROM ingredients
      WHERE ingredients.shopping_list = true''',
      )
    return cur.fetchall() 

def get_ingredients(cur, recipe_id):
    cur.execute('''SELECT 
        DISTINCT list_references.name, 
        list_references.word_coefficient, 
        ingredients.list_reference,
        list_references.position
      FROM ingredients 
      INNER JOIN list_references on ingredients.list_reference = list_references.id
      WHERE ingredients.recipe_id = %s
      ORDER BY list_references.position ''',
      (recipe_id,))
    return cur.fetchall() 

def get_instructions_by_name(cur, recipe_id, name):
    cur.execute('''SELECT 
        instructions.context,
        instructions.position
      FROM instructions 
      WHERE instructions.recipe_id = %s and instructions.list_reference = %s
      ORDER BY instructions.position''',
      (recipe_id, name))
    return cur.fetchall() 

def get_instructions(cur, recipe_id):
    cur.execute('''SELECT 
        DISTINCT list_references.name, 
        list_references.word_coefficient, 
        instructions.list_reference,
        list_references.position
      FROM instructions 
      INNER JOIN list_references on instructions.list_reference = list_references.id
      WHERE instructions.recipe_id = %s
      ORDER BY list_references.position ''',
      (recipe_id,))
    return cur.fetchall() 

def create_recipe(cur, recipe):
    cur.execute('''INSERT INTO recipes 
        (id, name, serving, serving_amount, serving_units, preparation_time, cook_time, date, todo_list, image_url)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING;''',(recipe.id, recipe.name, recipe.serving, recipe.serving_amount, recipe.serving_units, recipe.preparation_time,recipe.cook_time, recipe.date, recipe.todo_list, ''))

def create_instruction(cur, instruction):
    cur.execute('''INSERT INTO instructions (id, position, context, list_reference, recipe_id)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;''',(instruction.id,instruction.position,instruction.context,instruction.list_reference, instruction.recipe_id))
            
def create_ingredient(cur,ingredient,modifier):
    amount = ingredient.amount/modifier if ingredient.amount != None else None
    amount_upper = ingredient.amount_upper/modifier if ingredient.amount_upper != None else None
    cur.execute('''INSERT INTO ingredients (id, name, amount, amount_upper, units, shopping_list, list_reference, recipe_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;''',(ingredient.id,ingredient.name, amount, amount_upper, ingredient.units,ingredient.shopping_list, ingredient.list_reference, ingredient.recipe_id))

def create_reference(cur,reference):
    cur.execute('''INSERT INTO list_references (id, name, word_coefficient, position, recipe_id)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;''',(reference.id,reference.name, reference.word_coefficient, reference.position,reference.recipe_id))
                  
def update_ingredient(cur,id,ingredients,modifier):
    amount = ingredients[0]/modifier if ingredients[0] != None else None
    amount_upper = ingredients[1]/modifier if ingredients[1] != None else None
    cur.execute('''UPDATE ingredients SET 
                amount = %s, 
                amount_upper = %s, 
                units = %s, 
                name = %s
                WHERE id = %s;''',(amount,amount_upper,ingredients[2],ingredients[3],id))
    
def delete_ingredient(cur,id):
    cur.execute('''DELETE FROM ingredients WHERE id=%s''',(id,))
    
def update_list_reference(cur,id,name):
    cur.execute('''UPDATE list_references SET 
                name = %s
                WHERE id = %s;''',(name,id))
    
def create_list_reference(cur,id,position, name,recipe_id):
    cur.execute('''INSERT INTO list_references (id, position, name, word_coefficient, recipe_id)
                VALUES (%s,%s,%s,%s,%s)''',(id,position,name,10,recipe_id))
    
def commit_and_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

def commit(conn):
    conn.commit()



    