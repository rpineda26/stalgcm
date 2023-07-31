from queue import Queue
import sys
from model import *
"""

    Author : Ralph Dawson G. Pineda
    Section : STALGCM S13
    Model : 2-way Deterministic Finite Automata
    Todo checklist:     

                    change return 0 in whichTransition() function to something better

                    cases where the machine is stuck in a loop
                    validation for 

                    validation for uniqueness of state name and symbols
                    fix for updating colors
""" 

"""

@definition : Reads the text file and returns the machine definition. Check README.md file for the
              text format of the file input
@params : filename  -  file name of the text file input
@returns :  Q  -  set of all states
            sigma  -  the alphabet of all symbols to be read
            start  -  the start state from Q
            final  -  the acceptance state from Q
            reject  -  the reject state from Q
            transition  - (current state, input, next state, direction)
                        -  set of all transition functions

"""

def readMachine(filename):
    transition_list = []
    with open(filename) as f:
      #  size = int(f.readline())
        Q = f.readline().split()
        sigma = f.readline().split()
        read_states = f.readline().split()
        start = read_states[0]
        accept = read_states[1]
        reject = read_states[2]
        while True:
            transition = f.readline().split()
            if not transition:
                break
            transition_list.append(transition)

    return Q, sigma, start, accept, reject, transition_list
"""
@definition: This function is called after receiving the machine definition through file input. It first checks 
                if the machine definition complies with all the rules of a 2-way dfa. Then it instantiates a 2-way dfa
                object if the machine definition is valid.
@params:    Q  -  set of all states
            sigma  -  the alphabet of all symbols to be read
            start  -  the start state from Q
            final  -  the acceptance state from Q
            reject  -  the reject state from Q
            delta  -  set of all transition functions
                   -  transition function: (current state, input, next state, direction)
@returns:   code  -  the validity of the machine, can point out which part of the machine definition is invalid
            machine  -  the 2-way dfa object if the machine definition is valid, None otherwise
"""
def initializeMachine(Q, sigma, delta, start, accept, reject):
    if not validateDeterministic(Q, sigma, delta):
        code = 1
        machine = None
    elif not validateTransition(sigma,delta, Q, accept, reject):
        code = 2
        machine = None
    else:
        Q = validateUniqueStateName(Q)
        code = 0
        machine = Machine_2DFA(Q, sigma, delta, start, accept, reject)
        
    return code, machine

"""
@definiiton: This function makes sure that the given names of the states in the machine definition
              are unique. If not, it appends a number to the state name to make it unique.
@params:  Q  -  set of all states
@returns:  Q  -  set of all states with unique names
"""

def validateUniqueStateName(Q):
    for i in Q:
        counter = 0
        for j in Q:
            if i != j:
                if Q[i] == Q[j]:
                    counter +=1
                    Q[j] += str(counter)
    return Q

"""

@definition: This gives the appropriate transition function according to the input given
@params:  list_transition  -  set of all transition functions defined in the machine definition
          input  -  the current character being read
@returns: next_state   - the next state to move to
          direction  - the direction to read the next input from

"""

def nextStep(list_transition, state, input):
    filtered_list = filterTransistionList(list_transition, state)

    for i in filtered_list:
        _, req_input, next_state, direction = i
        if req_input == input:
            return next_state, direction, i
        
"""

@definition: This function filters the set all all transitions from the machine definition based
            on the current state
@params:  list_transition  -  this is the set of all transitions defined in the machine definition
          state  -  the current state you're in
@returns: new_list  -  the filtered list where every transition function here has their current state
                        equal to the param state

"""

def filterTransistionList(list_transition, state):
    new_list = []
    for i in list_transition:
        curr_state,_,_,_ = i
        if curr_state == state:
            new_list.append(i)
    return new_list

"""
@definition: This gives the appropriate transition function according to the input given
@params:  list_transition  -  list of tansitions transitions are all based on the current state
          input  -  the current character being read
@returns: next_state   - the next state to move to
          direction  - the direction to read the next input from
"""

def whichTransition_Exact(list_transition, input):
    for i in list_transition:
        _, req_input, next_state, direction = i
        if req_input == input:
            return next_state, direction
    return 0

"""

@definition: This checks if the character input is in the alphabet of the machine
@params:  character  -  the current character being read
            sigma  -  the alphabet of all symbols to be read
@returns: True  - character is in the alphabet

"""

