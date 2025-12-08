"""
configuration for animal spritesheets and game settings
defines sprite animations, prices, incomes and sizes for all game objects

format for animal sprites:
{
    'animal_name': {
        'walk': {
            Direction.SOUTH: (row, frame_count),
            Direction.NORTH: (row, frame_count),
            Direction.EAST: (row, frame_count),
            Direction.WEST: (row, frame_count)
        },
        'idle': {
            Direction.SOUTH: (row, frame_count),
            Direction.NORTH: (row, frame_count),
            Direction.EAST: (row, frame_count),
            Direction.WEST: (row, frame_count)
        }
    }
}

note: row numbers start at 1 (first row = 1)
"""

from utils import Direction

# animal sprite configuration dictonary
# maps each animal species to their walk and idle animations for all 4 directions
ANIMAL_SPRITES_CONFIG = {
    'rooster': {
        'walk': {
            Direction.SOUTH: (1, 6),
            Direction.NORTH: (2, 6),
            Direction.EAST: (4, 6),
            Direction.WEST: (3, 6)
        },
        'idle': {
            Direction.SOUTH: (5, 6),
            Direction.NORTH: (6, 6),
            Direction.EAST: (8, 6),
            Direction.WEST: (7, 6)
        }
    },
    'sheep': {
        'walk': {
            Direction.SOUTH: (1, 6),
            Direction.NORTH: (2, 6),
            Direction.EAST: (4, 6),
            Direction.WEST: (3, 6)
        },
        'idle': {
            Direction.SOUTH: (5, 4),
            Direction.NORTH: (6, 4),
            Direction.EAST: (7, 4),
            Direction.WEST: (8, 4)
        }
    },
    'bull': {
        'walk': {
            Direction.SOUTH: (1, 6),
            Direction.NORTH: (2, 6),
            Direction.EAST: (4, 6),
            Direction.WEST: (3, 6)
        },
        'idle': {
            Direction.SOUTH: (5, 4),
            Direction.NORTH: (6, 4),
            Direction.EAST: (7, 4),
            Direction.WEST: (8, 4)
        }
    },
    'calf': {
        'walk': {
            Direction.SOUTH: (1, 6),
            Direction.NORTH: (2, 6),
            Direction.EAST: (4, 6),
            Direction.WEST: (3, 6)
        },
        'idle': {
            Direction.SOUTH: (5, 4),
            Direction.NORTH: (6, 4),
            Direction.EAST: (7, 4),
            Direction.WEST: (8, 4)
        }
    },
    'turkey': {
        'walk': {
            Direction.SOUTH: (1, 6),
            Direction.NORTH: (2, 6),
            Direction.EAST: (4, 6),
            Direction.WEST: (3, 6)
        },
        'idle': {
            Direction.SOUTH: (5, 4),
            Direction.NORTH: (6, 4),
            Direction.EAST: (7, 4),
            Direction.WEST: (8, 4)
        }
    },
    'chick': {
        'walk': {
            Direction.SOUTH: (1, 6),
            Direction.NORTH: (2, 6),
            Direction.EAST: (4, 6),
            Direction.WEST: (3, 6)
        },
        'idle': {
            Direction.SOUTH: (5, 4),
            Direction.NORTH: (6, 4),
            Direction.EAST: (7, 4),
            Direction.WEST: (8, 4)
        }
    },
    'lamb': {
        'walk': {
            Direction.SOUTH: (1, 6),
            Direction.NORTH: (2, 6),
            Direction.EAST: (4, 6),
            Direction.WEST: (3, 6)
        },
        'idle': {
            Direction.SOUTH: (5, 4),
            Direction.NORTH: (6, 4),
            Direction.EAST: (7, 4),
            Direction.WEST: (8, 4)
        }
    },
    'piglet': {
        'walk': {
            Direction.SOUTH: (1, 6),
            Direction.NORTH: (2, 6),
            Direction.EAST: (4, 6),
            Direction.WEST: (3, 6)
        },
        'idle': {
            Direction.SOUTH: (5, 4),
            Direction.NORTH: (6, 4),
            Direction.EAST: (7, 4),
            Direction.WEST: (8, 4)
        }
    }
}


