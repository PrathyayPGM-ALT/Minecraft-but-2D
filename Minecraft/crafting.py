import pygame

GRID = 3
CELL = 64
PADDING = 8

PANEL_COLOR = (30, 30, 30)
CELL_COLOR = (70, 70, 70)
OUTLINE_COLOR = (255, 255, 0)


class CraftingTable:
    def __init__(self, inventory):
        self.inventory = inventory

        self.grid = [[None for _ in range(GRID)] for _ in range(GRID)]
        self.output = None
        self.matched_recipe = None

        self.icons = {}
        self.load_icons()

        self.font = pygame.font.SysFont("Arial", 22)

        self.recipes = {
            # sticks
            (("wood",),
             ("wood",)): ("stick", 4),

            # crafting table
            (("wood", "wood"),
             ("wood", "wood")): ("crafting_table", 1),

            # wooden pickaxe
            (("wood", "wood", "wood"),
             (None, "stick", None),
             (None, "stick", None)): ("wood_pickaxe", 1),

            # stone pickaxe
            (("stone", "stone", "stone"),
             (None, "stick", None),
             (None, "stick", None)): ("stone_pickaxe", 1),

            # wooden sword
            (("wood",),
             ("wood",),
             ("stick",)): ("wood_sword", 1),

            # stone sword
            (("stone",),
             ("stone",),
             ("stick",)): ("stone_sword", 1),
        }


    def load_icons(self):
        items = [
            "wood", "stone", "stick",
            "crafting_table",
            "wood_pickaxe", "stone_pickaxe",
            "wood_sword", "stone_sword"
        ]

        for item in items:
            try:
                img = pygame.image.load(f"textures/{item}.png").convert_alpha()
                self.icons[item] = pygame.transform.scale(img, (CELL - 16, CELL - 16))
            except:
                surf = pygame.Surface((CELL - 16, CELL - 16))
                surf.fill((200, 200, 200))
                self.icons[item] = surf
                print(f"[WARNING] Missing texture: textures/{item}.png")


    def update_craft_result(self):
        pattern = self.trim_pattern(self.grid)
        self.output = None
        self.matched_recipe = None

        for recipe_pattern, result in self.recipes.items():
            if self.pattern_match(pattern, recipe_pattern):
                self.output = result
                self.matched_recipe = recipe_pattern
                break

    def trim_pattern(self, grid):
        rows = [r[:] for r in grid]
        rows = [r for r in rows if any(r)]
        if not rows:
            return ()

        cols = list(zip(*rows))
        cols = [c for c in cols if any(c)]

        return tuple(tuple(cell for cell in row) for row in zip(*cols))

    def pattern_match(self, a, b):
        if len(a) != len(b):
            return False
        for y in range(len(a)):
            if len(a[y]) != len(b[y]):
                return False
            for x in range(len(a[y])):
                if a[y][x] != b[y][x]:
                    return False
        return True

    def consume_ingredients(self, recipe_pattern):
        if not recipe_pattern:
            return

        ph = len(recipe_pattern)
        pw = len(recipe_pattern[0])

        for gy in range(GRID - ph + 1):
            for gx in range(GRID - pw + 1):

                match = True
                for y in range(ph):
                    for x in range(pw):
                        if recipe_pattern[y][x] != self.grid[gy + y][gx + x]:
                            match = False
                            break
                    if not match:
                        break

                if match:
                    for y in range(ph):
                        for x in range(pw):
                            if recipe_pattern[y][x] is not None:
                                self.grid[gy + y][gx + x] = None
                    return

    def remove_from_inventory(self, item_type):
        for slot in self.inventory.values():
            if slot["type"] == item_type:
                slot["count"] -= 1
                if slot["count"] <= 0:
                    slot["type"] = None
                    slot["count"] = 0
                return

    def add_to_inventory(self, item_type, count=1):
        for slot in self.inventory.values():
            if slot["type"] == item_type:
                slot["count"] += count
                return
        for slot in self.inventory.values():
            if slot["type"] is None:
                slot["type"] = item_type
                slot["count"] = count
                return

    def handle_click(self, mpos, mb, selected_item):
        cell = self.get_hover_cell(mpos)

        # OUTPUT SLOT
        if self.hover_output(mpos) and mb[0]:
            if self.output:
                name, count = self.output
                self.add_to_inventory(name, count)
                self.consume_ingredients(self.matched_recipe)
                self.update_craft_result()
            return

        if cell is None:
            return

        cx, cy = cell

        if mb[0] and selected_item:
            if self.grid[cy][cx] is None:
                self.grid[cy][cx] = selected_item
                self.remove_from_inventory(selected_item)
                self.update_craft_result()

        # REMOVE ITEM → RETURN TO INVENTORY
        if mb[2]:
            if self.grid[cy][cx] is not None:
                self.add_to_inventory(self.grid[cy][cx])
                self.grid[cy][cx] = None
                self.update_craft_result()

    def draw(self, screen):
        W, H = screen.get_size()

        total = GRID * CELL + (GRID + 1) * PADDING
        sx = (W - total) // 2
        sy = (H - total) // 2 - 20

        pygame.draw.rect(
            screen, PANEL_COLOR,
            (sx - 30, sy - 30, total + 60, total + 180)
        )

        mx, my = pygame.mouse.get_pos()
        hover = self.get_hover_cell((mx, my))

        for r in range(GRID):
            for c in range(GRID):
                x = sx + c * (CELL + PADDING)
                y = sy + r * (CELL + PADDING)

                rect = pygame.Rect(x, y, CELL, CELL)
                pygame.draw.rect(screen, CELL_COLOR, rect)

                if hover == (c, r):
                    pygame.draw.rect(screen, OUTLINE_COLOR, rect, 2)

                item = self.grid[r][c]
                if item in self.icons:
                    screen.blit(self.icons[item], (x + 8, y + 8))

        # OUTPUT SLOT
        out_x = sx + total // 2 - CELL // 2
        out_y = sy + total + 20

        out_rect = pygame.Rect(out_x, out_y, CELL, CELL)
        pygame.draw.rect(screen, CELL_COLOR, out_rect)

        if self.hover_output((mx, my)):
            pygame.draw.rect(screen, OUTLINE_COLOR, out_rect, 2)

        if self.output:
            name, count = self.output
            screen.blit(self.icons[name], (out_x + 8, out_y + 8))
            txt = self.font.render(f"x{count}", True, OUTLINE_COLOR)
            screen.blit(txt, (out_x + CELL + 10, out_y + CELL // 3))

    def get_hover_cell(self, mpos):
        mx, my = mpos
        W, H = pygame.display.get_surface().get_size()

        total = GRID * CELL + (GRID + 1) * PADDING
        sx = (W - total) // 2
        sy = (H - total) // 2 - 20

        for r in range(GRID):
            for c in range(GRID):
                x = sx + c * (CELL + PADDING)
                y = sy + r * (CELL + PADDING)
                if pygame.Rect(x, y, CELL, CELL).collidepoint(mx, my):
                    return (c, r)
        return None

    def hover_output(self, mpos):
        mx, my = mpos
        W, H = pygame.display.get_surface().get_size()

        total = GRID * CELL + (GRID + 1) * PADDING
        sx = (W - total) // 2
        sy = (H - total) // 2 - 20

        out_x = sx + total // 2 - CELL // 2
        out_y = sy + total + 20

        return pygame.Rect(out_x, out_y, CELL, CELL).collidepoint(mx, my)
