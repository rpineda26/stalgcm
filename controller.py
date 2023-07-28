from queue import Queue
import sys

"""
    Todo:  verification of integrity of text input
    checklist:      do both start and final states exist in Q
                    does every element from every transition function exist in Q and sigma and directions   (directions = left, right by default)
                    does every state have a transition function for all symbols defined in sigma (deterministic fa)

    Todo: test cases - 4 valid, 1 invalid
    checklist:
        valid     even number 
                  divisible by 4 
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
    transition = []
    with open(filename) as f:
      #  size = int(f.readline())
        Q = f.readline().split()
        sigma = f.readline().split()
        start, accept, reject = f.readline().split()
        length_states = int(f.readline())
        for _ in range(length_states):
            t = f.readline().split()
            transition.append(t)

    return Q, sigma, start, accept, reject, transition

"""

@definition: This step by step traces the machine's process as the word is being read per symbol
@params:  list_transition  -  set of all transition functions defined in the machine definition
          start  -  start state
          accept = accept state
          reject = reject state
          word = the string word to be read
@returns: accepted  - is word accepted in the 2-way dfa defined in the machine definition via text file

"""

def allStep(list_transition, start, accept, reject, word):
    flag=  True
    head=0 # this is the pointer to which character will be read from the word 
    curr_state = start
    accepted = False
    while(flag):
        _ = input("Step: ")
        curr_state, direction = nextStep(list_transition, curr_state, word[head])
        if direction =="left":
            head -=1
        else:
            head +=1
        if isEnd(curr_state, accept, reject):
            flag = False
            if isAccepted(curr_state, accept):
                accepted = True
        displayAction(curr_state, word[head], word)
    return accepted

def quickStep(list_transition, start, accept, reject):
    flag=  True
    head=0 # this is the pointer to which character will be read from the word 
    curr_state = start
    accepted = False
    while(flag):
        curr_state, direction = nextStep(list_transition, curr_state, word[head])
        if direction =="left":
            head -=1
        else:
            head +=1
        if isEnd(curr_state, accept, reject):
            flag = False
            if isAccepted(curr_state, accept):
                accepted = True
        displayAction(curr_state, word[head], word)
    return accepted

"""

 I plan to do something on the transiion, check paper to recall
transition is a list of transitions whose current state = state
the appropriate transition list according to the state should be found before calling this function

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
        curr_state, _,_,_ = i
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
@definition: This checks if the process should end terminate or not
@params:  state   -  the current state
        accept  -  the acceptance state
        reject - the rejected state
@returns: True  - process should terminate
          False - keep reading inputs
"""

def isEnd(state, accept,reject):
    if state == accept | state == reject:
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
    
def displayAction(state, input, string):
    print("Current State: "+state)
    print("Current Input: "+input)
    print("Word Input: " +string)

def main():
    _, _, start, accept, reject, list_transition = readMachine("test.txt")
    #Q, sigma will be included once the verification is accomplished
    word = input("Enter Word: ")
    accepted = allStep(list_transition, start, accept, reject, word)

    if(accepted):
        print("Accepted")
    else:
        print("Rejected")
