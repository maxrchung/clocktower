import pygame
import vector
from pygame.locals import *

# returns all actors in a given group that collided with the given actor
# each actor is mapped to the point of collision
def checkCollisionAgainstGroup(actor, group):
    # check preliminary collision against group. get list of colliding sprites.
    collision = pygame.sprite.spritecollide(actor, group, False)
    # if collision occurred, do a mask check against the sprites it collided with
    maskCollided = {}
    for collider in collision:
        # if there was a collision point on the mask, put it in the return list
        collisionPoint = pygame.sprite.collide_mask(collider, actor)
        if collisionPoint:
            maskCollided[collider] = collisionPoint
    return maskCollided

def resolveIntersection(actor, colliders):
    # get the direction to move the actor out of the colliders
    increment = vector.Vector(0.0, 0.0)
    actorVec = vector.Vector(actor.mask.centroid()[0], actor.mask.centroid()[1])
    for collider in colliders:
        colliderVec = vector.Vector(collider.mask.centroid()[0], collider.mask.centroid()[1])
        increment += actorVec - colliderVec
    increment = increment.get_norm()
    # while the actor is colliding, move it until it isn't colliding
    if increment.mag == 0:
        increment = vector.Vector(0.0, 1.0)
    colliding = True
    while colliding:
        stillColliding = False
        for collider in colliders:
            if pygame.sprite.collide_mask(collider, actor):
                stillColliding = True
        if stillColliding:
            actor.moveActor(increment.x, increment.y)
        else:
            colliding = False
