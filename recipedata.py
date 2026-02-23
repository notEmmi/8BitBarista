# items
# Updated recipes with reduced ingredient quantities
theRecipes = {
    "Sweet Coffee": [("Coffee Beans", 3), ("Sugar", 2), ("Milk", 4)],
    "Tea Cake": [("Wheat", 1), ("Tea Leaves", 3), ("Sugar", 2), ("Milk", 4)],
    "Honey Cornbread": [("Corn", 1), ("Honey", 4), ("Milk", 4)],
    "Tomato Jam": [("Tomato", 2), ("Sugar", 2)],
    "Hot Chocolate": [("Cocoa", 5), ("Milk", 4), ("Sugar", 2)],
}

def parseIngredients(ingredients: list) -> str:
    ingredientString = ""
    for ingredientAndAmount in ingredients:
        ingredientString = ingredientString + " " + str(ingredientAndAmount[1]) + "x " + ingredientAndAmount[0]
    return ingredientString[1:]

def getFirstTwoIngredients(ingredients: list) -> list:
    if (len(ingredients) < 2): return ingredients[0]
    return ingredients[0:2]