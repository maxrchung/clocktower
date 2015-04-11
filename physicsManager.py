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

def resolveIntersection(actor, other):
    # default to moving the actor up to resolve intersections
    increment = vector.Vector(0.0, 1.0)
    # if the actor has some velocity, move along the reverse velocity until it's
    # no longer intersecting with the other collider
    if actor.velocity.mag > 0.0:
        # normalized reverse of actor's velocity
        increment = actor.velocity.reverse().get_norm()
    # otherwise, check if the actor's mask is below the other's. If so, move down.
    elif actor.mask.centroid()[1] < other.mask.centroid()[1]:
        increment = vector.Vector(0.0, -1.0)
        
    # while actor's mask is inside other's mask, move it until it's not intersecting anymore
    while pygame.sprite.collide_mask(actor, other):
        actor.moveActor(increment.x, increment.y)
