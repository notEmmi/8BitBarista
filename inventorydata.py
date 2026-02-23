# inventory
"""
three types of items:
- stackables (wheat)
- multi-tier tools (wood axe, copper hoe)
- non-stackables (ex: filled/empty buckets, fishing rod)
"""

# Initialize the inventory with empty slots
theInventory = [
    [None, None, None, None],
    [None, None, None, None],
    [None, None, None, None],
    [None, None, None, None],
]

def normalize_item_name(name: str) -> str:
    """Normalize item names by removing spaces and capitalizing."""
    return name.replace(" ", "").capitalize()

# Normalize item names in allowed shop items
allowed_shop_items = {normalize_item_name(item) for item in [
    "Wheat", "Corn", "Tomato", "Sugar", "CoffeeBeans", "TeaLeaves", "Milk", "Honey", "Cocoa"
]}

def baseItemString(item) -> str:
    if isinstance(item, tuple): return item[0]
    elif isinstance(item, str): return item
    else: return "Empty"

def itemStateString(item) -> str:
    # return item tier/bucket state if the item is non-stackable
    # else return quantity if item is stackable
    # else return unknown
    if isinstance(item, tuple):
        secondPart = item[1]
        if (isinstance(secondPart, int)): return "x" + str(secondPart)
        else: return "Unknown"
    else: return "Empty"

def parseInventoryItem(item) -> str:
    if isinstance(item, tuple): return itemStateString(item) + " " + baseItemString(item)
    elif isinstance(item, str): return item
    else: return "None"

def parseStacklessInventoryItem(item) -> str:
    if isinstance(item, tuple):
        if isinstance(item[1], int): return baseItemString(item)
    return parseInventoryItem(item)

def isTupleOrString(item) -> bool:
    if (not isinstance(item, tuple) and not isinstance(item, str)):
        print(f"the item {item} was not a tuple or a string!")
        return False
    return True

def isValidTuple(item) -> bool:
    if (not isinstance(item[1], int)): return False
    return True

def isInvalidName(item) -> bool:
    if (len(str(item)) < 1):
        print(f"the item you tried inserting was a string, but its name is empty!")
        return False
    return True

def isAllowedItem(item) -> bool:
    """Check if the item is allowed in the inventory."""
    if isinstance(item, tuple) and normalize_item_name(item[0]) in allowed_shop_items:
        return True
    elif isinstance(item, str) and normalize_item_name(item) in allowed_shop_items:
        return True
    return False

def putInSlot(item, row: int, column: int):
    """Place an item in a specific inventory slot if it is allowed."""
    if item is not None:
        if not isAllowedItem(item):
            print(f"Item {item} is not allowed in the inventory!")
            return None
        if not isTupleOrString(item):
            return None
        elif isinstance(item, tuple) and not isValidTuple(item):
            return None
        elif isinstance(item, str) and not isInvalidName(item):
            return None
    theInventory[row][column] = item
    print(f"Item {item} was placed in row {row} and column {column} of the inventory")

def hasEnoughOfItem(item) -> bool:
    if item is None: return False
    for row in range(len(theInventory)):
        for column in range(len(theInventory[row])):
            itemAt = theInventory[row][column]
            if itemAt is None: continue
            elif not isinstance(itemAt, tuple): continue
            elif not isinstance(itemAt[0], str): continue
            elif itemAt[0] != item[0]: continue
            elif isinstance(itemAt[1], int) and isinstance(item[1], int):
                if item[1] > itemAt[1]: return False
                else: return True
    return False

def quantityForItem(item) -> int:
    """Calculate the total quantity of an item in the inventory."""
    if item is None:
        return 0

    total_quantity = 0
    normalized_item_name = normalize_item_name(item[0]) if isinstance(item, tuple) else normalize_item_name(item)

    for row in theInventory:
        for slot in row:
            if slot is None:
                continue
            if isinstance(slot, tuple) and normalize_item_name(slot[0]) == normalized_item_name:
                if isinstance(slot[1], int):
                    total_quantity += slot[1]
            elif isinstance(slot, str) and normalize_item_name(slot) == normalized_item_name:
                total_quantity += 1  # Non-stackable items count as 1

    return total_quantity

def insertItemIntoSpareSlot(item):
    for row in range(len(theInventory)):
        for column in range(len(theInventory[row])):
            itemAt = theInventory[row][column]
            if itemAt is not None:
                if isinstance(item, tuple) and item[0] == itemAt[0] and isinstance(itemAt[1], int) and isinstance(item[1], int):
                    updatedQuantity = itemAt[1] + item[1]
                    putInSlot(None, row, column)
                    if (updatedQuantity > 0): putInSlot((item[0], updatedQuantity), row, column)
                    return
                else: continue
            elif quantityForItem(item) == 0:
                putInSlot(item, row, column)
                return