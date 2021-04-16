"""
    domonic.particles
    ====================================
    fun stuff

"""

from domonic.javascript import *


class Particle():

    def __init__(self, size=1):
        self.x=0
        self.y=0
        self.width=size
        self.height=size
        self.rotation=0
        self.vx=0
        self.vy=0
        self.damp=0.9
        self.bounce=-0.5
        self.grav=0
        self.wander=0
        self._k=0.2
        self.edges="wrap"
        self._drag=False
        self._oldx=None
        self._oldy=None
        self._turnToPath=False
        self._bounds = {}
        self.set_bounds( {'xMin':0, 'yMin':0, 'yMax': 800, 'xMax': 800} )
        self.maxSpeed = Number.MAX_VALUE

    def set_bounds( self, oBounds ):
        self._bounds['top'] = oBounds['yMin']
        self._bounds['bottom'] = oBounds['yMax']
        self._bounds['left'] = oBounds['xMin']
        self._bounds['right'] = oBounds['xMax']

    def turnToPath( self, bTurn ):
        self._turnToPath = bTurn

    def update( self ):
        if self._drag:
            self.vx = self.x - self._oldx
            self.vy = self.y - self._oldy
            self._oldx = self.x
            self._oldy = self.y

        else:
            self.vx += Math.random() * self.wander - self.wander / 2
            self.vy += Math.random() * self.wander - self.wander / 2
            self.vy += self.grav
            self.vx *= self.damp
            self.vy *= self.damp

            speed = Math.sqrt(self.vx * self.vx + self.vy * self.vy)
            if speed > self.maxSpeed:
                self.vx = self.maxSpeed * self.vx / speed
                self.vy = self.maxSpeed * self.vy / speed

            if self._turnToPath:
                self.rotation = Math.atan2(self.vy, self.vx)

            self.x += self.vx
            self.y += self.vy
            if self.edges == "wrap":
                if self.x > (self._bounds['right'] + self.width/2):
                    self.x = self._bounds['left'] - self.width/2
                elif self.x<self._bounds['left'] - self.width/2:
                    self.x = self._bounds['right'] + self.width/2

                if( self.y > self._bounds['bottom'] + self.height/2):
                    self.y = self._bounds['top'] - self.height/2
                elif (self.y<self._bounds['top'] - self.height/2):
                    self.y = self._bounds['bottom'] + self.height/2

            elif self.edges == "bounce":
                if self.x > (self._bounds['right'] - self.width/2):                   
                    self.x = self._bounds['right'] - self.width/2
                    self.vx *= self.bounce
                elif self.x<(self._bounds['left'] + self.width/2):
                    self.x = self._bounds['left'] + self.width/2
                    self.vx *= self.bounce

                if self.y >(self._bounds['bottom'] - self.height/2):                                 
                    self.y = self._bounds['bottom'] - self.height/2
                    self.vy *= self.bounce
                elif self.y<(self._bounds['top'] + self.height/2):
                    self.y = self._bounds['top'] + self.height/2
                    self.vy *= self.bounce

            # else if self.edges == "remove":
            #     if( self.x > self._bounds.right + self.width/2 || self.x<self._bounds.left - self.width/2 ||
            #        self.y > self._bounds.bottom + self.height/2 || self.y<self._bounds.top - self.height/2){
        
        if Global.isNaN(self.x):
            self.x=self.y=self.vx=self.vy=0




class Particle3D():

    def __init__(self,  size=1):
        self.x=0
        self.y=0
        self.z=0
        self.width=size
        self.height=size
        self.length=size
        self.rotation=0
        self.vx=0
        self.vy=0
        self.vz=0
        self.damp=0.9
        self.bounce=-0.5
        self.grav=0
        self.wander=0
        self._k=0.2
        self.edges="wrap"
        self._drag=False
        self._oldx=None
        self._oldy=None
        self._oldz=None
        self._turnToPath=False
        self._bounds = {}
        self.set_bounds( {'xMin':0, 'yMin':0, 'yMax': 800, 'xMax': 800} )
        self.maxSpeed = Number.MAX_VALUE

    def set_bounds( self, oBounds ):
        self._bounds['top'] = oBounds['yMin']
        self._bounds['bottom'] = oBounds['yMax']
        self._bounds['left'] = oBounds['xMin']
        self._bounds['right'] = oBounds['xMax']

    def turnToPath( self, bTurn ):
        self._turnToPath = bTurn

    def update( self ):
        if self._drag:
            self.vx = self.x - self._oldx
            self.vy = self.y - self._oldy
            self.vz = self.z - self._oldz
            self._oldx = self.x
            self._oldy = self.y
            self._oldz = self.z

        else:
            self.vx += Math.random() * self.wander - self.wander / 2
            self.vy += Math.random() * self.wander - self.wander / 2
            self.vz += Math.random() * self.wander - self.wander / 2
            self.vy += self.grav
            self.vx *= self.damp
            self.vy *= self.damp
            self.vz *= self.damp

            speed = Math.sqrt(self.vx * self.vx + self.vy * self.vy + self.vz * self.vz)
            if speed > self.maxSpeed:
                self.vx = self.maxSpeed * self.vx / speed
                self.vy = self.maxSpeed * self.vy / speed
                self.vz = self.maxSpeed * self.vz / speed

            if self._turnToPath:
                self.rotation = Math.atan2(self.vy, self.vx)

            self.x += self.vx
            self.y += self.vy
            self.z += self.vz

            if self.edges == "wrap":
                if self.x > (self._bounds['right'] + self.width/2):
                    self.x = self._bounds['left'] - self.width/2
                elif self.x<self._bounds['left'] - self.width/2:
                    self.x = self._bounds['right'] + self.width/2

                if( self.y > self._bounds['bottom'] + self.height/2):
                    self.y = self._bounds['top'] - self.height/2
                elif (self.y<self._bounds['top'] - self.height/2):
                    self.y = self._bounds['bottom'] + self.height/2

            elif self.edges == "bounce":
                if self.x > (self._bounds['right'] - self.width/2):                   
                    self.x = self._bounds['right'] - self.width/2
                    self.vx *= self.bounce
                elif self.x<(self._bounds['left'] + self.width/2):
                    self.x = self._bounds['left'] + self.width/2
                    self.vx *= self.bounce

                if self.y >(self._bounds['bottom'] - self.height/2):                                 
                    self.y = self._bounds['bottom'] - self.height/2
                    self.vy *= self.bounce
                elif self.y<(self._bounds['top'] + self.height/2):
                    self.y = self._bounds['top'] + self.height/2
                    self.vy *= self.bounce

            # else if self.edges == "remove":
            #     if( self.x > self._bounds.right + self.width/2 || self.x<self._bounds.left - self.width/2 ||
            #        self.y > self._bounds.bottom + self.height/2 || self.y<self._bounds.top - self.height/2){
        
        if Global.isNaN(self.x):
            self.x=self.y=self.vx=self.vy=0

