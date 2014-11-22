# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

class Solution:
    # @return a ListNode
    def addTwoNumbers(self, l1, l2):

        p = l1
        q = l2
        l3 = ListNode( 0 )
        x = l3

        while p is not None or q is not None:
            sum_num = x.val
            if p is not None:
                sum_num += p.val
                p = p.next
            if q is not None:
                sum_num += q.val
                q = q.next

            x.val = sum_num % 10

            carry = sum_num / 10
            if q is None and p is None and carry == 0:
                break
            x.next = ListNode( carry )
            x = x.next

        return l3

l1 = ListNode( 0 )
l2 = ListNode( 0 )

s = Solution()
x = s.addTwoNumbers( l1, l2 )
while x is not None:
    print x.val
    x = x.next
