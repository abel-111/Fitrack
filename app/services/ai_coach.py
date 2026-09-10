import os
import json
import random
import urllib.request
import urllib.parse
from datetime import datetime, date, timedelta

# Role definitions & descriptions
ROLE_DETAILS = {
    'desk_worker': {
        'title': 'Desk Worker / Corporate',
        'icon': '💼',
        'summary': 'Tailored for prolonged sitting, metabolic health, posture recovery, and sustained cognitive energy without afternoon energy crashes.',
        'diet_focus': 'Low-glycemic complex carbs, high fiber, anti-inflammatory fats (omega-3), and lighter lunches to prevent sluggishness.',
        'hydration_target': 3.5,
        'activity_multiplier': 1.35,
        'tips': [
            'Take a 2-minute posture & shoulder retraction break every 45 minutes.',
            'Keep a 1L water bottle at your desk; AC environments cause unnoticed dehydration.',
            'Avoid heavy carb-loaded lunches to steer clear of the 2 PM insulin crash.',
            'Keep healthy desk snacks handy: roasted almonds, Greek yogurt, or boiled eggs.'
        ],
        'workout_focus': 'Emphasize rear delts, upper back rows, and hip flexor stretches to combat seated forward posture.'
    },
    'student': {
        'title': 'Student',
        'icon': '🎓',
        'summary': 'Budget-friendly, time-efficient nutrition and training strategies optimized for busy lecture schedules, exams, and tight budgets.',
        'diet_focus': 'High protein on a budget (eggs, lentils, peanut butter, oats, canned tuna), bulk meal prepping, brain-boosting omega fats.',
        'hydration_target': 3.0,
        'activity_multiplier': 1.45,
        'tips': [
            'Batch prep 3-4 days of rice, chicken/lentils, and boiled eggs on Sundays.',
            'Peanut butter, eggs, and Greek yogurt are your top cost-per-gram protein allies.',
            'Prioritize 7-8 hours of sleep especially during exam weeks for muscle and memory synthesis.',
            'If you have only 35 minutes between classes, hit compound supersets (Bench + Row, Squat + Plank).'
        ],
        'workout_focus': 'High-density compound workouts (Squat, Press, Pull) for maximum output in under 50 minutes.'
    },
    'athlete': {
        'title': 'Athlete / Sports',
        'icon': '🏃',
        'summary': 'Designed for high energy turnover, explosive power, endurance, fast glycogen replenishment, and rapid tissue repair.',
        'diet_focus': 'Higher complex carbohydrate intake around training, lean protein for fast recovery, electrolyte replenishment.',
        'hydration_target': 4.0,
        'activity_multiplier': 1.75,
        'tips': [
            'Consume fast-digesting carbs (banana, white rice, honey) 45-60 mins pre-training.',
            'Replenish electrolytes (sodium, potassium, magnesium) post-intense sweat sessions.',
            'Aim for 2.0-2.4g protein per kg to accelerate muscle fiber recovery.',
            'Incorporate 10 minutes of dynamic mobility and activation prior to all heavy sessions.'
        ],
        'workout_focus': 'Periodized explosive compound movements, unilateral balance work, and posterior chain strength.'
    },
    'bodybuilder': {
        'title': 'Bodybuilder / Hypertrophy',
        'icon': '🏋️',
        'summary': 'Engineered for maximal muscle hypertrophy, optimal protein distribution (leucine threshold), and strict macronutrient precision.',
        'diet_focus': 'High protein spaced every 3-4 hours, timed post-workout nutrition, dialed-in calorie surplus or deficit.',
        'hydration_target': 4.0,
        'activity_multiplier': 1.6,
        'tips': [
            'Distribute protein into 4-5 feedings with at least 30g protein each to maximize muscle protein synthesis (MPS).',
            'Take 5g creatine monohydrate daily with water or carbs for ATP replenishment.',
            'Train close to muscular failure (1-2 RIR) on working sets with strict form and tempo control.',
            'Log every set and rep to enforce progressive overload week over week.'
        ],
        'workout_focus': 'Push/Pull/Legs or Upper/Lower split with controlled eccentrics and targeted isolation.'
    },
    'busy_parent': {
        'title': 'Busy Parent / Professional',
        'icon': '👨‍👩‍👧',
        'summary': 'High-efficiency routines, minimal cooking fuss, family-friendly healthy meals, and high return-on-time workouts.',
        'diet_focus': 'Sheet-pan dinners, slow cooker stews, healthy high-protein snacks you can share with family.',
        'hydration_target': 3.0,
        'activity_multiplier': 1.45,
        'tips': [
            'One-pan oven roasts (chicken + sweet potatoes + broccoli) save both prep time and dishwashing.',
            'Keep Greek yogurt cups and fruit ready for grab-and-go moments.',
            '25-35 minute focused workouts deliver 90% of the health benefits when done consistently.',
            'Involve family in outdoor active walks or park sessions on rest days.'
        ],
        'workout_focus': 'Full-body circuits or 30-minute compound supersets that maximize time efficiency.'
    },
    'general': {
        'title': 'General Fitness & Health',
        'icon': '🧘',
        'summary': 'Sustainable lifelong vitality, functional strength, cardiovascular endurance, and balanced, low-stress nutrition.',
        'diet_focus': 'The 80/20 principle: 80% nutrient-dense whole foods, 20% flexibility, with balanced macros.',
        'hydration_target': 3.0,
        'activity_multiplier': 1.45,
        'tips': [
            'Aim for 8,000 to 10,000 steps daily outside the gym.',
            'Fill half your plate with colorful vegetables at lunch and dinner.',
            'Consistency over perfection: 3 workouts a week every week beats 6 workouts followed by burnout.',
            'Drink a tall glass of water first thing every morning before coffee.'
        ],
        'workout_focus': 'Balanced full-body resistance training combined with light cardio and mobility work.'
    }
}

