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
        import copy
        p = copy.deepcopy( predicate )

        for i in range(len(p['vars'])):
            if p['vars'][i] in theta:
                p['vars'][i] = theta[p['vars'][i]]

        return p

    def backward_chaining( self, goal ):
        for s in self.statements:
            if self.isPredicateEqual( goal, s )[0]:
                return True
        for rule in self.rules:
            r, theta = self.isPredicateEqual( goal, rule['right'] )
            if not r:
                continue

            result = True
            for p in rule['left']:
                predicate = self.subst( p, theta )
                result &= self.backward_chaining( predicate )
            return result

        return False

if __name__ == "__main__":
    logic = FirstLogic()
    r = logic.backward_chaining( logic.goal )
    with open( "output.txt", "w" ) as f:
        if r:
            f.write( "TRUE" )
        else:
            f.write( "FALSE" )
