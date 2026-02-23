import pygame, random, sys, recipedata, os, Recipes, inventorydata  # type: ignore

class InteractionsUI:
    def __init__(self, game_instance):
        pygame.init()
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.transparentSurface = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        pygame.display.set_caption("CUSTOMER INTERACTIONS")
        self.game = game_instance
        # Colors
        self.LIGHT_BROWN = (99, 55, 44)
        self.DARK_BROWN = (38, 35, 34)
        self.BROWN = (99, 55, 44)
        self.WHITE = (255, 255, 255)
        self.BRIGHT_BROWN = (143, 89, 68)
        self.BRIGHTEST_BROWN = (201, 125, 96)
        self.TRANSPARENT = (143, 89, 68, 0)
        self.GOLD = (255, 215, 0)  # Gold color for the gold display

        # Fonts
        self.titleText = pygame.font.Font(pygame.font.match_font('courier'), 45)
        self.buttonText = pygame.font.Font(pygame.font.match_font('courier'), 22)
        self.dialougeText = pygame.font.Font(pygame.font.match_font('courier'), 24)
        self.headerText = pygame.font.Font(pygame.font.match_font('courier'), 48)
        self.bodyText = pygame.font.Font(pygame.font.match_font('courier'), 20)
        self.font = pygame.font.Font(pygame.font.match_font('courier'), 18)  # For gold display

        # State variables
        self.currentScene = "interior"  # Skip the first page by starting at "interior"
        self.previousScene = "NONE"
        self.waitingResponse = None  # Removed "I'm still waiting..."
        self.acceptedResponse = "Thanks! You've got talent."
        self.rejectedResponse = "That sucks. I'll head out."
        self.orderAccepted = False
        self.running = True
        self.closed = False

        self.randomCustomerNames = [
            "Pheonix", "Riley", "Alex",  # Neutral names
            "Emma", "Liam", "Sophia"   # 3 girls, 3 boys
        ]
        random.shuffle(self.randomCustomerNames)  # Shuffle the list in place
        self.nameIndex = 0
        self.currentCustomerName = self.randomCustomerNames[self.nameIndex]  # Initialize with the first customer
        self.previousCustomerName = ""  # Track the previous customer for dialogue
        self.customerResponses = {
            "Pheonix": {
            "accepted": "Wow, this is amazing! You're a true \nartist.",
            "rejected": "Hmm, not quite what I expected. \nBetter luck next time."
            },
            "Riley": {
            "accepted": "This is perfect! Thank you so much!",
            "rejected": "Oh no, this isn't what I wanted.\nI'm disappointed."
            },
            "Alex": {
            "accepted": "Nice! This is exactly what I needed.\nYou're the best!",
            "rejected": "Ugh, this isn't good. I expected \nbetter."
            },
            "Emma": {
            "accepted": "This is delightful! You're so \ntalented!",
            "rejected": "Oh dear, this isn't what I was \nhoping for.I'm sad."
            },
            "Liam": {
            "accepted": "This is fantastic! You're a \ngenius!",
            "rejected": "Hmm, this isn't what I wanted.\nI'm not happy."
            },
            "Sophia": {
            "accepted": "This is wonderful! You're amazing!",
            "rejected": "Oh no, this isn't good.\nI'm disappointed."
            }
        }

        # Create a round coin icon for gold display
        self.coin_icon = pygame.Surface((25, 25), pygame.SRCALPHA)
        pygame.draw.circle(self.coin_icon, self.GOLD, (12, 12), 12)
        pygame.draw.circle(self.coin_icon, self.DARK_BROWN, (12, 12), 12, 1)

        self.mainButtons = {
            "Enter Shop": ("exterior", "interior", "PROBABLY_ILLEGAL_ASSETS/shop.png"),
            "Exit Shop": ("interior", "exterior", "PROBABLY_ILLEGAL_ASSETS/exit.png"),
            "Complete Order": ("customerOrder", "interior", "PROBABLY_ILLEGAL_ASSETS/check_button.png"),
            "Reject Order": ("customerOrder", "interior", "PROBABLY_ILLEGAL_ASSETS/x_button.png"),
            "Protagonist": ("interior", "", os.path.join(game_instance.SPRITE_PATH, game_instance.selected_character, "down_idle.png")),
            "Recipes": ("interior", "", "PROBABLY_ILLEGAL_ASSETS/recipe.png"),
        }
        self.renderedButtons = {}

        # Buttons
        self.menuButtons = {
            "QUIT": pygame.Rect(self.WIDTH // 2 - 150, 540, 80, 30),
            "Back to Garden": pygame.Rect(self.WIDTH // 2 - 20, 540, 200, 30)
        }

        # Take Order button
        self.take_order_button = pygame.Rect(0, 0, 160, 40)  # Wider button, will be positioned properly in run()
        self.take_order_button_visible = False

        self.listOfRecipes = list(recipedata.theRecipes.keys())
        self.currentOrder = ""
        print(f"currentOrder: {self.currentOrder}")
        print(f"currentCustomerName: {self.currentCustomerName}")

        self.generatedFakeAmounts = False
        self.notEnoughIngredients = False
        self.editedItemsAlready = False

        self.dialougeAnchorX = -60
        self.dialougeAnchorY = 275
        self.dialougeMaxWidth = 440
        self.dialougeMaxHeight = 110
        
        self.randomAmount = random.randint(100, 700)
        
        # For the shop panel reference in gold display
        self.shop_panel = pygame.Rect(30, 20, self.WIDTH - 60, self.HEIGHT - 40)
        
        # Gold UI position
        self.gold_bg = None

    def load_customer_portrait(self, customer_name):
        """Load a customer's portrait image"""
        try:
            portrait_path = os.path.join("PROBABLY_ILLEGAL_ASSETS", f"{customer_name.lower()}_portrait.png")
            portrait = pygame.image.load(portrait_path)
            # Scale to appropriate size for dialogue box
            portrait = pygame.transform.scale(portrait, (80, 80))
            return portrait
        except:
            # Fallback if portrait can't be loaded
            placeholder = pygame.Surface((80, 80), pygame.SRCALPHA)
            pygame.draw.circle(placeholder, self.BRIGHT_BROWN, (40, 40), 40)
            pygame.draw.circle(placeholder, self.DARK_BROWN, (40, 40), 40, 2)
            return placeholder

    def center_x(self, width):
        """Return x coordinate to center an element with given width"""
        return (self.WIDTH - width) // 2
    
    def center_y(self, height):
        """Return y coordinate to center an element with given height"""
        return (self.HEIGHT - height) // 2

    def update_gold_display(self):
        # Draw gold in the top right corner with round coin icon
        self.gold_bg = pygame.Rect(self.shop_panel.right - 120, self.shop_panel.top + 10, 100, 40)
        
        # Draw shadow
        shadow_rect = self.gold_bg.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        pygame.draw.rect(self.screen, self.DARK_BROWN, shadow_rect, border_radius=10)
        
        # Draw gold background
        pygame.draw.rect(self.screen, self.LIGHT_BROWN, self.gold_bg, border_radius=10)
        pygame.draw.rect(self.screen, self.DARK_BROWN, self.gold_bg, 2, border_radius=10)  # Border
        
        gold_surface = self.font.render(f"{self.game.gold}", True, self.GOLD)
        self.screen.blit(gold_surface, (self.gold_bg.x + 15, self.gold_bg.y + 10))
        self.screen.blit(self.coin_icon, (self.gold_bg.right - 30, self.gold_bg.y + 8))

    def drawMainButton(self, name, xPos, yPos, buttonInformation):
        length = 300
        buttonRect = pygame.Rect(xPos // 2 + 60, yPos, length // 2, length // 2)
        if name == "Enter Shop":
            buttonRect = buttonRect.scale_by(2).move(185, 50)
        elif name == "Exit Shop":
            buttonRect = buttonRect.scale_by(.5).move(-125, -95)
        elif name == "Complete Order" and not self.notEnoughIngredients:
            # Position at bottom right corner
            buttonRect = pygame.Rect((self.WIDTH - 60) // 2 - 40, self.HEIGHT - 130, 60, 60)
        elif name == "Reject Order":
            # Position at bottom left corner
            buttonRect = pygame.Rect((self.WIDTH - 60) // 2 + 40, self.HEIGHT - 130, 60, 60)
        elif name == "Protagonist":
            buttonRect = pygame.Rect(330, 220, 14 * 3, 29 * 3)
        elif name == "Recipes":
            buttonRect = pygame.Rect(self.WIDTH - 90, self.HEIGHT - 90, 64, 64)

        self.renderedButtons[name] = (buttonRect, buttonInformation[0], buttonInformation[1])

        if self.currentScene != buttonInformation[0]: return
        if name == "Complete Order" and self.notEnoughIngredients: return

        buttonImage = pygame.image.load(buttonInformation[2])
        buttonImage = pygame.transform.scale(buttonImage, (buttonRect.width, buttonRect.height))
        self.screen.blit(self.transparentSurface, (0, 0))
        pygame.draw.rect(self.transparentSurface, self.TRANSPARENT, buttonRect, border_radius=7)
        self.screen.blit(buttonImage, (buttonRect.x, buttonRect.y))

    def run(self):
        lost_money_animation = None  # Track the animation state for losing money
        lost_money_start_time = 0  # Track when the animation starts
        lost_money_y = 0  # Track the current y position of the animation
        waiting_for_click = False  # Track if waiting for user to dismiss dialogue

        while self.running:
            if self.currentScene == "customerOrder":
                if not self.currentOrder:  # Only set the order if it's not already set
                    self.currentOrder = random.choice(self.listOfRecipes)

                self.screen.fill(self.LIGHT_BROWN)
                middle_rect = pygame.Rect(30, 20, self.WIDTH - 60, self.HEIGHT - 40)
                shadow_offset = 6
                shadow_surface = pygame.Surface((middle_rect.width, middle_rect.height), pygame.SRCALPHA)
                shadow_surface.fill((0, 0, 0, 0))
                pygame.draw.rect(shadow_surface, (20, 20, 20, 50), shadow_surface.get_rect(), border_radius=12)
                self.screen.blit(shadow_surface, (middle_rect.x + shadow_offset, middle_rect.y + shadow_offset))
                pygame.draw.rect(self.screen, self.DARK_BROWN, middle_rect, border_radius=12)

                panel_rect = pygame.Rect(80, 50, 645, 500)
                shadow_surface_inner = pygame.Surface((panel_rect.width, panel_rect.height), pygame.SRCALPHA)
                shadow_surface_inner.fill((0, 0, 0, 0))
                pygame.draw.rect(shadow_surface_inner, (20, 20, 20, 50), shadow_surface_inner.get_rect(), border_radius=12)
                self.screen.blit(shadow_surface_inner, (panel_rect.x + shadow_offset, panel_rect.y + shadow_offset))
                pygame.draw.rect(self.screen, self.BROWN, panel_rect, border_radius=12)
                
                # Hide Take Order button in order screen
                self.take_order_button_visible = False

                # Ensure bootlegIngredients is initialized before use
                if not self.generatedFakeAmounts:
                    bootlegIngredients = []
                    self.notEnoughIngredients = False
                    for ingredient in recipedata.theRecipes.get(self.currentOrder):
                        have_quantity = inventorydata.quantityForItem(ingredient)
                        bootlegIngredients.append((ingredient[0], have_quantity))
                        if have_quantity < ingredient[1]:
                            self.notEnoughIngredients = True
                    self.generatedFakeAmounts = True

                # Header - centered properly
                headerLabel = self.headerText.render(self.currentOrder, True, self.WHITE)
                header_x = self.center_x(headerLabel.get_width())
                self.screen.blit(headerLabel, (header_x, 80))

                ingredients = recipedata.theRecipes.get(self.currentOrder)

                # Recipe image - positioned on left side
                recipeImage = pygame.image.load("PROBABLY_ILLEGAL_ASSETS/" + str.lower(self.currentOrder.replace(" ", "")) + ".png")
                recipeImage = pygame.transform.scale(recipeImage, (200, 200))
                recipe_x = 130
                recipe_y = self.center_y(200)
                self.screen.blit(recipeImage, (recipe_x, recipe_y))

                # Ingredients section - table layout
                ingredients_section_x = 380
                ingredients_section_y = 180
                
                # Ingredients header
                ingredients_header = self.bodyText.render("Ingredients:", True, self.WHITE)
                self.screen.blit(ingredients_header, (ingredients_section_x, ingredients_section_y))
                
                # Column headers
                need_x = ingredients_section_x + 180
                have_x = need_x + 80
                
                need_header = self.bodyText.render("Need", True, self.WHITE)
                have_header = self.bodyText.render("Have", True, self.WHITE)
                
                self.screen.blit(need_header, (need_x + 20, ingredients_section_y + 30))
                self.screen.blit(have_header, (have_x + 20, ingredients_section_y + 30))
                
                # Draw ingredients in rows
                row_height = 60
                img_size = 40
                
                for i, ingredient in enumerate(recipedata.theRecipes.get(self.currentOrder)):
                    row_y = ingredients_section_y + 70 + (i * row_height)
                    
                    # Load and display ingredient image
                    try:
                        img_path = "PROBABLY_ILLEGAL_ASSETS/" + str.lower(ingredient[0]).replace(" ", "") + ".png"
                        ingredient_img = pygame.image.load(img_path)
                        ingredient_img = pygame.transform.scale(ingredient_img, (img_size, img_size))
                        self.screen.blit(ingredient_img, (ingredients_section_x, row_y))
                    except:
                        # Fallback if image not found
                        placeholder = self.bodyText.render("?", True, self.WHITE)
                        self.screen.blit(placeholder, (ingredients_section_x + 15, row_y + 10))
                    
                    # Ingredient name
                    name_label = self.bodyText.render(ingredient[0], True, self.WHITE)
                    self.screen.blit(name_label, (ingredients_section_x + img_size + 10, row_y + 10))
                    
                    # Need amount
                    need_amount = self.bodyText.render(str(ingredient[1]), True, self.WHITE)
                    self.screen.blit(need_amount, (need_x + 20, row_y + 10))
                    
                    # Have amount
                    have_amount = inventorydata.quantityForItem(ingredient)
                    have_label = self.bodyText.render(str(have_amount), True, self.WHITE)
                    self.screen.blit(have_label, (have_x + 20, row_y + 10))

                # Render "Complete Order" button only if ingredients are sufficient
                if not self.notEnoughIngredients:
                    complete_order_button = pygame.Rect((self.WIDTH - 60) // 2 - 40, self.HEIGHT - 130, 60, 60)
                    self.renderedButtons["Complete Order"] = (complete_order_button, "customerOrder", "interior")
                else:
                    self.renderedButtons.pop("Complete Order", None)

            else:
                # Reset the order when leaving the customerOrder scene
                if self.previousScene == "customerOrder" and not waiting_for_click:
                    self.currentOrder = ""
                self.screen.fill(self.WHITE)
                bg = pygame.image.load("PROBABLY_ILLEGAL_ASSETS/cafe_bg_og.png")  # Updated background
                bg = pygame.transform.scale(bg, (self.WIDTH, self.HEIGHT))
                self.screen.blit(bg, (0, 0))
                
                # Show customer and Take Order button in interior scene
                if self.currentScene == "interior" and not waiting_for_click:
                    self.take_order_button_visible = True
                    
                    # Draw customer name above their head
                    customer_name_surface = self.buttonText.render(self.currentCustomerName, True, self.WHITE)
                    name_x = 400 - customer_name_surface.get_width() // 2  # Center above customer
                    name_y = 330  # Position slightly lower
                    
                    # Draw name background for better visibility
                    name_bg = pygame.Rect(name_x - 5, name_y - 5, 
                                         customer_name_surface.get_width() + 10, 
                                         customer_name_surface.get_height() + 10)
                    pygame.draw.rect(self.screen, self.DARK_BROWN, name_bg, border_radius=5)
                    
                    self.screen.blit(customer_name_surface, (name_x, name_y))
                    
                    # Draw customer image (not as a button) - same size as protagonist and lower position
                    try:
                        customer_img_path = os.path.join("PROBABLY_ILLEGAL_ASSETS", f"{self.currentCustomerName.lower()}.png")
                        customer_img = pygame.image.load(customer_img_path)
                        # Match protagonist size (14*3 x 29*3)
                        customer_img = pygame.transform.scale(customer_img, (14 * 3, 29 * 3))
                        customer_x = 400 - (14 * 3) // 2  # Center horizontally
                        customer_y = 370  # Position slightly lower
                        self.screen.blit(customer_img, (customer_x, customer_y))
                    except:
                        # Fallback if image can't be loaded
                        placeholder = pygame.Surface((14 * 3, 29 * 3), pygame.SRCALPHA)
                        pygame.draw.rect(placeholder, self.BRIGHT_BROWN, (0, 0, 14 * 3, 29 * 3), border_radius=5)
                        pygame.draw.rect(placeholder, self.DARK_BROWN, (0, 0, 14 * 3, 29 * 3), 2, border_radius=5)
                        self.screen.blit(placeholder, (customer_x, customer_y))
                    
                    # Position and draw Take Order button below customer image - wider button
                    self.take_order_button = pygame.Rect(320, 460, 160, 40)  # Wider button, positioned lower
                    pygame.draw.rect(self.screen, self.BRIGHT_BROWN, self.take_order_button, border_radius=5)
                    pygame.draw.rect(self.screen, self.DARK_BROWN, self.take_order_button, 2, border_radius=5)  # Border
                    
                    take_order_text = self.buttonText.render("Take Order", True, self.WHITE)
                    text_rect = take_order_text.get_rect(center=self.take_order_button.center)
                    self.screen.blit(take_order_text, text_rect)
                else:
                    self.take_order_button_visible = False

            # Main Buttons
            xOffset = 300 - (len(self.mainButtons) * 25)
            yPosition = xOffset
            for name, info in self.mainButtons.items():
                self.drawMainButton(name, xOffset, yPosition, info)
                if self.currentScene == info[0] and name != "Exit Shop":
                    xOffset += 350

            # Display gold in the top right corner
            if self.currentScene == "interior":
                self.update_gold_display()

            showDialogue = self.currentScene == "interior" and self.previousScene == "customerOrder"
            if self.currentScene == "customerOrder":
                # Store current customer name before potentially changing it
                self.previousCustomerName = self.currentCustomerName

            elif showDialogue:
                # Widen the dialogue box
                dialogue_width = self.dialougeMaxWidth + 200  # Increase width by 150
                dialogue_height = self.dialougeMaxHeight + 40  # Increase height by 50
                dialogue_x = 20  # Left side
                dialogue_y = self.HEIGHT - dialogue_height - 20  # Adjust for increased height

                # Draw dialogue box with smaller border
                dialougeBrownRectPseudoOutline = pygame.Rect(dialogue_x, dialogue_y, dialogue_width, dialogue_height)
                pygame.draw.rect(self.screen, self.BROWN, dialougeBrownRectPseudoOutline, border_radius=3)

                # Inner white rectangle with consistent padding
                padding = 10
                dialougeWhiteRect = pygame.Rect(
                    dialogue_x + padding, 
                    dialogue_y + padding, 
                    dialogue_width - (padding * 2), 
                    dialogue_height - (padding * 2)
                )
                pygame.draw.rect(self.screen, self.WHITE, dialougeWhiteRect, border_radius=3)

                # Dialogue text
                dialogue_name = self.previousCustomerName if (self.orderAccepted or not self.closed) else self.currentCustomerName
                text = dialogue_name + ":\n\""
                if self.orderAccepted:
                    text += self.customerResponses[dialogue_name]["accepted"]
                else:
                    text += self.customerResponses[dialogue_name]["rejected"]
                text += "\""

                dialogueLabel = self.dialougeText.render(text, True, self.BROWN)
                text_x = dialogue_x + (padding * 2) + 90  # Adjust for portrait
                text_y = dialogue_y + (padding * 2)
                self.screen.blit(dialogueLabel, (text_x, text_y))

                # Portrait remains inside the dialogue box
                portrait = self.load_customer_portrait(dialogue_name)
                portrait_x = dialogue_x + padding + 10
                portrait_y = dialogue_y + padding + 5
                self.screen.blit(portrait, (portrait_x, portrait_y))

                # # Happy or Sad icon - repositioned to align with the end of the dialogue text
                # iconImage = pygame.image.load("PROBABLY_ILLEGAL_ASSETS/happy.png" if self.orderAccepted else "PROBABLY_ILLEGAL_ASSETS/sad.png")
                # iconImage = pygame.transform.scale(iconImage, (40, 40))
                # icon_x = text_x + dialogueLabel.get_width() + 10  # Position to the right of the text
                # icon_y = dialogue_y + (dialogue_height - 40) // 2  # Centered vertically
                # self.screen.blit(iconImage, (icon_x, icon_y))

                # Add "Click to Continue" text for accepted/rejected dialogue
                if not self.closed:
                    click_to_continue = self.bodyText.render("Click to Continue", True, (0, 0, 0))
                    click_x = dialogue_x + dialogue_width - click_to_continue.get_width() - 20
                    click_y = dialogue_y + dialogue_height - click_to_continue.get_height() - 10
                    self.screen.blit(click_to_continue, (click_x, click_y))
                    waiting_for_click = True

                # Display money indicators below the gold UI
                if self.gold_bg and not self.closed:
                    if self.orderAccepted:
                        # Show gain amount below gold UI
                        gain_y = self.gold_bg.bottom + 10
                        gain_text = self.bodyText.render("+" + str(self.randomAmount), True, self.GOLD)
                        self.screen.blit(gain_text, (self.gold_bg.x + 15, gain_y))
                        
                        # Draw small coin icon
                        small_coin = pygame.Surface((20, 20), pygame.SRCALPHA)
                        pygame.draw.circle(small_coin, self.GOLD, (10, 10), 10)
                        pygame.draw.circle(small_coin, self.DARK_BROWN, (10, 10), 10, 1)
                        self.screen.blit(small_coin, (self.gold_bg.right - 30, gain_y))
                        
                        if not self.editedItemsAlready:
                            self.game.gold += self.randomAmount
                            self.editedItemsAlready = True
                    else:
                        # Show loss amount below gold UI
                        if not self.editedItemsAlready:
                            lost_money_animation = f"-{self.randomAmount}"  # Set the animation text
                            lost_money_start_time = pygame.time.get_ticks()  # Start the animation timer
                            lost_money_y = self.gold_bg.bottom + 10  # Initial y position
                            self.game.gold -= self.randomAmount
                            self.editedItemsAlready = True

                        # Handle the animation
                        if lost_money_animation:
                            elapsed_time = pygame.time.get_ticks() - lost_money_start_time
                            if elapsed_time < 2000:  # Show for 2 seconds
                                # Gradually move the text upward
                                lost_money_y -= 0.5  # Adjust the speed of upward movement
                                loss_text = self.bodyText.render(lost_money_animation, True, (200, 0, 0))  # Red for loss
                                loss_text_bold = pygame.font.Font(pygame.font.match_font('courier', bold=True), 20)
                                bold_loss_text = loss_text_bold.render(lost_money_animation, True, (200, 0, 0))
                                self.screen.blit(bold_loss_text, (self.gold_bg.x + 15, lost_money_y))
                            else:
                                lost_money_animation = None  # Clear the animation after 2 seconds


            # Event Handling
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()  # Ensure pygame.quit() is called only when exiting the program
                    sys.exit()  # Exit the program safely
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Handle Take Order button click
                    if self.take_order_button_visible and self.take_order_button.collidepoint(mouse_pos):
                        print("Take Order button clicked!")
                        self.previousScene = self.currentScene
                        self.currentScene = "customerOrder"
                        continue
                        
                    # Handle click to dismiss dialogue
                    if waiting_for_click and not self.closed:
                        waiting_for_click = False
                        # Change to next customer
                        self.nameIndex += 1
                        if self.nameIndex >= len(self.randomCustomerNames):
                            self.nameIndex = 0
                            random.shuffle(self.randomCustomerNames)
                        self.currentCustomerName = self.randomCustomerNames[self.nameIndex]

                        # Reset for next order
                        self.currentOrder = random.choice(self.listOfRecipes)
                        self.randomAmount = random.randint(100, 700)
                        self.generatedFakeAmounts = False
                        self.notEnoughIngredients = False
                        self.editedItemsAlready = False
                        self.previousScene = self.currentScene
                        self.currentScene = "interior"
                        continue
                        
                    # Handle other button clicks
                    for name, info in self.renderedButtons.items():
                        if not (info[0].collidepoint(mouse_pos) and self.currentScene == info[1]): continue
                        if name == "Recipes": 
                            Recipes.Recipes(cafe_instance=self).run()  # Pass the current instance as the cafe
                        elif name == "Exit Shop":
                                print("Returning to game...")
                                self.running = False  # You can swap this to a callback to your Game instance
                                self.game.run()
                                break
                        elif info[2] != "":
                            print(f"{name} clicked! switching scene to {info[2]}")
                            self.closed = True
                            if name == "Reject Order" or name == "Complete Order":
                                if name == "Complete Order" and self.notEnoughIngredients:
                                    print(f"NOT ENOUGH INGREDIENTS. ABORT MISSION.")
                                    break
                                self.orderAccepted = name == "Complete Order"
                                self.closed = False
                                toDeduct = recipedata.theRecipes.get(self.currentOrder)
                                for i in range(len(toDeduct)):
                                    if not self.orderAccepted: break
                                    fakeAmount = toDeduct[i][1] * -1
                                    inventorydata.insertItemIntoSpareSlot((toDeduct[i][0], fakeAmount))
                                
                                # Store the current customer name before changing
                                self.previousCustomerName = self.currentCustomerName
                                
                                # Change to next customer
                                self.nameIndex += 1
                                if self.nameIndex >= len(self.randomCustomerNames):
                                    self.nameIndex = 0
                                    random.shuffle(self.randomCustomerNames)
                                self.currentCustomerName = self.randomCustomerNames[self.nameIndex]
                                
                                # Reset for next order
                                self.currentOrder = random.choice(self.listOfRecipes)
                                self.randomAmount = random.randint(100, 700)
                                self.generatedFakeAmounts = False
                                self.notEnoughIngredients = False
                                self.editedItemsAlready = False
                            
                            self.previousScene = self.currentScene
                            self.currentScene = info[2]
                            break

            pygame.display.flip()

        sys.exit()