# Culinary database categorized by dietary preferences
MEAL_RECIPES = {
    'standard': {
        'breakfast': [
            {
                'name': 'Power Scramble & Avocado Sourdough',
                'description': '3 whole eggs scrambled with spinach and cherry tomatoes, served on toasted sourdough with sliced avocado.',
                'ingredients': ['3 large eggs', '1 cup fresh baby spinach', '2 slices sourdough bread', '1/2 avocado', '1 tsp extra virgin olive oil', 'Pinch of black pepper & sea salt'],
                'prep_time': '12 mins',
                'base_cals': 520, 'p': 32, 'c': 42, 'f': 24
            },
            {
                'name': 'High-Protein Berry & Greek Yogurt Bowl',
                'description': 'Creamy non-fat Greek yogurt layered with whey protein, mixed antioxidant berries, chia seeds, and raw honey.',
                'ingredients': ['250g plain Greek yogurt', '1 scoop (30g) vanilla whey protein', '1/2 cup blueberries', '1/2 cup strawberries', '1 tbsp chia seeds', '1 tbsp raw honey or almond slices'],
                'prep_time': '5 mins',
                'base_cals': 440, 'p': 46, 'c': 45, 'f': 8
            },
            {
                'name': 'Steel-Cut Oats with Whey & Peanut Butter',
                'description': 'Slow-simmered oats stirred with chocolate whey protein, topped with sliced banana and natural peanut butter.',
                'ingredients': ['60g rolled oats', '1 scoop chocolate whey protein', '1 medium banana', '1.5 tbsp natural peanut butter', '1 cup unsweetened almond milk'],
                'prep_time': '8 mins',
                'base_cals': 530, 'p': 38, 'c': 62, 'f': 15
            }
        ],
        'lunch': [
            {
                'name': 'Grilled Herb Chicken & Quinoa Harvest Bowl',
                'description': 'Tender grilled chicken breast over fluffy quinoa, roasted zucchini, bell peppers, and lemon tahini drizzle.',
                'ingredients': ['180g skinless chicken breast', '1 cup cooked quinoa', '1 roasted bell pepper', '1 sliced zucchini', '1 tbsp lemon-tahini dressing', 'Fresh parsley'],
                'prep_time': '20 mins',
                'base_cals': 560, 'p': 48, 'c': 52, 'f': 16
            },
            {
                'name': 'Lean Beef & Sweet Potato Power Plate',
                'description': '90% lean ground beef sauteed with garlic and paprika, alongside roasted cinnamon sweet potato wedges and steamed broccoli.',
                'ingredients': ['170g extra-lean ground beef', '200g sweet potato cubes', '1.5 cups steamed broccoli florets', '1 tsp olive oil', 'Smoked paprika & garlic powder'],
                'prep_time': '22 mins',
                'base_cals': 580, 'p': 46, 'c': 56, 'f': 18
            },
            {
                'name': 'Mediterranean Turkey & Hummus Wrap',
                'description': 'Sliced roasted turkey breast in a whole wheat wrap with crisp cucumbers, tomatoes, kalamata olives, and garlic hummus.',
                'ingredients': ['160g roasted turkey slices', '1 large whole wheat tortilla', '2 tbsp roasted garlic hummus', 'Cucumber slices', 'Shredded romaine lettuce', '1 tbsp feta cheese'],
                'prep_time': '10 mins',
                'base_cals': 490, 'p': 42, 'c': 44, 'f': 15
            }
        ],
        'snack': [
            {
                'name': 'Banana & Almond Butter Rice Cakes',
                'description': 'Crispy whole grain brown rice cakes spread with crunchy almond butter and sliced banana.',
                'ingredients': ['2 whole brown rice cakes', '1.5 tbsp almond butter', '1/2 sliced banana', 'Pinch of cinnamon'],
                'prep_time': '3 mins',
                'base_cals': 260, 'p': 8, 'c': 34, 'f': 12
            },
            {
                'name': 'Cottage Cheese with Pineapple & Walnuts',
                'description': 'Slow-digesting casein-rich cottage cheese paired with tropical fresh pineapple and crushed walnuts.',
                'ingredients': ['1 cup low-fat cottage cheese', '1/2 cup fresh diced pineapple', '15g crushed walnuts'],
                'prep_time': '3 mins',
                'base_cals': 270, 'p': 26, 'c': 22, 'f': 9
            },
            {
                'name': 'Hard-Boiled Eggs & Crisp Apple',
                'description': 'Two pasture-raised hard-boiled eggs with sea salt and a crisp Honeycrisp apple.',
                'ingredients': ['2 large hard-boiled eggs', '1 crisp medium apple', 'Everything bagel seasoning'],
                'prep_time': '2 mins',
                'base_cals': 240, 'p': 14, 'c': 25, 'f': 10
            }
        ],
        'dinner': [
            {
                'name': 'Wild Atlantic Salmon & Asparagus with Brown Rice',
                'description': 'Pan-seared salmon fillet glazed with lemon and dill, served with charred asparagus spears and steamed brown rice.',
                'ingredients': ['180g wild salmon fillet', '1 cup cooked brown rice', '8 spears fresh asparagus', '1 tsp olive oil', 'Lemon wedges & sea salt'],
                'prep_time': '20 mins',
                'base_cals': 610, 'p': 44, 'c': 48, 'f': 24
            },
            {
                'name': 'Chicken Breast Stir-Fry with Cashews & Jasmine Rice',
                'description': 'Diced chicken breast stir-fried with crisp sugar snap peas, carrots, baby corn, ginger soy glaze, and roasted cashews.',
                'ingredients': ['180g chicken breast', '1 cup cooked jasmine rice', '1.5 cups mixed stir-fry vegetables', '15g roasted cashews', '1 tbsp low-sodium tamari soy sauce'],
                'prep_time': '18 mins',
                'base_cals': 580, 'p': 46, 'c': 58, 'f': 16
            },
            {
                'name': 'Hearty Turkey & Bean Chili',
                'description': 'Slow-simmered lean minced turkey with black beans, kidney beans, crushed fire-roasted tomatoes, and cumin.',
                'ingredients': ['170g lean ground turkey', '1/2 cup black beans', '1/2 cup kidney beans', '1 cup crushed tomatoes', '1/4 diced onion', 'Cumin, chili flakes, cilantro'],
                'prep_time': '25 mins',
                'base_cals': 520, 'p': 48, 'c': 50, 'f': 12
            }
        ]
    },
    'vegetarian': {
        'breakfast': [
            {
                'name': 'Spiced Paneer Scramble (Bhurji) with Multigrain Roti',
                'description': 'Fresh low-fat paneer crumbled and sauteed with turmeric, onions, bell peppers, green chilies, served with warm roti.',
                'ingredients': ['150g low-fat paneer', '2 small multigrain rotis', '1/2 onion & 1/2 tomato diced', '1 cup baby spinach', '1 tsp cold-pressed mustard or olive oil'],
                'prep_time': '15 mins',
                'base_cals': 510, 'p': 34, 'c': 46, 'f': 20
            },
            {
                'name': 'Greek Yogurt Berry Parfait with Hemp Hearts',
                'description': 'Thick protein-dense Greek yogurt with chia seeds, wild blueberries, raw walnuts, and shelled hemp hearts.',
                'ingredients': ['250g plain Greek yogurt', '3 tbsp shelled hemp seeds', '1/2 cup blueberries', '1 tbsp pumpkin seeds', '1 tsp cinnamon'],
                'prep_time': '5 mins',
                'base_cals': 460, 'p': 38, 'c': 32, 'f': 18
            },
            {
                'name': 'Protein Oatmeal with Peanut Butter & Chia',
                'description': 'Warm oats whipped with plant/whey protein powder, chia seeds, sliced bananas, and rich peanut butter.',
                'ingredients': ['60g rolled oats', '1 scoop protein powder', '1 tbsp chia seeds', '1.5 tbsp natural peanut butter', '1 cup oat/soy milk'],
                'prep_time': '8 mins',
                'base_cals': 520, 'p': 36, 'c': 58, 'f': 16
            }
        ],
        'lunch': [
            {
                'name': 'Mediterranean Chickpea & Grilled Halloumi Salad',
                'description': 'Tossed chickpeas, cucumber, cherry tomatoes, kalamata olives, and warm seared halloumi with lemon-herb vinaigrette.',
                'ingredients': ['1.5 cups cooked chickpeas', '60g grilled halloumi or paneer', '1 cup diced cucumbers & tomatoes', '1 tbsp extra virgin olive oil', 'Fresh mint and lemon juice'],
                'prep_time': '15 mins',
                'base_cals': 560, 'p': 32, 'c': 54, 'f': 22
            },
            {
                'name': 'High-Protein Lentil Dahl with Brown Basmati Rice',
                'description': 'Golden simmered yellow and red lentils with ginger, cumin, spinach, and a side of nutty brown basmati rice.',
                'ingredients': ['1.5 cups cooked yellow dal', '1 cup cooked brown basmati rice', '1 cup wilted spinach', '1 tsp ghee or coconut oil', 'Fresh coriander'],
                'prep_time': '20 mins',
                'base_cals': 520, 'p': 28, 'c': 76, 'f': 10
            },
            {
                'name': 'Tofu & Edamame Soba Noodle Bowl',
                'description': 'Crispy pan-seared firm tofu with edamame beans, shredded purple cabbage, soba noodles, and toasted sesame dressing.',
                'ingredients': ['180g extra-firm tofu', '1/2 cup shelled edamame', '70g dry weight buckwheat soba noodles', '1 cup shredded cabbage', '1 tbsp sesame oil & soy sauce'],
                'prep_time': '18 mins',
                'base_cals': 540, 'p': 36, 'c': 56, 'f': 18
            }
        ],
        'snack': [
            {
                'name': 'Roasted Spiced Chickpeas & Almonds',
                'description': 'Crunchy oven-roasted chickpeas tossed in smoked paprika with raw roasted almonds.',
                'ingredients': ['1/2 cup roasted chickpeas', '20g raw almonds', 'Sea salt & smoked paprika'],
                'prep_time': '3 mins',
                'base_cals': 250, 'p': 12, 'c': 28, 'f': 11
            },
            {
                'name': 'Cottage Cheese with Berries & Flax',
                'description': 'Fresh creamy cottage cheese with strawberries and golden ground flaxseed.',
                'ingredients': ['1 cup low-fat cottage cheese', '1/2 cup strawberries', '1 tbsp ground flaxseeds'],
                'prep_time': '2 mins',
                'base_cals': 230, 'p': 26, 'c': 18, 'f': 6
            },
            {
                'name': 'Soy Milk Shake with Banana & Cacao',
                'description': 'Chilled organic soy milk blended with dark cacao powder, banana, and a spoon of peanut butter.',
                'ingredients': ['1.5 cups soy milk', '1 medium banana', '1 tbsp unsweetened cacao', '1 tbsp peanut butter'],
                'prep_time': '4 mins',
                'base_cals': 300, 'p': 16, 'c': 38, 'f': 11
            }
        ],
        'dinner': [
            {
                'name': 'Grilled Paneer & Quinoa Buddha Bowl',
                'description': 'Charred spiced paneer cubes over tricolor quinoa with steamed broccoli, bell peppers, and lemon tahini dressing.',
                'ingredients': ['150g grilled paneer', '1 cup cooked quinoa', '1.5 cups steamed broccoli & peppers', '1 tbsp tahini dressing'],
                'prep_time': '22 mins',
                'base_cals': 580, 'p': 36, 'c': 48, 'f': 26
            },
            {
                'name': 'Black Bean & Sweet Potato Enchilada Skillet',
                'description': 'Simmered black beans, diced sweet potato, sweet corn, salsa verde, topped with melted low-fat mozzarella or feta.',
                'ingredients': ['1.5 cups cooked black beans', '150g roasted sweet potatoes', '1/2 cup salsa verde', '40g shredded cheese', 'Fresh cilantro & lime'],
                'prep_time': '25 mins',
                'base_cals': 510, 'p': 28, 'c': 72, 'f': 12
            },
            {
                'name': 'Creamy Red Lentil & Spinach Curry with Warm Naan',
                'description': 'Rich coconut-tomato red lentil curry loaded with spinach, served with a portion of whole wheat naan or flatbread.',
                'ingredients': ['1.5 cups cooked red lentils', '1 cup fresh baby spinach', '2 tbsp light coconut milk', '1 whole wheat naan/roti', 'Ginger, turmeric, garam masala'],
                'prep_time': '20 mins',
                'base_cals': 530, 'p': 29, 'c': 74, 'f': 12
            }
        ]
    },
    'vegan': {
        'breakfast': [
            {
                'name': 'Southwest Tofu Scramble with Avocado & Sprouted Toast',
                'description': 'Crumbled turmeric tofu sauteed with black beans, nutritional yeast, peppers, served with sprouted grain toast.',
                'ingredients': ['200g firm tofu crumbled', '1/3 cup black beans', '2 tbsp nutritional yeast', '2 slices sprouted bread', '1/4 avocado'],
                'prep_time': '12 mins',
                'base_cals': 480, 'p': 32, 'c': 45, 'f': 18
            },
            {
                'name': 'Chia Seed & Hemp Superfood Pudding',
                'description': 'Overnight chia pudding made with unsweetened soy milk, pea protein, hemp seeds, and fresh berries.',
                'ingredients': ['3 tbsp chia seeds', '1 scoop plant protein powder', '1.5 cups unsweetened soy milk', '2 tbsp hemp seeds', '1/2 cup blueberries'],
                'prep_time': '5 mins',
                'base_cals': 440, 'p': 35, 'c': 32, 'f': 18
            }
        ],
        'lunch': [
            {
                'name': 'Tempeh Grain Bowl with Steamed Greens & Tahini',
                'description': 'Marinated maple-tamari tempeh strips over farro, massaged kale, roasted beets, and lemon tahini.',
                'ingredients': ['160g organic tempeh', '1 cup cooked farro or brown rice', '1.5 cups chopped kale', '1.5 tbsp lemon tahini dressing'],
                'prep_time': '20 mins',
                'base_cals': 550, 'p': 36, 'c': 54, 'f': 22
            },
            {
                'name': 'Spiced Chickpea & Edamame Crunch Salad',
                'description': 'Tossed edamame, chickpeas, bell peppers, sunflower seeds, and tangy apple cider vinaigrette.',
                'ingredients': ['1 cup cooked chickpeas', '1 cup shelled edamame', '1 cup chopped bell peppers & cucumber', '2 tbsp sunflower seeds', '1 tbsp olive oil vinaigrette'],
                'prep_time': '12 mins',
                'base_cals': 520, 'p': 32, 'c': 50, 'f': 20
            }
        ],
        'snack': [
            {
                'name': 'Pea Protein Shake with Banana & Flax',
                'description': 'Rich vanilla pea protein shaken with oat milk, a banana, and ground flaxseed.',
                'ingredients': ['1 scoop pea protein (25g P)', '1.5 cups oat/soy milk', '1 medium banana', '1 tbsp ground flax'],
                'prep_time': '3 mins',
                'base_cals': 310, 'p': 29, 'c': 38, 'f': 6
            },
            {
                'name': 'Edamame in Pod with Sea Salt',
                'description': 'Steamed organic edamame pods sprinkled with coarse flaky sea salt.',
                'ingredients': ['1.5 cups steamed edamame pods', 'Flaky sea salt'],
                'prep_time': '5 mins',
                'base_cals': 210, 'p': 18, 'c': 15, 'f': 8
            }
        ],
        'dinner': [
            {
                'name': 'Crispy Sesame Tofu & Broccoli with Jasmine Rice',
                'description': 'Air-fried sesame crusted tofu cubes tossed with garlic broccoli florets and steamed fragrant jasmine rice.',
                'ingredients': ['220g extra-firm tofu', '1.5 cups broccoli florets', '1 cup cooked jasmine rice', '1 tbsp toasted sesame seeds & oil', 'Low-sodium soy sauce'],
                'prep_time': '22 mins',
                'base_cals': 570, 'p': 34, 'c': 62, 'f': 20
            },
            {
                'name': 'Lentil Bolognese over High-Protein Chickpea Pasta',
                'description': 'Rich slow-simmered green lentil ragu with crushed Italian tomatoes, served over Banza chickpea pasta.',
                'ingredients': ['1 cup cooked brown lentils', '75g chickpea pasta', '1 cup marinara sauce', '1 tbsp nutritional yeast', 'Fresh basil'],
                'prep_time': '25 mins',
                'base_cals': 540, 'p': 38, 'c': 76, 'f': 9
            }
        ]
    },
    'keto': {
        'breakfast': [
            {
                'name': 'Keto Avocado & Bacon Omelette',
                'description': '3 pasture-raised eggs folded with crispy bacon, sharp cheddar cheese, and freshly sliced hass avocado.',
                'ingredients': ['3 large eggs', '2 strips nitrate-free bacon', '30g sharp cheddar cheese', '1/2 avocado', '1 tbsp grass-fed butter'],
                'prep_time': '12 mins',
                'base_cals': 590, 'p': 34, 'c': 4, 'f': 49
            },
            {
                'name': 'Smoked Salmon & Cream Cheese Flaxseed Wrap',
                'description': 'Premium smoked wild salmon with chive cream cheese, capers, and cucumber in a low-carb flax wrap.',
                'ingredients': ['120g smoked salmon', '2 tbsp full-fat cream cheese', '1 low-carb tortilla (under 3g net carbs)', 'Cucumbers & capers'],
                'prep_time': '6 mins',
                'base_cals': 420, 'p': 32, 'c': 5, 'f': 28
            }
        ],
        'lunch': [
            {
                'name': 'Grilled Chicken Caesar Salad with Crispy Bacon',
                'description': 'Crisp romaine lettuce hearts tossed with grilled chicken, bacon bits, parmesan crisps, and rich olive-oil Caesar dressing.',
                'ingredients': ['180g grilled chicken breast', '2 cups romaine lettuce', '2 tbsp full-fat Caesar dressing', '30g shaved parmesan', '1 strip crumbled bacon'],
                'prep_time': '15 mins',
                'base_cals': 560, 'p': 50, 'c': 4, 'f': 37
            }
        ],
        'snack': [
            {
                'name': 'Macadamia Nuts & String Cheese',
                'description': 'Raw buttery macadamia nuts paired with whole milk mozzarella string cheese.',
                'ingredients': ['28g raw macadamia nuts', '1 mozzarella string cheese'],
                'prep_time': '1 min',
                'base_cals': 280, 'p': 9, 'c': 4, 'f': 26
            }
        ],
        'dinner': [
            {
                'name': 'Pan-Seared Ribeye Steak with Garlic Butter Mushrooms & Asparagus',
                'description': 'Juicy grass-fed ribeye seared with garlic herb butter, served alongside sauteed cremini mushrooms and asparagus.',
                'ingredients': ['200g ribeye steak', '1 tbsp grass-fed butter', '1 cup sliced cremini mushrooms', '6 spears asparagus', 'Fresh rosemary & sea salt'],
                'prep_time': '20 mins',
                'base_cals': 640, 'p': 46, 'c': 5, 'f': 48
            }
        ]
    }
}


