import pygame, inventorydata, os # type: ignore [this is so vscode doesn't yell at me]

def run(gameInstance):
    # Initialize Pygame
    pygame.init()

    # Screen Configuration
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("INVENTORY")

    # Colors
    LIGHT_BROWN = (99, 55, 44)  # Outer Background
    DARK_BROWN = (38, 35, 34)  # Middle Dark Background
    BROWN = (99, 55, 44)  # Inner Panel Color
    WHITE = (255, 255, 255)
    BRIGHT_BROWN = (143, 89, 68)
    BRIGHTEST_BROWN = (201, 125, 96)

    # Fonts
    titleText = pygame.font.Font(pygame.font.match_font('courier'), 45)
    stackSizeText = pygame.font.Font(pygame.font.match_font('courier'), 24)
    buttonText = pygame.font.Font(pygame.font.match_font('courier'), 18)
    smallText = pygame.font.Font(pygame.font.match_font('courier'), 18)

    renderedInventorySlots = {}

    # Bottom menu buttons
    menuButtons = {
        "BACK": pygame.Rect(WIDTH // 2 - 40, 485, 80, 30),
        "DELETE": pygame.Rect(WIDTH - 200, 85, 80, 30)
    }

    # Function to draw a toggle
    def drawInventorySlot(itemName, xPos, yPos, rowInt, columnInt, rawData):
        length = 125
        height = 75
        buttonRect = pygame.Rect(xPos, yPos, length, height)
        if (itemSelectedOriginalX != rowInt or itemSelectedOriginalY != columnInt): pygame.draw.rect(screen, BRIGHT_BROWN, buttonRect, border_radius=7)
        else: pygame.draw.rect(screen, BRIGHTEST_BROWN, buttonRect, border_radius=7)
        # rect for collisionpoint, itemName for display, (row/column inven slot location), rawData
        renderedInventorySlots[str(xPos) + str(yPos)] = (buttonRect, itemName, (rowInt, columnInt), rawData)
        if (rawData == None): return
        filePath = "assets/images/tools/" + str.lower(str.replace(inventorydata.baseItemString(item), " ", "")) + ".png"
        if not os.path.isfile(filePath):
            filePath = "PROBABLY_ILLEGAL_ASSETS/" + str.lower(str.replace(inventorydata.baseItemString(item), " ", "")) + ".png"
        itemImage = pygame.image.load(filePath)
        itemImage = pygame.transform.scale(itemImage, (height, height))
        screen.blit(itemImage, (buttonRect.x + length // 4, buttonRect.y))
        stackSizeLabel = stackSizeText.render(str(rawData[1]), True, WHITE)
        screen.blit(stackSizeLabel, (xPos + (length // 2) + 15, yPos + (height - 20)))

    # Main Loop
    running = True
    itemSelected = None # filler data so the python file wont crash
    itemSelectedOriginalX = -1
    itemSelectedOriginalY = -1
    while running:
        screen.fill(LIGHT_BROWN)  # Outer Coffee Background
        
        # Middle Dark Background
        middle_rect = pygame.Rect(30, 20, WIDTH - 60, HEIGHT - 40)
        shadow_offset = 6
        shadow_surface = pygame.Surface((middle_rect.width, middle_rect.height), pygame.SRCALPHA)
        shadow_surface.fill((0, 0, 0, 0))  # Fully transparent
        pygame.draw.rect(shadow_surface, (20, 20, 20, 50), shadow_surface.get_rect(), border_radius=12)
        screen.blit(shadow_surface, (middle_rect.x + shadow_offset, middle_rect.y + shadow_offset))
        pygame.draw.rect(screen, DARK_BROWN, middle_rect, border_radius=12)
        
        # Inner Panel
        panel_rect = pygame.Rect(80, 50, 645, 500)
        shadow_surface_inner = pygame.Surface((panel_rect.width, panel_rect.height), pygame.SRCALPHA)
        shadow_surface_inner.fill((0, 0, 0, 0))  # Fully transparent
        pygame.draw.rect(shadow_surface_inner, (20, 20, 20, 50), shadow_surface_inner.get_rect(), border_radius=12)
        screen.blit(shadow_surface_inner, (panel_rect.x + shadow_offset, panel_rect.y + shadow_offset))
        pygame.draw.rect(screen, BROWN, panel_rect, border_radius=12)
        
        # Draw Title
        titleLabel = titleText.render("INVENTORY", True, WHITE)
        screen.blit(titleLabel, (WIDTH // 2 - titleLabel.get_width() // 2, 68.5))
        # Draw Current Selected
        chosenString = "None"
        if (itemSelected is not None): chosenString = inventorydata.parseStacklessInventoryItem(itemSelected)
        smallLabel = smallText.render(("Currently Selected: " + chosenString), True, WHITE)
        screen.blit(smallLabel, (WIDTH // 2 - smallLabel.get_width() // 2, 108.5))
        
        itemsPerRow = 4
        itemOnRow = 1
        xPosition = 100
        yPosition = 300 - (4 * 25) - 60
        rowInt = 0
        columnInt = 0
        for row in inventorydata.theInventory:
            for item in row:
                drawInventorySlot(inventorydata.parseInventoryItem(item), xPosition, yPosition, rowInt, columnInt, item)
                xPosition += 160
                itemOnRow += 1
                columnInt += 1
            if (itemOnRow > itemsPerRow):
                itemOnRow = 1
                columnInt = 0
                xPosition = 100
                yPosition += 85
                rowInt += 1

        # draw menuButtons
        for name, rect in menuButtons.items():
            pygame.draw.rect(screen, BRIGHT_BROWN, rect.inflate(9, 9), border_radius=14)
            pygame.draw.rect(screen, BRIGHTEST_BROWN, rect, border_radius=14)
            text = buttonText.render(name, True, WHITE)
            screen.blit(text, text.get_rect(center=rect.center))  # Outer button rectangle
            pygame.draw.rect(screen, BRIGHTEST_BROWN, rect, border_radius=8)  # Inner button rectangle
            text = buttonText.render(name, True, WHITE)
            screen.blit(text, text.get_rect(center=rect.center))

        # Event Handling
        mousePosition = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for name, rect in menuButtons.items():
                    if not rect.collidepoint(mousePosition): continue
                    if name == "BACK":
                        running = False
                        gameInstance.shop.sync_inventory_from_data()  # Sync inventory before returning to the shop
                        return gameInstance.run()
                    if name == "DELETE":
                        if itemSelected is not None:
                            # Lower the owned count for the item in the store
                            itemName = inventorydata.baseItemString(itemSelected)
                            normalizedName = inventorydata.normalize_item_name(itemName)
                            if normalizedName in gameInstance.shop.inventory:
                                gameInstance.shop.inventory[normalizedName] = 0
                                print(f"Set owned count for {itemName} to 0 in the store.")
                            # Delete the item from the inventory
                            inventorydata.putInSlot(None, itemSelectedOriginalX, itemSelectedOriginalY)
                            print(f"deleted {itemSelected}!")
                            itemSelected = None
                            itemSelectedOriginalX = -1
                            itemSelectedOriginalY = -1
                        else:
                            print("tried deleting items from an already empty slot.")
                    break
                # rect for collisionpoint, itemName for display, (row/column inven slot location), rawData
                # renderedInventorySlots[str(xPos) + str(yPos)] = (buttonRect, itemName, (rowInt, columnInt), rawData)
                for _, slotItemData in renderedInventorySlots.items():
                    inventorySlotRect = slotItemData[0]
                    if not inventorySlotRect.collidepoint(mousePosition): continue
                    clickedItemName = slotItemData[1]
                    clickedItemInvenX = slotItemData[2][0]
                    clickedItemInvenY = slotItemData[2][1]
                    clickedItemData = slotItemData[3]
                    if itemSelected is None and clickedItemData is not None:
                        itemSelected = clickedItemData
                        itemSelectedOriginalX = clickedItemInvenX
                        itemSelectedOriginalY = clickedItemInvenY
                        print(f"selected {clickedItemName}!")
                        break
                    elif itemSelected is not None:
                        # clear both inventory slots so no data loss happens
                        inventorydata.putInSlot(None, clickedItemInvenX, clickedItemInvenY)
                        inventorydata.putInSlot(None, itemSelectedOriginalX, itemSelectedOriginalY)
                        # swap item data between both slots
                        inventorydata.putInSlot(itemSelected, clickedItemInvenX, clickedItemInvenY)
                        inventorydata.putInSlot(clickedItemData, itemSelectedOriginalX, itemSelectedOriginalY)
                        itemSelected = None
                        itemSelectedOriginalX = -1
                        itemSelectedOriginalY = -1
                        break
        pygame.display.flip()

def drawBundle(screen) -> pygame.Rect:
    backpackImage = pygame.image.load("assets/buttons/backpack.png").convert_alpha()
    backpackImage = pygame.transform.scale(backpackImage, (70, 70))
    backpackImage.set_colorkey((0, 0, 0))
    rect = pygame.Rect(25, 505, 70, 70)
    screen.blit(backpackImage, rect)
    return rect