def validateSymbol(character, sigma):
    extended_sigma = ['-','+']
    for i in sigma:
        extended_sigma.append(i)
    if character in extended_sigma:
        return True
    else:
        print("Invalid input : input not in alphabet")
        return False

"""

definition: This checks the all transition functions in the 
            list provided by the machine definition is valid
            A transition function is considered valid if: 
                1. the input is in the alphabet union (left and right end markers)
                2. the current state is in the set of states
                3. the next state is in the set of states
                4. the accept state has no outgoing transition
                5. the reject state has no outgoing transition
                6. the left end marker has no outgoing transition to the left
                7. the right end marker has no outgoing transition to the right
@params:  list_transition  -  set of all transition functions defined in the machine definition
            sigma  -  the alphabet of all symbols to be read
            Q  -  the set of all states
            accept = accept state
            reject = reject state
@returns: True  - all transition functions are valid
            False - atleast one transition function is invalid

"""
def validateTransition(sigma, list_transition, Q, accept, reject):
    extended_sigma = ['-','+']
    for i in sigma:
        extended_sigma.append(i)

    for i in list_transition:
        state, req_input, state2, direction = i
        if req_input not in extended_sigma:
            print("Invalid transition function : input not in alphabet")
            print("transition function in question: "+ str(i))
            return False
        if state not in Q:
            print("Invalid transition function : current state not in set of states")
            print("transition function in question: "+ str(i))
            return False
        if state2 not in Q:
            if state2 != 'NA':
                print("Invalid transition function : next state not in set of states")
                print("transition function in question: "+ str(i))
                return False
        if state == accept and state2 != accept:
            print("Invalid transition function : accept state cannot have an outgoing transition")
            print("transition function in question: "+ str(i))
            return False
        if state == reject and state2 != reject:
            print("Invalid transition function : reject state cannot have an outgoing transition")
            print("transition function in question: "+ str(i))
            return False
        if req_input == '-'and direction == 'left':
            print("Invalid transition function : cannot move left from left end marker")
            print("transition function in question: "+ str(i))
            return False
        if req_input == '+'and direction == 'right':
            print("Invalid transition function : cannot move right from right end marker")
            print("transition function in question: "+ str(i))
            return False
    return True

"""

@definition: This checks if the machine is deterministic or not. A machine is deterministic if:
             every state has a transition function for every input in the alphabet union (left and right end markers)

@params:  list_transition  -  set of all transition functions defined in the machine definition
            sigma  -  the alphabet of all symbols to be read
            Q  -  the set of all states
@returns: False - machine is non-deterministic, True otherwise

"""

def validateDeterministic(Q, sigma, list_transition):
    extended_sigma = ['-','+']
    for i in sigma:
        extended_sigma.append(i)
    flag = False
    for state in Q:
        transitions = filterTransistionList(list_transition, state)
        for i in extended_sigma:
            flag = False
            for t in transitions:
                _, req_input, _, _ = t
                if req_input == i:
                    flag = True
            if flag == False:
                print("state "+ state+" has no transition for input "+ i)
    return flag

"""

note: might update this function. As of my current understanding, 
the machine will end if it reaches either accepting state and reject state
and if the head points to an end marker.

@definition: This checks if the process should end terminate or not
@params:  state   -  the current state
        accept  -  the acceptance state
        reject - the rejected state
@returns: True  - process should terminate
          False - keep reading inputs

"""

def isEnd(state, accept,reject, input):
    if (state == accept or state == reject) and input in ('-','+'):
        return True
    else:
        return False
    
"""

@definition: This checks if the process should end terminate or not
@params:  state   -  the current state
        accept  -  the acceptance state
        reject - the rejected state
@returns: True  - process should terminate

"""

def isAccepted(state, accept):
    if state == accept:
        return True
    else:
        return False

"""

@definition: This encapsulates the word input with left and right end markers
@params: word - the word to be encapsulated
@return: -w+  - where w is the word input

"""

def attachEndMarker(word):
    return  '-' + word + '+'

"""

HELPER FUNCTION 
@definition: This displays the current state of the machine
@params:  state   -  the current state
        input  -  the current input
        string - the word input
        head - the pointer to the current character being read

"""   

def displayAction(state, input, string, head):
    print("Current State: "+state)
    print("Current Input: "+input)
    print("Word Input: " +string)
    print("head: "+head)

    main()