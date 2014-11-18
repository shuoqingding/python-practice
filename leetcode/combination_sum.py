class Solution:
    # @param candidates, a list of integers
    # @param target, integer
    # @return a list of lists of integers

    def combinationSum(self, candidates, target):
        candidates = list( set(candidates) )
        candidates.sort()
        results = []
        self._combinationSum( [], candidates, target, 0, results )
        return results

    def _combinationSum(self, pre_ints, candidates, target, k, results ):

        if target < 0:
            return

        if target == 0:
            if pre_ints not in results:
                results.append( pre_ints )
            return
        if candidates[k] <= target:
            for i in range( k, len(candidates) ):
                c = candidates[i]
                pre = pre_ints[:]
                pre.append( c )
                pre.sort()
                self._combinationSum( pre, candidates, target-c, i, results )

s = Solution()
print s.combinationSum( [8,7,4,3], 11)
