from queue import Queue
import sys

"""

    Author : Ralph Dawson G. Pineda
    Section : STALGCM S13
    Model : 2-way Deterministic Finite Automata
    Todo:  verification of integrity of text input
    checklist:      do both start and final states exist in Q
                    does every element from every transition function exist in Q and sigma and directions   (directions = left, right by default)
                    does every state have a transition function for all symbols defined in sigma (deterministic fa)

                    change return 0 in whichTransition() function to something better

                    cases where the machine is stuck in a loop
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
        start, accept, reject = read_states
        while True:
            transition = f.readline().split()
            if not transition:
                break
            transition_list.append(transition)

    return Q, sigma, start, accept, reject, transition_list

"""

@definition: This step by step traces the machine's process as the word is being read per symbol
@params:  list_transition  -  set of all transition functions defined in the machine definition
          start  -  start state
          accept = accept state
          reject = reject state
          word = the string word to be read
@returns: accepted  - is word accepted in the 2-way dfa defined in the machine definition via text file

"""

def allStep(list_transition, start, accept, reject, word, sigma):
    flag=  True
    head=0 # this is the pointer to which character will be read from the word 
    curr_state = start
    accepted = False
    while(flag):
        _ = input("Step: ")
        if validateSymbol(word[head], sigma):
            curr_state, direction = nextStep(list_transition, curr_state, word[head])
        else:
            return False
        if direction =="left":
            head -=1
        else:
            head +=1
        if isEnd(curr_state, accept, reject):
            flag = False
            if isAccepted(curr_state, accept):
                accepted = True
        displayAction(curr_state, word[head], word, head)
    return accepted

"""

@definition: This gives accepts a list of string inputs and determines whether each string
                is accepted or rejected by the machine
@params:  list_transition  -  set of all transition functions defined in the machine definition
            start  -  start state
            accept = accept state
            reject = reject state
            words = list of words to be read
@returns: accepted  - a list of booleans where true is for accepted and false otherwise

"""

def quickStep(list_transition, start, accept, reject, words, sigma):
    accepted = []
    for word in words:
        flag=  True
        head=0 # this is the pointer to which character will be read from the word 
        curr_state = start
        while(flag):
            if validateSymbol(word[head], sigma):
                curr_state, direction = nextStep(list_transition, curr_state, word[head])
            else:
                return False
            if direction =="left":
                head -=1
            else:
                head +=1
            if isEnd(curr_state, accept, reject):
                flag = False
                if isAccepted(curr_state, accept):
                    accepted.append(True)
            displayAction(curr_state, word[head], word, head)
            accepted.append(False)
    return accepted

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
            return next_state, direction
        
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
    if character in sigma:
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
    extended_sigma =('-','+')
    extended_sigma.append(sigma)
    for i in list_transition:
        state, req_input, state2, direction = i
        if req_input not in extended_sigma:
            print("Invalid transition function : input not in alphabet")
            print("transition function in question: "+ i)
            return False
        if state not in Q:
            print("Invalid transition function : current state not in set of states")
            print("transition function in question: "+ i)
            return False
        if state2 not in Q:
            print("Invalid transition function : next state not in set of states")
            print("transition function in question: "+ i)
            return False
        if state == accept and state2 != accept:
            print("Invalid transition function : accept state cannot have an outgoing transition")
            print("transition function in question: "+ i)
            return False
        if state == reject and state2 != reject:
            print("Invalid transition function : reject state cannot have an outgoing transition")
            print("transition function in question: "+ i)
            return False
        if req_input == '-'and direction == 'left':
            print("Invalid transition function : cannot move left from left end marker")
            print("transition function in question: "+ i)
            return False
        if req_input == '+'and direction == 'right':
            print("Invalid transition function : cannot move right from right end marker")
            print("transition function in question: "+ i)
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
    extended_sigma = ('-','+')
    extended_sigma.append(sigma)
    for state in Q:
        transitions = filterTransistionList(list_transition, state)
        for i in extended_sigma:
            if i not in transitions:
                print("Machine is not deterministic")
                print("state "+ state+" has no transition for input "+ i)
                return False
    return True

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

def main():
    Q, sigma, start, accept, reject, list_transition = readMachine("/tests/test.txt")
    #Q, sigma will be included once the verification is accomplished
    word = input("Enter Word: ")
    word = attachEndMarker(word)
    if validateTransition(sigma, list_transition, Q, accept, reject) and validateDeterministic(Q, sigma, list_transition):
        print("Machine is valid")
    else:
        print("Machine is invalid")
        return 0

    """
    print("start: "  + start)
    print("accept: " + accept)
    print("reject: " + reject)
    for i in list_transition:
        print(i)
     """
    accepted = allStep(list_transition, start, accept, reject, word, sigma)
    if(accepted):
        print("Accepted")
    else:
        print("Rejected")


if __name__ == "__main__":
    main()