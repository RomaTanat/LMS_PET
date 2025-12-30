from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from .models import ShopItem, UserInventory, Achievement, UserAchievement, StudentProfile
from .gamification import purchase_item, check_achievement

User = get_user_model()

class GamificationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='gamer', password='password')
        # Profile is created via signal, get it
        self.profile = self.user.student_profile
        self.profile.coins = 1000
        self.profile.save()

        self.item = ShopItem.objects.create(
            name="Test Item",
            cost=500,
            item_type="THEME"
        )

        self.achievement = Achievement.objects.create(
            name="Sniper",
            criteria_type="sniper",
            criteria_value=1
        )

    def test_purchase_item_success(self):
        success, msg = purchase_item(self.user, self.item.id)
        self.assertTrue(success)
        # Refresh profile from db to get updated coins
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.coins, 500)
        self.assertTrue(UserInventory.objects.filter(student=self.profile, item=self.item).exists())

    def test_purchase_item_insufficient_funds(self):
        self.profile.coins = 100
        self.profile.save()
        success, msg = purchase_item(self.user, self.item.id)
        self.assertFalse(success)
        self.assertEqual(msg, "Недостаточно монет.")

    def test_achievement_logic(self):
        check_achievement(self.user, 'sniper', value=True)
        self.assertTrue(UserAchievement.objects.filter(user=self.user, achievement=self.achievement, progress=100).exists())

    def test_shop_view(self):
        client = Client()
        client.login(username='gamer', password='password')
        response = client.get('/shop/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Item")
