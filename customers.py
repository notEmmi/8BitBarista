import pygame, random, sys, recipedata, Recipes  # type: ignore

class CustomerUI:
    def __init__(self, game_instance):
        pygame.init()

        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.transparentSurface = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        pygame.display.set_caption("ORDER FULFILLMENT")
        self.game = game_instance

        # Colors
        self.LIGHT_BROWN = (99, 55, 44)
        self.DARK_BROWN = (38, 35, 34)
        self.BROWN = (99, 55, 44)
        self.WHITE = (255, 255, 255)
        self.SHADOW_COLOR = (20, 20, 20, 30)
        self.GRAY = (100, 100, 100)
        self.ACTIVE_COLOR = (160, 100, 80)
        self.BRIGHT_BROWN = (143, 89, 68)
        self.BRIGHTEST_BROWN = (201, 125, 96)
        self.TRANSPARENT = (143, 89, 68, 0)

        # Fonts
        self.titleText = pygame.font.Font(pygame.font.match_font('courier'), 45)
        self.recipeNameText = pygame.font.Font(pygame.font.match_font('courier'), 22)
        self.ingredientText = pygame.font.Font(pygame.font.match_font('courier'), 18)
        self.buttonText = pygame.font.Font(pygame.font.match_font('courier'), 18)
        self.smallText = pygame.font.Font(pygame.font.match_font('courier'), 18)

        self.renderedRecipes = {}

        # Menu Buttons
        self.menuButtons = {
            "BACK": pygame.Rect(self.WIDTH // 2 - 40, 485, 80, 30)
        }

        # Game state
        self.running = True
        self.hasOrder = False
        self.placedOrder = False
        self.customersOrder = None
        self.listOfRecipes = list(recipedata.theRecipes.keys())
        self.smallTextContents = ""

    def drawRecipe(self, recipeName, xPos, yPos, ingredients):
        length = 125
        buttonRect = pygame.Rect(xPos, yPos, length, length)
        self.renderedRecipes[recipeName] = (buttonRect, recipedata.parseIngredients(ingredients))
        self.screen.blit(self.transparentSurface, (0, 0))
        pygame.draw.rect(self.transparentSurface, self.TRANSPARENT, buttonRect, border_radius=7)
        recipeImage = pygame.image.load("PROBABLY_ILLEGAL_ASSETS/" + str.lower(recipeName) + ".png")
        recipeImage = pygame.transform.scale(recipeImage, (length, length))
        self.screen.blit(recipeImage, (buttonRect.x, buttonRect.y))
        recipeLabel = self.recipeNameText.render(recipeName, True, self.WHITE)
        self.screen.blit(recipeLabel, (xPos, yPos - recipeLabel.get_height() // 2))

    def run(self):
        while self.running:
            self.screen.fill(self.LIGHT_BROWN)

            # Middle and Inner Panels with Shadows
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

            # Title
            titleLabel = self.titleText.render("ORDER FULFILLMENT", True, self.WHITE)
            self.screen.blit(titleLabel, (self.WIDTH // 2 - titleLabel.get_width() // 2, 72.5))

            # Recipe buttons
            itemsPerRow = 3
            itemOnRow = 1
            xOffset = 300 - (len(recipedata.theRecipes) * 25)
            yOffset = 300 - (len(recipedata.theRecipes) * 25) + 10
            for name, ingredients in recipedata.theRecipes.items():
                self.drawRecipe(name, xOffset, yOffset, ingredients)
                xOffset += 190
                itemOnRow += 1
                if itemOnRow > itemsPerRow:
                    itemOnRow = 1
                    xOffset = 300 - (len(recipedata.theRecipes) * 25)
                    yOffset += 175

            # Menu buttons
            for name, rect in self.menuButtons.items():
                pygame.draw.rect(self.screen, self.BRIGHT_BROWN, rect.inflate(9, 9), border_radius=14)
                pygame.draw.rect(self.screen, self.BRIGHTEST_BROWN, rect, border_radius=14)
                text = self.buttonText.render(name, True, self.WHITE)
                self.screen.blit(text, text.get_rect(center=rect.center))

            # Order logic
            if not self.hasOrder:
                self.smallTextContents = ""
                self.hasOrder = random.randint(0, 100) > 20
            if self.hasOrder and not self.placedOrder:
                print("Order up!")
                randomRecipe = random.choice(self.listOfRecipes)
                self.customersOrder = self.renderedRecipes[randomRecipe]
                print(f"customer wants {randomRecipe}")
                self.placedOrder = True
                self.smallTextContents = "Customer wants " + randomRecipe + "."
            smallTextLabel = self.smallText.render(self.smallTextContents, True, self.WHITE)
            self.screen.blit(smallTextLabel, (self.WIDTH // 2 - smallTextLabel.get_width() // 2, 115))

            # Event handling
            mousePosition = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                keys = pygame.key.get_pressed()
                if keys[pygame.K_TAB]:
                    recipeStart = Recipes.Recipes()
                    recipeStart.run()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for name, rect in self.menuButtons.items():
                        if rect.collidepoint(mousePosition):
                            self.running = False
                            self.game.run()
                            break
                    for recipe, (buttonRect, ingredients) in self.renderedRecipes.items():
                        if buttonRect.collidepoint(mousePosition):
                            print(f"User wants to craft {recipe}, and needs\n\t{ingredients}.")
                            if self.placedOrder and self.customersOrder[0] == buttonRect:
                                print("order fulfilled!")
                                self.hasOrder = False
                                self.placedOrder = False
                            else:
                                print(f"{recipe} is not what the customer ordered.")
                            break

            pygame.display.flip()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    app = CustomerUI()
    app.run()