def calculate_user_targets(user, custom_calories=None):
    """Calculate personalized calorie and macro targets based on role, goal, and metrics."""
    bmr = user.calculate_bmr()
    tdee = user.calculate_tdee()

    if custom_calories:
        calories = int(custom_calories)
    else:
        calories = user.get_calorie_target()

    macros = user.get_target_macros()
    # adjust for custom calories if supplied
    if custom_calories and custom_calories != macros['calories']:
        ratio = custom_calories / max(1000, macros['calories'])
        macros['calories'] = int(custom_calories)
        macros['protein'] = int(macros['protein'] * ratio)
        macros['carbs'] = int(macros['carbs'] * ratio)
        macros['fat'] = int(macros['fat'] * ratio)

    role_key = user.role if user.role in ROLE_DETAILS else 'general'
    role_info = ROLE_DETAILS[role_key]

    return {
        'bmr': bmr,
        'tdee': tdee,
        'calories': macros['calories'],
        'protein': macros['protein'],
        'carbs': macros['carbs'],
        'fat': macros['fat'],
        'water_liters': role_info['hydration_target'],
        'role_title': role_info['title'],
        'role_icon': role_info['icon'],
        'role_summary': role_info['summary'],
        'role_tips': role_info['tips'],
        'workout_focus': role_info['workout_focus']
    }


