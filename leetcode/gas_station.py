class Solution:
    # @param gas, a list of integers
    # @param cost, a list of integers
    # @return an integer
    def canCompleteCircuit(self, gas, cost):
        curGas = []
        total = len(gas)
        count = 0
        k = 0

        seq = range(0,total)
        seq.reverse()
        print gas
        print cost
        for i in seq:
            if count == 0:
                curGas.append(0)
            else:
                curGas.append( curGas[count-1] + gas[i] - cost[i] )

            print i, curGas
            for j in range(k, total):
                pos = (i + j) % total
                tmpGas = gas[pos] - cost[pos]
                if count > 0:
                    tmpGas = tmpGas + curGas[count-1]

                print count, j, tmpGas
                k = pos
                if curGas[count] + tmpGas < 0:
                    break
                curGas[count] += tmpGas
            else:
                return i

            count += 1
        return -1


s = Solution()
print s.canCompleteCircuit( [1,2], [2,1] )
print s.canCompleteCircuit( [2,3,1], [3,1,2] )
