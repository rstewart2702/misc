class Heap(object):
    
    def __init__(self,size = 350):
        self.h = [] # "null" initial element, in "slot" 0.
        i=0
        while (i < size):
            self.h.append(None)
            i = i+1
        #
        self.heapend = 1
        #
        self.ticks=0

    def heapordered(self, x, y):
        """
        This is an attempt to write a function which will evaluate the
        truth of the "bottom-up" heap-ordering requirement.
        """
        if ( y <= x ):
            return True
        elif (x < y):
            return (self.h[ y // 2 ] <= self.h[y]) and self.heapordered(x, (y//2))

    def isheap(self, j, L):
        """
        This is another predicate which is used in a loop invariant.
        This method is recursive.
        """
        if ((2*j + 1) < L):
            # The heap element at j has two children, so each of those elements
            # must be individually checked for compliance with the heap property,
            # and then the subheaps rooted at each of those two elements must
            # be recursively checked.
            return (self.h[j] <= self.h[2*j + 1] and self.h[j] <= self.h[2*j] and
                    self.isheap((2*j + 1),L)             and self.isheap(2*j,L)                  )
        elif (2*j < L):
            # The heap element at j has only a left-hand child.
            # This is possible because a heap is "complete binary tree" in which
            # every element, except for the last one, must have two children.
            # The individual element at j has only a left-hand child, so it
            # must be checked for compliance with the heap property and then
            # the subheap rooted at the left-hand child must be recursively checked.
            return (self.h[j] <= self.h[2*j]     and
                    self.isheap(2*j,L)                      )
        elif (L <= 2*j):
            return True

    def heap_add(self, item):
        """
        Add the new item to the heap.
        """
        print "Adding: ", item.key
        j = self.heapend
        # Thus self.heapend always denotes the "empty" slot into which
        # a new item will be inserted?
        #
        # Loop invariant:
        # heapordered(1, j) && heapordered(j, self.heapend) && 1 <= j <= self.heapend
        #
        while (1 < j and item < self.h[j // 2]):
            self.h[j], j = self.h[j // 2], (j // 2)
            # Check the invariant:
            print "j is: ", j, " self.h[j].key is: ", self.h[j].key
            print "self.heapordered(%d,%d) is: %s"%(1, j, self.heapordered(1,j))
            print "self.heapordered(%d,%d) is: %s"%(
                    j, self.heapend, self.heapordered(j, self.heapend)
                )
            print
        self.h[j], self.heapend = item, (self.heapend + 1)

    def down_heap(self,i):
        # Adjust subheap rooted at item i, by swapping it with the smaller
        # of its two children (if there are any, right?)
        j = i
        while (True):
            if (    2*j + 1 < self.heapend
                and self.h[2*j] <= self.h[2*j+1]
                and self.h[2*j] <= self.h[j]):
                # There are at least two children and
                # the left child is smaller and
                # item j is larger than the left child
                t = self.h[2*j]
                self.h[2*j]=self.h[j]
                self.h[j] = t
                j = j*2
                #
                self.ticks+=1
                #
            elif (    2*j + 1 < self.heapend
                  and self.h[2*j+1] < self.h[2*j]
                  and self.h[2*j+1] < self.h[j]):
                # There are at least two children and
                # the right child is smaller than the left child and
                # item j is larger than the right child
                t = self.h[2*j+1]
                self.h[2*j+1]=self.h[j]
                self.h[j] = t
                j=2*j+1
                #
                self.ticks+=1
                #
            elif (    2*j < self.heapend
                  and self.h[2*j] < self.h[j]):
                t = self.h[2*j]
                self.h[2*j] = self.h[j]
                self.h[j] = t
                j=2*j
                #
                self.ticks+=1
                #
            else:
                self.ticks+=1
                break
            ##
            

    def up_heap(self,i):
        # Percolate item at index i upwards, until the heap property
        # is satisfied.
        j = i
        while (1 < j and self.h[j] <= self.h[j//2]):
            # if (self.h[j] <= self.h[j//2]):
            # swap self.h[j] and self.h[j//2]
            t = self.h[j]
            self.h[j]=self.h[j//2]
            self.h[j//2]=t
            #
            j=j//2
            self.ticks+=1
        #

    def heapify(self):
        self.ticks=0
        j=self.heapend
        while (1 <= j):
            self.down_heap(j)
            j=j-1
        #
        print "after heapify, ticks==%d"%self.ticks


    def heapifyOld(self):
        """
        Heap-ify the data already stored within, which should be a Python
        list of objects which respond to a message named "key" and which
        also respond to all the other "comparison operator" messages.
        """
        # Copy newList into the h array.
        # Execute the "up_heap" operation on each of the elements in
        # the set of elements from index self.heapend down to (self.heapend//2)?
        # How do we know, or prove, that this will take linear time?
        # Does it matter whether or not we perform it in reverse order?
        self.ticks=0
        j=2
        while (j <= self.heapend):
            self.up_heap(j)
            j=j+1
        #
        # j = self.heapend
        # while ( 1 < j ):
        #     self.up_heap(j)
        #     j = j-1
        #     #
        #     # if (self.h[j] <= self.h[j // 2]):
        #     #     self.up_heap(j)
        #     #     t = self.h[j // 2]
        #     #     self.h[j // 2] = self.h[j]
        #     #     self.h[j] = t
        #     ##
        #     # j=j-1
        #
        print "after heapfiy, ticks==%d"%self.ticks
                
        
    
    def heap_add_old(self, item):
        """
        Add the new item to the heap.
        """
        print "Adding: ", item.key
        self.h[self.heapend] = item  # store it into the new heap location
        # Now, "percolate" the new item to its proper place in the
        # heap array, h.
        j = self.heapend
        # Loop invariant:
        # heapordered(1, (j//2)) && heapordered(j, self.heapend) && 1 <= j <= self.heapend
        #
        while (1 < j and self.h[ j // 2 ] >= self.h[j]):
            temp = self.h[ j // 2 ]
            self.h[ j // 2 ] = self.h[j]
            self.h[j] = temp
            j = ( j // 2 )
            # Check the invariant:
            print "j is: ", j, " self.h[j].key is: ", self.h[j].key
            # print "self.heapordered(1, (j//2)) is: ", self.heapordered(1, (j//2))
            print "self.heapordered(%d,%d) is: %s"%(1, (j//2), self.heapordered(1,(j//2)))
            # print "self.heapordered(j, self.heapend) is: ", self.heapordered(j, self.heapend)
            print "self.heapordered(%d,%d) is: %s"%(j, self.heapend, self.heapordered(j,self.heapend))
            print 
        # Upon loop termination: heapordered(1, self.heapend)
        # Now, adjust the "end of the heap"
        self.heapend = self.heapend + 1
        print "Finished adding.\n"

    def heap_del(self):
        """
        Remove the minimum element from the heap.
        (This is the revised version!)
        """
        # There are a couple of things to look out for:
        # 
        # 1. Multiple-assignment statements:
        #      j, self.h[j] = j*2, self.h[j*2]
        #    is probably NOT what you want to say. The reason is that the
        #    above is really equivalent to a sequence of "single-assignments":
        #      j = j*2 ; self.h[j] = self.h[j*2]
        #    So, we should say this instead:
        #      self.h[j], j = self.h[j*2], j*2
        # 
        # 2. This version of the heap_del routine assumes that there
        #    are "default comparison operators" defined for the items
        #    placed into the self.h array. Then an expressions like:
        #      self.h[j*2] <= self.h[j*2 + 1]
        #    is equivalent to:
        #      self.h[j*2].key <= self.h[j*2+1].key
        #
        # In comparison to previous versions of this subprogram, this version
        # is breaktaking in its simplicity and beauty. And it is possible to
        # argue for its correctness.
        #
        print "Here is the key to be deleted: %d"%self.h[1].key
        j, newitem, self.heapend = 1, self.h[self.heapend-1], self.heapend-1
        # Loop invariant:
        #   heapordered(1, j) && isheap(j, heapend) && self.h[j] <= newitem
        while (True):
            if   (    j*2 + 1 < self.heapend
                  and self.h[j*2] <= self.h[j*2+1]
                  and self.h[j*2] < newitem):
                self.h[j], j = self.h[j*2], j*2
            elif (    j*2 + 1 < self.heapend
                  and self.h[j*2+1] < self.h[j*2]
                  and self.h[j*2+1] < newitem):
                self.h[j], j = self.h[j*2+1], j*2+1
            elif (    j*2 < self.heapend
                  and self.h[j*2] < newitem):
                self.h[j], j = self.h[j*2], j*2
            else:
                break
            #
            ## print "j is: %d"%j
            ## print "heapordered(1,%d) is: %s"%(j, self.heapordered(1,j))
            ## print "isheap(%d,%d) is: %s"%(j,self.heapend,self.isheap(j,self.heapend))
            ## print
        self.h[j] = newitem

    def heap_del_old1(self):
        """
        Remove the minimum element from the heap.
        (This is the revised version!)
        """
        j, newitem, self.heapend = 1, self.h[self.heapend-1], self.heapend-1
        # Loop invariant:
        #   heapordered(1, j) && isheap(j, heapend) && self.h[j].key <= newitem.key
        while (True):
            if (    j*2 + 1 < self.heapend
                and self.h[j*2].key < newitem.key
                and self.h[j*2].key <= self.h[j*2 + 1].key):
                self.h[j], j = self.h[j*2], j*2
            elif (    j*2 + 1 < self.heapend
                  and self.h[j*2+1].key < self.h[j*2].key
                  and self.h[j*2+1].key < newitem.key):
                self.h[j], j = self.h[j*2+1], j*2+1
            elif (    j*2 < self.heapend
                  and self.h[j*2].key < newitem.key):
                self.h[j], j = self.h[j*2], j*2
            else:
                break
            #
            print "j is: %d"%j
            print "heapordered(1,%d) is: %s"%(j, self.heapordered(1,j))
            print "isheap(%d,%d) is: %s"%(j,self.heapend,self.isheap(j,self.heapend))
            print
            
        self.h[j] = newitem

    def heap_del_old(self):
        """
        Remove the minimum element from the heap.
        """
        # PROBLEM WITH THIS CODE: we're not swapping the newly promoted
        # item with the smaller of its children?
        # STILL HAVE A PROBLEM?
        # I think I have that problem fixed now, but we may still be
        # "stopping too soon" in the loop.
        #
        # If the heap is: [9, 14, 8, 21, 33, 11, 12]
        # then this operation results in this heap: [8, 14, 12, 21, 33, 11]
        # which is incorrect...
        # I think changing the loop guard, to ( j*2 <= (self.heapend-1) ),
        # dealt with that problem.
        #
        # Now we have another problem:
        #   the code does not swap the element being percolated downwards
        #   with the smaller of the two children!
        #
        #
        # Now we move "down" the heap array, promoting one of the children?
        # self.h[1],heapend = self.h[heapend-1],heapend-1
        print "Removing ", self.h[1].key
        self.h[1] = self.h[self.heapend-1]
        self.heapend = self.heapend-1
        j = 1
        # The loop invariant should probably be something like:
        #   heapordered(1, floor(j/2)) && isheap(j*2, heapend) && isheap(j*2 + 1, heapend)
        #
        # while ( j < (self.heapend // 2) ):
        while ( j*2 <= (self.heapend-1) ):
            # if (self.h[j].key >= self.h[ j*2 ].key):
            #     temp = self.h[ j*2 ]
            #     self.h[ j*2 ] = self.h[j]
            #     self.h[j] = temp
            #     j = j*2
            # elif (    self.h[j].key <= self.h[ j*2 ].key
            #       and ( (j*2+1) <= (self.heapend-1) )
            #       and self.h[ j*2 ].key > self.h[ j*2 + 1 ].key
            #       and self.h[j].key >= self.h[ j*2 + 1 ].key
            #      ):
            #     temp = self.h[ j*2 + 1 ]
            #     self.h[ j*2 + 1 ] = self.h[j]
            #     self.h[j] = temp
            #     j = j*2 + 1
            # else:
            #     break
            #
            if (    (j*2+1) <= (self.heapend-1)
                and self.h[j*2].key <= self.h[j*2+1].key
                and self.h[j].key > self.h[j*2].key     ):
                temp = self.h[ j*2 ]
                self.h[ j*2 ] = self.h[j]
                self.h[j] = temp
                j = j*2
            elif (    (j*2+1) <= (self.heapend-1)
                  and self.h[j*2+1].key < self.h[j*2].key
                  and self.h[j].key > self.h[j*2+1].key  ):
                temp = self.h[ j*2 + 1 ]
                self.h[ j*2 + 1 ] = self.h[j]
                self.h[j] = temp
                j = j*2 + 1
            elif (    (self.heapend-1) < (j*2+1)
                  and self.h[j].key > self.h[j*2].key):
                temp = self.h[ j*2 ]
                self.h[ j*2 ] = self.h[j]
                self.h[j] = temp
                j = j*2
            else:
                break
            # elif ( (self.heapend // 2) <= j ):
            #     break
            print "j is: %d"%j
            print "heapordered(1,%d) is: %s"%((j//2), self.heapordered(1,(j//2)))
            print "isheap(%d,%d) is: %s"%(j*2,self.heapend,self.isheap(j*2,self.heapend))
            print "isheap(%d,%d) is: %s"%(j*2+1,self.heapend,self.isheap(j*2+1,self.heapend))
            print

        # version of the above loop that is incorrect:
#         while ( j < (self.heapend // 2) ):
#             if (self.h[j].key >= self.h[ j*2 ].key):
#                 temp = self.h[ j*2 ]
#                 self.h[ j*2 ] = self.h[j]
#                 self.h[j] = temp
#                 j = j*2
#             elif (self.h[j].key >= self.h[ j*2 + 1 ].key):
#                 temp = self.h[ j*2 + 1 ]
#                 self.h[ j*2 + 1 ] = self.h[j]
#                 self.h[j] = temp
#                 j = j*2 + 1
#         #

# older, incorrect version
#     def heap_del(self):
#         """
#         Remove the minimum element from the heap.
#         """
#         # Now we move "down" the heap array, promoting one of the children?
#         # self.h[1],heapend = self.h[heapend-1],heapend-1
#         self.h[1] = self.h[self.heapend-1]
#         self.heapend = self.heapend-1
#         j = 1
#         while ( j < (self.heapend // 2) ):
#             if (self.h[j].key >= self.h[ j*2 ].key):
#                 temp = self.h[ j*2 ]
#                 self.h[ j*2 ] = self.h[j]
#                 self.h[j] = temp
#             j = ( j*2 )
#         #

class heap_item(object):
    def __init__(self, key = -99):
        self.key = key

    # Comparison operator definitions, so as to make syntax more
    # convenient:
    def __le__(self, other):
        return self.key <= other.key
    def __lt__(self, other):
        return self.key < other.key
    def __ge__(self, other):
        return self.key >= other.key
    def __gt__(self, other):
        return self.key > other.key
    def __eq__(self, other):
        return self.key == other.key
    def __ne__(self, other):
        return self.key != other.key


# So, there would be a pretty nice implementation of what was
# mentioned in the book on software-specifications regarding
# the tallying of distinct values in an array:

def heap_test(arr):
    myHeap = Heap()
    for i in arr:
        myHeap.heap_add(heap_item(i))
        print [ myHeap.h[x].key for x in range(1,myHeap.heapend)]
    #
    print "Before tallying the distinct values, the heap contains:"
    print [ myHeap.h[x].key for x in range(1,myHeap.heapend)]
    #
    last_value = None
    while (myHeap.heapend != 1):
        print [ myHeap.h[x].key for x in range(1,myHeap.heapend)]
        x = myHeap.h[1].key
        if (last_value != x):
            print "Next value is: ", x
            last_value = x
        myHeap.heap_del()

def heapify_test(arr):
    myHeap = Heap()
    for i in range(0,len(arr)):
        myHeap.h[i+1]=heap_item(arr[i])
    myHeap.heapend=len(arr)
    print [myHeap.h[x].key for x in range(1,myHeap.heapend+1)]
    #
    myHeap.heapify()
    print "After heapify operation, here is the heap:"
    print [ myHeap.h[x].key for x in range(1,myHeap.heapend+1)]
    print "Is it a heap?  %s"%myHeap.isheap(1,myHeap.heapend)

def heap_test_driver():
    heap_test([3,6,21,6,3,14,7,8,9])
    print 
    heap_test([18,47,18,16,3,3,6,7,3,9,8,51,105])


def big_heapify_test_new(size):
    myArr = range(size,0,-1)
    myHeap = Heap()
    for i in range(0,len(myArr)):
        myHeap.h[i+1]=heap_item(myArr[i])
    #
    myHeap.heapend=len(myArr)+1
    print [myHeap.h[x].key for x in range(1,myHeap.heapend)]
    #
    myHeap.heapify()
    print [myHeap.h[x].key for x in range(1,myHeap.heapend)]
    print "Is it a heap? %s"%myHeap.isheap(1,myHeap.heapend)
    print myHeap.heapend
    #
    outputArr=[]
    i=1
    limit=myHeap.heapend
    while (i != limit):
        outputArr.append(myHeap.h[1].key)
        myHeap.heap_del()
        if (myHeap.heapend < 11 or myHeap.heapend == 50):
            print [myHeap.h[x].key for x in range(1,myHeap.heapend)]
            print myHeap.heapend
        i = i+1
    #
    print [outputArr[x] for x in range(0,len(outputArr))]

def big_heapify_test_old(size):
    myArr = range(size,0,-1)
    myHeap = Heap()
    for i in range(0,len(myArr)):
        myHeap.h[i+1]=heap_item(myArr[i])
    #
    myHeap.heapend=len(myArr)
    print [myHeap.h[x].key for x in range(1,myHeap.heapend+1)]
    #
    myHeap.heapifyOld()
    print [myHeap.h[x].key for x in range(1,myHeap.heapend+1)]
    print "Is it a heap? %s"%myHeap.isheap(1,myHeap.heapend)
    #
    outputArr=[]
    while (myHeap.heapend!=0):
        outputArr.append(myHeap.h[1].key)
        myHeap.heap_del()
    #
    print [outputArr[x] for x in range(0,len(outputArr))]