def generate_ai_diet_plan(user, dietary_preference=None, custom_calories=None):
    """
    Generates a structured daily meal plan (Breakfast, Lunch, Snack, Dinner)
    scaled to the user's role, goal, and target macros.
    """
    pref = dietary_preference or user.dietary_preference or 'standard'
    if pref not in MEAL_RECIPES:
        pref = 'standard'

    targets = calculate_user_targets(user, custom_calories)
    target_cals = targets['calories']
    role_key = user.role if user.role in ROLE_DETAILS else 'general'
    role_info = ROLE_DETAILS[role_key]

    # Target breakdown: Breakfast ~26%, Lunch ~33%, Snack ~15%, Dinner ~26%
    meal_allocations = [
        ('breakfast', 'Breakfast', '07:30 - 08:30', 0.26),
        ('lunch', 'Lunch', '12:30 - 13:30', 0.33),
        ('snack', 'Mid-Day Fuel / Snack', '16:00 - 16:30', 0.15),
        ('dinner', 'Dinner', '19:30 - 20:30', 0.26),
    ]

    recipe_catalog = MEAL_RECIPES[pref]
    fallback_catalog = MEAL_RECIPES['standard']

    meals = []
    total_planned_cals = 0
    total_p = 0
    total_c = 0
    total_f = 0

    for slot_id, slot_name, time_str, alloc_pct in meal_allocations:
        slot_recipes = recipe_catalog.get(slot_id) or fallback_catalog.get(slot_id, fallback_catalog['breakfast'])
        chosen = random.choice(slot_recipes)

        slot_target_cals = round(target_cals * alloc_pct)
        base_cals = chosen.get('base_cals', 400)
        scale = max(0.6, min(1.8, slot_target_cals / base_cals))

        scaled_cals = round(base_cals * scale)
        scaled_p = round(chosen.get('p', 30) * scale)
        scaled_c = round(chosen.get('c', 40) * scale)
        scaled_f = round(chosen.get('f', 15) * scale)

        total_planned_cals += scaled_cals
        total_p += scaled_p
        total_c += scaled_c
        total_f += scaled_f

        # Add role-specific note for this meal
        if role_key == 'desk_worker':
            if slot_id == 'lunch':
                benefit = 'Engineered with clean slow-release energy to eliminate the post-lunch 2 PM slump.'
            elif slot_id == 'snack':
                benefit = 'Desk-friendly bite to maintain dopamine and blood sugar while seated.'
            else:
                benefit = 'Anti-inflammatory nutrients supporting joint comfort during long sitting.'
        elif role_key == 'student':
            benefit = 'Fast preparation, cost-effective protein source with optimal study brain-fuel.'
        elif role_key == 'athlete':
            benefit = 'Glycogen re-synthesis blend optimized for stamina and rapid muscle replenishment.'
        elif role_key == 'bodybuilder':
            benefit = 'Exceeds the 3g leucine threshold to fully trigger Muscle Protein Synthesis (MPS).'
        elif role_key == 'busy_parent':
            benefit = 'Zero-fuss preparation time so you spend less time cooking and more with family.'
        else:
            benefit = 'Nutrient-dense whole foods designed for sustained vitality and gut health.'

        meals.append({
            'id': slot_id,
            'name': chosen['name'],
            'slot_name': slot_name,
            'time': time_str,
            'description': chosen['description'],
            'ingredients': chosen['ingredients'],
            'prep_time': chosen['prep_time'],
            'calories': scaled_cals,
            'protein': scaled_p,
            'carbs': scaled_c,
            'fat': scaled_f,
            'role_benefit': benefit,
            'completed': False
        })

    title = f"{role_info['icon']} AI Nutrition: {user.goal.capitalize()} ({role_info['title']} Edition)"

    return {
        'title': title,
        'goal': user.goal,
        'role': role_key,
        'dietary_preference': pref,
        'target_calories': targets['calories'],
        'target_protein': targets['protein'],
        'target_carbs': targets['carbs'],
        'target_fat': targets['fat'],
        'planned_calories': total_planned_cals,
        'planned_protein': total_p,
        'planned_carbs': total_c,
        'planned_fat': total_f,
        'water_liters': targets['water_liters'],
        'meals': meals,
        'role_tips': role_info['tips'],
        'role_summary': role_info['summary'],
        'diet_focus': role_info['diet_focus']
    }


