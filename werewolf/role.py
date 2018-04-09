import asyncio

class Role:
    """
    Base Role class for werewolf game
    
    Category enrollment guide as follows (category property):
        Town:
        1: Random, 2: Investigative, 3: Protective, 4: Government,
        5: Killing, 6: Power (Special night action)
        
        Werewolf:
        11: Random, 12: Deception, 15: Killing, 16: Support
        
        Neutral:
        21: Benign, 22: Evil, 23: Killing
        
        
        Example category:
        category = [1, 5, 6] Could be Veteran
        category = [1, 5] Could be Bodyguard
        category = [11, 16] Could be Werewolf Silencer
        
    
    Action guide as follows (on_event function):
        _at_night_start
        0. No Action
        1. Detain actions (Jailer/Kidnapper)
        2. Group discussions and Pick targets
        
        _at_night_end
        0. No Action
        1. Self actions (Veteran)
        2. Target switching and role blocks (bus driver, witch, escort)
        3. Protection / Preempt actions (bodyguard/framer)
        4. Non-disruptive actions (seer/silencer)
        5. Disruptive actions (werewolf kill)
        6. Role altering actions (Cult / Mason)
    """
    
    rand_choice = False  # Determines if it can be picked as a random role (False for unusually disruptive roles)
    category = [0]      # List of enrolled categories (listed above)
    allignment = 0      # 1: Town, 2: Werewolf, 3: Neutral
    channel_id = ""     # Empty for no private channel
    unique = False      # Only one of this role per game
    game_start_message= (
        "Your role is **Default**\n"
        "You win by testing the game\n"
        "Lynch players during the day with `[p]ww lynch <ID>`"
        )

    def __init__(self, game):
        self.game = game
        self.player = None
        self.blocked = False
        self.properties = {}  # Extra data for other roles (i.e. arsonist)
        
        self.action_list = [
            (self._at_game_start, 0),  # (Action, Priority)
            (self._at_day_start, 0),
            (self._at_voted, 0),
            (self._at_kill, 0),
            (self._at_hang, 0),
            (self._at_day_end, 0),
            (self._at_night_start, 0),
            (self._at_night_end, 0)
            ]
        
    async def on_event(self, event, data):
        """
        See Game class for event guide
        """
            
        await self.action_list[event][0](data)
        
        
    async def assign_player(self, player):
        """
        Give this role a player
        Can be used after the game has started  (Cult, Mason, other role swap)
        """

        player.role = self
        self.player = player
    
    async def _get_role(self, source=None):
        """
        Interaction for powerful access of role
        Unlikely to be able to deceive this
        """
        return "Default"
    
    async def _see_role(self, source=None):
        """
        Interaction for investigative roles.
        More common to be able to deceive this action
        """
        return "Role"
    
    async def _at_game_start(self, data=None):
        if self.channel_id:
            await self.game.register_channel(self.channel_id, self)
        
        await self.player.send_dm(self.game_start_message) #Maybe embeds eventually
        
    async def _at_day_start(self, data=None):
        pass
        
    async def _at_voted(self, data=None):
        pass
        
    async def _at_kill(self, data=None):
        pass
        
    async def _at_hang(self, data=None):
        pass
        
    async def _at_day_end(self, data=None):
        pass
        
    async def _at_night_start(self, data=None):
        pass
        
    async def _at_night_end(self, data=None):
        pass
