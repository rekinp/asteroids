from bullet import Bullet

class CollisionController:
    @staticmethod
    def detect_asteroid_bullet_collisions(asteroids, bullets):
        asteroids_that_were_hit = []
        bullets_that_hit_asteroids = []
        asteroids_hit = 0
        for b in bullets:
            asteroids_hit_by_bullet = CollisionController.find_asteroids_hit_by_bullet(asteroids, b)
            if asteroids_hit_by_bullet:
                asteroids_that_were_hit.extend(asteroids_hit_by_bullet)
            if len(asteroids_that_were_hit) > asteroids_hit:
                bullets_that_hit_asteroids.append(b)
                asteroids_hit += len(asteroids_hit_by_bullet)
        return asteroids_that_were_hit, bullets_that_hit_asteroids

    @staticmethod
    def find_asteroids_hit_by_bullet(asteroids, bullet: Bullet):
        asteroids_that_were_hit = []
        for asteroid in asteroids:
            if asteroid.hitbox.colliderect(bullet.rect):
                asteroids_that_were_hit.append(asteroid)
        return asteroids_that_were_hit