def get_user_ai_recommendations(user):
    """
    Generates dynamic, real-time AI coaching insights based on the user's
    current role, streak, attendance history, weight logs, and goal.
    """
    bmi, bmi_cat = user.calculate_bmi()
    streak = user.get_current_streak()
    month_checkins = user.get_month_checkin_count()
    role_key = user.role if user.role in ROLE_DETAILS else 'general'
    role_info = ROLE_DETAILS[role_key]

    # Analyze weight logs
    weights = [w.weight_kg for w in user.weight_logs]
    weight_insight = None
    if len(weights) >= 2:
        diff = round(weights[-1] - weights[0], 1)
        if user.goal == 'cutting':
            if diff < 0:
                weight_insight = f"Down {abs(diff)} kg since starting. Your caloric deficit is working smoothly. Keep dietary fiber high."
            elif diff > 0:
                weight_insight = f"Weight is up by {diff} kg. This could be temporary water retention or subtle caloric surplus; consider tracking sodium and weekend snacks."
            else:
                weight_insight = "Weight is plateaued. If this persists for >10 days, reduce daily carbs/fats by 150 kcal."
        elif user.goal == 'bulking':
            if diff > 0:
                weight_insight = f"Gained {diff} kg. Solid muscle-building trajectory! Aim for 0.25-0.5kg/week to minimize excess fat."
            else:
                weight_insight = "Weight hasn't increased yet. You need more caloric density—add a handful of nuts or an extra scoop of oats."
        else:
            weight_insight = f"Weight fluctuation is minimal ({diff:+} kg). You are maintaining your target equilibrium."
    elif user.weight_kg and user.target_weight_kg:
        diff = round(abs(user.weight_kg - user.target_weight_kg), 1)
        weight_insight = f"You are {diff} kg away from your target of {user.target_weight_kg} kg. Consistency is your highest leverage asset."
    else:
        weight_insight = "Log your weight consistently every few days to unlock predictive progress forecasting."

    # Consistency score (0 - 100)
    consistency_score = min(100, (month_checkins * 5) + (streak * 7))

    # Daily coaching priority
    if streak == 0:
        priority = "Hit the gym today! One session is all it takes to reignite your streak and boost your mood."
    elif streak >= 5:
        priority = f"🔥 Phenomenal {streak}-day streak! Ensure you prioritize 8 hours of sleep and adequate hydration ({role_info['hydration_target']}L) to prevent overtraining."
    else:
        priority = f"You're on a {streak}-day streak. Lock in today's session according to your workout plan."

    # Supplement recommendations
    supplements = [
        {'name': 'Creatine Monohydrate', 'dosage': '5g daily', 'benefit': 'Enhances ATP energy production, power output, and cognitive focus.'},
        {'name': 'Whey or Plant Protein', 'dosage': '1 scoop (25-30g)', 'benefit': 'Convenient method to hit daily protein target.'},
        {'name': 'Omega-3 Fish Oil / Algae', 'dosage': '1000-2000mg EPA/DHA', 'benefit': 'Combats inflammation and supports heart & brain function.'},
        {'name': 'Vitamin D3 + K2', 'dosage': '2000-5000 IU', 'benefit': 'Crucial for immunity, testosterone/hormonal balance, and bone density.'}
    ]

    return {
        'role_title': role_info['title'],
        'role_icon': role_info['icon'],
        'role_summary': role_info['summary'],
        'consistency_score': consistency_score,
        'streak': streak,
        'month_checkins': month_checkins,
        'bmi': bmi,
        'bmi_category': bmi_cat,
        'weight_insight': weight_insight,
        'daily_priority': priority,
        'role_tips': role_info['tips'],
        'workout_focus': role_info['workout_focus'],
        'supplements': supplements,
        'hydration_target': role_info['hydration_target']
    }


