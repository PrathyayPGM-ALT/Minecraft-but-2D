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

        # 3x3 grid
        self.grid = [[None for _ in range(GRID)] for _ in range(GRID)]

        # output slot
        self.output = None

        # load icons
        self.icons = {}
        self.load_icons()

        self.font = pygame.font.SysFont("Arial", 22)

        # RECIPES — SHAPED
        self.recipes = {
            # 2 wood vertical → sticks
            (("wood",),
             ("wood",)): ("stick", 4),

            # crafting table → 2×2 wood
            (("wood", "wood"),
             ("wood", "wood")): ("crafting_table", 1),

            # pickaxe
            (("stone", "stone", "stone"),
             (None, "wood", None),
             (None, "wood", None)): ("stone_pickaxe", 1),
        }

    # ---------------------------------------------------------
    # LOAD ICONS FROM /textures/
    # ---------------------------------------------------------
    def load_icons(self):
        items = ["wood", "stone", "stick", "crafting_table", "stone_pickaxe"]

        for item in items:
            try:
                img = pygame.image.load(f"textures/{item}.png").convert_alpha()
                self.icons[item] = pygame.transform.scale(img, (CELL - 16, CELL - 16))
            except:
                print(f"[WARNING] Missing texture: textures/{item}.png")
                # fallback placeholder
                surf = pygame.Surface((CELL - 16, CELL - 16))
                surf.fill((200, 200, 200))
                self.icons[item] = surf

    # ---------------------------------------------------------
    # MATCH RECIPES
    # ---------------------------------------------------------
    def update_craft_result(self):
        pattern = self.trim_pattern(self.grid)
        self.output = None

        for recipe_pattern, result in self.recipes.items():
            if self.pattern_match(pattern, recipe_pattern):
                self.output = result
                break

    def trim_pattern(self, grid):
        rows = [r[:] for r in grid]
        rows = [r for r in rows if any(r)]
        if not rows:
            return ()
        cols = list(zip(*rows))
        cols = [c for c in cols if any(c)]
        return tuple(tuple(c for c in col) for col in zip(*cols))

    def pattern_match(self, a, b):
        if len(a) != len(b):
            return False
        for r in range(len(a)):
            if len(a[r]) != len(b[r]):
                return False
            for c in range(len(a[r])):
                if a[r][c] != b[r][c]:
                    return False
        return True

    # ---------------------------------------------------------
    # HANDLE MOUSE ACTIONS
    # ---------------------------------------------------------
    def handle_click(self, mpos, mb, selected_item):
        mx, my = mpos
        cell = self.get_hover_cell(mpos)

        # CLICK OUTPUT SLOT
        if self.hover_output(mpos) and mb[0]:
            if self.output:
                self.give_to_inventory(self.output)
                self.clear_grid()
            return

        # CLICK GRID
        if cell is None:
            return

        cx, cy = cell

        # LEFT CLICK → place item from hotbar
        if mb[0]:
            if selected_item:
                self.grid[cy][cx] = selected_item
                self.update_craft_result()

        # RIGHT CLICK → clear cell
        if mb[2]:
            self.grid[cy][cx] = None
            self.update_craft_result()

    # ---------------------------------------------------------
    # DRAW UI
    # ---------------------------------------------------------
    def draw(self, screen):
        W, H = screen.get_size()

        total = GRID * CELL + (GRID + 1) * PADDING
        sx = (W - total) // 2
        sy = (H - total) // 2 - 20

        # panel
        pygame.draw.rect(screen, PANEL_COLOR,
                         (sx - 30, sy - 30, total + 60, total + 180))

        mx, my = pygame.mouse.get_pos()
        hover = self.get_hover_cell((mx, my))

        # DRAW GRID
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
            if name in self.icons:
                screen.blit(self.icons[name], (out_x + 8, out_y + 8))

            txt = self.font.render(f"x{count}", True, OUTLINE_COLOR)
            screen.blit(txt, (out_x + CELL + 10, out_y + CELL // 3))

    # ---------------------------------------------------------
    # SAFE GIVE-TO-INVENTORY (no crashes)
    # ---------------------------------------------------------
    def give_to_inventory(self, result):
        name, count = result

        # INVENTORY IS DICTIONARY LIKE:
        # {0: {"type": "wood", "count": 3}, ...}
        if isinstance(self.inventory, dict):

            # Try stacking first
            for i in self.inventory:
                slot = self.inventory[i]
                if isinstance(slot, dict) and slot["type"] == name:
                    slot["count"] += count
                    return

            # Put in empty slot
            for i in self.inventory:
                slot = self.inventory[i]
                if isinstance(slot, dict) and (slot["type"] is None or slot["type"] == 0):
                    slot["type"] = name
                    slot["count"] = count
                    return

        # Fallback
        print("[WARNING] Could not add crafted item! Inventory format unknown.")

    # ---------------------------------------------------------
    def clear_grid(self):
        self.grid = [[None for _ in range(GRID)] for _ in range(GRID)]
        self.update_craft_result()

    # ---------------------------------------------------------
    # ADD BACKWARD COMPATIBLE SPACE CRAFTING
    # ---------------------------------------------------------
    def apply_craft(self):
        if not self.output:
            return
        self.give_to_inventory(self.output)
        self.clear_grid()

    # ---------------------------------------------------------
    # MOUSE DETECTION HELPERS
    # ---------------------------------------------------------
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

        rect = pygame.Rect(out_x, out_y, CELL, CELL)
        return rect.collidepoint(mx, my)
