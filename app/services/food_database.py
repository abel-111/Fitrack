"""
Preset Food Database & Search Utility for Fitrack.
Provides popular Indian, South Indian, and international fitness foods with
accurate calories, protein, carbs, and fat per standard serving.
"""

COMMON_FOODS = [
    # --- HIGH PROTEIN (EGGS, MEAT, DAIRY & VEG PROTEIN) ---
    {
        'id': 'egg_boiled',
        'name': 'Boiled Egg (Large)',
        'category': 'high_protein',
        'category_label': 'High Protein',
        'serving_size': '1 egg (50g)',
        'calories': 78,
        'protein': 6.3,
        'carbs': 0.6,
        'fat': 5.3,
        'icon': '🥚',
        'tags': ['egg', 'boiled', 'protein', 'breakfast']
    },
    {
        'id': 'egg_scrambled',
        'name': 'Scrambled Eggs / Egg Bhurji (2 eggs)',
        'category': 'high_protein',
        'category_label': 'High Protein',
        'serving_size': '2 eggs with onion & spices',
        'calories': 185,
        'protein': 13.5,
        'carbs': 2.5,
        'fat': 13.0,
        'icon': '🍳',
        'tags': ['egg', 'bhurji', 'podimas', 'protein', 'breakfast']
    },
    {
        'id': 'egg_white',
        'name': 'Egg White (Boiled)',
        'category': 'high_protein',
        'category_label': 'High Protein',
        'serving_size': '1 egg white (33g)',
        'calories': 17,
        'protein': 3.6,
        'carbs': 0.2,
        'fat': 0.1,
        'icon': '🥚',
        'tags': ['egg', 'egg white', 'pure protein', 'lean']
    },
    {
        'id': 'chicken_breast_grilled',
        'name': 'Grilled Chicken Breast',
        'category': 'high_protein',
        'category_label': 'High Protein',
        'serving_size': '100g cooked',
        'calories': 165,
        'protein': 31.0,
        'carbs': 0.0,
        'fat': 3.6,
        'icon': '🍗',
        'tags': ['chicken', 'breast', 'grilled', 'lean protein']
    },
    {
        'id': 'chicken_curry_sukka',
        'name': 'South Indian Chicken Sukka / Curry',
        'category': 'high_protein',
        'category_label': 'High Protein',
        'serving_size': '1 bowl (150g)',
        'calories': 255,
        'protein': 27.5,
        'carbs': 6.0,
        'fat': 13.5,
        'icon': '🍗',
        'tags': ['chicken', 'sukka', 'curry', 'chettinad']
    },
    {
        'id': 'paneer_raw',
        'name': 'Paneer (Cottage Cheese, Cubed)',
        'category': 'high_protein',
        'category_label': 'High Protein',
        'serving_size': '100g',
        'calories': 296,
        'protein': 18.3,
        'carbs': 4.1,
        'fat': 22.5,
        'icon': '🧀',
        'tags': ['paneer', 'cottage cheese', 'veg protein']
    },
    {
        'id': 'paneer_bhurji',
        'name': 'Paneer Bhurji (Spiced)',
        'category': 'high_protein',
        'category_label': 'High Protein',
        'serving_size': '1 bowl (150g)',
        'calories': 275,
        'protein': 16.5,
        'carbs': 7.0,
        'fat': 20.0,
        'icon': '🧀',
        'tags': ['paneer', 'bhurji', 'veg protein']
    },
    {
        'id': 'soya_chunks_boiled',
        'name': 'Soya Chunks (Boiled & Spiced)',
        'category': 'high_protein',
        'category_label': 'High Protein',
        'serving_size': '1 bowl (50g dry / 150g boiled)',
        'calories': 175,
        'protein': 26.0,
        'carbs': 16.5,
        'fat': 0.5,
        'icon': '🌱',
        'tags': ['soya', 'meal maker', 'vegan protein', 'plant protein']
    },
    {
        'id': 'whey_protein',
        'name': 'Whey Protein Shake (1 scoop)',
        'category': 'high_protein',
        'category_label': 'High Protein',
        'serving_size': '1 scoop (30g powder in water)',
        'calories': 120,
        'protein': 24.0,
        'carbs': 3.0,
        'fat': 1.5,
        'icon': '🥤',
        'tags': ['whey', 'protein powder', 'shake', 'supplement']
    },
    {
        'id': 'fish_curry',
        'name': 'Fish Curry / Meen Curry',
        'category': 'high_protein',
        'category_label': 'High Protein',
        'serving_size': '1 bowl (150g fish + gravy)',
        'calories': 225,
        'protein': 26.0,
        'carbs': 5.0,
        'fat': 11.0,
        'icon': '🐟',
        'tags': ['fish', 'meen', 'curry', 'kerala', 'seafood']
    },
    {
        'id': 'greek_yogurt',
        'name': 'Greek Yogurt (Plain, Unsweetened)',
        'category': 'high_protein',
        'category_label': 'High Protein',
        'serving_size': '1 cup (170g)',
        'calories': 130,
        'protein': 17.0,
        'carbs': 6.0,
        'fat': 3.5,
        'icon': '🥣',
        'tags': ['greek yogurt', 'curd', 'dahi', 'protein']
    },

    # --- SOUTH INDIAN BREAKFAST & TIFFIN ---
    {
        'id': 'idli',
        'name': 'Steamed Idli (1 piece)',
        'category': 'south_indian',
        'category_label': 'South Indian',
        'serving_size': '1 medium idli (40g)',
        'calories': 60,
        'protein': 2.0,
        'carbs': 12.5,
        'fat': 0.3,
        'icon': '⚪',
        'tags': ['idli', 'steamed', 'tiffin', 'breakfast']
    },
    {
        'id': 'idli_set',
        'name': 'Idli Set (3 Idlis + Sambar)',
        'category': 'south_indian',
        'category_label': 'South Indian',
        'serving_size': '3 idlis with 1 cup sambar',
        'calories': 310,
        'protein': 12.5,
        'carbs': 56.0,
        'fat': 4.0,
        'icon': '⚪',
        'tags': ['idli', 'sambar', 'tiffin', 'breakfast', 'combo']
    },
    {
        'id': 'plain_dosa',
        'name': 'Plain Dosa / Roast',
        'category': 'south_indian',
        'category_label': 'South Indian',
        'serving_size': '1 medium dosa (60g)',
        'calories': 135,
        'protein': 3.2,
        'carbs': 22.0,
        'fat': 4.0,
        'icon': '🥞',
        'tags': ['dosa', 'roast', 'tiffin', 'breakfast']
    },
    {
        'id': 'pesarattu',
        'name': 'Pesarattu (Green Moong Dal Dosa)',
        'category': 'south_indian',
        'category_label': 'South Indian',
        'serving_size': '1 medium dosa (75g)',
        'calories': 145,
        'protein': 7.5,
        'carbs': 20.0,
        'fat': 3.5,
        'icon': '🥞',
        'tags': ['pesarattu', 'moong dal', 'andhra', 'high protein tiffin']
    },
    {
        'id': 'masala_dosa',
        'name': 'Masala Dosa with Potato Filling',
        'category': 'south_indian',
        'category_label': 'South Indian',
        'serving_size': '1 dosa (120g)',
        'calories': 285,
        'protein': 5.5,
        'carbs': 42.0,
        'fat': 10.5,
        'icon': '🥞',
        'tags': ['masala dosa', 'dosa', 'tiffin']
    },
    {
        'id': 'puttu_kadala',
        'name': 'Kerala Puttu with Kadala Curry',
        'category': 'south_indian',
        'category_label': 'South Indian',
        'serving_size': '1 puttu + 1 cup kadala curry',
        'calories': 420,
        'protein': 18.0,
        'carbs': 66.0,
        'fat': 10.0,
        'icon': '🌴',
        'tags': ['puttu', 'kadala', 'kerala', 'breakfast']
    },
    {
        'id': 'upma',
        'name': 'Rava Upma with Veggies',
        'category': 'south_indian',
        'category_label': 'South Indian',
        'serving_size': '1 bowl (150g)',
        'calories': 220,
        'protein': 4.5,
        'carbs': 38.0,
        'fat': 6.0,
        'icon': '🍲',
        'tags': ['upma', 'rava', 'breakfast']
    },
    {
        'id': 'pongal_ven',
        'name': 'Ven Pongal (Ghee Khichdi)',
        'category': 'south_indian',
        'category_label': 'South Indian',
        'serving_size': '1 bowl (150g)',
        'calories': 290,
        'protein': 7.0,
        'carbs': 44.0,
        'fat': 10.0,
        'icon': '🍲',
        'tags': ['pongal', 'ven pongal', 'tiffin']
    },
    {
        'id': 'ragi_mudde',
        'name': 'Ragi Mudde (Finger Millet Ball)',
        'category': 'south_indian',
        'category_label': 'South Indian',
        'serving_size': '1 medium ball (150g)',
        'calories': 190,
        'protein': 4.5,
        'carbs': 42.0,
        'fat': 0.8,
        'icon': '🌾',
        'tags': ['ragi', 'mudde', 'millet', 'karnataka', 'fiber']
    },
    {
        'id': 'appam',
        'name': 'Kerala Appam (Palappam)',
        'category': 'south_indian',
        'category_label': 'South Indian',
        'serving_size': '1 piece (45g)',
        'calories': 95,
        'protein': 1.5,
        'carbs': 18.0,
        'fat': 2.0,
        'icon': '🥞',
        'tags': ['appam', 'kerala', 'breakfast']
    },

    # --- RICE, GRAINS & ROTIS (MAINS) ---
    {
        'id': 'rice_ponni_cooked',
        'name': 'Steamed Rice (Ponni / Sona Masoori)',
        'category': 'staples',
        'category_label': 'Grains & Rotis',
        'serving_size': '1 cup cooked (150g)',
        'calories': 195,
        'protein': 4.0,
        'carbs': 43.0,
        'fat': 0.5,
        'icon': '🍚',
        'tags': ['rice', 'ponni', 'steamed rice', 'white rice', 'lunch']
    },
    {
        'id': 'rice_matta_cooked',
        'name': 'Kerala Red Matta Rice',
        'category': 'staples',
        'category_label': 'Grains & Rotis',
        'serving_size': '1 cup cooked (150g)',
        'calories': 180,
        'protein': 4.3,
        'carbs': 39.0,
        'fat': 0.8,
        'icon': '🍚',
        'tags': ['matta rice', 'red rice', 'kerala', 'fiber']
    },
    {
        'id': 'rice_brown_cooked',
        'name': 'Brown Rice (Cooked)',
        'category': 'staples',
        'category_label': 'Grains & Rotis',
        'serving_size': '1 cup cooked (150g)',
        'calories': 185,
        'protein': 4.5,
        'carbs': 39.0,
        'fat': 1.2,
        'icon': '🍚',
        'tags': ['brown rice', 'whole grain', 'complex carb']
    },
    {
        'id': 'chapati_roti',
        'name': 'Whole Wheat Chapati / Phulka',
        'category': 'staples',
        'category_label': 'Grains & Rotis',
        'serving_size': '1 medium roti (35g dry flour)',
        'calories': 85,
        'protein': 3.1,
        'carbs': 16.5,
        'fat': 0.8,
        'icon': '🫓',
        'tags': ['chapati', 'roti', 'phulka', 'wheat', 'bread']
    },
    {
        'id': 'oatmeal_water',
        'name': 'Rolled Oats (in Water / light milk)',
        'category': 'staples',
        'category_label': 'Grains & Rotis',
        'serving_size': '1 bowl (40g dry oats)',
        'calories': 160,
        'protein': 6.0,
        'carbs': 28.0,
        'fat': 2.5,
        'icon': '🥣',
        'tags': ['oats', 'oatmeal', 'breakfast', 'fiber']
    },
    {
        'id': 'quinoa_cooked',
        'name': 'Quinoa (Cooked)',
        'category': 'staples',
        'category_label': 'Grains & Rotis',
        'serving_size': '1 cup cooked (185g)',
        'calories': 222,
        'protein': 8.1,
        'carbs': 39.4,
        'fat': 3.6,
        'icon': '🌾',
        'tags': ['quinoa', 'grain', 'complete protein']
    },
    {
        'id': 'parotta_maida',
        'name': 'Malabar Parotta / Barotta',
        'category': 'staples',
        'category_label': 'Grains & Rotis',
        'serving_size': '1 piece (80g)',
        'calories': 290,
        'protein': 4.5,
        'carbs': 36.0,
        'fat': 14.0,
        'icon': '🫓',
        'tags': ['parotta', 'barotta', 'malabar', 'dinner']
    },

    # --- DALS, SAMBAR & CURRIES ---
    {
        'id': 'toor_dal_sambar',
        'name': 'Toor Dal Sambar with Vegetables',
        'category': 'south_indian',
        'category_label': 'South Indian',
        'serving_size': '1 cup (200ml)',
        'calories': 130,
        'protein': 6.5,
        'carbs': 18.0,
        'fat': 3.5,
        'icon': '🥘',
        'tags': ['sambar', 'toor dal', 'vegetables', 'curry', 'lunch']
    },
    {
        'id': 'rasam_pepper',
        'name': 'Milagu / Pepper Rasam',
        'category': 'south_indian',
        'category_label': 'South Indian',
        'serving_size': '1 cup (180ml)',
        'calories': 45,
        'protein': 1.5,
        'carbs': 7.0,
        'fat': 1.2,
        'icon': '🥣',
        'tags': ['rasam', 'pepper rasam', 'milagu', 'soup']
    },
    {
        'id': 'dal_tadka',
        'name': 'Yellow Moong / Dal Tadka',
        'category': 'north_indian',
        'category_label': 'North Indian',
        'serving_size': '1 bowl (150g)',
        'calories': 160,
        'protein': 9.2,
        'carbs': 22.0,
        'fat': 4.0,
        'icon': '🍲',
        'tags': ['dal', 'dal tadka', 'yellow dal', 'moong']
    },
    {
        'id': 'rajma_masala',
        'name': 'Punjabi Rajma Masala (Kidney Beans)',
        'category': 'north_indian',
        'category_label': 'North Indian',
        'serving_size': '1 bowl (180g)',
        'calories': 210,
        'protein': 10.5,
        'carbs': 32.0,
        'fat': 4.5,
        'icon': '🍛',
        'tags': ['rajma', 'kidney beans', 'protein curry', 'north indian']
    },
    {
        'id': 'chole_masala',
        'name': 'Chole / Chana Masala (Chickpeas)',
        'category': 'north_indian',
        'category_label': 'North Indian',
        'serving_size': '1 bowl (180g)',
        'calories': 230,
        'protein': 11.0,
        'carbs': 34.0,
        'fat': 5.5,
        'icon': '🍛',
        'tags': ['chole', 'chana', 'chickpeas', 'curry']
    },
    {
        'id': 'keerai_kootu',
        'name': 'Keerai Kootu (Spinach & Moong Dal)',
        'category': 'south_indian',
        'category_label': 'South Indian',
        'serving_size': '1 cup (150g)',
        'calories': 125,
        'protein': 7.0,
        'carbs': 15.0,
        'fat': 4.0,
        'icon': '🥬',
        'tags': ['keerai', 'spinach', 'kootu', 'greens', 'fiber']
    },
    {
        'id': 'vegetable_poriyal',
        'name': 'Vegetable Poriyal / Thoran (Beans/Carrot)',
        'category': 'south_indian',
        'category_label': 'South Indian',
        'serving_size': '1 cup (120g)',
        'calories': 95,
        'protein': 2.8,
        'carbs': 12.0,
        'fat': 4.0,
        'icon': '🥕',
        'tags': ['poriyal', 'thoran', 'veggies', 'beans', 'carrot', 'fiber']
    },
    {
        'id': 'vegetable_avial',
        'name': 'Kerala Avial with Coconut & Curd',
        'category': 'south_indian',
        'category_label': 'South Indian',
        'serving_size': '1 bowl (150g)',
        'calories': 165,
        'protein': 3.5,
        'carbs': 16.0,
        'fat': 10.0,
        'icon': '🥥',
        'tags': ['avial', 'kerala', 'coconut', 'curd', 'vegetables']
    },

    # --- SNACKS, SUNDAL & SIDES ---
    {
        'id': 'kala_chana_sundal',
        'name': 'Kala Chana Sundal (Black Chickpeas)',
        'category': 'snacks_drinks',
        'category_label': 'Snacks & Drinks',
        'serving_size': '1 cup (150g)',
        'calories': 210,
        'protein': 11.5,
        'carbs': 32.0,
        'fat': 4.0,
        'icon': '🌱',
        'tags': ['sundal', 'chana', 'kala chana', 'snack', 'fiber', 'protein']
    },
    {
        'id': 'moong_sprouts_sundal',
        'name': 'Sprouted Moong Salad / Sundal',
        'category': 'snacks_drinks',
        'category_label': 'Snacks & Drinks',
        'serving_size': '1 cup (120g)',
        'calories': 135,
        'protein': 9.5,
        'carbs': 22.0,
        'fat': 1.5,
        'icon': '🌱',
        'tags': ['sprouts', 'moong', 'salad', 'clean protein', 'raw']
    },
    {
        'id': 'peanuts_roasted',
        'name': 'Roasted Peanuts (Kadalai)',
        'category': 'snacks_drinks',
        'category_label': 'Snacks & Drinks',
        'serving_size': '1 handful (30g)',
        'calories': 170,
        'protein': 7.8,
        'carbs': 4.8,
        'fat': 14.5,
        'icon': '🥜',
        'tags': ['peanuts', 'kadalai', 'roasted', 'healthy fat', 'protein']
    },
    {
        'id': 'peanut_butter',
        'name': 'Peanut Butter (1 tbsp)',
        'category': 'snacks_drinks',
        'category_label': 'Snacks & Drinks',
        'serving_size': '1 tablespoon (16g)',
        'calories': 95,
        'protein': 4.0,
        'carbs': 3.5,
        'fat': 8.0,
        'icon': '🥜',
        'tags': ['peanut butter', 'spread', 'healthy fat']
    },
    {
        'id': 'almonds',
        'name': 'Almonds (Badam, 10-12 pieces)',
        'category': 'snacks_drinks',
        'category_label': 'Snacks & Drinks',
        'serving_size': '12 almonds (15g)',
        'calories': 90,
        'protein': 3.2,
        'carbs': 3.0,
        'fat': 7.8,
        'icon': '🌰',
        'tags': ['almonds', 'badam', 'nuts', 'healthy fat']
    },
    {
        'id': 'makhana_roasted',
        'name': 'Roasted Makhana (Fox Nuts)',
        'category': 'snacks_drinks',
        'category_label': 'Snacks & Drinks',
        'serving_size': '1 big bowl (30g)',
        'calories': 110,
        'protein': 3.0,
        'carbs': 22.0,
        'fat': 1.0,
        'icon': '🍿',
        'tags': ['makhana', 'fox nuts', 'low calorie snack']
    },
    {
        'id': 'banana',
        'name': 'Banana (Medium)',
        'category': 'snacks_drinks',
        'category_label': 'Snacks & Drinks',
        'serving_size': '1 medium (118g)',
        'calories': 105,
        'protein': 1.3,
        'carbs': 27.0,
        'fat': 0.3,
        'icon': '🍌',
        'tags': ['banana', 'fruit', 'pre-workout', 'potassium']
    },
    {
        'id': 'apple',
        'name': 'Apple (Medium)',
        'category': 'snacks_drinks',
        'category_label': 'Snacks & Drinks',
        'serving_size': '1 medium (180g)',
        'calories': 95,
        'protein': 0.5,
        'carbs': 25.0,
        'fat': 0.3,
        'icon': '🍎',
        'tags': ['apple', 'fruit', 'fiber', 'snack']
    },

    # --- BEVERAGES & DAIRY ---
    {
        'id': 'curd_homemade',
        'name': 'Homemade Curd / Plain Dahi',
        'category': 'snacks_drinks',
        'category_label': 'Snacks & Drinks',
        'serving_size': '1 cup (150g)',
        'calories': 95,
        'protein': 5.0,
        'carbs': 7.0,
        'fat': 5.0,
        'icon': '🥣',
        'tags': ['curd', 'dahi', 'yogurt', 'probiotic', 'calcium']
    },
    {
        'id': 'neer_mor',
        'name': 'Spiced Neer Mor / Buttermilk',
        'category': 'snacks_drinks',
        'category_label': 'Snacks & Drinks',
        'serving_size': '1 tall glass (250ml)',
        'calories': 45,
        'protein': 2.2,
        'carbs': 4.5,
        'fat': 1.8,
        'icon': '🥛',
        'tags': ['neer mor', 'buttermilk', 'chaas', 'electrolytes', 'gut health']
    },
    {
        'id': 'tender_coconut',
        'name': 'Tender Coconut Water',
        'category': 'snacks_drinks',
        'category_label': 'Snacks & Drinks',
        'serving_size': '1 fresh coconut (250ml)',
        'calories': 48,
        'protein': 1.7,
        'carbs': 9.0,
        'fat': 0.5,
        'icon': '🥥',
        'tags': ['coconut water', 'elaneer', 'electrolyte', 'hydration']
    },
    {
        'id': 'filter_coffee_milk',
        'name': 'South Indian Filter Coffee (Toned Milk)',
        'category': 'snacks_drinks',
        'category_label': 'Snacks & Drinks',
        'serving_size': '1 tumbler (150ml with 1 tsp sugar)',
        'calories': 75,
        'protein': 2.8,
        'carbs': 9.5,
        'fat': 2.5,
        'icon': '☕',
        'tags': ['filter coffee', 'coffee', 'caffeine', 'tiffin']
    },
    {
        'id': 'black_coffee',
        'name': 'Black Coffee / Espresso (No Sugar)',
        'category': 'snacks_drinks',
        'category_label': 'Snacks & Drinks',
        'serving_size': '1 cup (150ml)',
        'calories': 5,
        'protein': 0.3,
        'carbs': 0.0,
        'fat': 0.0,
        'icon': '☕',
        'tags': ['black coffee', 'pre-workout', 'zero calorie', 'caffeine']
    },
    {
        'id': 'whole_milk',
        'name': 'Cow Milk (Toned)',
        'category': 'snacks_drinks',
        'category_label': 'Snacks & Drinks',
        'serving_size': '1 glass (200ml)',
        'calories': 120,
        'protein': 6.5,
        'carbs': 10.0,
        'fat': 6.0,
        'icon': '🥛',
        'tags': ['milk', 'dairy', 'calcium']
    }
]


FOOD_CATEGORIES = [
    ('all', '🌟 All Items'),
    ('high_protein', '🥩 High Protein'),
    ('south_indian', '🍛 South Indian'),
    ('staples', '🌾 Grains & Rotis'),
    ('north_indian', '🍲 North Indian'),
    ('snacks_drinks', '🥜 Snacks & Drinks'),
]


def search_foods(query='', category=None, limit=25):
    """
    Search foods by keyword in name, category, or tags.
    Optionally filter by category.
    """
    q = (query or '').strip().lower()
    results = []

    for food in COMMON_FOODS:
        if category and category != 'all' and food.get('category') != category:
            continue

        if not q:
            results.append(food)
        else:
            name_match = q in food['name'].lower()
            tag_match = any(q in tag for tag in food.get('tags', []))
            cat_match = q in food.get('category', '').lower()

            if name_match or tag_match or cat_match:
                results.append(food)

        if len(results) >= limit:
            break

    return results


def get_food_by_id(food_id):
    """Retrieve food dictionary by id."""
    for f in COMMON_FOODS:
        if f['id'] == food_id:
            return f
    return None
