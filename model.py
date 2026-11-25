from antlr4 import *
from gramLexer import gramLexer
from gramListener import gramListener
from gramParser import gramParser

        
class Transition :
    def __init__(self,state_from,weights,states_target,action=None):
        self.state_from=state_from
        self.states_target=states_target
        self.action=action
        self.weights=weights
        
    def __str__(self):
        if self.action is None:
            return (f"Transition from {self.state_from} with no action "
                    f"and targets {self.states_target} with weights {self.weights}")
        else:
            return (f"Transition from {self.state_from} with action {self.action} "
                    f"and targets {self.states_target} with weights {self.weights}")
         
class Model(gramListener):
    
    def __init__(self):
        self.transitions=[]
    
    
    def enterDefstates(self, ctx):
        self.states=[str(x) for x in ctx.ID()]
    
    def enterDefactions(self, ctx):
        self.actions=[str(x) for x in ctx.ID()]
        
    def enterTransact(self, ctx):
        ids = [str(x) for x in ctx.ID()]
        dep = ids.pop(0)
        act = ids.pop(0)
        weights = [int(str(x)) for x in ctx.INT()]
        transition=Transition(dep,weights,ids,act)
        if act not in self.actions:
            raise ValueError(f"The action {act} is not defined")
        else:
            self.transitions.append(transition)
            
    def enterTransnoact(self, ctx):
        ids = [str(x) for x in ctx.ID()]
        dep = ids.pop(0)
        weights = [int(str(x)) for x in ctx.INT()]
        transition=Transition(dep,weights,ids)
        self.transitions.append(transition)
     
    def exitProgram(self, ctx:gramParser.ProgramContext):
        for s in self.states:
            state_vu_in_from=False
            state_vu_in_target=False
            state_with_action=None

            for t in self.transitions:
                # verify The state is isolated or has no target
                if state_vu_in_from==False and s in t.state_from :
                    state_vu_in_from=True
                if state_vu_in_target==False and s in t.states_target :
                    state_vu_in_target=True
                    
                #verify if The state has transitions with actions and no actions
                if t.state_from==s:
                    if state_with_action==None :
                        state_with_action = (t.action!=None)
                    
                    if (state_with_action==True and t.action==None) or (state_with_action == False  and t.action !=None):
                        raise ValueError(f"The state {s} has transitions with actions and no actions")           
            
            if not state_vu_in_target :
                raise ValueError(f"The state {s} is isolated")
            if not state_vu_in_from :
                raise ValueError(f"The state {s} has no target")
            
        # verify if all defined actions are used   
        for a in self.actions:
            action_used=False
            for t in self.transitions:
                if action_used==False and a == t.action:
                    action_used=True
                    break
            if not action_used :
                raise ValueError(f"The action {a} is defined but not used")
                
            
        
                
               
            
    def __str__(self):
        result = f"Actions: {self.actions}\n"
        result += f"States: {self.states}\n"

        for t in self.transitions:
            result += str(t) + "\n"

        return result

        
def play(path):
    path = "ex.mdp"
    lexer = gramLexer(FileStream(path))
    # Pour lire directement depuis le fichier
    stream = CommonTokenStream(lexer)
    parser = gramParser(stream)
    tree = parser.program()
    model = Model()
    walker = ParseTreeWalker()
    walker.walk(model, tree)
    return(model)   
 
def main():
    #lexer = gramLexer(StdinStream())
    path = "ex.mdp"
    model=play(path)
    print(model)

if __name__ == '__main__':
    main()