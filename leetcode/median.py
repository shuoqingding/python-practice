class Solution:
    # @return a float
    def findMedianSortedArrays( self, A, B ):
        i = 0
        j = 0
        k=0
        median = [0,0]

        total = len(A) + len(B)
        even = False
        if total%2 == 0:
            even = True

        C = None
        if len(A) == 0:
            C = B
        elif len(B) == 0:
            C = A

        if C is not None:
            if not even:
                return C[total/2]
            else:
                return (C[total/2-1] + C[total/2])/2.0

        if len(A) == len(B) == 1:
            return (A[0]+B[0])/2.0


        while(1):
            count = 0

            if j>=len(B) or ( i<len(A) and A[i] <= B[j] ):
                print "Touch A:",A[i],i,j,k
                median[k] = A[i]
                i+=1
            elif j<len(B):
                print "Touch B:",B[j],i,j,k
                median[k] = B[j]
                j+=1

            count = i+j
            if not even:
                if count  == ( (total/2+1) ) :
                    return sum(median)
            else:
                if count == (total/2):
                    k += 1
                if count == (total/2+1):
                    return sum(median)/2.0


test = Solution()
print test.findMedianSortedArrays( [1,2], [1,1] )
