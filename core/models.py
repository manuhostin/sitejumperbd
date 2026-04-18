from django.db import models

class Game(models.Model):
    game_id = models.IntegerField(unique=True, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Game #{self.game_id}"

    class Meta:
        ordering = ['-created_at']


class Like(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='likes')
    user_id = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('game', 'user_id')
        ordering = ['-created_at']

    def __str__(self):
        return f"Like on Game #{self.game.game_id}"


class Comment(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='comments')
    user_id = models.IntegerField(null=True, blank=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment on Game #{self.game.game_id}"


class View(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='views')
    user_id = models.IntegerField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"View on Game #{self.game.game_id}"