# prop sizes in tiles (width, height)
# defines how much space each prop occupys on the game grid
PROPS_SIZES = {
    
    "rock2": (1, 1),      
    "rock3": (1, 1),
    "log1": (1, 1),
    "flag": (1, 1),
    "rock1": (1, 1),
    "log2": (1, 1),
    "bush1": (1, 1),
    "bush2": (1, 1),
    "barrel": (1, 1),
    "banner": (1, 2),
    "banner2": (1, 2),
    "bush3": (2, 1),
    "campfire": (1, 1),
    "chest": (1, 1),
    "well": (1, 1),
    "nexus": (2, 3),
    "watchtower1": (2, 2),
    "tree3": (2, 2),
    "bridge": (4, 2),
    "bridge2": (2, 3),
    "tent": (2, 2),
    "watchtower2": (2, 3),
    "cart": (2, 1),
    "tree2": (2, 2),
    "castle2": (3, 3),
    "tree1": (3, 4),
    "castle1": (3, 5),
    "house": (4, 6),
    "windmill": (7, 7),
}

# enclosure pricing based on size (width x height)
# price = base cost + (width * height * cost per tile)
ENCLOSURE_BASE_PRICE = 100
ENCLOSURE_COST_PER_TILE = 50

# prop prices and income (price, income per second)
# decorative props have zero income, functional buildings genrate money
PROP_PRICES = {
 
    "rock1": {"price": 25, "income": 0},
    "rock2": {"price": 25, "income": 0},
    "rock3": {"price": 25, "income": 0},
    "log1": {"price": 25, "income": 0},
    "log2": {"price": 25, "income": 0},
    
 
    "bush1": {"price": 25, "income": 0},
    "bush2": {"price": 25, "income": 0},
    "bush3": {"price": 25, "income": 0},
    "flag": {"price": 200, "income": 1},
    "banner": {"price": 200, "income": 1},
    "banner2": {"price": 200, "income": 1},
    

    "campfire": {"price": 100, "income": 0},
    "barrel": {"price": 100, "income": 0},
    "chest": {"price": 150, "income": 1},
    "well": {"price": 150, "income": 1},
    
  
    "tree1": {"price": 150, "income": 0},
    "tree2": {"price": 150, "income": 0},
    "tree3": {"price": 150, "income": 0},

    "tent": {"price": 100, "income": 0},
    "cart": {"price": 100, "income": 0},
    "bridge": {"price": 400, "income": 2},
    "bridge2": {"price": 400, "income": 2},
    
 
    "house": {"price": 800, "income": 5},
    "watchtower1": {"price": 1000, "income": 6},
    "watchtower2": {"price": 1000, "income": 6},
    

    "windmill": {"price": 1500, "income": 10},
    "castle1": {"price": 2500, "income": 15},
    "castle2": {"price": 2500, "income": 15},
    
    "nexus": {"price": 5000, "income": 25}
}

# animal prices and income generaton (price, income per second)
# each animal produces passive income when placed in enclosures
ANIMAL_PRICES = {
    "sheep": {"price": 1200, "income": 5},      
    "rooster": {"price": 600, "income": 3},    
    "bull": {"price": 3000, "income": 15},       
    "calf": {"price": 500, "income": 2},       
    "turkey": {"price": 300, "income": 3},     
    "chick": {"price": 200, "income": 1000},      
    "lamb": {"price": 250, "income": 2},    
    "piglet": {"price": 250, "income": 2}     
}

# sort dictionaries by price for easier shop display
ANIMAL_PRICES = dict(sorted(ANIMAL_PRICES.items(), key=lambda item: item[1]['price']))
PROP_PRICES = dict(sorted(PROP_PRICES.items(), key=lambda item: item[1]['price']))

# bulldozer cost per use for destroying props and enclosurs
BULLDOZER_BASE_COST = 300

# starting money for new game
STARTING_MONEY = 2000