# An Abstract State 'interface' that defines what every state shall implement.

class AbstractState:
    def handle_input(self): pass
    def update(self): pass
    def render(self): pass
    def get_next_state(self): return self
