#!/usr/bin/env python2.6

from __future__ import absolute_import, division, print_function
import re

next_line = lambda f: f.readline().rstrip()

class FirstLogic( object ):

    rules = []
    statements = []
    theta = {}

    def __init__( self, ):
        with open( "input.txt", "U" ) as f:

            self.goal = self.parse_predicate( next_line( f ) )
            self.num_rules = int( next_line( f ) )
            for i in range( self.num_rules ):
                self.append_rule( next_line(f) )

    def parse_predicate( self, str_predicate ):
        name = str_predicate.strip().split("(")[0]
        variables  = re.search("\((.*)\)", str_predicate ).groups(0)[0].replace(" ","")
        variables = variables.split(',')

        return { "name": name, "vars": variables }

    def append_rule( self, str_rule ):
        if "=>" not in str_rule:
            self.statements.append( self.parse_predicate( str_rule ) )
            return

        left, right = str_rule.strip().split( "=>" )
        left_predicates = left.split( "&" )
        left_predicates = [ self.parse_predicate( p ) for p in left_predicates ]
        # assume there is only one predicate in the right side
        right_predicate = self.parse_predicate( right )

        self.rules.append( { "left": left_predicates, "right": right_predicate } )

    def isPredicateEqual( self, p1, p2 ):
        if p1['name'] != p2['name']:
            return False, None
        if len( p1['vars'] ) != len( p2['vars'] ):
            return False, None

        theta = {}
        for i in range(len(p1['vars'])):
            if p1['vars'][i] == 'x' and p2['vars'][i] != 'x':
                theta['x'] = p2['vars'][i]
            elif p2['vars'][i] == 'x' and p1['vars'][i] != 'x':
                theta['x'] = p1['vars'][i]
            elif p1['vars'][i] != 'x' and p1['vars'][i] != p2['vars'][i]:
                return False, None

        return True, theta

    def subst( self, predicate, theta ):
        if theta is None:
            return

        import copy
        p = copy.deepcopy( predicate )

        for i in range(len(p['vars'])):
            if p['vars'][i] in theta:
                p['vars'][i] = theta[p['vars'][i]]

        return p

    def list_all_thetas( self, goal ):
        for s in self.statements:
            r, theta = self.isPredicateEqual( goal, s )
            if r:
                yield theta

        for rule in self.rules:
            r, theta = self.isPredicateEqual( goal, rule['right'] )
            if r:
                yield theta

    def backward_chaining_multigoals( self, goals ):
        for theta in self.list_all_thetas( goals[0] ):
            result = True

            for goal in goals:
                new_goal = self.subst( goal, theta )
                r = self.backward_chaining( new_goal )
                result &= r

            if result:
                return True

        return False

    def backward_chaining( self, goal ):
        for s in self.statements:
            r, theta = self.isPredicateEqual( goal, s )
            if r:
                return True

        for rule in self.rules:
            r, theta = self.isPredicateEqual( goal, rule['right'] )
            if not r:
                continue

            new_goals = []
            for p in rule['left']:
                new_goals.append( self.subst( p, theta ) )

            r = self.backward_chaining_multigoals( new_goals )
            if r:
                return True

        return False

if __name__ == "__main__":
    logic = FirstLogic()
    r = logic.backward_chaining( logic.goal )
    with open( "output.txt", "w" ) as f:
        if r:
            f.write( "TRUE" )
        else:
            f.write( "FALSE" )
