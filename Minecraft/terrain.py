# not for use (for now) but will be later
import random
import math

BLOCK_SIZE = 50


class TerrainGenerator:
    def __init__(self, seed=None):
        if seed is None:
            seed = random.randint(0, 999999)
        self.seed = seed
        random.seed(seed)

        # Terrain tuning (polish)
        self.base_height = 12          # average ground height
        self.height_variation = 6      # hills amplitude
        self.smoothness = 40           # bigger = smoother terrain

    def get_height(self, x):
        """
        Returns terrain column height (number of blocks).
        """
        height = (
            self.base_height +
            math.sin(x / self.smoothness) * self.height_variation +
            random.uniform(-1.5, 1.5)
        )

        return max(6, int(height))

    def generate_column(self, x, world_height):
        """
        Generates a single vertical column of terrain blocks.
        Returns a list of (block_type, y_position).
        """
        column = []
        height = self.get_height(x)

        for y in range(height):
            world_y = world_height - (height - y) * BLOCK_SIZE
            if y == height - 1:
                column.append(("grass", world_y))

            elif y >= height - 6:
                column.append(("dirt", world_y))
            else:
                r = random.random()

                if y > 18 and r < 0.02:
                    column.append(("diamond", world_y))
                elif y > 12 and r < 0.05:
                    column.append(("ironore", world_y))
                elif y > 8 and r < 0.08:
                    column.append(("coal", world_y))
                else:
                    column.append(("stone", world_y))

        return column
