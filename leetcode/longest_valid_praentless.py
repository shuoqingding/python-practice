class Solution:
    # @param s, a string
    # @return an integer
    def longestValidParentheses(self, s): 
        if s in ("","(",")"):
            return 0

        longest_valid = [0]
        for i in range(1,len(s)):
            c = s[i]
            if c == "(":
                longest_valid.append( 0 )

            else:
                print s[i],i,longest_valid
                if s[i-1] == "(":
                    longest_valid.append( longest_valid[i-2] + 2 if i > 1 else 2 )
                elif i-longest_valid[i-1]-1 >= 0 and s[i-longest_valid[i-1]-1] == '(':
                    longest_valid.append( longest_valid[i-1] + 2 )
                    if i-longest_valid[i-1]-2 >= 0:
                        longest_valid[i] = longest_valid[i] + longest_valid[i-longest_valid[i-1]-2]

        return max(longest_valid)

s = Solution()
s.longestValidParentheses( "))))((()((" )
