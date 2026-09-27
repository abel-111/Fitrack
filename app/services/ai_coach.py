import os
import json
import random
import urllib.request
import urllib.parse
from datetime import datetime, date, timedelta

# Role definitions & descriptions tailored for lifestyle & South Indian daily routines
ROLE_DETAILS = {
    'desk_worker': {
        'title': 'Desk Worker / Corporate',
        'icon': '💼',
        'summary': 'Crafted for corporate & desk routines: helps prevent afternoon energy crashes after rice lunches, promotes metabolic health, and relieves posture strain from sitting.',
        'diet_focus': 'Low-GI complex carbs (unpolished brown Ponni rice, millets, pesarattu), high fiber keerai (greens), and protein to avoid the post-lunch 2 PM slump.',
        'hydration_target': 3.5,
        'activity_multiplier': 1.35,
        'tips': [
            'Take a 2-minute shoulder & hip flexor stretch every 45 minutes of sitting.',
            'Keep a 1L water bottle or spiced neer mor at your desk; AC environments cause unnoticed dehydration.',
            'Keep your lunch rice to 1 cup, and double your dal kootu or poriyal to stay light and energetic.',
            'Smart desk snacks: roasted chana (kadalai), boiled eggs, or a cup of unsweetened filter coffee with sundal.'
        ],
        'workout_focus': 'Focus on rear delts, chest openers, and glute bridges to counteract hours of hunched desk sitting.'
    },
    'student': {
        'title': 'Student',
        'icon': '🎓',
        'summary': 'Budget-friendly, high-protein South Indian nutrition and smart workouts designed for tight hostel or college schedules and study sessions.',
        'diet_focus': 'Affordable high protein (eggs, toor dal, soya chunks, peanuts, sundal, curd), hostel-friendly meal choices, and sustained brain fuel.',
        'hydration_target': 3.0,
        'activity_multiplier': 1.45,
        'tips': [
            'Hostel hack: Sundal (black chana), boiled eggs, and peanut chikki give you the highest protein per rupee.',
            'Order or prepare pesarattu (moong dal dosa) or idlis instead of deep-fried parottas or poori.',
            'Get 7-8 hours of sleep during exam periods for muscle recovery and memory consolidation.',
            'If study hours are tight, do 35-minute focused compound supersets in the gym.'
        ],
        'workout_focus': 'Time-efficient compound movements (Squat, Overhead Press, Rows) for maximum strength in 45 minutes.'
    },
    'athlete': {
        'title': 'Athlete / Sports',
        'icon': '🏃',
        'summary': 'Optimized for high stamina, explosive power, fast muscle recovery, and electrolyte replenishment for runners, cricketers, and athletes.',
        'diet_focus': 'Clean complex carbs (red matta rice, ragi mudde, pongal), lean protein, and natural electrolytes (tender coconut water, neer mor).',
        'hydration_target': 4.0,
        'activity_multiplier': 1.75,
        'tips': [
            'Fuel 45-60 mins before sports with easily digestible carbs (banana, steamed idlis with honey or sambar).',
            'Sip fresh tender coconut water or spiced neer mor with pink salt right after sweaty sessions for natural electrolytes.',
            'Aim for 2.0-2.2g protein per kg using chicken, fish, eggs, paneer, or whey.',
            'Do 10 minutes of dynamic leg swings and hip mobility before every sprint or lifting session.'
        ],
        'workout_focus': 'Periodized explosive compound lifts, rotational core strength, and unilateral leg stability.'
    },
    'bodybuilder': {
        'title': 'Bodybuilder / Hypertrophy',
        'icon': '🏋️',
        'summary': 'Precision muscle building with South Indian staples, dialed-in protein distribution, and targeted surplus/deficit planning.',
        'diet_focus': 'High protein spaced every 3-4 hours (chicken breast sukka, seer fish, egg podimas, paneer bhurji, soya chunks), with clean carb timing.',
        'hydration_target': 4.0,
        'activity_multiplier': 1.6,
        'tips': [
            'Space your protein across 4 meals (30-45g each) to keep muscle protein synthesis running strong.',
            'Take 5g creatine monohydrate daily with water or warm lime water for strength and muscle fullness.',
            'Train 1-2 reps shy of failure on your heaviest working sets with strict tempo and mind-muscle connection.',
            'Track your weights and progressive overload weekly in your workout log.'
        ],
        'workout_focus': 'Push/Pull/Legs or Upper/Lower split with controlled negatives and high mind-muscle tension.'
    },
    'busy_parent': {
        'title': 'Busy Parent / Professional',
        'icon': '👨‍👩‍👧',
        'summary': 'Realistic, family-friendly healthy South Indian meals, quick cooking tricks, and high-impact 30-minute home or gym workouts.',
        'diet_focus': 'Wholesome one-pot South Indian meals (vegetable sambar sadam with soya, bisi bele bath with paneer, keerai kootu, sundal).',
        'hydration_target': 3.0,
        'activity_multiplier': 1.45,
        'tips': [
            'Cook the family sambar or kootu, but ladle extra dal and add boiled eggs or pan-seared paneer for yourself.',
            'A 25-minute brisk walk or kettlebell circuit at home is far better than skipping exercise entirely.',
            'Keep roasted makhana, peanuts, and spiced buttermilk handy when family snacks on sweets.',
            'Involve family in outdoor evening walks in the park.'
        ],
        'workout_focus': 'Full-body circuit or 30-minute compound supersets for maximum calorie burn and cardiovascular health.'
    },
    'general': {
        'title': 'General Fitness & Health',
        'icon': '🧘',
        'summary': 'Sustainable lifelong vitality, functional strength, gut health, and balanced South Indian home cooking without strict restrictions.',
        'diet_focus': 'The 80/20 balance: 80% wholesome home-cooked South Indian staples with ample vegetables and protein, 20% flexibility.',
        'hydration_target': 3.0,
        'activity_multiplier': 1.45,
        'tips': [
            'Aim for 8,000 to 10,000 steps daily outside your gym sessions.',
            'Fill half your plate with colorful poriyals (beetroot, beans, carrot, cabbage) and keerai.',
            'Consistency over perfection: 3 workouts a week every week beats 6 workouts followed by burnout.',
            'Start your morning with a tall glass of warm water or jeera water before your filter coffee.'
        ],
        'workout_focus': 'Balanced full-body resistance training combined with daily walking and mobility.'
    }
}

