"""
Primary module for Alien Invaders

This module contains the main controller class for the Alien Invaders application. There
is no need for any additional classes in this module.  If you need more classes, 99% of
the time they belong in either the wave module or the models module. If you are unsure
about where a new class should go, post a question on Piazza.

# Toshi Tokuyama (tt426)
# December 2nd 2018
"""
from consts import *
from game2d import *
from wave import *



# PRIMARY RULE: Invaders can only access attributes in wave.py via getters/setters
# Invaders is NOT allowed to access anything in models.py

class Invaders(GameApp):
    """
    The primary controller class for the Alien Invaders application

    This class extends GameApp and implements the various methods necessary for processing
    the player inputs and starting/running a game.

        Method start begins the application.

        Method update either changes the state or updates the Play object

        Method draw displays the Play object and any other elements on screen

    Because of some of the weird ways that Kivy works, you SHOULD NOT create an
    initializer __init__ for this class.  Any initialization should be done in
    the start method instead.  This is only for this class.  All other classes
    behave normally.

    Most of the work handling the game is actually provided in the class Wave.
    Wave should be modeled after subcontrollers.py from lecture, and will have
    its own update and draw method.

    The primary purpose of this class is to manage the game state: which is when the
    game started, paused, completed, etc. It keeps track of that in an attribute
    called _state.

    INSTANCE ATTRIBUTES:
        view:   the game view, used in drawing (see examples from class)
                [instance of GView; it is inherited from GameApp]
        input:  the user input, used to control the ship and change state
                [instance of GInput; it is inherited from GameApp]
        _state: the current state of the game represented as a value from consts.py
                [one of STATE_INACTIVE, STATE_NEWWAVE, STATE_ACTIVE, STATE_PAUSED, STATE_CONTINUE, STATE_COMPLETE]
        _wave:  the subcontroller for a single wave, which manages the ships and aliens
                [Wave, or None if there is no wave currently active]
        _text:  the currently active message
                [GLabel, or None if there is no message to display]

    STATE SPECIFIC INVARIANTS:
        Attribute _wave is only None if _state is STATE_INACTIVE.
        Attribute _text is only None if _state is STATE_ACTIVE.

    For a complete description of how the states work, see the specification for the
    method update.

    You may have more attributes if you wish (you might want an attribute to store
    any score across multiple waves). If you add new attributes, they need to be
    documented here.

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY

    _last_keys: the number of keys pressed during the frame [int > 0]
    _soundEffect: sound effect implemented when the alien or the ship is destroyed (extension)
    _scoreBoard:
    """

    # DO NOT MAKE A NEW INITIALIZER!

    # THREE MAIN GAMEAPP METHODS
    def start(self):
        """
        Initializes the application.

        This method is distinct from the built-in initializer __init__ (which you
        should not override or change). This method is called once the game is running.
        You should use it to initialize any game specific attributes.

        This method should make sure that all of the attributes satisfy the given
        invariants. When done, it sets the _state to STATE_INACTIVE and create a message
        (in attribute _text) saying that the user should press to play a game.
        """
        self._state = STATE_INACTIVE
        self._wave = None
        self._text = GLabel(x=GAME_WIDTH/2.0, y=GAME_HEIGHT/2.0,
                            font_size=30, linecolor=introcs.HSV(0.5,1.0,0.3),
                            fillcolor = introcs.HSV(0.2,0.3,0.4),
                            text='PRESS ANY KEY TO PLAY', 
                            font_name = "Retrogame.ttf")
        self._last_keys = None
        self._scoreBoard = None
        # self._soundEffect = True # Extension

    def update(self,dt):
        """
        Animates a single frame in the game.

        It is the method that does most of the work. It is NOT in charge of playing the
        game.  That is the purpose of the class Wave. The primary purpose of this
        game is to determine the current state, and -- if the game is active -- pass
        the input to the Wave object _wave to play the game.

        As part of the assignment, you are allowed to add your own states. However, at
        a minimum you must support the following states: STATE_INACTIVE, STATE_NEWWAVE,
        STATE_ACTIVE, STATE_PAUSED, STATE_CONTINUE, and STATE_COMPLETE.  Each one of these
        does its own thing and might even needs its own helper.  We describe these below.

        STATE_INACTIVE: This is the state when the application first opens.  It is a
        paused state, waiting for the player to start the game.  It displays a simple
        message on the screen. The application remains in this state so long as the
        player never presses a key.  In addition, this is the state the application
        returns to when the game is over (all lives are lost or all aliens are dead).

        STATE_NEWWAVE: This is the state creates a new wave and shows it on the screen.
        The application switches to this state if the state was STATE_INACTIVE in the
        previous frame, and the player pressed a key. This state only lasts one animation
        frame before switching to STATE_ACTIVE.

        STATE_ACTIVE: This is a session of normal gameplay.  The player can move the
        ship and fire laser bolts.  All of this should be handled inside of class Wave
        (NOT in this class).  Hence the Wave class should have an update() method, just
        like the subcontroller example in lecture.

        STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However, the game is
        still visible on the screen.

        STATE_CONTINUE: This state restores the ship after it was destroyed. The
        application switches to this state if the state was STATE_PAUSED in the
        previous frame, and the player pressed a key. This state only lasts one animation
        frame before switching to STATE_ACTIVE.

        STATE_COMPLETE: The wave is over, and is either won or lost.

        You are allowed to add more states if you wish. Should you do so, you should
        describe them here.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        #backgroundMusic = Sound('background.wav')

        if self._state == STATE_INACTIVE:
            self.determine_state()

        if self._state == STATE_NEWWAVE:
            self._wave = Wave()
            self._state = STATE_ACTIVE

        if self._state == STATE_ACTIVE:
            self.updateGame(dt)
            self.alive_again()
            self.determine_win_or_lose()
            self.turnOnOffSound() #Extension
            self.scoreBoard() #Extension
            #backgroundMusic.play()

        if self._state == STATE_CONTINUE:
            self._state = STATE_ACTIVE

        if self._state == STATE_PAUSED:
            self._text = GLabel(x=GAME_WIDTH/2.0, y=GAME_HEIGHT/2.0,
                                font_size=30, linecolor=LINE_COLOR,
                fillcolor=TEXT_COLOR, text='PRESS S TO CONTINUE '
                + str(self._wave.getLives()) + ' LIFE LEFT',
                font_name="Retrogame.ttf")
            self._last_keys = None
            self.determine_state()

    def updateGame(self, dt):
        """
        Updates the game when self._state == STATE_ACTIVE.
        """
        self.moveShip()
        self.moveAlien(dt)
        self.moveBolts()
        self.moveAlienBolts()
        self.collisionActivated()
        self.alive_again()

    def moveShip(self):
        """
        Moves the ship by calling updateShip() when self._state == STATE_ACTIVE
        """

        self._wave.updateShip(self.input)

    def moveAlien(self, dt):
        """
        Moves the alien by calling updateAlien() when self._state == STATE_ACTIVE
        """

        self._wave.updateAlien(dt)

    def moveBolts(self):
        """
        Moves the bolts by the ship by calling updateBolts() 
        when self._state == STATE_ACTIVE
        """
        self._wave.updateBolts(self.input)

    def moveAlienBolts(self):
        """
        Moves the bolts by the alien by calling updateAlienBolts() 
        when self._state == STATE_ACTIVE
        """
        self._wave.updateAlienBolts()


    def collisionActivated(self):
        """
        Handles the collision between the bolt and the alien, and between 
        the ship and the alienBolt when self._state == STATE_ACTIVE.
        """
        self._wave.collision()
        self._wave.collisionShip()


    def draw(self):
        """
        Draws the game objects to the view.

        Every single thing you want to draw in this game is a GObject.  To draw a GObject
        g, simply use the method g.draw(self.view).  It is that easy!

        Many of the GObjects (such as the ships, aliens, and bolts) are attributes in
        Wave. In order to draw them, you either need to add getters for these attributes
        or you need to add a draw method to class Wave.  We suggest the latter.  See
        the example subcontroller.py from class.
        """

        if self._text != None:
            self._text.draw(self.view)

        if self._wave != None:
            self._wave.draw(self.view)

    # HELPER METHODS FOR THE STATES GO HERE
    def determine_state(self):
        """
        Determines the current state depending on whether a key was pressed
        and assigns it to self.state.

        This method checks for a key press, and if there is one, changes the state
        to the next value.  A key press is when a key is pressed for the FIRST TIME.
        We do not want the state to continue to change as we hold down the key.  The
        user must release the key and press it again to change the state.
        """
        current_keys = self.input.key_count

        if ((current_keys > 0 and self._last_keys is None)
                and self._state == STATE_INACTIVE):
            self._state = STATE_NEWWAVE
            self._text = None

        # FIX HERE
        if ((self.input.is_key_down('s') and self._last_keys is None) 
                and self._state == STATE_PAUSED):
            self._state = STATE_CONTINUE
            self._wave.restoreShip()
            self._text = None

        #Copied code from state.py by Walker White

    def alive_again(self):
        """
        Changes the state of the game and life number when the player loses
        the round.
        """
        #print(self._wave.getLives())
        if self._wave.loseRound() and self._state == STATE_ACTIVE:
            self._wave.setLives(self._wave.getLives()-1)
            if self._wave.getLives() != 0:
                self._state = STATE_PAUSED


    def determine_win_or_lose(self):
        """
        Determines whether the player loses of wins the game. The player wins
        if there are no more aliens remaining on the screen. The player loses
        if the life of the ship reaches 0, or if the alien passes the defense 
        line
        """
        count = 0

        if self._wave.getLives() < 1 or self._wave.overDefenseLine():
            self._text = GLabel(x=GAME_WIDTH/2.0, y=GAME_HEIGHT/2.0,
                                font_size=30, 
                                linecolor=introcs.HSV(0.5, 1.0, 0.3),
                                text='GAME OVER')
            self._state = STATE_COMPLETE
        
        for row in range(ALIEN_ROWS):
            for col in range(ALIENS_IN_ROW):
                if self._wave.getAliens()[row][col] == None:
                    count += 1
                if count == ALIEN_ROWS * ALIENS_IN_ROW:
                    self._text = GLabel(x=GAME_WIDTH/2.0, y=GAME_HEIGHT/2.0,
                                        font_size=30, 
                                        linecolor=introcs.HSV(0.5, 1.0, 0.3),
                                        text='CONGRADULATION YOU WON!!')
                    self._state = STATE_COMPLETE

    def turnOnOffSound(self):
        """
        Turns the music on and off when a certain key is pressed.
        """

        if self.input.is_key_down('n'):
            self._wave.setsoundEffect(True)
        elif self.input.is_key_down('m'):
            self._wave.setsoundEffect(False)

    def scoreBoard(self):
        """
        Shows the score board on the screen
        """
        if self._state == STATE_ACTIVE:
            self._text = GLabel(x=GAME_WIDTH/6.0, y=GAME_HEIGHT - 
            GAME_HEIGHT/10.0, font_size=30, linecolor=TEXT_COLOR,
            text='SCORE:' + str(self._wave.getScore()))

