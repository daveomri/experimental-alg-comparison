#!/usr/bin/python3

# David Omrai
# probSAT algorithm
# 18.11.2022

import sys, getopt
from random import randint
import numpy
import copy  

# Class represents the ProbSat algorithm
# user can set the params through the command
class ProbSat:
  def __init__(self, argv = None):
    self.ifile_name = ""
    self.ofile_name = ""
    
    # Algorithm params
    self.cm = 0
    self.cb = 2.3
    self.eps = 0.0001
    
    # Algorithm params
    self.max_turns = 1
    self.max_flips = 300
    
    # SAT formula representation
    self.formula = []
    self.var_num = 0
    self.clause_num = 0
    
    # Load the input data
    if (argv != None):
      self.load_input(argv)
    self.load_formula(self.ifile_name)
    
  # Loading the command input
  def load_input(self, argv):
    command_format = "probsat.py -i <inputfile> -o <outputfile> -f <maxflips> -t <maxturns>"
    
    try:
      opts, args = getopt.getopt(argv, "hi:o:f:t:")
    except getopt.GetoptError:
      print(command_format)
      sys.exit(2)
    
    if not opts:
      print(command_format)
      sys.exit(2)
    
    for opt, arg in opts:
      if opt == '-h':
        print(command_format)
        sys.exit(2)
      elif opt in ("-i"):
        self.ifile_name = arg
      elif opt in ("-o"):
        self.ofile_name = arg
      elif opt in ("-f"):
        self.max_flips = int(arg)
      elif opt in ("-t"):
        self.max_turns = int(arg)
    
  # Loads the formula from file
  def load_formula(self, file_name):
    file_lines = self.read_file(file_name)
    self.formula, self.var_num = self.get_formula(file_lines)
    self.clause_num = len(self.formula)

  # Reading the data from given file
  def read_file(self, file_name):
    # Open the file
    f = open(file_name, "r")

    return f.readlines()
  
  # Getting the formula from the file data
  def get_formula(self, file_lines):
    if (len(file_lines) < 8 ):
      print("Error: not valid input file")
      sys.exit(2)
      
    formula = []
    var_num = 0
    try:
      ins_info = file_lines[7].strip().split()
      var_num = int(ins_info[2])
      claus_num = int(ins_info[3])
      
      if claus_num + 8 != len(file_lines):
        raise ValueError("Error: Bad file data format")
      
      for line in file_lines[8:]:
        var_array = [int(num) for num in line.strip().split()[:-1]]
        formula.append(var_array)
    except:
      print("Error: can't load data from file")
      raise

    return formula, var_num
  
  # Function randomly assign truth values to
  # each of the vavariables
  def get_random_assignment(self):
    new_t = [0] * self.var_num
    for i in range(self.var_num):
      new_t[i] = randint(0, 1)
    return new_t
  
  # With given setting of varialbe x
  # the function evaluates clause
  # and returns if it's satisfied or not
  def evaluate_clause(self, clause, truth_eval):
    for c_x in clause:
      if c_x > 0 and truth_eval[abs(c_x)-1] == 1:
        return True
      if c_x < 0 and truth_eval[abs(c_x)-1] == 0:
        return True
    return False
  
  # Evaluate the formula
  def evaluate_formula(self, truth_eval):
    for clause in self.formula:
      if self.evaluate_clause(clause, truth_eval) == False:
        return False
    return True

  # Function returns ids of unsatistied clausules
  def get_unsatisfied_clauses(self, truth_eval):
    clausules = []
    for i in range(self.clause_num):
      clause = self.formula[i]
      if self.evaluate_clause(clause, truth_eval) == False:
        clausules.append(i)
    
    return clausules
  
  # Function return value defined by equation
  def f (self, var_x, truth_eval):
    # Parameters
    num_new = 0
    num_lost = 0
    for clause in self.formula:
      prev_eval = self.evaluate_clause(clause, truth_eval)
      # flip the truth value
      truth_eval[var_x-1] = (truth_eval[var_x-1] + 1) % 2
      new_eval = self.evaluate_clause(clause, truth_eval)
      # flip the truth value back
      truth_eval[var_x-1] = (truth_eval[var_x-1] + 1) % 2
      
      if (prev_eval == 1 and new_eval == 0):
        num_lost += 1
      elif (prev_eval == 0 and new_eval == 1):
        num_new += 1
      

    return (num_new**self.cm) / ((self.eps + num_lost)**self.cb)
  
  # Function returns probabilies of variables 
  # given by the f function
  def get_clause_var_probs(self, clause_id, truth_eval):
    clause_probs = []
    for x in self.formula[clause_id]:
      clause_probs.append(self.f(abs(x), truth_eval))
      
    # Normalize values
    probs_sum = sum(clause_probs)

    clause_norm_probs = []

    for prob in clause_probs:
      clause_norm_probs.append(prob / probs_sum)

    return clause_norm_probs
  
  # Prints the message to standart error output
  def eprint(self, *args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
    
  # The main part of the algorithm
  def run (self):
    num_runs = 0
    
    # Initialization of variable values
    best_t = []
    best_sat_clauses = 0
    truth_eval = []
    
    
    for i in range(0, self.max_turns):
      truth_eval = self.get_random_assignment()
      
      for j in range(0, self.max_flips):
        num_runs += 1
        if self.evaluate_formula(truth_eval) == True:
          best_sat_clauses = self.clause_num
          self.eprint("{} {} {} {}".format(num_runs, self.max_flips*self.max_turns, best_sat_clauses, self.clause_num))
          return truth_eval
        
        # Get set of unsatisfied clauses
        unsat_clauses = self.get_unsatisfied_clauses(truth_eval)
        
        if self.clause_num - len(unsat_clauses) > best_sat_clauses:
          best_sat_clauses = self.clause_num - len(unsat_clauses)
          best_t = copy.deepcopy(truth_eval)
        # Random id of unsatisfied clause
        clause_id = unsat_clauses[randint(0, len(unsat_clauses) - 1)]
        # Clause vars probabilies
        clause_vars_probs = self.get_clause_var_probs(clause_id, truth_eval)
        # Get random varialbe from unsat clause, range given by 3-sat
        rand_id = numpy.random.choice(
          numpy.arange(0, len(self.formula[clause_id])), p=clause_vars_probs)
        rand_var = abs(self.formula[clause_id][rand_id])
        
        # Flip the truth assinment of choosen variable
        truth_eval[rand_var-1] = (truth_eval[rand_var-1] + 1) % 2
    
    
    self.eprint("{} {} {} {}".format(num_runs, self.max_flips*self.max_turns, best_sat_clauses, self.clause_num))
    return best_t
      
   
if __name__ == "__main__":
  probsat = ProbSat(sys.argv[1:]) #(["-i", "data/uf75-325/uf75-01.cnf", "-o", "output.dat"])#
  
  print(probsat.run())
  