# State-specific recipe highlights — merged into base pool based on user's state
STATE_RECIPE_HIGHLIGHTS = {
    'Tamil Nadu': {
        'breakfast': [
            {
                'name': 'Chettinad Kavuni Arisi Idli with Pepper Sambar',
                'description': 'Black rice idlis from Chettinad tradition, soft and nutty, served with bold whole-pepper toor dal sambar.',
                'ingredients': ['3 black rice idlis', '1.5 cups whole pepper sambar', '1 tbsp coconut chutney', 'Curry leaves & mustard temper'],
                'prep_time': '12 mins', 'base_cals': 460, 'p': 22, 'c': 68, 'f': 10,
                'region': 'Chettinad, Tamil Nadu', 'badge': '🌶️ Chettinad Heritage'
            },
        ],
        'lunch': [
            {
                'name': 'Tamil Nadu Meals — Paruppu, Rasam, Keerai Poriyal & Curd Rice',
                'description': 'Traditional Tamil banana-leaf style: steamed Ponni rice, watery toor dal, tangy pepper rasam, stir-fried spinach, fresh curd, and papad.',
                'ingredients': ['1 cup Ponni rice', '1 cup toor dal (paruppu)', '1 cup hot pepper rasam', '1 cup keerai (spinach) poriyal', '1/2 cup fresh curd', '1 roasted papad'],
                'prep_time': '25 mins', 'base_cals': 590, 'p': 30, 'c': 80, 'f': 14,
                'region': 'Tamil Nadu', 'badge': '🍌 Traditional Meals'
            },
        ],
        'snack': [
            {
                'name': 'Murukku & Sundal with Filter Coffee',
                'description': 'One crisp home-made rice flour murukku alongside a cup of kala chana sundal and aromatic South Indian degree coffee.',
                'ingredients': ['1 murukku', '3/4 cup kala chana sundal', '1 cup filter coffee (toned milk, low sugar)'],
                'prep_time': '3 mins', 'base_cals': 270, 'p': 12, 'c': 32, 'f': 10,
                'region': 'Tamil Nadu', 'badge': '☕ Tamil Tiffin'
            },
        ],
        'dinner': [
            {
                'name': 'Milagu Rasam Sadam with Egg Bhurji',
                'description': 'Comforting pepper rasam rice mixed with a generous spoon of cold-pressed sesame ghee, paired with a spiced 2-egg scramble.',
                'ingredients': ['1 cup rasam sadam (rasam rice)', '2 scrambled eggs with shallots', '1 tsp cold-pressed sesame oil', 'Fresh coriander'],
                'prep_time': '15 mins', 'base_cals': 490, 'p': 28, 'c': 58, 'f': 16,
                'region': 'Tamil Nadu', 'badge': '🌶️ Comfort Classic'
            },
        ]
    },
    'Kerala': {
        'breakfast': [
            {
                'name': 'Puttu with Kadala Curry & Banana',
                'description': 'Steamed rice flour and coconut puttu cylinders, paired with spicy roasted coconut black chickpea curry and a ripe nendran banana.',
                'ingredients': ['2 pieces steamed puttu (rice flour + coconut)', '1 cup kadala (black chickpea) curry', '1 nendran banana'],
                'prep_time': '15 mins', 'base_cals': 520, 'p': 24, 'c': 70, 'f': 14,
                'region': 'Kerala', 'badge': '🌴 Kerala Breakfast'
            },
        ],
        'lunch': [
            {
                'name': 'Kerala Sadya Style — Matta Rice, Avial, Olan & Pulissery',
                'description': 'Sadya-inspired wholesome plate: red matta rice, mixed vegetable avial in curd-coconut, ash gourd olan in thin coconut milk, and tangy probiotic pulissery.',
                'ingredients': ['1 cup Kerala matta rice', '1 cup vegetable avial (drumstick, raw banana, curd)', '1 cup olan (ash gourd coconut milk)', '1/2 cup pulissery (curd curry)'],
                'prep_time': '25 mins', 'base_cals': 560, 'p': 20, 'c': 80, 'f': 18,
                'region': 'Kerala', 'badge': '🌴 Sadya Inspired'
            },
        ],
        'snack': [
            {
                'name': 'Kerala Banana Chips & Tender Coconut Water',
                'description': 'Crisp cold-pressed coconut oil banana chips (small portion) alongside natural tender coconut water — a classic Kerala evening ritual.',
                'ingredients': ['20g thin banana chips (coconut oil)', '1 fresh tender coconut water', 'Pinch of salt'],
                'prep_time': '2 mins', 'base_cals': 220, 'p': 2, 'c': 28, 'f': 10,
                'region': 'Kerala', 'badge': '🥥 Kerala Classic'
            },
        ],
        'dinner': [
            {
                'name': 'Kerala Fish Curry (Meen Curry) with Matta Rice & Stir-fried Beans',
                'description': 'Traditional fish cooked in kokum and red chili coconut gravy, served with red matta rice and stir-fried long beans thoran.',
                'ingredients': ['180g fish in Kerala coconut-kokum gravy', '1 cup matta rice', '1 cup long beans thoran with coconut', 'Fresh lime'],
                'prep_time': '22 mins', 'base_cals': 560, 'p': 42, 'c': 56, 'f': 18,
                'region': 'Kerala', 'badge': '🐟 Coastal Feast'
            },
        ]
    },
    'Karnataka': {
        'breakfast': [
            {
                'name': 'Akki Roti with Coconut Chutney & Egg Fry',
                'description': 'Karnataka-style flat rice flour bread (akki roti) made with onions and cumin, served with thick coconut chutney and a pan-fried egg.',
                'ingredients': ['2 akki rotis', '1 pan-fried egg', '2 tbsp thick coconut chutney', 'Green chili, curry leaves & onion in roti'],
                'prep_time': '14 mins', 'base_cals': 490, 'p': 22, 'c': 52, 'f': 20,
                'region': 'Karnataka', 'badge': '🌾 Karnataka Classic'
            },
        ],
        'lunch': [
            {
                'name': 'Bisi Bele Bath with Papad, Raita & Raw Salad',
                'description': 'Karnataka one-pot classic: lentil-rice cooked with tamarind, jaggery, and spiced bisi bele bath masala powder, served with roasted papad and cucumber raita.',
                'ingredients': ['1.5 cups bisi bele bath', '1 roasted papad', '1/2 cup cucumber raita', '1 tsp ghee', 'Roasted cashews & curry leaf tempering'],
                'prep_time': '20 mins', 'base_cals': 550, 'p': 22, 'c': 72, 'f': 16,
                'region': 'Karnataka', 'badge': '🌾 Karnataka One-Pot'
            },
        ],
        'snack': [
            {
                'name': 'Savige Bath (Vermicelli Upma) & Black Coffee',
                'description': 'Light Karnataka-style rice vermicelli upma with mustard, curry leaves, and peanuts, paired with black filter coffee.',
                'ingredients': ['1 cup rice vermicelli upma', '20g roasted peanuts', '1 cup black South Indian coffee'],
                'prep_time': '8 mins', 'base_cals': 260, 'p': 8, 'c': 36, 'f': 9,
                'region': 'Karnataka', 'badge': '🌿 Bangalore Snack'
            },
        ],
        'dinner': [
            {
                'name': 'Ragi Mudde with Spicy Chicken Saaru & Curd',
                'description': 'Traditional steamed finger millet ball served with Udupi-style spiced chicken saaru (thin broth) and cooling homemade curd.',
                'ingredients': ['1 ragi mudde', '170g chicken in saaru gravy', '1/2 cup fresh curd', 'Onion & cucumber slices'],
                'prep_time': '20 mins', 'base_cals': 530, 'p': 42, 'c': 56, 'f': 14,
                'region': 'Karnataka', 'badge': '🌾 Ragi Tradition'
            },
        ]
    },
    'Andhra Pradesh': {
        'breakfast': [
            {
                'name': 'Pesarattu Upma with Ginger Allam Pachadi',
                'description': 'Andhra signature: whole green gram pesarattu filled with hot roasted semolina (rava) upma, served with fiery tangy ginger allam pachadi.',
                'ingredients': ['2 pesarattus stuffed with rava upma', '2 tbsp allam pachadi', 'Green chilies & onion'],
                'prep_time': '15 mins', 'base_cals': 510, 'p': 26, 'c': 64, 'f': 12,
                'region': 'Andhra Pradesh', 'badge': '🌶️ Andhra Signature'
            },
        ],
        'lunch': [
            {
                'name': 'Andhra Gutti Vankaya (Stuffed Brinjal) with Rice & Pappu',
                'description': 'Hollowed brinjals stuffed with roasted peanut and sesame masala, slow-cooked in tamarind gravy, served with hot Sona Masoori rice and toor dal pappu.',
                'ingredients': ['3 stuffed brinjals in tamarind-peanut gravy', '1 cup Sona Masoori rice', '1 cup toor dal pappu', 'Fresh lime & raw onion'],
                'prep_time': '22 mins', 'base_cals': 560, 'p': 24, 'c': 72, 'f': 18,
                'region': 'Andhra Pradesh', 'badge': '🍆 Andhra Delicacy'
            },
        ],
        'snack': [
            {
                'name': 'Punugulu with Coconut Chutney',
                'description': 'Crisp Andhra-style batter balls made from leftover idli dough, deep-fried or air-fried until crunchy, served with fresh coconut chutney.',
                'ingredients': ['5-6 air-fried punugulu', '2 tbsp fresh coconut chutney', 'Curry leaves & onion dip'],
                'prep_time': '5 mins', 'base_cals': 250, 'p': 9, 'c': 34, 'f': 9,
                'region': 'Andhra Pradesh', 'badge': '🌶️ Andhra Snack'
            },
        ],
        'dinner': [
            {
                'name': 'Gongura Chicken Curry with Hot Steamed Rice',
                'description': 'Andhra specialty chicken cooked in tart gongura (sorrel leaves) gravy with red chilies and shallots — bold, spicy, and deeply satisfying.',
                'ingredients': ['180g chicken pieces in gongura gravy', '1 cup steamed Sona Masoori rice', '1 cup dal soup', 'Fresh lime'],
                'prep_time': '25 mins', 'base_cals': 570, 'p': 44, 'c': 56, 'f': 16,
                'region': 'Andhra Pradesh', 'badge': '🌶️ Andhra Bold'
            },
        ]
    },
    'Telangana': {
        'breakfast': [
            {
                'name': 'Telangana Pesarattu with Tomato Gongura Chutney',
                'description': 'Classic whole moong pesarattu dosas served with tangy roasted tomato and gongura chutney, a Hyderabad morning staple.',
                'ingredients': ['2 moong pesarattus', '2 tbsp tomato-gongura chutney', 'Onion & green chili'],
                'prep_time': '12 mins', 'base_cals': 470, 'p': 24, 'c': 62, 'f': 10,
                'region': 'Telangana', 'badge': '🌶️ Hyderabad Classic'
            },
        ],
        'lunch': [
            {
                'name': 'Hyderabadi Brown Rice with Mutton/Chicken Shorba & Mirchi ka Salan',
                'description': 'Protein-rich Hyderabadi influenced meal: brown Basmati rice, spiced chicken shorba (thin curry), and classic mirchi ka salan (chili curry in peanut sesame gravy).',
                'ingredients': ['1 cup brown basmati rice', '180g chicken shorba curry', '1 cup mirchi ka salan', 'Fresh mint & lemon'],
                'prep_time': '22 mins', 'base_cals': 580, 'p': 44, 'c': 58, 'f': 18,
                'region': 'Telangana', 'badge': '🌶️ Hyderabadi Style'
            },
        ],
        'snack': [
            {
                'name': 'Khara Boondi & Chai',
                'description': 'Crunchy spiced chickpea flour boondi with turmeric, pepper, and curry leaves, paired with a glass of cardamom chai.',
                'ingredients': ['30g khara boondi', '1 cup cardamom-ginger chai (low sugar)', 'Roasted peanuts'],
                'prep_time': '2 mins', 'base_cals': 255, 'p': 7, 'c': 30, 'f': 11,
                'region': 'Telangana', 'badge': '🍵 Telangana Chai Snack'
            },
        ],
        'dinner': [
            {
                'name': 'Jowar Roti (Jolada Roti) with Chicken Curry & Raita',
                'description': 'Telangana-style sorghum flatbread served with light chicken curry and cool cucumber yogurt raita — wholesome and high-fiber.',
                'ingredients': ['2 jowar (sorghum) rotis', '160g chicken curry', '1/2 cup cucumber raita', 'Onion & lime'],
                'prep_time': '18 mins', 'base_cals': 510, 'p': 40, 'c': 50, 'f': 14,
                'region': 'Telangana', 'badge': '🌾 Jowar Power'
            },
        ]
    }
}

# Continental / fusion healthy recipes
CONTINENTAL_RECIPES = {
    'breakfast': [
        {
            'name': 'Avocado Toast with 2 Poached Eggs & Cherry Tomatoes',
            'description': 'Whole grain toast topped with mashed avocado seasoned with lemon and sea salt, paired with soft poached eggs and halved cherry tomatoes.',
            'ingredients': ['2 slices whole grain toast', '1/2 ripe avocado (mashed)', '2 poached eggs', '8 cherry tomatoes', 'Chili flakes & sea salt'],
            'prep_time': '12 mins', 'base_cals': 520, 'p': 28, 'c': 38, 'f': 28,
            'region': 'Continental', 'badge': '🥑 Healthy Fusion'
        },
        {
            'name': 'Greek Yogurt Parfait with Mixed Berries & Muesli',
            'description': 'Thick Greek yogurt layered with seasonal fresh or frozen berries, crunchy muesli, a drizzle of honey, and a handful of walnuts.',
            'ingredients': ['200g thick Greek yogurt', '80g mixed berries (blueberry, strawberry)', '30g muesli', '1 tsp honey', '15g walnuts'],
            'prep_time': '5 mins', 'base_cals': 460, 'p': 26, 'c': 44, 'f': 18,
            'region': 'Continental', 'badge': '🫐 High Protein Parfait'
        },
    ],
    'lunch': [
        {
            'name': 'Grilled Chicken Caesar Salad with Whole Grain Crackers',
            'description': 'Juicy grilled chicken breast on crisp romaine lettuce with cherry tomatoes, parmesan shavings, and light Caesar dressing, served with whole grain crackers.',
            'ingredients': ['200g grilled chicken breast', '2 cups romaine lettuce', '10 cherry tomatoes', '20g parmesan', '2 tbsp light Caesar dressing', '4 whole grain crackers'],
            'prep_time': '18 mins', 'base_cals': 540, 'p': 48, 'c': 24, 'f': 24,
            'region': 'Continental', 'badge': '🥗 High Protein Salad'
        },
        {
            'name': 'Brown Rice Buddha Bowl with Grilled Tofu & Tahini',
            'description': 'Warm brown rice bowl with pan-seared turmeric tofu, roasted sweet potato, steamed broccoli, chickpeas, and a creamy tahini-lemon drizzle.',
            'ingredients': ['1 cup cooked brown rice', '130g firm tofu (grilled)', '1/2 cup roasted sweet potato', '1 cup broccoli', '60g chickpeas', '2 tbsp tahini lemon sauce'],
            'prep_time': '20 mins', 'base_cals': 560, 'p': 34, 'c': 64, 'f': 20,
            'region': 'Continental', 'badge': '🥙 Vegan Power Bowl'
        },
    ],
    'snack': [
        {
            'name': 'Hummus & Veggie Sticks with Walnuts',
            'description': 'Creamy homemade chickpea hummus with carrot batons, cucumber slices, and a handful of walnuts — a perfect healthy mid-afternoon snack.',
            'ingredients': ['3 tbsp hummus', 'Carrot & cucumber sticks', '20g walnuts', 'Pinch of paprika'],
            'prep_time': '3 mins', 'base_cals': 240, 'p': 9, 'c': 20, 'f': 14,
            'region': 'Continental', 'badge': '🥕 Clean Snack'
        },
    ],
    'dinner': [
        {
            'name': 'Baked Herb Salmon with Steamed Broccoli & Quinoa',
            'description': 'Oven-baked salmon fillet with lemon, garlic, and fresh rosemary, served with fluffy quinoa and tender steamed broccoli florets.',
            'ingredients': ['200g salmon fillet', '3/4 cup cooked quinoa', '1.5 cups steamed broccoli', '1 lemon', 'Fresh rosemary & olive oil'],
            'prep_time': '25 mins', 'base_cals': 570, 'p': 52, 'c': 32, 'f': 26,
            'region': 'Continental', 'badge': '🐟 Omega-3 Rich'
        },
        {
            'name': 'Grilled Chicken Steak with Roasted Vegetables & Brown Rice',
            'description': 'Lean chicken breast steak grilled with herbs and olive oil, served with oven-roasted bell peppers, zucchini, onions, and nutty brown rice.',
            'ingredients': ['200g grilled chicken breast', '1 cup mixed roasted vegetables', '3/4 cup cooked brown rice', '1 tbsp olive oil', 'Herbs & garlic'],
            'prep_time': '22 mins', 'base_cals': 545, 'p': 50, 'c': 42, 'f': 18,
            'region': 'Continental', 'badge': '🥩 Lean & Clean'
        },
    ]
}

