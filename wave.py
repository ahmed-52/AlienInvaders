"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in
the Alien Invaders game.  Instances of Wave represent a single wave. Whenever
you move to a new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on
screen. These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or
models.py. Whether a helper method belongs in this module or models.py is
often a complicated issue.  If you do not know, ask on Piazza and we will
answer.

# Ahmed Abdulla (aaa384), Harvey Zhu(hz639) 
# Dec 5 2023
"""
from game2d import *
from consts import *
from models import *
import random

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.

    This subcontroller has a reference to the ship, aliens, and any laser bolts
    on screen. It animates the laser bolts, removing any aliens as necessary.
    It also marches the aliens back and forth across the screen until they are
    all destroyed or they reach the defense line (at which point the player
    loses). When the wave is complete, you  should create a NEW instance of
    Wave (in Invaders) if you want to make a new wave of aliens.

    If you want to pause the game, tell this controller to draw, but do not
    update.  See subcontrollers.py from Lecture 24 for an example.  This
    class will be similar to than one in how it interacts with the main class
    Invaders.

    All of the attributes of this class ar to be hidden. You may find that
    you want to access an attribute in class Invaders. It is okay if you do,
    but you MAY NOT ACCESS THE ATTRIBUTES DIRECTLY. You must use a getter
    and/or setter for any attribute that you need to access in Invaders.
    Only add the getters and setters that you need for Invaders. You can keep
    everything else hidden.

    """
    # HIDDEN ATTRIBUTES:
    # Attribute _ship: the player ship to control
    # Invariant: _ship is a Ship object or None
    #
    # Attribute _aliens: the 2d list of aliens in the wave
    # Invariant: _aliens is a rectangular 2d list containing Alien objects or
    #            None
    #
    # Attribute _bolts: the laser bolts currently on screen
    # Invariant: _bolts is a list of Bolt objects, possibly empty
    #
    # Attribute _dline: the defensive line being protected
    # Invariant : _dline is a GPath object
    #
    # Attribute _lives: the number of lives left
    # Invariant: _lives is an int >= 0

    # Attribute _heart: List of heart images representing player lives
    # Invariant: _heart is a list of GImage objects, length corresponds to
    #           _lives

    # Attribute _time: the amount of time since the last Alien "step"
    # Invariant: _time is a float >= 0s

    # Attribute _hit: True if the ship had been hit
    # Invariant : _hit is a boolean expression

    # Attribute _score: Tracks the player's score
    # Invariant: _score is an integer greater than or equal to 0

    # Attribute _scoreBoard: Displays the current player score
    # Invariant: _scoreBoard is a GLabel object

    # Attribute _step is number of steps
    #Invariant : _step is an int >= 0, can be rest to 0

    # Attribute _random: Randomly determined interval for alien bolt firing
    # Invariant: _random is an integer within a specified range (1 to BOLT_RATE)

    # Attribute _switch: Controls the direction of alien movement
    # Invariant: _switch is a boolean that dictates alien horizontal movement;
    #            it's toggled internally.

    # Attribute _alien_speed: the current speed which the aliens go
    # Invariant: _alien_speed is a float or int > 0

    # Attribute _boss_alien: the boss alien object in the wave
    # Invariant: _boss_alien is a BossAlien object or None

    # Attribute _boss_switch: a flag to control the horizontal movement direction of the boss alien
    # Invariant: _boss_switch is a boolean

    # Attribute _boss_speed: the speed at which the boss alien moves horizontally
    # Invariant: _boss_speed is a float or int > 0, representing the time between steps

    # Attribute _boss_time: the amount of time since the last boss alien "step" or movement
    # Invariant: _boss_time is a float >= 0

    # Attribute _boss_shoot_time: the amount of time since the boss alien last shot a bolt
    # Invariant: _boss_shoot_time is a float >= 0

    # Attribute _boss_bolt_count: the number of bolts shot in the current shooting sequence by the boss alien
    # Invariant: _boss_bolt_count is an int >= 0, reset after reaching a certain number of shots



    def getShip(self):
        """Returns the current instance of the ship object."""
        return self._ship


    def getAliens(self):
        """Returns the list of alien objects currently in the game."""
        return self._aliens


    def getBolts(self):
        """Returns the list of bolt objects present in the game at the current moment."""
        return self._bolts


    def getDline(self):
        """Returns the defense line object in the game."""
        return self._dline


    def getLives(self):
        """Returns the current number of lives remaining in the game."""
        return self._lives


    def getTime(self):
        """Returns the amount of time since the last Alien "step"."""
        return self._time


    def getStep(self):
        """Returns the amount of steps taken since its last shot"""
        return self._step


    def getHit(self):
        """Returns whether the ship has been hit"""
        return self._hit


    def setHit(self,value):
        """
        Sets whether the ship has been hit

        Parameter value: whether the ship has been hit
        Precondition: value is a boolean
        """
        assert isinstance(value,bool), "value is not a boolean"

        self._hit = value


    def getScoreBoard(self):
        """Returns the current score of the game"""
        return self._scoreBoard


    def getHearts(self):
        """Returns the amount of hearts the player has"""
        return self._heart


    def __init__(self):
        """
        Initializes a new instance of the Wave class.

        This method sets up the initial state of the wave, including creating the
        ship, aliens, the defense line, and initializing other gameplay elements like
        the score, lives, and time. It prepares the wave for the start of the game or
        a new level.
        """
        self._aliens = self.createAlien()
        self._ship = Ship(GAME_WIDTH/2, SHIP_BOTTOM + SHIP_HEIGHT/2,"ship.png")
        self._dline = GPath(points=[0, DEFENSE_LINE, GAME_WIDTH, DEFENSE_LINE],
                        linewidth=2, linecolor='white')
        self._bolts = []
        self._boss_alien = None
        self._time = 0
        self._step = 0
        self._switch = True
        self._hit = False
        self._lives = SHIP_LIVES
        self._random = random.randint(1,BOLT_RATE)
        self._score  = 0
        self._scoreBoard = GLabel(text="Score: "+str(self._score),font_size=35,
                                    x = 650, y = 650, font_name = 'Arcade.ttf',
                                            fillcolor=None,linecolor='white')
        self._heart= self.hearts()
        self._alien_speed = ALIEN_SPEED
        self._boss_alien = None
        self._boss_switch = True  
        self._boss_speed = BOSS_ALIEN_SPEED  
        self._boss_time = 0
        self._boss_shoot_time = 0 
        self._boss_bolt_count = 0 


    def createAlien(self):
        """
        Creates and initializes a 2-Dimensional list of Alien objects
        for the game.

        Each row of aliens is created based on constants such
        as the ALIEN_ROWS, the separation between aliens, and their initial
        positions. The function cycles through a set of 3 alien images.

        Returns:
            A 2-D list where each inner list contains Alien objects,
            representing a row of aliens in the game.
        """
        final=[]
        y = GAME_HEIGHT - ALIEN_CEILING - ALIEN_HEIGHT/2
        for i in range(ALIEN_ROWS):
            k = int(float(i)/2)
            source = ALIEN_IMAGES[k % len(ALIEN_IMAGES)]
            x = ALIEN_H_SEP + ALIEN_WIDTH/2
            row = []
            for j in range(ALIENS_IN_ROW):
                row.append(Alien(x,y,source))
                x = x + ALIEN_H_SEP + ALIEN_WIDTH
            y = y - ALIEN_V_SEP - ALIEN_HEIGHT
            final.append(row)
        return final


    def update(self,input,dt):
        """
        Updates ship and alien movements in the Wave subcontroller each animation frame.

        Handles ship movements based on left or right keyboard inputs and
        progresses alien movements based on elapsed time. This method must be called from
        the update method of the Invaders controller. It uses the 'input' argument,
        an instance of GInput, to read keyboard inputs since Wave cannot directly
        access Invaders' attributes.

        Parameter input: GInput instance to check keyboard states for ship control.
        Precondition: 'input' should have a method is_key_down with a string key argument.

        Parameter dt: Elapsed time since last update, for alien movement progression.
        Precondition: 'dt' is a non-negative float representing time in seconds.
        """
        assert isinstance(input, GInput), "input is not a GInput type"
        assert isinstance(dt, float) and dt > 0
        if input.is_key_down('right'):
            self._ship.MoveRight()
        if input.is_key_down('left'):
            self._ship.MoveLeft()
        if input.is_key_down('up'):
            if not self.CheckIfPlayer():
                self._bolts.append(Bolt(x = self._ship.getXPosition(), 
                    y = SHIP_BOTTOM +
                    SHIP_HEIGHT + BOLT_HEIGHT/2, velocity = BOLT_SPEED))
        if self._step == self._random:
            self.AlienFire()
        self._scoreBoard.text = "Score: "+ str(self._score)
        if self.AlienExists():
            self.AlienMovement(dt)
        self.BoltLoop()
        self.AlienCollison()
        self.ShipCollison()
        if not self.AlienExists() and not self._boss_alien:
            self._PreBossTitle = True
            self._boss_alien = self.createBossAlien()
        if self._boss_alien:
            self.BossAlienMovement(dt)
            self.BossAlienCollision()
            self.BossAlienShoot(dt) 


    def AlienMovement(self,dt):
        """
        Manages the movement of aliens in the game.

        This function updates the position of each alien based on the elapsed
        time (dt). It determines the direction of the alien wave (left, right,
        or down) based on the positions of the aliens at the extremes
        (determined by the Extreme function) and adjusts their positions
        accordingly.

        Parameter dt: The time elapsed since the last update
        Precondition: dt is a non-negative float
        """
        assert isinstance(dt,float)
        assert dt > 0

        max = self.ExtremeX()[0]
        min = self.ExtremeX()[1]

        self._time += dt

        if self._time > self._alien_speed:

            self._step += 1
            self._time = 0

            if self._switch:
                if max + ALIEN_H_WALK + ALIEN_WIDTH/2 < GAME_WIDTH:
                    self.ALoopRight()
                else:
                    self.ALoopDown()
                    self._switch = False
            else:
                if min - ALIEN_H_WALK - ALIEN_WIDTH/2 > 0:
                    self.ALoopLeft()
                else:
                    self.ALoopDown()
                    self._switch = True


    def ExtremeX(self):
        """
        Finds the extreme horizontal positions
        of the alien wave.

        This function iterates through all the aliens and identifies the
        maximum and minimum x-coordinates. These coordinates are used to
        determine the movement boundaries of the alien wave in the
        AlienMovement function.

        Returns a tuple where the first element is
        the maximum x-coordinate and the
        second element is the minimum x-coordinate
        of the aliens.
        """
        xlist = []
        for row in self._aliens:
            for alien in row:
                if alien != None:
                    xlist.append(alien.getX())
        return (max(xlist),min(xlist))


    def ExtremeY(self):
        """
        Determines if any alien has reached the defense line.
        This function checks if the y-coordinate of any alien is at or below the
        defense line. It is used to determine if the game is lost.

        Returns:
        True if any alien has reached the defense line, False otherwise.
        """

        if self._boss_alien == None:
            for row in self._aliens:
                for alien in row:
                    if alien != None:
                        if (alien.getY() - ALIEN_HEIGHT/2) <= DEFENSE_LINE:
                            return True
        else:
            if (self._boss_alien.getY() - ALIEN_HEIGHT/2) <= DEFENSE_LINE:
                return True


    def ALoopRight(self):
        """
        Moves all aliens in the wave to the right.

        This function iterates through each alien in the wave and calls the AlienRight
        method on each alien to move them to the right.
        """

        for row in self._aliens:
            for alien in row:
                if alien != None:
                    alien.AlienRight()

    def ALoopLeft(self):
        """
        Moves all aliens in the wave to the left.

        This function iterates through each alien in the wave and calls the
        AlienLeft method on each alien to move them to the left.
        """
        for row in self._aliens:
            for alien in row:
                if alien != None:
                    alien.AlienLeft()


    def ALoopDown(self):
        """
        Moves all aliens in the wave downwards.

        This function iterates through each alien in the wave and calls the
        AlienDown method on each alien to move them downward.
        """
        for row in self._aliens:
            for alien in row:
                if alien != None:
                    alien.AlienDown()


    def AlienFire(self):
        """
        Handles the firing action of an alien.

        This function randomly selects an alien to fire a bolt. It updates the
        bolts list with the new bolt from the selected alien.

        Postcondition:
        Adds a new Bolt object to the _bolts list if an alien fires.
        """
        alien = self.ChooseAlien()
        if alien != None:
            self._bolts.append(Bolt(x = alien.getX(), y = alien.getY() -
                ALIEN_HEIGHT/2 - BOLT_HEIGHT/2, velocity = -BOLT_SPEED))
            self._step = 0
            self._random = random.randint(1,BOLT_RATE)


    def ChooseAlien(self):
        """
        Randomly selects an alien from the bottom-most row for firing.

        This method picks a random column and then selects the bottom-most alien
        in that column that is not None (i.e., an alien that exists).

        Returns:
            An Alien object that will fire a bolt, or None if no aliens are present.
        """
        list = self.FindNotNone()
        pick = random.randint(0,len(list)-1)
        for row in range(len(self._aliens)-1,-1,-1):
            if self._aliens[row][pick] != None:
                return self._aliens[row][pick]


    def AlienCollison(self):
        """
        Checks and handles collisions between alien ships and player bolts.

        This method iterates through each bolt in _bolts and each alien in _aliens.
        If a collision is detected between a bolt and an alien (using the collides method
        of the Alien class), the bolt is removed from _bolts, the score is updated using
        the ScoreChanger method, and the alien is set to None to indicate its destruction.

        """
        alien_hit = False
        for bolt in self._bolts:
            for row in self._aliens:
                for alien in row:
                    if alien != None:
                        if alien.collides(bolt):
                            self._bolts.remove(bolt)
                            self.ScoreChanger(alien)
                            self._aliens[self._aliens.index(row)]\
                            [row.index(alien)] = None
                            alien_hit = True
        if alien_hit:
            self._alien_speed = self._alien_speed * ALIEN_SPEED_ADJUSTMENT_FACTOR


    def ShipCollison(self):
        """
        Checks and handles collisions between the player's ship and alien bolts.

        This method iterates through each bolt in _bolts. If a collision is detected
        between a bolt and the player's ship (using the collides method of the Ship class),
        the bolt is removed from _bolts, and the player's ship status is updated.
        If the player has no remaining lives, the ship is set to None,
        Otherwise, the player loses one life, a element is popped from self_heart,
        and the _hit attribute is set to True.

        Postcondition:
            - Any bolt that collides with the ship is removed from _bolts.
            - The player's lives are updated; one life is subtracted for each collision.
            - If lives reach zero, the ship is set to None.
            - The _hit attribute is updated to reflect the collision status.
        """
        for bolt in self._bolts:
            if self._ship.collides(bolt):
                if self._lives == 0:
                    self._ship = None
                else:
                    self._heart.pop()
                    self._hit = True
                    self._lives -= 1
                    self._bolts.remove(bolt)


    def FindNotNone(self):
        """
        Identifies columns in the alien grid that have at least one alien.

        This method creates a list of column indices where at least one alien is present.
        It's used to determine valid columns for alien firing.

        Returns:
            A list of column indices that contain aliens.
        """
        listNone = []
        switch = False
        row = len(self._aliens)
        col = len(self._aliens[0])
        for c in range(col):

            for alien in range(row):
                if alien != None:
                    switch = True

            if switch:
                listNone.append(c)
                switch = False
        return listNone


    def AlienExists(self):
        """
        Determines if any aliens are still present in the game.

        This method iterates through the 2D list _aliens. If it finds any
        object that is not None, it returns True, indicating that at least one alien
        still exists.

        Returns:
            True if at least one alien exists, False otherwise.
        """
        exist = False
        for row in self._aliens:
            for alien in row:
                if alien != None:
                    exist = True
        return exist


    def BoltLoop(self):
        """
        Updates the position of each bolt and removes off-screen bolts.

        This method iterates through each bolt in _bolts, moves them, and checks
        their position. If a bolt goes off the top or bottom of the screen, it is
        removed from the _bolts list.

        Postcondition:
            - Updates the position of each bolt based on its velocity.
            - Removes bolts that have moved off-screen.
        """
        for x in self._bolts:
            x.BoltMove()
            if x.getVelocity() == BOLT_SPEED:
                if x.getY() - BOLT_HEIGHT/2 >= GAME_HEIGHT:
                    self._bolts.remove(x)
            else:
                if x.getY() + BOLT_HEIGHT/2 <= 0:
                    self._bolts.remove(x)


    def CheckIfPlayer(self):
        """
        Checks if any player bolts are currently on the screen.

        This method iterates through the bolts in _bolts and checks if any of them
        are player bolts (i.e., fired by the player's ship).

        Returns:
            True if at least one player bolt is on the screen, False otherwise.
        """
        pswitch = False
        for x in self._bolts:
            if x.isPlayerBolt():
                pswitch = True
        return pswitch


    def ScoreChanger(self,alien):
        """
        Updates the score when an alien is hit.

        This method increases the player's score based on the type of alien hit.

        Parameter alien: The alien that was hit by a bolt.
        Precondition: alien is an instance of Alien.
        """
        assert isinstance(alien,Alien), "alien is not an Alien type"

        newscore = int(alien.getSource()[5])
        #if the first alien is hit (lowest score)
        if newscore == 3:
            self._score += 5
        elif newscore == 2:
            self._score += 7
        else:
            self._score += 10


    def hearts(self):
        """
        Creates and returns a list of heart images representing player lives.

        This method generates heart GImage objects equal to the number of lives the
        player has left. Each heart image visually represents a single life.

        Returns:
        A list of GImage objects representing the player's remaining lives.
        """
        thelist = []
        xpos = 30
        for i in range(self._lives):
            thelist.append(GImage(x=xpos,y=650,width=40\
                        ,height=40,source='heart.png'))
            xpos += 40
        return thelist
    

    def createBossAlien(self):
        """
        Creates and initializes the boss alien for the game.
        
        Returns:
            A BossAlien object representing the boss enemy in the game.
        """
        
        x = GAME_WIDTH / 2
        y = GAME_HEIGHT - 100  
        source = 'AlienBoss.png'
        health = BOSS_HEALTH

        return BossAlien(x, y, source, health)
    

    def BossAlienCollision(self):
        
        """
        Checks for and handles collisions between the boss alien and player-fired bolts.

        This method iterates through all bolts in the _bolts list. If a collision
        is detected between a player-fired bolt and the boss alien, 
        it checks if the boss alien is destroyed by the hit 
        (based on its health). If the boss alien is destroyed,
        it is removed from the game, and the player's score is increased by a set
        amount. Regardless of the boss alien's destruction, the bolt is removed
        from the game after a collision
    """
        for bolt in self._bolts:
            if self._boss_alien and bolt.isPlayerBolt() and self._boss_alien.collides(bolt):
                if self._boss_alien.hit():
                    self._boss_alien = None
                    self._score += 50  
                self._bolts.remove(bolt)


    def bossAlienExists(self):
        """
        Determines if the boss alien is currently present in the game.

        Returns:
            True if the boss alien exists, False otherwise.
        """
        if self._boss_alien is not None:
            return True
    

    def getBossAlien(self):
        """
        Returns the current instance of the boss alien object.

        Returns:
            The boss alien object if it exists, otherwise None.
        """
        return self._boss_alien
    

    def BossAlienMovement(self, dt):
        """
        Manages the horizontal movement of the boss alien.

        The boss alien moves left and right across the screen, changing direction
        when it reaches the edge. The movement speed is determined by the _boss_speed
        attribute.

        Parameter dt: The time elapsed since the last update
        Precondition: dt is a non-negative float
        """
        assert isinstance(dt, float) and dt > 0

        if self._boss_alien:
            self._boss_time += dt
            if self._boss_time > self._boss_speed:
                self._boss_time = 0
                # Horizontal Movement
                if self._boss_switch:
                    if self._boss_alien.x + BOSS_ALIEN_H_WALK + self._boss_alien.width/2 < GAME_WIDTH:
                        self._boss_alien.x += BOSS_ALIEN_H_WALK
                    else:
                        self._boss_switch = False
                        self._boss_alien.y -= BOSS_ALIEN_V_WALK  # Move down
                else:
                    if self._boss_alien.x - BOSS_ALIEN_H_WALK - self._boss_alien.width/2 > 0:
                        self._boss_alien.x -= BOSS_ALIEN_H_WALK
                    else:
                        self._boss_switch = True
                        self._boss_alien.y -= BOSS_ALIEN_V_WALK


    def BossAlienShoot(self, dt):
        """
        Manages the shooting mechanism of the boss alien.

        The boss alien fires three bolts consecutively every four seconds.

        Parameter dt: The time elapsed since the last update
        Precondition: dt is a non-negative float
        """
        if self._boss_alien:
            self._boss_shoot_time += dt


            if self._boss_shoot_time >= 4:
                self._boss_shoot_time = 0  
                self._boss_bolt_count = 0  

            shot_interval = 0.2 
            if self._boss_bolt_count < 3 and self._boss_shoot_time >= \
                self._boss_bolt_count * shot_interval:
                self._boss_bolt_count += 1
                bolt = Bolt(x=self._boss_alien.x, y=self._boss_alien.y\
                 - self._boss_alien.height/2, velocity=-BOLT_SPEED)
                self._bolts.append(bolt)