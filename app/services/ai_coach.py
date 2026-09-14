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

# Culinary database categorized by South Indian dietary preferences
MEAL_RECIPES = {'standard': {'breakfast': [{'name': 'Steamed Idlis & High-Protein Dal Sambar with Boiled Eggs', 'description': '3 soft steamed idlis served with thick toor dal vegetable sambar, roasted coconut-mint chutney, and 2 pasture-raised boiled eggs.', 'ingredients': ['3 steamed idlis', '1.5 cups toor dal vegetable sambar', '2 boiled eggs', '2 tbsp coconut mint chutney', 'Fresh curry leaves & mustard temper'], 'prep_time': '12 mins', 'base_cals': 490, 'p': 28, 'c': 58, 'f': 14}, {'name': 'Crisp Moong Dal Pesarattu with Kerala Egg Roast', 'description': 'Protein-dense whole green gram dosa served with Kerala-style spiced onion-tomato boiled egg roast.', 'ingredients': ['2 moong dal pesarattus', '2 boiled eggs in spiced onion-tomato masala', '1 tbsp ginger chutney (inji puli)', '1 tsp cold-pressed coconut oil'], 'prep_time': '15 mins', 'base_cals': 520, 'p': 34, 'c': 48, 'f': 18}, {'name': 'Ven Pongal with Moong Dal & Chicken Pepper Sukka', 'description': 'Traditional savory rice and yellow moong dal porridge tempered with black pepper and cumin, served with tender chicken pepper sukka.', 'ingredients': ['1 cup ven pongal (rice + moong dal)', '130g lean chicken breast pepper sukka', '1 tsp A2 cow ghee', 'Cashews, curry leaves & crushed pepper'], 'prep_time': '15 mins', 'base_cals': 530, 'p': 38, 'c': 54, 'f': 16}], 'lunch': [{'name': 'Chettinad Spiced Chicken Curry with Brown Ponni Rice', 'description': 'Fragrant freshly ground Chettinad chicken breast curry served with steamed brown rice, beetroot poriyal, and soothing pepper rasam.', 'ingredients': ['180g skinless chicken breast', '1 cup cooked brown Ponni rice', '1 cup beetroot & carrot poriyal', '1 cup traditional pepper rasam', '1 tsp cold-pressed sesame oil'], 'prep_time': '22 mins', 'base_cals': 570, 'p': 46, 'c': 56, 'f': 15}, {'name': 'Kerala Meen Pollichathu (Pan-Seared Fish) with Matta Rice', 'description': 'Spiced fish fillet coated in shallots and tomato masala, wrapped in banana leaf, served with nutrient-rich Kerala red matta rice and cabbage thoran.', 'ingredients': ['180g seer fish / ayila (mackerel) or tilapia', '1 cup cooked Kerala matta rice', '1 cup cabbage thoran with grated coconut', '1 cup moru curry (buttermilk curry)'], 'prep_time': '20 mins', 'base_cals': 550, 'p': 42, 'c': 54, 'f': 16}, {'name': 'Andhra Style Pepper Chicken with Steamed Rice & Keerai Kootu', 'description': 'Fiery black pepper chicken breast toss served alongside warm steamed rice, spinach-moong dal kootu, and cucumber curd raitha.', 'ingredients': ['170g chicken breast strips', '1 cup steamed Ponni rice', '1 cup keerai (spinach) moong dal kootu', '1/2 cup fresh cucumber curd raitha'], 'prep_time': '20 mins', 'base_cals': 560, 'p': 48, 'c': 52, 'f': 14}], 'snack': [{'name': 'Sundal (Tempered Black Chickpeas) & Neer Mor', 'description': 'Boiled black chana tempered with mustard seeds, curry leaves, and shredded coconut, paired with chilled spiced buttermilk.', 'ingredients': ['1 cup boiled black chana (kala chana)', '1.5 tbsp freshly grated coconut', '1 glass spiced neer mor (buttermilk with crushed ginger & green chili)', 'Curry leaves & hing'], 'prep_time': '5 mins', 'base_cals': 260, 'p': 14, 'c': 34, 'f': 7}, {'name': 'Roasted Spiced Kadalai (Chana) with 2 Boiled Eggs & Filter Coffee', 'description': 'Crunchy roasted chana with chaat spices, two boiled eggs seasoned with black pepper, and unsweetened South Indian filter coffee.', 'ingredients': ['40g roasted chana', '2 boiled eggs with pepper and pink salt', '1 cup South Indian filter coffee (unsweetened, toned milk)'], 'prep_time': '4 mins', 'base_cals': 280, 'p': 22, 'c': 20, 'f': 11}, {'name': 'Tender Coconut Water & Spiced Egg Podimas', 'description': 'Fresh natural tender coconut water paired with a 2-egg scramble sauteed with shallots, curry leaves, and green chilies.', 'ingredients': ['2 large eggs scrambled (podimas)', '1 fresh tender coconut water', 'Handful of curry leaves, shallots & green chili', '1 tsp coconut oil'], 'prep_time': '6 mins', 'base_cals': 240, 'p': 16, 'c': 15, 'f': 12}], 'dinner': [{'name': 'Whole Wheat Chapatis with Chicken Keema Matar & Kachumber', 'description': '2 soft phulkas / chapatis served with spiced minced chicken breast and green peas curry, accompanied by sliced onions and cucumber.', 'ingredients': ['2 whole wheat chapatis', '180g lean chicken keema with green peas', 'Fresh cucumber and onion salad with lemon squeeze', '1 tsp ghee'], 'prep_time': '20 mins', 'base_cals': 520, 'p': 44, 'c': 48, 'f': 14}, {'name': 'Kerala Egg Curry with Appam / Multigrain Dosa', 'description': 'Lightly spiced coconut milk and shallot egg curry served with 2 crispy lace appams or multigrain dosas.', 'ingredients': ['3 boiled eggs in roasted spices & light coconut gravy', '2 steamed appams or multigrain dosas', 'Fresh coriander & curry leaves'], 'prep_time': '18 mins', 'base_cals': 490, 'p': 26, 'c': 46, 'f': 20}, {'name': 'Tandoori Spiced Fish Tikka with Curd Rice & Pomegranate', 'description': 'Herb-marinated grilled fish fillet served with protein-rich probiotic curd rice tempered with mustard seeds and pomegranate.', 'ingredients': ['180g fish fillet (tilapia/salmon/seer fish)', '3/4 cup curd rice (brown rice + low-fat dahi)', '1 tbsp pomegranate seeds', 'Mint coriander dip'], 'prep_time': '22 mins', 'base_cals': 540, 'p': 42, 'c': 45, 'f': 16}]}, 'vegetarian': {'breakfast': [{'name': 'High-Protein Paneer Podi Dosa with Sambar', 'description': 'Crisp multigrain dosa stuffed with spiced low-fat crumbled paneer and roasted gun powder (idli podi), served with vegetable toor dal sambar.', 'ingredients': ['1 crisp multigrain dosa', '120g low-fat paneer bhurji', '1.5 cups toor dal vegetable sambar', '1 tbsp mint coconut chutney', '1 tsp sesame oil'], 'prep_time': '12 mins', 'base_cals': 510, 'p': 32, 'c': 50, 'f': 18}, {'name': 'Steamed Idlis & Soya Chunks Keema Sambar', 'description': '3 steamed soft idlis served with protein-enriched toor dal sambar simmered with high-protein soya chunks and fresh drumsticks.', 'ingredients': ['3 steamed idlis', '40g soya chunks simmered in sambar', '1.5 cups vegetable sambar', '1 tbsp tomato onion chutney'], 'prep_time': '14 mins', 'base_cals': 480, 'p': 30, 'c': 62, 'f': 8}, {'name': 'Pesarattu (Green Gram Dosa) with Low-Fat Paneer & Ginger Pachadi', 'description': 'Andhra whole moong dal crepe stuffed with grated paneer and onions, accompanied by allam pachadi (tangy ginger chutney).', 'ingredients': ['2 green moong dal pesarattus', '100g grated low-fat paneer filling', '2 tbsp tangy allam (ginger) chutney', 'Green chilies & cumin'], 'prep_time': '12 mins', 'base_cals': 520, 'p': 34, 'c': 52, 'f': 16}], 'lunch': [{'name': 'Soya Chunks & Paneer South Indian Kurma with Brown Rice', 'description': 'Hearty South Indian coconut and fennel spiced curry loaded with tender soya chunks and paneer cubes, served with steamed brown rice and carrot poriyal.', 'ingredients': ['40g dry soya chunks (boiled)', '100g low-fat paneer', '1 cup cooked brown rice', '1 cup carrot-beans poriyal', 'South Indian kurma masala with poppy seeds & fennel'], 'prep_time': '20 mins', 'base_cals': 560, 'p': 38, 'c': 62, 'f': 16}, {'name': 'Bisi Bele Bath with Sprouted Moong, Paneer & Curd', 'description': 'Karnataka classic spiced lentil-rice pot dish cooked with toor dal, sprouted green gram, vegetables, topped with roasted paneer cubes and homemade curd.', 'ingredients': ['1.5 cups prepared bisi bele bath', '80g pan-seared paneer cubes', '1/2 cup fresh homemade low-fat dahi (curd)', '1 tsp ghee', 'Roasted cashews & curry leaves'], 'prep_time': '20 mins', 'base_cals': 540, 'p': 32, 'c': 68, 'f': 16}, {'name': 'Dal Keerai Kootu with Brown Rice, Vazhaikkai Roast & Curd', 'description': 'Slow-cooked spinach and yellow moong dal kootu, accompanied by steamed brown rice, spiced raw banana (vazhaikkai) stir fry, and fresh curd.', 'ingredients': ['1.5 cups keerai (spinach) & moong dal kootu', '1 cup cooked brown rice', '1 cup spiced raw banana roast', '1/2 cup homemade curd'], 'prep_time': '18 mins', 'base_cals': 520, 'p': 28, 'c': 74, 'f': 12}], 'snack': [{'name': 'Spiced Kala Chana Sundal with Coconut & Roasted Peanuts', 'description': 'Traditional temple-style black chickpea sundal tossed with mustard seeds, asafoetida, curry leaves, and crushed peanuts.', 'ingredients': ['1 cup boiled kala chana', '20g roasted peanuts', '1.5 tbsp freshly grated coconut', 'Green chillies & lemon juice'], 'prep_time': '4 mins', 'base_cals': 270, 'p': 14, 'c': 32, 'f': 9}, {'name': 'Spiced Neer Mor (Buttermilk) & Roasted Paneer Bites', 'description': 'Chilled spiced buttermilk with ginger and curry leaves, accompanied by air-fried chaat masala paneer cubes.', 'ingredients': ['1 glass spiced neer mor (diluted probiotic curd)', '80g air-fried or seared paneer cubes', 'Chaat masala & black salt'], 'prep_time': '5 mins', 'base_cals': 250, 'p': 20, 'c': 8, 'f': 14}, {'name': 'Sprouted Green Moong Kosambari with Pomegranate', 'description': 'Crunchy Karnataka salad made of sprouted green gram, grated carrots, cucumbers, pomegranate seeds, and fresh lemon-mustard tempering.', 'ingredients': ['1 cup sprouted moong beans', '1/2 cup diced cucumber & grated carrot', '2 tbsp pomegranate seeds', '1 tsp cold-pressed coconut oil temper'], 'prep_time': '5 mins', 'base_cals': 220, 'p': 14, 'c': 34, 'f': 4}], 'dinner': [{'name': 'Ragi Mudde with High-Protein Dal Sambar & Curd', 'description': 'Traditional Karnataka steamed finger millet (ragi) ball packed with calcium and slow-burning carbs, paired with thick toor dal vegetable sambar and fresh curd.', 'ingredients': ['1 medium ragi mudde (finger millet ball)', '1.5 cups thick toor dal vegetable sambar', '1/2 cup low-fat curd', 'Cucumber & onion slices'], 'prep_time': '18 mins', 'base_cals': 510, 'p': 26, 'c': 76, 'f': 10}, {'name': 'Whole Wheat Phulkas with Paneer Chettinad & Sprouts Salad', 'description': '2 soft whole wheat phulkas served with spicy Chettinad paneer curry and a crunchy sprouted bean salad.', 'ingredients': ['2 whole wheat phulkas', '140g low-fat paneer cooked in Chettinad masala', '1/2 cup mixed sprouts salad', '1 tsp ghee'], 'prep_time': '20 mins', 'base_cals': 540, 'p': 34, 'c': 50, 'f': 20}, {'name': 'Probiotic Curd Rice with Tempered Soya Bhurji', 'description': 'Comforting South Indian curd rice tempered with mustard, curry leaves, and ginger, topped with spiced crumbled high-protein soya chunks.', 'ingredients': ['1 cup brown curd rice with pomegranate', '50g cooked spiced soya granules bhurji', 'Ginger, green chili & mustard tempering'], 'prep_time': '12 mins', 'base_cals': 490, 'p': 32, 'c': 58, 'f': 12}]}, 'vegan': {'breakfast': [{'name': 'Sprouted Moong Pesarattu with Vegetable Sambar', 'description': 'Crispy green gram dosa naturally packed with plant protein, served with freshly simmered toor dal sambar and ginger chutney.', 'ingredients': ['2 whole moong pesarattus', '1.5 cups toor dal vegetable sambar', '1 tbsp allam ginger chutney', 'Chopped onions & cumin'], 'prep_time': '12 mins', 'base_cals': 480, 'p': 28, 'c': 62, 'f': 10}, {'name': 'Steamed Ragi Idlis with High-Protein Dal & Tomato Chutney', 'description': '3 finger millet and urad dal steamed idlis rich in iron and calcium, served with yellow moong dal and tangy roasted tomato chutney.', 'ingredients': ['3 ragi idlis', '1.5 cups thick toor & moong dal', '2 tbsp roasted onion-tomato chutney', 'Curry leaves & mustard temper'], 'prep_time': '14 mins', 'base_cals': 460, 'p': 26, 'c': 66, 'f': 8}], 'lunch': [{'name': 'Kerala Kadala Curry with Steamed Matta Rice & Cabbage Thoran', 'description': 'Authentic black chickpea curry simmered with roasted coconut paste and Malabar spices, served with red matta rice and cabbage thoran.', 'ingredients': ['1.5 cups boiled black chickpeas (kadala)', '1 cup cooked Kerala matta rice', '1 cup cabbage and coconut thoran', 'Curry leaves, shallots & mustard seeds'], 'prep_time': '20 mins', 'base_cals': 560, 'p': 30, 'c': 80, 'f': 14}, {'name': 'South Indian Soya Chunks & Tofu Kurma with Steamed Rice', 'description': 'Protein-dense firm tofu and soya chunks in a fragrant coconut-fennel gravy, served with warm Ponni rice, pepper rasam, and cucumber.', 'ingredients': ['120g firm tofu cubes', '30g soya chunks', '1 cup steamed rice', '1 cup tomato-pepper rasam', 'Coriander & curry leaves'], 'prep_time': '18 mins', 'base_cals': 540, 'p': 36, 'c': 64, 'f': 14}], 'snack': [{'name': 'Temple-Style White & Black Chana Sundal with Tender Coconut', 'description': 'Steamed chickpeas tossed with mustard, hing, curry leaves, and grated fresh coconut, paired with pure tender coconut water.', 'ingredients': ['1 cup boiled chickpeas (chana)', '1.5 tbsp fresh coconut', '1 cup natural tender coconut water', 'Pinch of sea salt & lemon'], 'prep_time': '4 mins', 'base_cals': 260, 'p': 13, 'c': 38, 'f': 6}, {'name': 'Roasted Spiced Peanuts & Makhana with Ginger Lemon Chai', 'description': 'Crunchy fox nuts (makhana) and roasted peanuts tossed in turmeric and chaat masala, paired with black ginger tea.', 'ingredients': ['25g roasted peanuts', '25g roasted makhana (foxnuts)', '1 cup spiced black tea with fresh crushed ginger', 'Chaat masala'], 'prep_time': '4 mins', 'base_cals': 240, 'p': 10, 'c': 24, 'f': 12}], 'dinner': [{'name': 'Finger Millet (Ragi Mudde) with Drumstick Dal Kootu', 'description': 'Traditional steamed finger millet ball served with iron-rich spinach, drumstick and toor dal kootu, with a side of raw onion and cucumber.', 'ingredients': ['1 ragi mudde', '1.5 cups drumstick & spinach toor dal kootu', 'Fresh cucumber and carrot slices', '1 tsp cold-pressed sesame oil'], 'prep_time': '20 mins', 'base_cals': 490, 'p': 24, 'c': 78, 'f': 8}, {'name': 'Foxtail Millet (Thinai) Khichdi with Mixed Veggies & Tofu', 'description': 'Comforting foxtail millet and yellow moong dal khichdi loaded with carrots, green beans, and seared turmeric tofu cubes.', 'ingredients': ['1.5 cups foxtail millet & moong dal khichdi', '100g pan-seared tofu cubes', '1 tsp cold-pressed coconut oil', 'Roasted cumin & black pepper'], 'prep_time': '22 mins', 'base_cals': 520, 'p': 30, 'c': 68, 'f': 12}]}, 'keto': {'breakfast': [{'name': 'South Indian Egg Podimas (Egg Scramble) with Coconut Chutney', 'description': '3 whole eggs scrambled with shallots, curry leaves, green chilies, and black pepper, accompanied by freshly ground thick coconut chutney.', 'ingredients': ['3 large eggs', '2 tbsp thick coconut chutney (no dal)', '1/2 onion & green chili sauteed in cold-pressed coconut oil', 'Curry leaves & black pepper'], 'prep_time': '10 mins', 'base_cals': 480, 'p': 26, 'c': 6, 'f': 38}, {'name': 'Pepper Paneer Tikka with Mint Coriander Chutney', 'description': 'Generous cubes of fresh paneer marinated in South Indian spices, black pepper, and yogurt, grilled crisp.', 'ingredients': ['180g paneer cubes', '2 tbsp thick hung curd marinade', 'Black pepper, turmeric, cumin', '2 tbsp fresh mint-coriander dip'], 'prep_time': '12 mins', 'base_cals': 520, 'p': 32, 'c': 7, 'f': 40}], 'lunch': [{'name': 'Chettinad Chicken Breast Roast with Cauliflower Poriyal', 'description': 'Tender chicken breast cooked dry in stone-ground Chettinad masala, served with grated cauliflower poriyal sauteed in coconut oil and mustard.', 'ingredients': ['200g chicken breast strips', '2 cups riced cauliflower poriyal', '1.5 tbsp cold-pressed coconut oil', 'Chettinad spices, curry leaves & shallots'], 'prep_time': '20 mins', 'base_cals': 540, 'p': 52, 'c': 8, 'f': 32}, {'name': 'Kerala Malabar Fish Curry with Coconut Cream & Cucumber Salad', 'description': 'Wild seer fish or salmon simmered in thick coconut milk, kokum (kudampuli), and green chilies, paired with crisp cucumber and shredded coconut salad.', 'ingredients': ['190g fish steak (seer fish/salmon)', '1/2 cup thick coconut milk gravy', '1.5 cups diced cucumber with lemon and curry leaf temper'], 'prep_time': '18 mins', 'base_cals': 560, 'p': 44, 'c': 7, 'f': 38}], 'snack': [{'name': 'Roasted Salted Almonds & Spiced Neer Mor', 'description': 'Handful of roasted almonds paired with a tall glass of diluted spiced buttermilk with ginger and curry leaves.', 'ingredients': ['30g roasted almonds', '1 glass spiced neer mor (thin buttermilk)', 'Crushed ginger, salt & curry leaves'], 'prep_time': '2 mins', 'base_cals': 240, 'p': 9, 'c': 6, 'f': 20}], 'dinner': [{'name': 'Kerala Style Chicken Stew (Coconut Milk) with Sauteed Greens', 'description': 'Succulent chicken simmered in aromatic whole spices, ginger, and coconut milk, served with a big bowl of sauteed spinach (keerai poriyal).', 'ingredients': ['200g chicken thighs or breast', '1/2 cup coconut milk', '2 cups keerai (spinach) sauteed in coconut oil with shallots'], 'prep_time': '20 mins', 'base_cals': 580, 'p': 48, 'c': 9, 'f': 38}, {'name': 'Tawa Fried Spiced Paneer & Cabbage Thoran', 'description': 'Thick slices of paneer seared in South Indian chili and turmeric masala, accompanied by warm cabbage and coconut thoran.', 'ingredients': ['170g paneer slices', '1.5 cups cabbage thoran', '1 tbsp cold-pressed coconut oil', 'Mustard seeds & red chili flakes'], 'prep_time': '15 mins', 'base_cals': 530, 'p': 30, 'c': 10, 'f': 41}]}}


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
                "• **Option 1 (Light Sundal):** 1 cup boiled kala chana sundal with grated coconut & curry leaves (~180 kcal, 24g carbs, 12g protein).\n"
                "• **Option 2 (Banana & Tender Coconut):** 1 ripe banana with a glass of fresh tender coconut water (~160 kcal, 35g carbs, 2g protein).\n"
                "• **Option 3 (Neer Mor & Boiled Egg):** Spiced buttermilk with 1 boiled egg & pinch of roasted cumin (~130 kcal, 5g carbs, 8g protein)."
            )
            timing = "Consume 45–60 minutes before training. Light, easily digestible South Indian staples that won't weigh you down during your caloric deficit."
        elif goal == 'bulking':
            snack_picks = (
                "• **Option 1 (Idli Power Stack):** 2 steamed idlis with sambar and 2 boiled eggs (~420 kcal, 28g protein, 52g carbs).\n"
                "• **Option 2 (Ragi Malt Shake):** Ragi malt with jaggery, banana & a scoop of whey protein (~400 kcal, 32g protein, 58g carbs).\n"
                "• **Option 3 (Peanut Chikki & Banana):** 2 peanut chikkis with 1 ripe banana & filter coffee (~380 kcal, 14g protein, 48g carbs)."
            )
            timing = "Consume 60–90 minutes before training to flood your muscles with glycogen from South Indian complex carbs."
        else: # maintaining / general
            snack_picks = (
                "• **Option 1 (Classic South Indian):** 1 ripe banana with a handful of roasted peanuts (~190 kcal, 28g carbs, 6g protein).\n"
                "• **Option 2 (Filter Coffee & Sundal):** Unsweetened filter coffee with 1 cup white chana sundal (~200 kcal, 26g carbs, 10g protein).\n"
                "• **Option 3 (Quick Fuel):** 2 steamed idlis with coconut chutney & tender coconut water (~220 kcal, 38g carbs, 6g protein)."
            )
            timing = "Consume 45–60 minutes before training for steady blood glucose from South Indian complex carbs."

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
            f"• **Top Meal 1:** Chettinad chicken breast or paneer curry with steamed brown rice and beetroot poriyal.\n"
            f"• **Top Meal 2:** 3 steamed idlis with thick sambar and 2 boiled eggs (or soya chunks scramble).\n"
            f"• **Top Meal 3:** Egg podimas (scrambled eggs) with 2 whole wheat chapatis and dal keerai kootu.\n"
            f"• **Hydration:** Rehydrate with 500ml tender coconut water or spiced neer mor (buttermilk) to replenish electrolytes."
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
            f"• **Top South Indian Sources:** Eggs (podimas/roast), chicken breast, seer fish/mackerel, paneer, soya chunks, toor dal, moong dal, sundal (chana), curd, and whey/plant protein powder.\n"
            f"• *Role tip:* {role_info['tips'][1] if len(role_info['tips']) > 1 else 'Keep roasted chana and boiled eggs within reach for quick protein hits.'}"
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
            f"• **South Indian Hydration Hacks:** Fresh tender coconut water, spiced neer mor (buttermilk with ginger & curry leaves), warm cumin water (jeera water), and plain water with lemon & pink salt.\n"
            f"• *Action step:* Drink 500ml water upon waking, sip neer mor after lunch, and have tender coconut post-workout."
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