def query_gemini_api(api_key, system_instruction, user_prompt):
    """Calls Google Gemini REST API directly with standard library urllib."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": f"System Context:\n{system_instruction}\n\nUser Question:\n{user_prompt}"}]
            }
        ],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 600
        }
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=10) as response:
        res_data = json.loads(response.read().decode('utf-8'))
        return res_data['candidates'][0]['content']['parts'][0]['text']


def ask_ai_coach(user, query):
    """
    Processes a user query with the Fitrack AI Coach.
    Uses Gemini API if GEMINI_API_KEY exists, otherwise uses our smart contextual knowledge engine.
    """
    query_clean = query.strip()
    q_lower = query_clean.lower()
    role_key = user.role if user.role in ROLE_DETAILS else 'general'
    role_info = ROLE_DETAILS[role_key]

    system_context = (
        f"You are FitBot, an elite, encouraging, and evidence-based AI Fitness & Nutrition Coach for the Fitrack app. "
        f"User Profile: Username: {user.username}, Role: {role_info['title']}, Goal: {user.goal}, "
        f"Fitness Level: {user.fitness_level}, Weight: {user.weight_kg or 'Not set'}kg, "
        f"Target: {user.target_weight_kg or 'Not set'}kg, Current Streak: {user.get_current_streak()} days. "
        f"Give concise, punchy, actionable advice with bullet points where appropriate."
    )

    # 1. Try external LLM API if key is set
    gemini_key = os.environ.get('GEMINI_API_KEY')
    if gemini_key:
        try:
            return query_gemini_api(gemini_key, system_context, query_clean)
        except Exception:
            # Fall back gracefully to built-in expert engine
            pass

    # 2. Built-in Contextual Expert Engine (Prioritized Semantic Intent Matching)
    
    # Intent 1: Pre-workout snacks, fuel, and quick snacks
    if any(k in q_lower for k in ['pre-workout', 'pre workout', 'preworkout', 'before workout', 'before gym', 'snack', 'snacks']):
        goal = user.goal or 'maintaining'
        if goal == 'cutting':
            snack_picks = (
                "• **Option 1 (Light & Crisp):** 2 whole brown rice cakes with 1 tbsp peanut butter & sea salt (~160 kcal, 22g carbs, 4g protein).\n"
                "• **Option 2 (High Protein Satiety):** 150g non-fat Greek yogurt with 1/2 cup blueberries and cinnamon (~130 kcal, 17g protein, 14g carbs).\n"
                "• **Option 3 (Quick Energy):** 1 medium crisp apple with 1 string cheese (~160 kcal, 20g carbs, 7g protein)."
            )
            timing = "Consume 45–60 minutes before training. Delivers quick-burning carbohydrates with minimal fat so digestion doesn't slow you down during your caloric deficit."
        elif goal == 'bulking':
            snack_picks = (
                "• **Option 1 (Glycogen Saturation):** 60g rolled oats cooked with 1 scoop whey protein, sliced banana & 1.5 tbsp peanut butter (~450 kcal, 36g protein, 55g carbs).\n"
                "• **Option 2 (Fast Glycogen):** 2 slices toasted sourdough with almond butter, honey drizzle & sliced strawberries (~380 kcal, 10g protein, 65g carbs).\n"
                "• **Option 3 (Power Fuel):** Whole wheat bagel with light cream cheese & sliced turkey or boiled egg (~350 kcal, 22g protein, 48g carbs)."
            )
            timing = "Consume 60–90 minutes before training to flood your muscles with glycogen for heavy lifting volume and muscular pumps."
        else: # maintaining / general
            snack_picks = (
                "• **Option 1 (The Classic):** 1 medium ripe banana paired with 1 tbsp natural peanut/almond butter (~190 kcal, 30g carbs, 4g protein).\n"
                "• **Option 2 (Rice Cake Pump Stack):** 2 brown rice cakes with raw honey and a dash of pink Himalayan salt (~160 kcal, 36g carbs — the sodium elevates muscle fullness).\n"
                "• **Option 3 (Liquid Fuel):** Whey or plant protein shake blended with 1/2 cup mixed berries and almond milk (~200 kcal, 25g protein, 15g carbs)."
            )
            timing = "Consume 45–60 minutes before training for steady blood glucose without digestive heaviness."

        # Role-specific adaptation note
        if role_key == 'desk_worker':
            role_note = "💼 *Desk Worker Tip:* Drink 500ml water alongside your snack. Office air-conditioning induces unnoticed dehydration, which can slash lifting power by up to 15%."
        elif role_key == 'student':
            role_note = "🎓 *Student Tip:* Bananas and rice cakes are cheap and backpack-portable—never head to the gym directly from lectures on empty glycogen reserves."
        elif role_key == 'athlete':
            role_note = "🏃 *Athlete Tip:* Add an electrolyte tablet or pinch of salt to your pre-workout hydration for peak intra-muscular hydration and cramp prevention."
        elif role_key == 'bodybuilder':
            role_note = "🏋️ *Bodybuilder Tip:* Consume 5g creatine monohydrate alongside your fast-acting carbs to maximize cellular hydration and ATP turnover."
        elif role_key == 'busy_parent':
            role_note = "👨‍👩‍👧 *Parent Tip:* Keep a jar of raw almonds and bananas in your car for an effortless grab-and-go snack on busy days."
        else:
            role_note = "🧘 *General Tip:* Avoid high-fat or greasy foods right before working out to avoid sluggish digestion."

        return (
            f"⚡ **Top Pre-Workout Snacks for Today ({role_info['title']} • {user.goal.capitalize()}):**\n\n"
            f"{snack_picks}\n\n"
            f"⏱ **Timing:** {timing}\n\n"
            f"{role_note}"
        )

    # Intent 2: Post-workout meals & recovery fuel
    elif any(k in q_lower for k in ['post-workout', 'post workout', 'postworkout', 'after workout', 'after gym']):
        return (
            f"💪 **Post-Workout Recovery Blueprint ({user.goal.capitalize()}):**\n\n"
            f"• **The Recovery Window:** Consume a nutrient-dense meal within 45–90 minutes post-workout containing 25–40g high-quality protein and complex carbs.\n"
            f"• **Top Meal 1:** Grilled chicken breast or paneer/tofu bowl with brown basmati rice, steamed broccoli, and olive oil drizzle.\n"
            f"• **Top Meal 2:** Whey or plant protein shake with a ripe banana and 2 rice cakes or whole wheat toast.\n"
            f"• **Top Meal 3:** 3-egg scramble (or tofu scramble) with sauteed spinach and roasted sweet potato cubes.\n"
            f"• **Hydration:** Rehydrate with 500–750ml water to replace fluid lost during the session."
        )

    # Intent 3: Role-specific hacks and lifestyle routines
    elif any(k in q_lower for k in ['role hack', 'role tip', 'role tips', 'hack for my role', 'desk hack', 'student hack', 'desk job', 'sitting', 'posture', 'desk']):
        return (
            f"💼 **Performance & Ergonomic Hacks for {role_info['title']}:**\n\n"
            + "\n".join([f"• {tip}" for tip in role_info['tips']]) + "\n\n"
            f"• **Mobility Focus:** {role_info['workout_focus']}\n"
            f"• **Daily Hydration:** Aim for {role_info['hydration_target']}L of water today."
        )

    # Intent 4: Supplements & Creatine
    elif any(k in q_lower for k in ['supplement', 'supplements', 'creatine', 'vitamin', 'omega', 'fish oil']):
        return (
            f"💊 **Evidence-Based Supplement Protocol ({user.goal.capitalize()}):**\n\n"
            f"• **Creatine Monohydrate:** 5g daily (every day, with water or carbs). Enhances cellular ATP, power output, and cognitive focus.\n"
            f"• **Whey or Plant Protein:** 1 scoop (25–30g) as needed to reach your daily {user.get_target_macros()['protein']}g protein goal.\n"
            f"• **Omega-3 Fish Oil / Algae:** 1,000–2,000mg EPA/DHA daily for cardiovascular support and joint inflammation reduction.\n"
            f"• **Vitamin D3 + K2:** 2,000–4,000 IU daily for bone density and hormonal health."
        )

    # Intent 5: Macros & Caloric Targets
    elif any(k in q_lower for k in ['macro', 'macros', 'calorie', 'calories', 'tdee', 'bmr', 'target']):
        cals = user.get_calorie_target()
        macros = user.get_target_macros()
        return (
            f"🥗 **Calculated Nutrition Blueprint ({role_info['title']} • {user.goal.capitalize()}):**\n\n"
            f"• **Daily Calorie Target:** ~**{cals} kcal** (BMR: {user.calculate_bmr()} | TDEE: {user.calculate_tdee()})\n"
            f"• **Protein:** **{macros['protein']}g** (~{macros['protein']*4} kcal) — Essential for muscle preservation & repair.\n"
            f"• **Carbohydrates:** **{macros['carbs']}g** (~{macros['carbs']*4} kcal) — Primary glycogen fuel source.\n"
            f"• **Healthy Fats:** **{macros['fat']}g** (~{macros['fat']*9} kcal) — Vital for hormonal and cell health.\n"
            f"• *Tip:* Head to your **AI Diet** tab to view your complete 4-meal daily blueprint."
        )

    # Intent 6: Protein Requirements & Sources
    elif any(k in q_lower for k in ['protein', 'how much protein', 'protein powder', 'whey']):
        macros = user.get_target_macros()
        return (
            f"🥩 **Protein Strategy for {user.username}:**\n\n"
            f"• Aim for **{macros['protein']}g protein daily** (~2.0-2.2g per kg of bodyweight).\n"
            f"• Distribute across 3-4 meals (~30-45g per feeding) to consistently stimulate muscle protein synthesis.\n"
            f"• **Top Sources:** Chicken breast, eggs, Greek yogurt, canned tuna, paneer, tofu, lentils, and whey/plant protein powder.\n"
            f"• *Role tip:* {role_info['tips'][1] if len(role_info['tips']) > 1 else 'Keep high-protein snacks within reach.'}"
        )

    # Intent 7: Diet & General Meal Planning
    elif any(k in q_lower for k in ['diet', 'meal', 'eat', 'food', 'nutrition', 'hungry']):
        cals = user.get_calorie_target()
        macros = user.get_target_macros()
        return (
            f"🥗 **Nutrition Strategy for your {role_info['title']} role ({user.goal}):**\n\n"
            f"• **Daily Calories:** ~**{cals} kcal**\n"
            f"• **Macros:** **{macros['protein']}g Protein** | **{macros['carbs']}g Carbs** | **{macros['fat']}g Fats**\n"
            f"• **Role Strategy:** {role_info['diet_focus']}\n"
            f"• Check the **AI Diet** tab for your full 4-meal breakfast, lunch, snack, and dinner plan."
        )

    # Intent 8: Soreness & Recovery
    elif any(k in q_lower for k in ['sore', 'pain', 'rest day', 'recovery', 'tired', 'doms', 'sleep']):
        return (
            f"🧘 **Recovery Protocol for {user.username}:**\n\n"
            f"• Delayed Onset Muscle Soreness (DOMS) is natural when increasing training stimulus or volume.\n"
            f"• **Active Recovery:** Go for a 20-minute brisk walk, do gentle foam rolling, and stretch.\n"
            f"• **Hydration & Electrolytes:** Aim for at least {role_info['hydration_target']}L water today.\n"
            f"• If soreness is sharp or joint-related, take a dedicated rest day or swap to mobility work."
        )

    # Intent 9: Streak & Motivation
    elif any(k in q_lower for k in ['streak', 'motivation', 'consistency', 'missed', 'lazy', 'discipline']):
        streak = user.get_current_streak()
        return (
            f"🔥 **Mindset & Momentum:**\n\n"
            f"• Your current streak is **{streak} day{'s' if streak != 1 else ''}**.\n"
            f"• Remember: Motivation is fickle, discipline is reliable. Even showing up for 20 minutes keeps the mental momentum unbroken.\n"
            f"• 'You don't have to be extreme, just consistent.' Head over to your dashboard and record your check-in!"
        )

    # Intent 10: Hydration
    elif any(k in q_lower for k in ['water', 'hydration', 'drink', 'liters']):
        target = role_info['hydration_target']
        return (
            f"💧 **Hydration Goal:**\n\n"
            f"• As a **{role_info['title']}**, your recommended daily target is **{target} Liters**.\n"
            f"• A 2% drop in hydration can reduce muscular power by up to 15% and cause brain fog.\n"
            f"• *Action step:* Drink 500ml upon waking, and keep a water bottle within arm's reach."
        )

    # Intent 11: Workouts & Routine (only triggers if NOT pre/post-workout snack)
    elif any(k in q_lower for k in ['workout', 'routine', 'split', 'exercise', 'train', 'lifting']):
        return (
            f"🏋️ **Training Advice for {role_info['title']}:**\n\n"
            f"• **Current Split:** Check your **Workout Plan** tab for your {user.fitness_level} routine.\n"
            f"• **Role Adaptation:** {role_info['workout_focus']}\n"
            f"• **Progression Rule:** When you hit the upper rep range on all sets with crisp form, add 2.5kg next session.\n"
            f"• **Rest & Recovery:** Don't skip sleep—muscles grow during deep rest, not while lifting."
        )

    # Fallback greeting & prompt guide
    else:
        return (
            f"👋 Hey {user.username}! As your Fitrack AI Coach for the **{role_info['title']}** lifestyle, I'm here to help you crush your **{user.goal}** goal.\n\n"
            f"You can ask me about:\n"
            f"• ⚡ Best pre-workout or post-workout snacks\n"
            f"• 🥗 Daily macros, calories, and meal ideas\n"
            f"• 🏋️ Workout splits and progressive overload\n"
            f"• 💼 Posture & energy hacks for desk workers / students\n"
            f"• 💊 Creatine and evidence-based supplements\n\n"
            f"What would you like to tackle today?"
        )

