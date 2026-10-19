import unittest
from datetime import date, timedelta
from app import create_app, db
from app.models import User, WorkoutLog, LiftLog
from app.services.workout_database import search_exercises, get_exercise_by_id, COMMON_EXERCISES, WORKOUT_CATEGORIES

class TestWorkoutTracker(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()

        # Find or create test user
        self.user = User.query.filter_by(username='test_workout_user').first()
        if not self.user:
            self.user = User(
                username='test_workout_user',
                email='test_workout@fitrack.local',
                weight_kg=75.0,
                height_cm=178.0,
                age=28,
                gender='male',
                goal='bulking',
                role='bodybuilder'
            )
            self.user.set_password('password123')
            db.session.add(self.user)
            db.session.commit()

        # Clean existing workout & lift logs for this test user
        WorkoutLog.query.filter_by(user_id=self.user.id).delete()
        LiftLog.query.filter_by(user_id=self.user.id).delete()
        db.session.commit()

    def tearDown(self):
        WorkoutLog.query.filter_by(user_id=self.user.id).delete()
        LiftLog.query.filter_by(user_id=self.user.id).delete()
        db.session.commit()
        self.ctx.pop()

    def test_preset_exercise_database(self):
        self.assertGreater(len(COMMON_EXERCISES), 20)
        self.assertGreater(len(WORKOUT_CATEGORIES), 5)

        # Search for bench press
        bench_results = search_exercises('bench')
        self.assertTrue(any('Bench Press' in e['name'] for e in bench_results))

        # Search by category
        chest_results = search_exercises('', category='chest')
        self.assertTrue(len(chest_results) > 0)
        self.assertTrue(all(e['category'] == 'chest' for e in chest_results))

        # Get by ID
        squat = get_exercise_by_id('barbell_back_squat')
        self.assertIsNotNone(squat)
        self.assertEqual(squat['category'], 'legs')
        self.assertTrue(squat['is_compound'])

    def test_progressive_overload_calculation(self):
        # Compound movement in kg: 50kg -> 55kg
        target = WorkoutLog.calculate_next_target(50.0, 'kg', 'Barbell Bench Press')
        self.assertEqual(target, 55.0)

        # Compound movement in lbs: 100 lbs -> 110 lbs
        target_lbs = WorkoutLog.calculate_next_target(100.0, 'lbs', 'Barbell Squat')
        self.assertEqual(target_lbs, 110.0)

        # Isolation movement in kg: 15kg -> 17.5kg
        target_iso = WorkoutLog.calculate_next_target(15.0, 'kg', 'Bicep Curl')
        self.assertEqual(target_iso, 17.5)

    def test_workout_summary_calculation(self):
        today = date.today()
        # Add a chest log: 3 sets * 10 reps @ 60kg = 1800kg volume
        log1 = WorkoutLog(
            user_id=self.user.id,
            date=today,
            category='chest',
            exercise_name='Barbell Bench Press',
            sets=3,
            reps=10,
            weight=60.0,
            unit='kg',
            target_next_weight=65.0,
            is_custom=False
        )
        # Add a custom workout log: 4 sets * 12 reps @ 25kg = 1200kg volume
        log2 = WorkoutLog(
            user_id=self.user.id,
            date=today,
            category='custom',
            exercise_name='Custom Incline Hex Press',
            sets=4,
            reps=12,
            weight=25.0,
            unit='kg',
            duration_mins=20,
            target_next_weight=27.5,
            notes='Felt strong',
            is_custom=True
        )
        db.session.add_all([log1, log2])
        db.session.commit()

        summary = self.user.get_daily_workout_summary(today)
        self.assertEqual(summary['total_exercises'], 2)
        self.assertEqual(summary['total_sets'], 7)
        self.assertEqual(summary['total_volume'], 3000.0)
        self.assertEqual(summary['total_duration'], 20)
        self.assertTrue(summary['has_workouts'])

        # Check category grouping
        self.assertEqual(len(summary['categories']['chest']['exercises']), 1)
        self.assertEqual(summary['categories']['chest']['total_sets'], 3)
        self.assertEqual(summary['categories']['chest']['total_volume'], 1800.0)

        self.assertEqual(len(summary['categories']['custom']['exercises']), 1)
        self.assertEqual(summary['categories']['custom']['total_sets'], 4)
        self.assertEqual(summary['categories']['custom']['total_volume'], 1200.0)

        self.assertEqual(len(summary['categories']['legs']['exercises']), 0)

    def test_routes_add_custom_and_delete(self):
        with self.client:
            # Login
            self.client.post('/login', data={'email': 'test_workout@fitrack.local', 'password': 'password123'})

            # Add custom workout via POST
            res = self.client.post('/workouts/log/add', data={
                'custom_exercise': 'Dips with +15kg Belt',
                'category': 'chest',
                'sets': '3',
                'reps': '10',
                'weight': '15',
                'unit': 'kg',
                'duration_mins': '15',
                'notes': 'New personal best',
                'date': date.today().strftime('%Y-%m-%d'),
                'is_custom': 'true'
            }, follow_redirects=True)
            self.assertEqual(res.status_code, 200)

            # Verify in DB
            log = WorkoutLog.query.filter_by(user_id=self.user.id, exercise_name='Dips with +15kg Belt').first()
            self.assertIsNotNone(log)
            self.assertEqual(log.sets, 3)
            self.assertEqual(log.weight, 15.0)
            self.assertTrue(log.is_custom)
            self.assertEqual(log.target_next_weight, 20.0)  # compound dips increment 5kg

            # Delete log
            del_res = self.client.post(f'/workouts/log/delete/{log.id}', follow_redirects=True)
            self.assertEqual(del_res.status_code, 200)
            self.assertIsNone(WorkoutLog.query.get(log.id))

    def test_quick_add_route(self):
        with self.client:
            self.client.post('/login', data={'email': 'test_workout@fitrack.local', 'password': 'password123'})

            res = self.client.post('/workouts/log/quick-add', data={
                'exercise_name': 'Barbell Back Squat',
                'category': 'legs',
                'sets': '4',
                'reps': '8',
                'weight': '70',
                'unit': 'kg',
                'date': date.today().strftime('%Y-%m-%d')
            }, follow_redirects=True)
            self.assertEqual(res.status_code, 200)

            log = WorkoutLog.query.filter_by(user_id=self.user.id, exercise_name='Barbell Back Squat').first()
            self.assertIsNotNone(log)
            self.assertEqual(log.category, 'legs')
            self.assertEqual(log.weight, 70.0)

    def test_api_exercises_endpoint(self):
        with self.client:
            self.client.post('/login', data={'email': 'test_workout@fitrack.local', 'password': 'password123'})
            res = self.client.get('/workouts/api/exercises?q=bench')
            self.assertEqual(res.status_code, 200)
            data = res.get_json()
            self.assertIn('exercises', data)
            self.assertTrue(any('bench' in e['name'].lower() for e in data['exercises']))

    def test_workouts_and_dashboard_pages_render(self):
        with self.client:
            self.client.post('/login', data={'email': 'test_workout@fitrack.local', 'password': 'password123'})

            # Check /workouts/
            workout_res = self.client.get('/workouts/')
            self.assertEqual(workout_res.status_code, 200)
            self.assertIn(b'Daily Workout Tracker', workout_res.data)
            self.assertIn(b'Total Volume', workout_res.data)
            self.assertIn(b'Workouts by Category', workout_res.data)

            # Check /dashboard
            dash_res = self.client.get('/dashboard')
            self.assertEqual(dash_res.status_code, 200)
            self.assertIn(b'Workout Tracker', dash_res.data)

if __name__ == '__main__':
    unittest.main()
