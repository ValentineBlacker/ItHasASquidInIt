'''
Created on Sep 8, 2014

@author: DemiCow
'''
import scene
import gameplay
import title
import cutscene

def main():
    """Add states to control here."""
    run_it = scene.Control()
    state_dict = {"TITLE" : title.Title(),
                  "INTRO" : cutscene.Cutscene0(),
                  "GAMEPLAY" : gameplay.gamePlay(),
                  "ENDING" : cutscene.Cutscene1()
                   }
    run_it.setup_states(state_dict, "TITLE")
    run_it.main()   

if __name__ == "__main__":

    main()     
    