MEAL_RECIPES = {
    'standard': {
        'breakfast': [
            {
                'name': 'Andhra Moong Dal Pesarattu with Kerala Egg Roast',
                'description': 'Crisp whole green gram dosa paired with a Kerala-style shallot and tomato boiled egg roast, served with tangy ginger allam chutney.',
                'ingredients': ['2 whole green moong pesarattus', '2 boiled eggs in spiced onion-tomato masala', '1.5 tbsp ginger chutney (allam pachadi)', '1 tsp cold-pressed coconut oil'],
                'prep_time': '15 mins',
                'base_cals': 520,
                'p': 34,
                'c': 48,
                'f': 18,
                'region': 'Andhra & Kerala',
                'badge': '🌶️ High Protein'
            },
            {
                'name': 'Steamed Idlis & High-Protein Toor Dal Sambar with Boiled Eggs',
                'description': '3 pillowy soft steamed idlis served with thick vegetable toor dal sambar, mint coconut chutney, and 2 pasture-raised boiled eggs.',
                'ingredients': ['3 steamed idlis', '1.5 cups thick toor dal vegetable sambar', '2 boiled eggs with crushed black pepper', '1.5 tbsp mint-coconut chutney', 'Curry leaves & mustard temper'],
                'prep_time': '12 mins',
                'base_cals': 490,
                'p': 28,
                'c': 58,
                'f': 14,
                'region': 'Tamil Nadu',
                'badge': '🍛 Traditional Classic'
            },
            {
                'name': 'Ven Pongal with Moong Dal & Chicken Pepper Sukka',
                'description': 'Aromatic rice and yellow moong dal porridge tempered with whole cumin and crushed black pepper, paired with lean chicken breast pepper sukka.',
                'ingredients': ['1 cup savory ven pongal (rice + moong dal)', '140g chicken breast pepper sukka', '1 tsp A2 cow ghee', 'Curry leaves, cashews & ginger temper'],
                'prep_time': '16 mins',
                'base_cals': 530,
                'p': 38,
                'c': 52,
                'f': 16,
                'region': 'Tamil Nadu',
                'badge': '⚡ Sustained Energy'
            },
            {
                'name': 'Lace Appams with Malabar Spiced Egg Curry',
                'description': '2 soft fermented rice & coconut lace appams served with Kerala-style boiled eggs simmered in light coconut milk, shallots, and curry leaves.',
                'ingredients': ['2 soft lace appams', '2 boiled eggs in light coconut gravy', 'Shallots, ginger, green chilies & curry leaves', 'Fresh coriander'],
                'prep_time': '15 mins',
                'base_cals': 480,
                'p': 24,
                'c': 52,
                'f': 18,
                'region': 'Kerala',
                'badge': '🌴 Kerala Specialty'
            }
        ],
        'lunch': [
            {
                'name': 'Chettinad Spiced Chicken Breast with Brown Ponni Rice & Keerai Kootu',
                'description': 'Stone-ground Chettinad chicken breast curry served with unpolished brown Ponni rice, slow-cooked spinach moong dal kootu, and soothing pepper rasam.',
                'ingredients': ['180g skinless chicken breast in Chettinad spices', '1 cup cooked brown Ponni rice', '1 cup keerai (spinach) & moong dal kootu', '1 cup hot pepper rasam', '1 tsp cold-pressed sesame oil'],
                'prep_time': '22 mins',
                'base_cals': 570,
                'p': 48,
                'c': 54,
                'f': 15,
                'region': 'Tamil Nadu',
                'badge': '🍗 Chettinad Spiced'
            },
            {
                'name': 'Kerala Meen Pollichathu (Spiced Pan Fish) with Red Matta Rice',
                'description': 'Fish fillet coated in roasted shallots and kokum masala wrapped in a banana leaf, accompanied by fiber-rich Kerala red matta rice, cabbage thoran, and moru curry.',
                'ingredients': ['180g seer fish (vanjaram) / tilapia fillet', '1 cup cooked Kerala red matta rice', '1 cup cabbage thoran with fresh coconut', '1 cup probiotic moru curry (buttermilk curry)'],
                'prep_time': '20 mins',
                'base_cals': 550,
                'p': 44,
                'c': 52,
                'f': 16,
                'region': 'Kerala',
                'badge': '🐟 Coastal Omega-3'
            },
            {
                'name': 'Andhra Pepper Chicken Roast with Steamed Rice & Palakura Pappu',
                'description': 'Fiery crushed black pepper chicken breast toss served alongside warm steamed rice, spinach toor dal (palakura pappu), and cooling cucumber curd pachadi.',
                'ingredients': ['170g chicken breast strips in crushed black pepper', '1 cup steamed Ponni rice', '1 cup palakura pappu (spinach toor dal)', '1/2 cup fresh cucumber curd pachadi'],
                'prep_time': '20 mins',
                'base_cals': 560,
                'p': 46,
                'c': 52,
                'f': 14,
                'region': 'Andhra & Telangana',
                'badge': '🌶️ Andhra Spiced'
            }
        ],
        'snack': [
            {
                'name': 'Temple-Style Kala Chana Sundal & Spiced Neer Mor',
                'description': 'Boiled black chickpeas tossed with mustard seeds, asafoetida, curry leaves, and grated coconut, paired with chilled spiced buttermilk.',
                'ingredients': ['1 cup boiled black chana (kala chana)', '1.5 tbsp freshly grated coconut', '1 tall glass spiced neer mor (buttermilk with ginger & green chili)', 'Curry leaves & hing'],
                'prep_time': '5 mins',
                'base_cals': 260,
                'p': 14,
                'c': 34,
                'f': 7,
                'region': 'Tamil Nadu',
                'badge': '🌱 High-Fiber Tiffin'
            },
            {
                'name': 'Roasted Kadalai (Chana) with 2 Boiled Eggs & Filter Coffee',
                'description': 'Crunchy roasted spiced chana, 2 boiled eggs sprinkled with black pepper and sea salt, and a cup of unsweetened South Indian filter coffee.',
                'ingredients': ['40g roasted chana', '2 boiled eggs with pepper and pink salt', '1 cup South Indian filter coffee (unsweetened, toned milk)'],
                'prep_time': '4 mins',
                'base_cals': 280,
                'p': 22,
                'c': 20,
                'f': 11,
                'region': 'South Indian',
                'badge': '☕ Pre-Workout Fuel'
            },
            {
                'name': 'Natural Tender Coconut Water & Spiced Egg Podimas',
                'description': 'Pure hydrating tender coconut water paired with a 2-egg scramble sauteed with shallots, curry leaves, green chilies, and black pepper.',
                'ingredients': ['2 large eggs scrambled (egg podimas)', '1 fresh tender coconut water', 'Handful of curry leaves, shallots & green chili', '1 tsp cold-pressed coconut oil'],
                'prep_time': '6 mins',
                'base_cals': 240,
                'p': 16,
                'c': 15,
                'f': 12,
                'region': 'Kerala & Tamil Nadu',
                'badge': '🥥 Natural Electrolytes'
            }
        ],
        'dinner': [
            {
                'name': 'Karnataka Ragi Mudde with Chicken Saaru & Curd',
                'description': 'Traditional steamed finger millet ball packed with calcium and slow-digesting carbs, served with aromatic chicken saaru and cooling homemade curd.',
                'ingredients': ['1 medium ragi mudde (finger millet ball)', '170g chicken pieces in aromatic pepper saaru', '1/2 cup fresh low-fat curd', 'Onion and cucumber slices'],
                'prep_time': '20 mins',
                'base_cals': 530,
                'p': 42,
                'c': 56,
                'f': 14,
                'region': 'Karnataka',
                'badge': '🌾 Calcium & Millets'
            },
            {
                'name': 'Whole Wheat Phulkas with Chicken Keema Matar & Kachumber',
                'description': '2 soft whole wheat phulkas served with spiced minced chicken breast and green peas, accompanied by crisp cucumber and onion salad with lemon squeeze.',
                'ingredients': ['2 whole wheat phulkas', '180g lean chicken keema with green peas', 'Fresh cucumber and onion kachumber salad', '1 tsp ghee'],
                'prep_time': '20 mins',
                'base_cals': 520,
                'p': 44,
                'c': 48,
                'f': 14,
                'region': 'South Indian',
                'badge': '⚖️ Clean & Balanced'
            },
            {
                'name': 'Tawa Seer Fish (Meen Varuval) with Tempered Curd Rice & Rasam',
                'description': 'Shallow-seared spiced fish steak served with gut-friendly probiotic curd rice tempered with mustard, ginger, and pomegranate, plus hot pepper rasam.',
                'ingredients': ['180g seer fish / tilapia fillet in chili-turmeric rub', '3/4 cup brown curd rice with pomegranate', '1 cup hot pepper rasam', 'Fresh mint chutney'],
                'prep_time': '20 mins',
                'base_cals': 540,
                'p': 42,
                'c': 46,
                'f': 16,
                'region': 'Tamil Nadu',
                'badge': '🐟 Probiotic & Protein'
            }
        ]
    },
    'vegetarian': {
        'breakfast': [
            {
                'name': 'High-Protein Paneer Podi Dosa with Drumstick Sambar',
                'description': 'Crisp multigrain dosa stuffed with spiced crumbled paneer and roasted gun powder (idli podi), served with vegetable toor dal sambar.',
                'ingredients': ['1 crisp multigrain dosa', '130g low-fat paneer bhurji', '1.5 cups toor dal vegetable sambar', '1 tbsp mint coconut chutney', '1 tsp cold-pressed sesame oil'],
                'prep_time': '12 mins',
                'base_cals': 510,
                'p': 32,
                'c': 50,
                'f': 18,
                'region': 'Tamil Nadu',
                'badge': '🧀 High Protein Veg'
            },
            {
                'name': 'Andhra Pesarattu with Grated Paneer & Allam Chutney',
                'description': 'Protein-dense whole green moong dal crepe filled with fresh grated paneer, cumin, and onions, served with tangy ginger allam pachadi.',
                'ingredients': ['2 green moong pesarattus', '110g grated low-fat paneer filling', '2 tbsp allam (ginger) chutney', 'Green chilies, cumin & curry leaves'],
                'prep_time': '12 mins',
                'base_cals': 520,
                'p': 34,
                'c': 52,
                'f': 16,
                'region': 'Andhra & Telangana',
                'badge': '🌶️ Andhra Power Dosa'
            },
            {
                'name': 'Mixed Dal Adai with Protein-Packed Vegetable Avial',
                'description': 'Traditional thick South Indian crepe made of toor, chana, and moong lentils, served with coconut-yogurt vegetable avial rich in micronutrients.',
                'ingredients': ['2 mixed dal adais (chana, toor, moong)', '1 cup vegetable avial (carrots, beans, drumstick, curd)', '1 tbsp homemade tomato thakkali chutney', '1 tsp coconut oil'],
                'prep_time': '16 mins',
                'base_cals': 510,
                'p': 28,
                'c': 60,
                'f': 16,
                'region': 'Tamil Nadu & Kerala',
                'badge': '🫘 Multi-Lentil Power'
            },
            {
                'name': 'Steamed Ragi Idlis & Soya Chunks Keema Sambar',
                'description': '3 finger millet and urad dal steamed idlis rich in iron and calcium, served with sambar simmered with high-protein soya chunks and fresh drumsticks.',
                'ingredients': ['3 steamed ragi idlis', '40g dry soya chunks simmered in sambar', '1.5 cups vegetable sambar', '1 tbsp tomato-onion chutney'],
                'prep_time': '14 mins',
                'base_cals': 480,
                'p': 30,
                'c': 62,
                'f': 8,
                'region': 'Karnataka & Tamil Nadu',
                'badge': '🌾 Millets & Plant Protein'
            }
        ],
        'lunch': [
            {
                'name': 'Soya Chunks & Paneer Chettinad Kurma with Brown Rice',
                'description': 'Hearty South Indian coconut and fennel spiced curry loaded with tender soya chunks and paneer cubes, served with steamed brown rice and carrot-beans poriyal.',
                'ingredients': ['40g dry soya chunks (boiled)', '100g low-fat paneer', '1 cup cooked brown rice', '1 cup carrot-beans poriyal with grated coconut', 'Chettinad fennel-poppy seed masala'],
                'prep_time': '20 mins',
                'base_cals': 560,
                'p': 38,
                'c': 62,
                'f': 16,
                'region': 'Tamil Nadu',
                'badge': '🍛 38g Veg Protein'
            },
            {
                'name': 'Karnataka Bisi Bele Bath with Sprouted Moong, Paneer & Curd',
                'description': 'Karnataka classic spiced lentil-rice pot dish cooked with toor dal, sprouted green gram, vegetables, topped with pan-seared paneer cubes and homemade curd.',
                'ingredients': ['1.5 cups prepared bisi bele bath', '90g pan-seared paneer cubes', '1/2 cup fresh low-fat dahi (curd)', '1 tsp ghee', 'Roasted cashews & curry leaves'],
                'prep_time': '20 mins',
                'base_cals': 540,
                'p': 32,
                'c': 68,
                'f': 16,
                'region': 'Karnataka',
                'badge': '🌾 Karnataka Classic'
            },
            {
                'name': 'Dal Keerai Kootu with Brown Rice, Vazhaikkai Roast & Curd',
                'description': 'Slow-cooked spinach and yellow moong dal kootu, accompanied by steamed brown Ponni rice, spiced raw banana (vazhaikkai) stir fry, and fresh curd.',
                'ingredients': ['1.5 cups keerai (spinach) & moong dal kootu', '1 cup cooked brown rice', '1 cup spiced raw banana roast', '1/2 cup homemade curd'],
                'prep_time': '18 mins',
                'base_cals': 520,
                'p': 28,
                'c': 74,
                'f': 12,
                'region': 'Tamil Nadu',
                'badge': '🌿 High-Fiber & Gut-Friendly'
            }
        ],
        'snack': [
            {
                'name': 'Spiced Kala Chana Sundal with Coconut & Roasted Peanuts',
                'description': 'Traditional temple-style black chickpea sundal tossed with mustard seeds, asafoetida, curry leaves, and crushed peanuts.',
                'ingredients': ['1 cup boiled kala chana', '20g roasted peanuts', '1.5 tbsp freshly grated coconut', 'Green chillies & fresh lemon juice'],
                'prep_time': '4 mins',
                'base_cals': 270,
                'p': 14,
                'c': 32,
                'f': 9,
                'region': 'Tamil Nadu',
                'badge': '🌱 Traditional Sundal'
            },
            {
                'name': 'Spiced Neer Mor (Buttermilk) & Roasted Paneer Bites',
                'description': 'Chilled spiced buttermilk with crushed ginger and curry leaves, accompanied by air-fried chaat masala paneer cubes.',
                'ingredients': ['1 tall glass spiced neer mor (diluted probiotic curd)', '90g air-fried or seared paneer cubes', 'Chaat masala & black salt'],
                'prep_time': '5 mins',
                'base_cals': 250,
                'p': 21,
                'c': 8,
                'f': 14,
                'region': 'South Indian',
                'badge': '🥛 Probiotic & Protein'
            },
            {
                'name': 'Sprouted Green Moong Kosambari with Pomegranate',
                'description': 'Crunchy Karnataka salad made of sprouted green gram, grated carrots, cucumbers, pomegranate seeds, and fresh lemon-mustard tempering.',
                'ingredients': ['1 cup sprouted moong beans', '1/2 cup diced cucumber & grated carrot', '2 tbsp pomegranate seeds', '1 tsp cold-pressed coconut oil temper'],
                'prep_time': '5 mins',
                'base_cals': 220,
                'p': 14,
                'c': 34,
                'f': 4,
                'region': 'Karnataka',
                'badge': '🥗 Live Enzymes & Iron'
            }
        ],
        'dinner': [
            {
                'name': 'Karnataka Ragi Mudde with High-Protein Dal Sambar & Curd',
                'description': 'Traditional Karnataka steamed finger millet (ragi) ball packed with calcium and slow-burning carbs, paired with thick toor dal vegetable sambar and fresh curd.',
                'ingredients': ['1 medium ragi mudde (finger millet ball)', '1.5 cups thick toor dal vegetable sambar', '1/2 cup low-fat curd', 'Cucumber & onion slices'],
                'prep_time': '18 mins',
                'base_cals': 510,
                'p': 26,
                'c': 76,
                'f': 10,
                'region': 'Karnataka',
                'badge': '🌾 Iron & Calcium'
            },
            {
                'name': 'Whole Wheat Phulkas with Paneer Chettinad & Sprouts Salad',
                'description': '2 soft whole wheat phulkas served with spicy Chettinad paneer curry and a crunchy sprouted bean salad.',
                'ingredients': ['2 whole wheat phulkas', '140g low-fat paneer cooked in Chettinad masala', '1/2 cup mixed sprouts salad', '1 tsp ghee'],
                'prep_time': '20 mins',
                'base_cals': 540,
                'p': 34,
                'c': 50,
                'f': 20,
                'region': 'Tamil Nadu',
                'badge': '🧀 Satiating Protein'
            },
            {
                'name': 'Probiotic Curd Rice with Tempered Soya Bhurji',
                'description': 'Comforting South Indian curd rice tempered with mustard, curry leaves, and ginger, topped with spiced crumbled high-protein soya chunks.',
                'ingredients': ['1 cup brown curd rice with pomegranate', '50g cooked spiced soya granules bhurji', 'Ginger, green chili & mustard tempering'],
                'prep_time': '12 mins',
                'base_cals': 490,
                'p': 32,
                'c': 58,
                'f': 12,
                'region': 'South Indian',
                'badge': '🥛 Gut Recovery'
            }
        ]
    },
    'vegan': {
        'breakfast': [
            {
                'name': 'Sprouted Moong Pesarattu with Vegetable Sambar',
                'description': 'Crispy whole green gram dosa naturally packed with plant protein, served with freshly simmered toor dal sambar and ginger chutney.',
                'ingredients': ['2 whole moong pesarattus', '1.5 cups toor dal vegetable sambar', '1 tbsp allam ginger chutney', 'Chopped onions & cumin'],
                'prep_time': '12 mins',
                'base_cals': 480,
                'p': 28,
                'c': 62,
                'f': 10,
                'region': 'Andhra & Telangana',
                'badge': '🌱 100% Plant Power'
            },
            {
                'name': 'Steamed Ragi Idlis with High-Protein Dal & Tomato Chutney',
                'description': '3 finger millet and urad dal steamed idlis rich in iron and calcium, served with yellow moong dal and tangy roasted tomato chutney.',
                'ingredients': ['3 ragi idlis', '1.5 cups thick toor & moong dal', '2 tbsp roasted onion-tomato chutney', 'Curry leaves & mustard temper'],
                'prep_time': '14 mins',
                'base_cals': 460,
                'p': 26,
                'c': 66,
                'f': 8,
                'region': 'Tamil Nadu',
                'badge': '🌾 Calcium Rich'
            }
        ],
        'lunch': [
            {
                'name': 'Kerala Kadala Curry with Steamed Matta Rice & Cabbage Thoran',
                'description': 'Authentic black chickpea curry simmered with roasted coconut paste and Malabar spices, served with red matta rice and cabbage thoran.',
                'ingredients': ['1.5 cups boiled black chickpeas (kadala)', '1 cup cooked Kerala matta rice', '1 cup cabbage and coconut thoran', 'Curry leaves, shallots & mustard seeds'],
                'prep_time': '20 mins',
                'base_cals': 560,
                'p': 30,
                'c': 80,
                'f': 14,
                'region': 'Kerala',
                'badge': '🌴 Malabar Kadala'
            },
            {
                'name': 'South Indian Soya Chunks & Tofu Kurma with Steamed Rice',
                'description': 'Protein-dense firm tofu and soya chunks in a fragrant coconut-fennel gravy, served with warm Ponni rice, pepper rasam, and cucumber.',
                'ingredients': ['120g firm tofu cubes', '30g soya chunks', '1 cup steamed rice', '1 cup tomato-pepper rasam', 'Coriander & curry leaves'],
                'prep_time': '18 mins',
                'base_cals': 540,
                'p': 36,
                'c': 64,
                'f': 14,
                'region': 'Tamil Nadu',
                'badge': '🌱 High Protein Soya'
            }
        ],
        'snack': [
            {
                'name': 'Temple-Style White & Black Chana Sundal with Tender Coconut',
                'description': 'Steamed chickpeas tossed with mustard, hing, curry leaves, and grated fresh coconut, paired with pure tender coconut water.',
                'ingredients': ['1 cup boiled chickpeas (chana)', '1.5 tbsp fresh coconut', '1 cup natural tender coconut water', 'Pinch of sea salt & lemon'],
                'prep_time': '4 mins',
                'base_cals': 260,
                'p': 13,
                'c': 38,
                'f': 6,
                'region': 'Tamil Nadu',
                'badge': '🥥 Natural Hydration'
            },
            {
                'name': 'Roasted Spiced Peanuts & Makhana with Ginger Lemon Chai',
                'description': 'Crunchy fox nuts (makhana) and roasted peanuts tossed in turmeric and chaat masala, paired with black ginger tea.',
                'ingredients': ['25g roasted peanuts', '25g roasted makhana (foxnuts)', '1 cup spiced black tea with fresh crushed ginger', 'Chaat masala'],
                'prep_time': '4 mins',
                'base_cals': 240,
                'p': 10,
                'c': 24,
                'f': 12,
                'region': 'South Indian',
                'badge': '☕ Antioxidant Snack'
            }
        ],
        'dinner': [
            {
                'name': 'Finger Millet (Ragi Mudde) with Drumstick Dal Kootu',
                'description': 'Traditional steamed finger millet ball served with iron-rich spinach, drumstick and toor dal kootu, with a side of raw onion and cucumber.',
                'ingredients': ['1 ragi mudde', '1.5 cups drumstick & spinach toor dal kootu', 'Fresh cucumber and carrot slices', '1 tsp cold-pressed sesame oil'],
                'prep_time': '20 mins',
                'base_cals': 490,
                'p': 24,
                'c': 78,
                'f': 8,
                'region': 'Karnataka',
                'badge': '🌾 Ancient Grain Power'
            },
            {
                'name': 'Foxtail Millet (Thinai) Khichdi with Mixed Veggies & Tofu',
                'description': 'Comforting foxtail millet and yellow moong dal khichdi loaded with carrots, green beans, and seared turmeric tofu cubes.',
                'ingredients': ['1.5 cups foxtail millet & moong dal khichdi', '100g pan-seared tofu cubes', '1 tsp cold-pressed coconut oil', 'Roasted cumin & black pepper'],
                'prep_time': '22 mins',
                'base_cals': 520,
                'p': 30,
                'c': 68,
                'f': 12,
                'region': 'Tamil Nadu',
                'badge': '🌾 Millets & Tofu'
            }
        ]
    },
    'keto': {
        'breakfast': [
            {
                'name': 'South Indian Egg Podimas (Egg Scramble) with Coconut Chutney',
                'description': '3 whole eggs scrambled with shallots, curry leaves, green chilies, and black pepper, accompanied by freshly ground thick coconut chutney.',
                'ingredients': ['3 large eggs', '2 tbsp thick coconut chutney (no dal)', '1/2 onion & green chili sauteed in cold-pressed coconut oil', 'Curry leaves & black pepper'],
                'prep_time': '10 mins',
                'base_cals': 480,
                'p': 26,
                'c': 6,
                'f': 38,
                'region': 'Tamil Nadu & Kerala',
                'badge': '🥑 Low-Carb Breakfast'
            },
            {
                'name': 'Pepper Paneer Tikka with Mint Coriander Chutney',
                'description': 'Generous cubes of fresh paneer marinated in South Indian spices, black pepper, and yogurt, pan-grilled crisp.',
                'ingredients': ['180g paneer cubes', '2 tbsp thick hung curd marinade', 'Black pepper, turmeric, cumin', '2 tbsp fresh mint-coriander dip'],
                'prep_time': '12 mins',
                'base_cals': 520,
                'p': 32,
                'c': 7,
                'f': 40,
                'region': 'South Indian',
                'badge': '🧀 Keto Paneer'
            }
        ],
        'lunch': [
            {
                'name': 'Chettinad Chicken Breast Roast with Cauliflower Poriyal',
                'description': 'Tender chicken breast cooked dry in stone-ground Chettinad masala, served with grated cauliflower poriyal sauteed in coconut oil and mustard.',
                'ingredients': ['200g chicken breast strips', '2 cups riced cauliflower poriyal', '1.5 tbsp cold-pressed coconut oil', 'Chettinad spices, curry leaves & shallots'],
                'prep_time': '20 mins',
                'base_cals': 540,
                'p': 52,
                'c': 8,
                'f': 32,
                'region': 'Tamil Nadu',
                'badge': '🍗 52g Protein Keto'
            },
            {
                'name': 'Kerala Malabar Fish Curry with Coconut Cream & Cucumber Salad',
                'description': 'Wild seer fish or salmon simmered in thick coconut milk, kokum (kudampuli), and green chilies, paired with crisp cucumber and shredded coconut salad.',
                'ingredients': ['190g fish steak (seer fish/salmon)', '1/2 cup thick coconut milk gravy', '1.5 cups diced cucumber with lemon and curry leaf temper'],
                'prep_time': '18 mins',
                'base_cals': 560,
                'p': 44,
                'c': 7,
                'f': 38,
                'region': 'Kerala',
                'badge': '🥥 Coconut & Fish'
            }
        ],
        'snack': [
            {
                'name': 'Roasted Salted Almonds & Spiced Neer Mor',
                'description': 'Handful of roasted almonds paired with a tall glass of diluted spiced buttermilk with ginger and curry leaves.',
                'ingredients': ['30g roasted almonds', '1 glass spiced neer mor (thin buttermilk)', 'Crushed ginger, salt & curry leaves'],
                'prep_time': '2 mins',
                'base_cals': 240,
                'p': 9,
                'c': 6,
                'f': 20,
                'region': 'South Indian',
                'badge': '🥛 Keto Friendly'
            }
        ],
        'dinner': [
            {
                'name': 'Kerala Style Chicken Stew with Sauteed Greens',
                'description': 'Succulent chicken simmered in aromatic whole spices, ginger, and coconut milk, served with a big bowl of sauteed spinach (keerai poriyal).',
                'ingredients': ['200g chicken thighs or breast', '1/2 cup coconut milk', '2 cups keerai (spinach) sauteed in coconut oil with shallots'],
                'prep_time': '20 mins',
                'base_cals': 580,
                'p': 48,
                'c': 9,
                'f': 38,
                'region': 'Kerala',
                'badge': '🌴 Clean Keto Stew'
            },
            {
                'name': 'Tawa Fried Spiced Paneer & Cabbage Thoran',
                'description': 'Thick slices of paneer seared in South Indian chili and turmeric masala, accompanied by warm cabbage and coconut thoran.',
                'ingredients': ['170g paneer slices', '1.5 cups cabbage thoran', '1 tbsp cold-pressed coconut oil', 'Mustard seeds & red chili flakes'],
                'prep_time': '15 mins',
                'base_cals': 530,
                'p': 30,
                'c': 10,
                'f': 41,
                'region': 'Kerala & Tamil Nadu',
                'badge': '🧀 High Healthy Fats'
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


def generate_ai_diet_plan(user, dietary_preference=None, custom_calories=None, state=None, cuisine_preference=None):
    """
    Generates a structured daily meal plan (Breakfast, Lunch, Snack, Dinner)
    scaled to the user's role, goal, and target macros.
    Supports state-specific South Indian recipes and continental option.
    """
    pref = dietary_preference or user.dietary_preference or 'standard'
    if pref not in MEAL_RECIPES:
        pref = 'standard'

    # Resolve state and cuisine preference
    user_state = state or getattr(user, 'state', None) or 'Tamil Nadu'
    user_cuisine = cuisine_preference or getattr(user, 'cuisine_preference', None) or 'home_state'

    targets = calculate_user_targets(user, custom_calories)
    target_cals = targets['calories']
    role_key = user.role if user.role in ROLE_DETAILS else 'general'
    role_info = ROLE_DETAILS[role_key]

    # Target breakdown: Breakfast ~26%, Lunch ~33%, Snack ~15%, Dinner ~26%
    meal_allocations = [
        ('breakfast', 'Breakfast', '07:30 - 08:30', 0.26),
        ('lunch', 'Lunch', '12:30 - 13:30', 0.33),
        ('snack', 'Evening Tiffin / Snack', '16:00 - 16:30', 0.15),
        ('dinner', 'Dinner', '19:30 - 20:30', 0.26),
    ]

    recipe_catalog = MEAL_RECIPES[pref]
    fallback_catalog = MEAL_RECIPES['standard']

    # Determine recipe pool based on cuisine preference
    # For continental: use CONTINENTAL_RECIPES entirely
    # For home_state: inject state-specific recipes as primary options
    # For other_states: use all MEAL_RECIPES across states (default pool)
    state_highlights = STATE_RECIPE_HIGHLIGHTS.get(user_state, {})

    meals = []
    total_planned_cals = 0
    total_p = 0
    total_c = 0
    total_f = 0

    for slot_id, slot_name, time_str, alloc_pct in meal_allocations:
        if user_cuisine == 'continental':
            # Use continental recipes pool
            slot_pool = CONTINENTAL_RECIPES.get(slot_id) or CONTINENTAL_RECIPES.get('dinner', [])
        elif user_cuisine == 'home_state' and state_highlights.get(slot_id):
            # Blend state-specific highlights (60%) with base pool (40%)
            base_pool = recipe_catalog.get(slot_id) or fallback_catalog.get(slot_id, fallback_catalog['breakfast'])
            state_pool = state_highlights[slot_id]
            # Randomly pick: 65% chance of state-specific recipe
            import random as _r
            slot_pool = state_pool if _r.random() < 0.65 else base_pool
        else:
            # other_states or no highlight: use standard regional recipe pool
            slot_pool = recipe_catalog.get(slot_id) or fallback_catalog.get(slot_id, fallback_catalog['breakfast'])

        chosen = random.choice(slot_pool)

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

        # Natural, human-written reason why this meal fits their lifestyle
        if role_key == 'desk_worker':
            if slot_id == 'lunch':
                benefit = 'Light, fiber-rich South Indian staples that give you steady afternoon energy without making you drowsy at your desk.'
            elif slot_id == 'snack':
                benefit = 'A satisfying, clean tiffin bite that satisfies hunger and prevents mindless office snacking.'
            else:
                benefit = 'Anti-inflammatory spices (turmeric, ginger, pepper) and quality protein supporting joint health and posture.'
        elif role_key == 'student':
            benefit = 'Affordable, easy-to-prep South Indian fuel packed with sustained brain energy and high protein.'
        elif role_key == 'athlete':
            benefit = 'Rich in natural electrolytes, wholesome complex carbs, and rapid protein for muscular endurance and bounce-back.'
        elif role_key == 'bodybuilder':
            benefit = 'Dialed-in protein density from South Indian staples to support continuous muscle growth and recovery.'
        elif role_key == 'busy_parent':
            benefit = 'Simple, comforting South Indian dish that you can easily share with your family or batch prep in advance.'
        else:
            benefit = 'Nutrient-dense home food with authentic spices, supporting healthy gut digestion and long-term vitality.'

        meals.append({
            'id': slot_id,
            'name': chosen['name'],
            'slot_name': slot_name,
            'time': time_str,
            'description': chosen['description'],
            'ingredients': chosen['ingredients'],
            'prep_time': chosen['prep_time'],
            'region': chosen.get('region', 'South Indian'),
            'badge': chosen.get('badge', 'Wholesome'),
            'calories': scaled_cals,
            'protein': scaled_p,
            'carbs': scaled_c,
            'fat': scaled_f,
            'role_benefit': benefit,
            'completed': False
        })

    # Generate a meaningful plan title
    if user_cuisine == 'continental':
        cuisine_label = 'Continental & Fusion'
    elif user_cuisine == 'other_states':
        cuisine_label = 'South Indian Regional Mix'
    else:
        cuisine_label = f'{user_state} Home Kitchen'

    title = f"{role_info['icon']} {cuisine_label}: {user.goal.capitalize()} Plan ({role_info['title']})"

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
    Generates dynamic coaching advice based on the user's
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
                weight_insight = f"Down {abs(diff)} kg since your first entry. Your South Indian caloric deficit is right on track. Keep your keerai and dal portions generous."
            elif diff > 0:
                weight_insight = f"Weight is up by {diff} kg. Don't worry—this can easily be temporary water or sodium retention. Watch weekend rice refills and snacks."
            else:
                weight_insight = "Weight has plateaued for a bit. If this continues for 10 days, try switching white rice with ragi mudde or pesarattu."
        elif user.goal == 'bulking':
            if diff > 0:
                weight_insight = f"Gained {diff} kg. Great steady muscle-building progress! Aim for 0.25 to 0.5 kg per week to keep gains lean."
            else:
                weight_insight = "Weight hasn't increased yet. You need more caloric density—add an extra spoon of ghee, a handful of roasted peanuts, or an extra glass of milk."
        else:
            weight_insight = f"Weight is holding steady ({diff:+} kg). You are maintaining your target balance smoothly."
    elif user.weight_kg and user.target_weight_kg:
        diff = round(abs(user.weight_kg - user.target_weight_kg), 1)
        weight_insight = f"You are {diff} kg away from your target of {user.target_weight_kg} kg. Consistency with daily meals and workouts will get you there."
    else:
        weight_insight = "Log your weight every few days in the Weight tab to track your trend and body recomposition."

    consistency_score = min(100, (month_checkins * 5) + (streak * 7))

    if streak == 0:
        priority = "Let's hit the gym today! Even a 30-minute session will reignite your streak and boost your energy for the week."
    elif streak >= 5:
        priority = f"🔥 Wonderful {streak}-day streak! Make sure you prioritize 7-8 hours of sleep and drink enough water ({role_info['hydration_target']}L) to allow full recovery."
    else:
        priority = f"You have an active {streak}-day streak going. Complete today's workout split and log your healthy meals!"

    supplements = [
        {'name': 'Creatine Monohydrate', 'dosage': '5g daily', 'benefit': 'Enhances strength, power output, and workout performance. Dissolves easily in water.'},
        {'name': 'Whey or Plant Protein', 'dosage': '1 scoop (25-30g) as needed', 'benefit': 'Convenient way to hit your daily protein goal on busy South Indian workdays.'},
        {'name': 'Omega-3 Fish Oil / Algae Oil', 'dosage': '1,000-2,000mg daily', 'benefit': 'Supports heart health, joints, and natural inflammation reduction.'},
        {'name': 'Vitamin D3', 'dosage': '2,000-4,000 IU daily', 'benefit': 'Essential for bone density, hormonal balance, and immunity.'}
    ]

    return {
        'daily_priority': priority,
        'consistency_score': consistency_score,
        'weight_insight': weight_insight,
        'bmi': bmi,
        'bmi_category': bmi_cat,
        'streak': streak,
        'month_checkins': month_checkins,
        'supplements': supplements,
        'workout_focus': role_info['workout_focus'],
        'role_tips': role_info['tips'],
        'hydration_target': role_info['hydration_target']
    }


def query_gemini_api(api_key, system_instruction, user_prompt):
    """Calls Google Gemini REST API directly with standard library urllib if API key is provided."""
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
    Coach Raghav — friendly, supportive South Indian fitness & nutrition mentor.
    Answers in warm, natural, human tone without robotic AI jargon.
    """
    query_clean = query.strip()
    q_lower = query_clean.lower()
    role_key = user.role if user.role in ROLE_DETAILS else 'general'
    role_info = ROLE_DETAILS[role_key]

    system_context = (
        f"You are Coach Raghav, a warm, experienced personal fitness and nutrition coach for the Fitrack app. "
        f"You deeply understand South Indian culinary staples "
        f"(idlis, dosas, sambar, rasam, neer mor, sundal, filter coffee, poriyal, ragi mudde, pesarattu, biryani, chicken sukka, meen curry). "
        f"IMPORTANT: Always respond in normal, clear English. Never use regional language greetings like 'Vanakkam', 'Namaste', or any Tamil/Telugu/Kannada/Malayalam phrases. "
        f"Start responses directly with the advice or a short English greeting like 'Hey!' or 'Great question!'. "
        f"Avoid robotic AI buzzwords like 'I am an AI model' or clinical jargon. "
        f"User Profile: Name: {user.username}, Role: {role_info['title']}, Goal: {user.goal}, "
        f"Weight: {user.weight_kg or 'Not set'}kg, Target: {user.target_weight_kg or 'Not set'}kg, Streak: {user.get_current_streak()} days. "
        f"Give concise, warm, practical advice with clear bullet points."
    )

    # 1. Check external LLM API if key is set
    gemini_key = os.environ.get('GEMINI_API_KEY')
    if gemini_key:
        try:
            return query_gemini_api(gemini_key, system_context, query_clean)
        except Exception:
            pass

    # 2. Rich Built-in Knowledge Engine tailored for South Indian Fitness & Diets

    # Filter Coffee & Caffeine
    if any(k in q_lower for k in ['coffee', 'filter coffee', 'kaapi', 'caffeine', 'tea', 'chai']):
        return (
            f"☕ **Can You Drink Filter Coffee on Your Fitness Journey? Yes!**\n\n"
            f"Good news, {user.username}: You don't have to give up your authentic South Indian filter coffee! Here is how to make it fitness-friendly:\n\n"
            f"• **Pre-Workout Booster:** Drink 1 cup 40-45 minutes before your workout. Caffeine boosts central nervous system drive, stamina, and fat mobilization.\n"
            f"• **Milk Choice:** Use toned cow's milk rather than full-fat buffalo milk to save ~60-80 calories per cup.\n"
            f"• **Sugar Strategy:** Cut refined white sugar in half, or transition to zero-calorie stevia/monk fruit, or enjoy it unsweetened. Two cups of heavily sweetened coffee can quietly add 150+ empty calories!\n"
            f"• **Timing Rule:** Avoid drinking coffee after 5:00 PM so it doesn't disturb your deep REM sleep, which is when your muscles recover and grow."
        )

    # Rice, Carbs & Sambar balance
    elif any(k in q_lower for k in ['rice', 'white rice', 'carbs', 'sambar', 'rasam', 'curd rice', 'ponni', 'matta']):
        return (
            f"🍛 **How to Enjoy South Indian Rice Without Guilt:**\n\n"
            f"You do NOT need to eliminate rice to lose fat or build muscle. The key is **portion size and plate composition**:\n\n"
            f"• **The 1-Cup Rule:** Limit cooked rice to 1 standard katori (cup) per meal. Never go for the automatic 2nd or 3rd refill.\n"
            f"• **Smart Grain Swaps:** Try Brown Ponni rice, Kerala Red Matta rice, or Foxtail Millet (Thinai). They have a lower glycemic index and keep you full much longer.\n"
            f"• **Double the Vegetables & Dal:** Fill half your plate with vegetable poriyal (beans, cabbage, beetroot) or keerai kootu before adding rice.\n"
            f"• **Sambar Protein Hack:** Traditional toor dal sambar has ~4-5g protein per bowl. Boost it by dropping 2 boiled eggs, 60g paneer cubes, or boiled soya chunks directly into your sambar bowl!\n"
            f"• **Curd Rice:** Homemade curd is a wonderful probiotic. Pair it with cucumber, pomegranate seeds, and a side of spiced sundal to turn it into a high-protein, gut-friendly meal."
        )

    # Vegetarian Protein for South Indians
    elif any(k in q_lower for k in ['veg protein', 'vegetarian', 'vegetarian protein', 'paneer', 'soya', 'dal protein', 'sprouts', 'pure veg']) or ('veg' in q_lower and 'protein' in q_lower):
        macros = user.get_target_macros()
        return (
            f"🧀 **High-Protein South Indian Vegetarian Guide ({macros['protein']}g Goal):**\n\n"
            f"Many South Indians find hitting protein challenging on a pure veg diet. Here are the most effective local foods to hit your target:\n\n"
            f"1. **Low-Fat Paneer:** 100g gives ~18g protein. Make Paneer Podi Dosa, Paneer Chettinad, or toss air-fried paneer cubes into your salad.\n"
            f"2. **Soya Chunks:** The ultimate plant-protein champion! 50g dry soya chunks provide **26g protein**. Simmer them in your daily sambar or make soya bhurji.\n"
            f"3. **Andhra Pesarattu (Moong Dal Dosa):** Made with whole green gram. Two pesarattus stuffed with paneer easily deliver **30g+ protein**.\n"
            f"4. **Temple-Style Sundal:** 1 cup of boiled black chana or green peas sundal delivers **14g protein** plus rich dietary fiber.\n"
            f"5. **Thick Homemade Curd / Greek Yogurt:** 1 cup provides 8-12g protein and keeps your gut cool in hot weather.\n"
            f"6. **Whey or Plant Protein:** 1 scoop post-workout or stirred into morning oats/ragi malt gives you a quick 25g protein boost."
        )

    # Pre-workout snacks
    elif any(k in q_lower for k in ['pre-workout', 'pre workout', 'preworkout', 'before workout', 'before gym', 'snack', 'snacks']):
        goal = user.goal or 'maintaining'
        if goal == 'cutting':
            snack_picks = (
                "• **Option 1 (Sundal & Neer Mor):** 1 cup boiled kala chana sundal with chilled spiced buttermilk (~190 kcal, 14g protein).\n"
                "• **Option 2 (Banana & Filter Coffee):** 1 small banana with black filter coffee (~110 kcal, clean carbohydrate energy).\n"
                "• **Option 3 (Boiled Eggs & Pepper):** 2 boiled eggs seasoned with black pepper and pink salt (~140 kcal, 12g protein)."
            )
        elif goal == 'bulking':
            snack_picks = (
                "• **Option 1 (Idli Stack):** 2 steamed idlis with sambar and 2 boiled eggs (~380 kcal, 24g protein, 48g carbs).\n"
                "• **Option 2 (Ragi Malt & Whey):** Warm ragi malt with half banana and 1 scoop whey protein (~350 kcal, 30g protein).\n"
                "• **Option 3 (Peanut Chikki & Filter Coffee):** 2 pieces peanut chikki with South Indian filter coffee (~280 kcal, 10g protein)."
            )
        else:
            snack_picks = (
                "• **Option 1 (Classic Tiffin):** 1 ripe banana with a handful of roasted peanuts (~190 kcal, 7g protein).\n"
                "• **Option 2 (White Chana Sundal):** 1 cup tempered sundal with freshly grated coconut (~200 kcal, 10g protein).\n"
                "• **Option 3 (Spiced Egg Podimas):** 2 eggs scrambled with shallots and curry leaves (~160 kcal, 12g protein)."
            )

        role_note = ""
        if role_key == 'desk_worker':
            role_note = "💼 *Desk Worker Note:* Drink 500ml of water alongside your snack. Sitting in air-conditioned offices causes unnoticed dehydration that can sap lifting strength by 15%."
        elif role_key == 'student':
            role_note = "🎓 *Student Note:* Bananas and roasted chana are cheap, portable, and easily carried in your backpack between classes."
        else:
            role_note = "🧘 *Coach Tip:* Eat your pre-workout snack 45 to 60 minutes before training so food doesn't sit heavy in your stomach."

        return (
            f"⚡ **Best Pre-Workout Snacks for {user.username} ({role_info['title']}):**\n\n"
            f"{snack_picks}\n\n"
            f"{role_note}"
        )

    # Post-workout recovery
    elif any(k in q_lower for k in ['post-workout', 'post workout', 'postworkout', 'after workout', 'after gym']):
        return (
            f"💪 **Post-Workout Recovery Guide for South Indian Meals:**\n\n"
            f"Within 60-90 minutes after lifting, give your muscles 25-40g of protein and quality complex carbs to recover:\n\n"
            f"• **Option 1:** Chettinad chicken breast (or paneer) with 1 cup brown Ponni rice, keerai kootu, and pepper rasam.\n"
            f"• **Option 2:** 3 steamed idlis with thick sambar and 2 boiled eggs (or soya chunks curry).\n"
            f"• **Option 3:** 2 whole wheat phulkas with egg podimas or chicken keema and a side of curd.\n"
            f"• **Option 4:** 1 scoop of whey protein in water or cold milk, paired with 1 banana.\n"
            f"• **Hydration:** Rehydrate with 1 glass of tender coconut water or spiced neer mor with a pinch of pink salt."
        )

    # Supplements
    elif any(k in q_lower for k in ['supplement', 'supplements', 'creatine', 'vitamin', 'omega', 'fish oil']):
        return (
            f"💊 **Evidence-Based Supplements Worth Taking:**\n\n"
            f"You don't need dozens of fancy pills. Stick to the proven essentials:\n\n"
            f"• **Creatine Monohydrate (5g daily):** The single most researched supplement for muscle strength, power, and mental alertness. Take it every day with water.\n"
            f"• **Whey or Plant Protein:** A convenient whole-food derivative to ensure you hit your daily {user.get_target_macros()['protein']}g protein goal.\n"
            f"• **Omega-3 (1,000-2,000mg):** Great for heart health, brain function, and soothing joint aches from heavy squats and presses.\n"
            f"• **Vitamin D3 (2,000-4,000 IU):** Many of us spend our days indoors in offices and colleges; maintaining healthy Vitamin D is crucial for testosterone, mood, and bone density."
        )

    # Daily Macros & Calories
    elif any(k in q_lower for k in ['macro', 'macros', 'calorie', 'calories', 'tdee', 'bmr', 'target']):
        cals = user.get_calorie_target()
        macros = user.get_target_macros()
        return (
            f"🥗 **Your Daily Nutrition Targets ({role_info['title']} • {user.goal.capitalize()}):**\n\n"
            f"• **Daily Calories:** ~**{cals} kcal** (BMR: {user.calculate_bmr()} | TDEE: {user.calculate_tdee()})\n"
            f"• **Protein:** **{macros['protein']}g** (~{macros['protein']*4} kcal) — For muscle repair & firm physique.\n"
            f"• **Carbohydrates:** **{macros['carbs']}g** (~{macros['carbs']*4} kcal) — From unpolished rice, idlis, millets & lentils.\n"
            f"• **Healthy Fats:** **{macros['fat']}g** (~{macros['fat']*9} kcal) — From cold-pressed oils, nuts, and modest ghee.\n\n"
            f"Check your **Nutrition Plan** tab to see your exact 4 meals planned for today!"
        )

    # General Diet / Food
    elif any(k in q_lower for k in ['diet', 'meal', 'eat', 'food', 'nutrition', 'hungry', 'plan']):
        cals = user.get_calorie_target()
        macros = user.get_target_macros()
        return (
            f"🍛 **Your Personalized South Indian Meal Plan:**\n\n"
            f"• **Target:** ~**{cals} kcal** ({macros['protein']}g Protein | {macros['carbs']}g Carbs | {macros['fat']}g Fat)\n"
            f"• **Style:** {role_info['diet_focus']}\n"
            f"• **Golden Rule:** Keep rice portions disciplined, prioritize dal, eggs, fish, or paneer in every meal, and stay hydrated.\n"
            f"• Visit your **Nutrition Plan** tab anytime to log meals or customize your preferences."
        )

    # Hydration
    elif any(k in q_lower for k in ['water', 'hydration', 'drink', 'liters', 'buttermilk', 'neer mor']):
        target = role_info['hydration_target']
        return (
            f"💧 **Hydration Guidelines for {role_info['title']}:**\n\n"
            f"• Your daily goal is **{target} Liters**.\n"
            f"• **Natural South Indian Hydration:**\n"
            f"  1. **Spiced Neer Mor:** Diluted churned curd with crushed ginger, green chili, curry leaves, and pink salt. Cools the stomach and restores electrolytes.\n"
            f"  2. **Tender Coconut Water:** Nature's isotonic drink with potassium and magnesium.\n"
            f"  3. **Jeera / Cumin Water:** Warm water boiled with cumin seeds helps ease digestion and bloating.\n"
            f"• *Simple habit:* Drink 1 big glass of water right when you wake up, sip water throughout work, and have neer mor after lunch."
        )

    # Workouts & Training
    elif any(k in q_lower for k in ['workout', 'routine', 'split', 'exercise', 'train', 'lifting', 'gym']):
        return (
            f"🏋️ **Training Tips for {user.username} ({role_info['title']}):**\n\n"
            f"• **Current Split:** Check the **Workouts** tab for your full week's exercise schedule.\n"
            f"• **Focus Area:** {role_info['workout_focus']}\n"
            f"• **Progressive Overload:** When you can perform the top of the rep range on all sets with solid form, increase the weight by 2.5kg next week.\n"
            f"• **Rest Days:** Recovery is when muscle builds—don't neglect your 7-8 hours of sleep!"
        )

    # Streak & Motivation
    elif any(k in q_lower for k in ['streak', 'motivation', 'consistency', 'missed', 'lazy', 'tired', 'discipline']):
        streak = user.get_current_streak()
        return (
            f"🔥 **Staying Consistent with Coach Raghav:**\n\n"
            f"• You are currently on a **{streak}-day streak**!\n"
            f"• Some days you won't feel 100% motivated, and that's completely normal. On those days, just showing up for 25 minutes keeps the habit alive.\n"
            f"• Remember: Fitness isn't an all-or-nothing test. Small, healthy choices with your meals and regular workouts add up to life-changing results.\n"
            f"• Head to your dashboard and log today's check-in!"
        )

    # Fallback greeting & helpful prompts
    else:
        return (
            f"Hello {user.username}! I'm Coach Raghav, your personal fitness and nutrition mentor.\n\n"
            f"I'm here to help you get great results while enjoying wholesome food (Kerala, Tamil Nadu, North Indian and beyond). What can I help you with?\n\n"
            f"• 🌴 **Kerala & Tamil Nadu Meal Styles:** Top traditional dishes & macro hacks\n"
            f"• ☕ **Filter Coffee & Energy:** How to enjoy it around your workouts\n"
            f"• 🏋️ **Progressive Overload:** Next weight targets for your bench, squats & rows\n"
            f"• 🧀 **High-Protein Staples:** Best choices for veg and non-veg diets\n"
            f"• 🥗 **Daily Targets:** Your calories, protein, and personalized meal ideas\n\n"
            f"Feel free to ask me anything about meals, workouts, or daily habits!"
        )


def get_regional_food_recommendations_today(user, dietary_preference=None):
    """
    Returns today's curated regional food recommendations comparing:
    - Kerala Style (Heavily Featured)
    - Tamil Nadu Style (Heavily Featured)
    - North Indian Style
    Each with morning tiffin, lunch feast, evening snack, and dinner with macros, portioning and health benefits.
    """
    pref = dietary_preference or getattr(user, 'dietary_preference', 'standard') or 'standard'
    is_veg = pref in ('vegetarian', 'vegan')
    is_low_carb = pref == 'keto'

    data = {
        'kerala': {
            'title': 'Kerala Style Food',
            'tagline': 'High Micronutrient Coastal & Coconut Infusions with Red Matta Rice & Steamed Staples',
            'icon': '🌴',
            'highlight': 'Deep Focus • Kerala Cuisine',
            'color': '#059669',
            'why_today': 'Rich in slow-digesting antioxidants from red matta rice, healthy medium-chain fats from cold-pressed coconut oil, and clean protein from fish or kadala curry.',
            'meals': [
                {
                    'slot': 'Breakfast',
                    'dish': 'Steamed Puttu with Kadala Curry & Nendran Banana' if not is_low_carb else 'Kerala Egg Roast with Coconut Poriyal',
                    'macros': '🔥 510 kcal • 24g Protein • 68g Carbs • 14g Fat' if not is_low_carb else '🔥 450 kcal • 28g Protein • 8g Carbs • 34g Fat',
                    'description': 'Classic steamed rice & grated coconut puttu cylinders paired with roasted coconut and whole black chickpea gravy.',
                    'pro_tip': 'Kadala (kala chana) gives steady morning amino acids and low-GI energy.'
                },
                {
                    'slot': 'Lunch',
                    'dish': 'Kerala Matta Sadya Plate (Avial, Olan, Thoran & Sambar)' if is_veg else 'Meen Pollichathu with Kerala Red Matta Rice & Cabbage Thoran',
                    'macros': '🔥 560 kcal • 32g Protein • 72g Carbs • 16g Fat' if is_veg else '🔥 580 kcal • 46g Protein • 58g Carbs • 16g Fat',
                    'description': 'Red matta rice paired with vegetable avial in fresh curd, coconut ash-gourd olan, and pan-seared spiced fish in banana leaf wrap.',
                    'pro_tip': 'Kerala Matta rice contains 3x more magnesium and zinc than polished white rice.'
                },
                {
                    'slot': 'Evening Tiffin',
                    'dish': 'Pazham Puzhungiyathu (Steamed Nendran) with Tender Coconut Water' if not is_low_carb else 'Roasted Spicy Coconut Podi Paneer Cubes with Neer Mor',
                    'macros': '🔥 220 kcal • 6g Protein • 42g Carbs • 3g Fat' if not is_low_carb else '🔥 260 kcal • 18g Protein • 6g Carbs • 18g Fat',
                    'description': 'Naturally sweet steamed plantain or roasted coconut cubes paired with electrolyte-rich tender coconut water.',
                    'pro_tip': 'Natural potassium and enzymes relieve afternoon muscle fatigue before workout.'
                },
                {
                    'slot': 'Dinner',
                    'dish': 'Lace Appams with Stew (Vegetable or Chicken/Egg) & Coconut Milk',
                    'macros': '🔥 490 kcal • 34g Protein • 52g Carbs • 16g Fat' if not is_veg else '🔥 470 kcal • 22g Protein • 62g Carbs • 15g Fat',
                    'description': 'Fermented crispy-edged lace appams simmered with aromatic shallot, ginger, and curry leaf stew.',
                    'pro_tip': 'Fermented appam batter aids gut biome digestion before bedtime.'
                }
            ]
        },
        'tamil_nadu': {
            'title': 'Tamil Nadu Style Food',
            'tagline': 'Bold Pepper, Toor Dal Paruppu, Chettinad Spices & Calcium-Rich Millets',
            'icon': '🌶️',
            'highlight': 'Deep Focus • Tamil Nadu Cuisine',
            'color': '#ff4757',
            'why_today': 'Perfect balance of plant proteins from toor dal and sundal, black pepper for nutrient absorption (piperine), and iron-rich green keerai.',
            'meals': [
                {
                    'slot': 'Breakfast',
                    'dish': 'Mixed Dal Adai with Protein-Packed Avial' if is_veg else 'Kavil Idli / Ragi Idlis with Chettinad Egg Sambar',
                    'macros': '🔥 510 kcal • 28g Protein • 62g Carbs • 15g Fat' if is_veg else '🔥 490 kcal • 32g Protein • 56g Carbs • 14g Fat',
                    'description': 'Crisp multi-lentil crepes (chana, toor, moong dal) cooked with curry leaves and paired with homemade vegetable avial.',
                    'pro_tip': 'Combining 3 lentils delivers a complete amino acid profile without any processed protein powder.'
                },
                {
                    'slot': 'Lunch',
                    'dish': 'Tamil Nadu Paruppu Meals — Ponni Rice, Keerai Poriyal & Pepper Rasam' if is_veg else 'Chettinad Pepper Chicken Sukka with Brown Rice & Dal Kootu',
                    'macros': '🔥 560 kcal • 30g Protein • 76g Carbs • 14g Fat' if is_veg else '🔥 590 kcal • 48g Protein • 54g Carbs • 16g Fat',
                    'description': 'Traditional banana leaf spread: 1 cup Ponni rice, fresh spinach keerai poriyal, thick toor dal, and fiery milagu rasam.',
                    'pro_tip': 'Tamil pepper rasam improves gastric enzyme secretion and digestion.'
                },
                {
                    'slot': 'Evening Tiffin',
                    'dish': 'Kala Chana / Sprouted Moong Sundal with Filter Coffee',
                    'macros': '🔥 260 kcal • 14g Protein • 34g Carbs • 6g Fat',
                    'description': 'Spiced boiled chickpeas tossed with mustard, curry leaves, ginger, and fresh grated coconut alongside degree filter coffee.',
                    'pro_tip': 'Sundal is the ultimate zero-junk Tamil fitness snack—14g pure fiber & protein.'
                },
                {
                    'slot': 'Dinner',
                    'dish': 'Whole Wheat Chapati / Milagu Rasam Sadam with Paneer or Egg Podimas',
                    'macros': '🔥 490 kcal • 32g Protein • 52g Carbs • 15g Fat',
                    'description': 'Warm spiced scramble of 2 eggs or fresh paneer with shallots, crushed pepper, and warm phulkas or light rasam rice.',
                    'pro_tip': 'Light and anti-inflammatory pepper broth ensures restful sleep.'
                }
            ]
        },
        'north_indian': {
            'title': 'North Indian Style Food',
            'tagline': 'Hearty Whole-Wheat Rotis, Paneer Bhurji, Soya Chaap & Slow-Simmered Dals',
            'icon': '🌾',
            'highlight': 'Wholesome North Indian Option',
            'color': '#7c3aed',
            'why_today': 'Rich in complex wheat gluten fiber, dairy-based caseins (paneer & dahi), and legume proteins (rajma, chole, and yellow moong dal).',
            'meals': [
                {
                    'slot': 'Breakfast',
                    'dish': 'Paneer Bhurji with 2 Whole Wheat Phulkas' if is_veg else 'Spiced 3-Egg Bhurji with Multigrain Roti',
                    'macros': '🔥 480 kcal • 28g Protein • 44g Carbs • 20g Fat' if is_veg else '🔥 470 kcal • 32g Protein • 38g Carbs • 18g Fat',
                    'description': 'Fresh crumbled cottage cheese or eggs tossed with cumin, chopped onions, tomatoes, and fresh coriander, served with warm dry phulkas.',
                    'pro_tip': 'Paneer provides slow-digesting casein protein that curbs hunger for 4-5 hours.'
                },
                {
                    'slot': 'Lunch',
                    'dish': 'Punjabi Rajma Chawal with Cucumber Mint Raita' if is_veg else 'Tandoori Murgh / Chicken Curry with 2 Phulkas & Dal Tadka',
                    'macros': '🔥 540 kcal • 26g Protein • 78g Carbs • 12g Fat' if is_veg else '🔥 570 kcal • 46g Protein • 52g Carbs • 16g Fat',
                    'description': 'Slow-simmered red kidney beans in roasted ginger-garlic gravy served with steamed basmati rice and cooling dahi raita.',
                    'pro_tip': 'Rajma is packed with soluble fiber which stabilizes blood glucose spikes.'
                },
                {
                    'slot': 'Evening Tiffin',
                    'dish': 'Roasted Chana Chaat / Sprouted Chole with Green Chutney',
                    'macros': '🔥 240 kcal • 13g Protein • 34g Carbs • 5g Fat',
                    'description': 'Crunchy roasted chickpeas with diced tomatoes, onions, lemon juice, chaat masala, and mint-coriander chutney.',
                    'pro_tip': 'High in resistant starch, ideal pre-workout fuel.'
                },
                {
                    'slot': 'Dinner',
                    'dish': 'Yellow Moong Dal Tadka with Paneer Tikka & Phulka' if is_veg else 'Grilled Chicken Tikka with Dal Palak & 2 Phulkas',
                    'macros': '🔥 480 kcal • 30g Protein • 50g Carbs • 16g Fat' if is_veg else '🔥 510 kcal • 45g Protein • 42g Carbs • 15g Fat',
                    'description': 'Light yellow lentil soup tempered with cumin and garlic, paired with spiced grilled paneer or chicken and fresh spinach dal.',
                    'pro_tip': 'Moong dal is easiest on the stomach for night-time gut recovery.'
                }
            ]
        },
        'continental': {
            'title': 'Continental Style Food',
            'tagline': 'Mediterranean Grills, Baked Proteins, Fresh Salads & Whole Grain Pastas',
            'icon': '🍝',
            'highlight': 'Global Fusion • Continental Cuisine',
            'color': '#e17055',
            'why_today': 'Lean grilled proteins, olive oil-based healthy fats, complex carbs from whole grains, and micronutrient-dense salads for optimal recovery and performance.',
            'meals': [
                {
                    'slot': 'Breakfast',
                    'dish': 'Greek Yogurt Parfait with Granola, Berries & Honey' if is_veg else 'Herb Scrambled Eggs on Sourdough Toast with Avocado',
                    'macros': '🔥 460 kcal • 22g Protein • 54g Carbs • 16g Fat' if is_veg else '🔥 480 kcal • 30g Protein • 38g Carbs • 22g Fat',
                    'description': 'Creamy Greek yogurt layered with crunchy oat granola, mixed berries, and a drizzle of raw honey.' if is_veg else 'Farm-fresh scrambled eggs with fresh herbs, served on toasted sourdough with smashed avocado and cherry tomatoes.',
                    'pro_tip': 'Greek yogurt has 2x the protein of regular yogurt and supports gut health with probiotics.'
                },
                {
                    'slot': 'Lunch',
                    'dish': 'Mediterranean Quinoa Bowl with Grilled Halloumi & Hummus' if is_veg else 'Grilled Chicken Caesar Salad with Whole Wheat Croutons',
                    'macros': '🔥 540 kcal • 28g Protein • 62g Carbs • 18g Fat' if is_veg else '🔥 560 kcal • 46g Protein • 32g Carbs • 24g Fat',
                    'description': 'Fluffy quinoa tossed with roasted bell peppers, olives, cucumber, cherry tomatoes, and pan-seared halloumi cheese.' if is_veg else 'Crisp romaine lettuce with herb-marinated grilled chicken breast, shaved parmesan, and a light lemon-anchovy dressing.',
                    'pro_tip': 'Quinoa is a complete protein source with all 9 essential amino acids — rare for a plant food.'
                },
                {
                    'slot': 'Evening Snack',
                    'dish': 'Baked Sweet Potato Wedges with Tzatziki Dip' if not is_low_carb else 'Caprese Skewers with Balsamic Glaze & Mixed Nuts',
                    'macros': '🔥 230 kcal • 8g Protein • 38g Carbs • 5g Fat' if not is_low_carb else '🔥 250 kcal • 14g Protein • 8g Carbs • 18g Fat',
                    'description': 'Oven-baked crispy sweet potato wedges seasoned with rosemary and paprika, paired with cool cucumber-yogurt tzatziki.' if not is_low_carb else 'Fresh mozzarella, cherry tomatoes, and basil drizzled with aged balsamic alongside a handful of roasted almonds.',
                    'pro_tip': 'Sweet potatoes are rich in beta-carotene and provide sustained energy without blood sugar spikes.'
                },
                {
                    'slot': 'Dinner',
                    'dish': 'Whole Wheat Penne Arrabbiata with Grilled Zucchini & Parmesan' if is_veg else 'Pan-Seared Salmon Fillet with Roasted Vegetables & Brown Rice',
                    'macros': '🔥 490 kcal • 24g Protein • 64g Carbs • 14g Fat' if is_veg else '🔥 530 kcal • 42g Protein • 38g Carbs • 20g Fat',
                    'description': 'Al dente whole wheat penne in spicy tomato-garlic sauce with charred zucchini ribbons and fresh basil.' if is_veg else 'Omega-3 rich salmon seared to perfection with a medley of roasted Mediterranean vegetables and nutty brown rice.',
                    'pro_tip': 'Salmon provides 2g+ of omega-3 fatty acids per serving — essential for reducing workout inflammation.'
                }
            ]
        }
    }
    return data

