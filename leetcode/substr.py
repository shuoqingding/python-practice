class Solution:
    # @return an integer
    def lengthOfLongestSubstring(self, s):
        sub = []
        max_len = 0

        for i in s:
            if i not in sub:
                sub.append( i )
            else:
                max_len = len(sub) if len(sub) > max_len else max_len

                idx = sub.index ( i )
                sub = sub[idx+1:]
                sub.append( i )

        max_len = len(sub) if len(sub) > max_len else max_len
        return max_len


sol = Solution()

print sol.lengthOfLongestSubstring( "bbbbbb" )
print sol.lengthOfLongestSubstring( "abcdabc" )
print sol.lengthOfLongestSubstring( "ababc" )
print sol.lengthOfLongestSubstring( "ababcabcd" )
