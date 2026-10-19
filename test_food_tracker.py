import unittest
from datetime import date, timedelta
from app import create_app, db
from app.models import User, FoodLog, UserDietPlan
from app.services.food_database import search_foods, get_food_by_id, COMMON_FOODS

class TestFoodTracker(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()

        # Find or create a test user
        self.user = User.query.filter_by(username='test_food_user').first()
        if not self.user:
            self.user = User(
                username='test_food_user',
                email='test_food@fitrack.local',
                weight_kg=72.0,
                height_cm=175.0,
                age=26,
                gender='male',
                goal='maintaining',
                role='athlete'
            )
            self.user.set_password('password123')
            db.session.add(self.user)
            db.session.commit()

        # Clean existing food logs for this test user
        FoodLog.query.filter_by(user_id=self.user.id).delete()
        db.session.commit()

    def tearDown(self):
        FoodLog.query.filter_by(user_id=self.user.id).delete()
        db.session.commit()
        self.ctx.pop()

    def test_preset_food_database(self):
        self.assertGreater(len(COMMON_FOODS), 30)
        
        # Test search
        egg_results = search_foods('egg')
        self.assertTrue(any('Egg' in f['name'] for f in egg_results))

        # Test category filter
        protein_results = search_foods('', category='high_protein')
        self.assertTrue(len(protein_results) > 0)
        self.assertTrue(all(f['category'] == 'high_protein' for f in protein_results))

        # Test get_food_by_id
        food = get_food_by_id('egg_boiled')
        self.assertIsNotNone(food)
        self.assertEqual(food['calories'], 78)
        self.assertEqual(food['protein'], 6.3)

    def test_food_summary_calculation(self):
        today = date.today()
        # Add breakfast item: 2 boiled eggs (78*2 = 156 kcal, 6.3*2 = 12.6g protein)
        log1 = FoodLog(
            user_id=self.user.id,
            date=today,
            meal_type='breakfast',
            food_name='Boiled Egg (Large)',
            serving_size='1 egg (50g)',
            quantity=2.0,
            calories=156.0,
            protein=12.6,
            carbs=1.2,
            fat=10.6
        )
        # Add lunch item: Grilled chicken breast (165 kcal, 31g protein)
        log2 = FoodLog(
            user_id=self.user.id,
            date=today,
            meal_type='lunch',
            food_name='Grilled Chicken Breast',
            serving_size='100g cooked',
            quantity=1.0,
            calories=165.0,
            protein=31.0,
            carbs=0.0,
            fat=3.6
        )
        db.session.add_all([log1, log2])
        db.session.commit()

        summary = self.user.get_daily_food_summary(today)
        self.assertEqual(summary['total_calories'], 321)
        self.assertEqual(summary['total_protein'], 43.6)
        self.assertEqual(len(summary['meals']['breakfast']['food_items']), 1)
        self.assertEqual(len(summary['meals']['lunch']['food_items']), 1)
        self.assertEqual(len(summary['meals']['dinner']['food_items']), 0)
        self.assertGreater(summary['calorie_target'], 0)
        self.assertGreater(summary['protein_target'], 0)
        self.assertGreater(summary['remaining_calories'], 0)
        self.assertGreater(summary['remaining_protein'], 0)

    def test_routes_add_and_delete(self):
        # Login
        with self.client:
            self.client.post('/login', data={'email': 'test_food@fitrack.local', 'password': 'password123'})
            
            # Post new food log
            res = self.client.post('/diet/food-log/add', data={
                'food_name': 'Paneer Bhurji',
                'meal_type': 'dinner',
                'serving_size': '1 bowl',
                'quantity': '1.0',
                'calories': '275',
                'protein': '16.5',
                'carbs': '7',
                'fat': '20',
                'date': date.today().strftime('%Y-%m-%d'),
                'is_per_unit': 'false'
            }, follow_redirects=True)
            self.assertEqual(res.status_code, 200)

            # Check it exists in database
            log = FoodLog.query.filter_by(user_id=self.user.id, food_name='Paneer Bhurji').first()
            self.assertIsNotNone(log)
            self.assertEqual(log.calories, 275.0)
            self.assertEqual(log.protein, 16.5)

            # Test delete
            del_res = self.client.post(f'/diet/food-log/delete/{log.id}', follow_redirects=True)
            self.assertEqual(del_res.status_code, 200)
            log_after = FoodLog.query.get(log.id)
            self.assertIsNone(log_after)

    def test_api_foods_endpoint(self):
        with self.client:
            self.client.post('/login', data={'email': 'test_food@fitrack.local', 'password': 'password123'})
            res = self.client.get('/diet/api/foods?q=dosa')
            self.assertEqual(res.status_code, 200)
            data = res.get_json()
            self.assertIn('foods', data)
            self.assertTrue(any('dosa' in f['name'].lower() for f in data['foods']))

    def test_diet_page_renders_with_tracker(self):
        with self.client:
            self.client.post('/login', data={'email': 'test_food@fitrack.local', 'password': 'password123'})
            res = self.client.get('/diet/')
            self.assertEqual(res.status_code, 200)
            self.assertIn(b'Daily Food Tracker', res.data)
            self.assertIn(b'Calories Consumed', res.data)
            self.assertIn(b'Protein Consumed', res.data)
            self.assertIn(b'Add What You Eat', res.data)

    def test_dashboard_renders_with_tracker(self):
        with self.client:
            self.client.post('/login', data={'email': 'test_food@fitrack.local', 'password': 'password123'})
            res = self.client.get('/dashboard')
            self.assertEqual(res.status_code, 200)
            self.assertIn(b'Food &amp; Nutrition', res.data)
            self.assertIn(b'Workout Tracker', res.data)

if __name__ == '__main__':
    unittest.main()
