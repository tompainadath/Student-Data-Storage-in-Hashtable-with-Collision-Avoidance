################################################################################
### Name: Tom Painadath
### Description: This program simulates packets of data arriving at irregular times. The data
###              gets read from the file and is placed in a queue where it waits for its turn
###              to get processed. The "processing" happens in a threaded subroutine called 
###              "process_input_data". This function pulls data fromthe queue, hash the
###              student ID number and then store the data in a hashtable. Hashing of the 
###              student ID is done by first fiding the module 100000 of student ID and subtracting
###              it from student ID which is then divided 10000 to extract first 5 numbers. 
###              This was then used as Hash key. The program does deals with collisions by creating 
###              a linked list. If collisions occur a new node is added at the index of hash table
###              and data is stored. Finally, proved that the hash table works by retrieving and 
###              printing information about students with the following IDs:
###
###              427980112
###              258399712
###              948140115
###              Used the same method used to find the Hash key was used on these IDs
################################################################################

# import the libraries needed to make all this work
import time
import os
from threading import Thread

# let the program know where you've put the data file
myDir = '/home/tuf94311/ece_3822/Project 3'
filename = 'student_data.txt'

class LinkedList:
    # linked list class inits to an empty pointer
    def __init__(self):
        self.head = None

    # to push a new student, first create a node, then place that node at the
    # front of the linked list
    def push(self,newStudent):
        newNode = Node(newStudent)  # create a node to be pushed on to LL
        newNode.next = self.head  # push that node onto LL
        self.head = newNode  # set the head of LL to new node
    
    # to print the list
    def printList(self):
        currNode = self.head  # set current node as head
        while (currNode != None):  # check if current node is empty
            print(currNode.student)  # if empty print the data in current node
            currNode = currNode.next  # set current to next node
    
    # to find the student by id        
    def find_id(self,id):
        currNode = self.head  # set current node as head
        while (currNode != None):  # check if current node has data
            if (int(currNode.student.studentID) == id):  # if current node has data check the studentID is the same as ID provided
                # customer has been found
                print(currNode.student)  # print student data
                return  # exit from function
            currNode = currNode.next  # set current node as next next node
        print("customer", id, "not found")  # if ID not found print this

# Create a Node class
class Node:
    # create the nodes for the linked list
    def __init__(self,student):
        self.student = student
        self.next = None

# create a class of type "student" that holds the data fields for each student.
# add whatever methods you see fit
class student:

    # DEFINE A CLASS TO HOLD STUDENT DATA
    # Create a constructor
    def __init__(self,  firstname = '', lastname = '', gpa= 0.0, studentID = 0, major = ''):
        self.firstname = firstname
        self.lastname = lastname
        self.studentID = studentID
        self.gpa = gpa
        self.major = major
    
    # String output
    def __str__(self):
        return ( self.firstname + " " + self.lastname + " " + str(self.studentID) + " " + str(self.gpa) + " " + self.major) #+ " " + str(hex(id(self))))
    
# this function will pop students out of the queue and place them in the hash
# table, which is to be a global variable called "hash_table"
def process_input_data(stop):
    global student_queue, hash_table
    
    hash_table = [None]*100000  # Create Hash table with size of 50000
    # for loop to add a linked list at each index of hashtable 
    for i in range (len(hash_table)):
        hash_table[i] = LinkedList()    
    # to read data from student_queue
    while not stop() or len(student_queue)>0:
        if len(student_queue)>0 :

            # POP ITEMS FROM QUEUE AND
            student_data = student_queue.pop()
            
            # PUT THEM IN THE HASH TABLE
            hash_student(student_data)
            
# To find key and push it to hashtable            
def hash_student(student_data):
    key = student_key(student_data.studentID)  # call student_key function to find key
    hash_table[key].push(student_data)  # push new student on the appropriate LL in hashtable index

# To find key
def student_key(studentID):
    # Extract the first 5 numbers of student ID, store it in key and return
    return((int(studentID) - (int(studentID) % 100000))//10000)

# To find student using ID    
def student_lookup(studentID):
    key = student_key(studentID)  # call student_key function to find key
    hash_table[key].find_id(studentID)  # call find_id function to find student in the linked list at hashtable index

def main():
    global student_queue
    student_queue = []

    # set up the thread so that it can process students once they're in the queue.
    # do not modify this
    stop_threads = False
    thr = Thread(target=process_input_data,args =(lambda : stop_threads, ))
    thr.start()


    # load data from file, enforcing delays in order to simulate
    # asynchronous data arrivals
    os.chdir(myDir)
    with open(filename,'r') as infile:
        # mark the initial time
        tStart = time.time()

        # for each line in the input file...
        for line in infile:

            # ... split the line into its components, and then ...        
            t, firstname, lastname, gpa, id_nmbr, mjr = line.split()

            # ... wait until the elapsed time matches the 'arrival' time of the
            #     line of data in the text file. This is how we are simulating
            #     data packets arriving at irregular times.
            while ((time.time()-tStart)< float(t)):
                pass

            # when it's time, create a new object of type "student" and push
            # it onto the queue
            
            # CREATE OBJECT USING  NAMES, GPA, ID, MAJOR, & PUSH IT TO student_queue
            newstudent = student(firstname, lastname,gpa, id_nmbr, mjr)
            
            student_queue.append(newstudent)  # Add the data to queue one by one

    # this is needed to stop the process_input_data function once all the data
    # has been read from the file into the queue
    stop_threads = True
    thr.join() 
    
    # code to search the hash table for the students with these student IDs
    # and to print all their information
    ###     427980112
    ###     258399712
    ###     948140115

    # FIND STUDENTS AND PRINT THEIR INFO
    
    student1_ID = 427980112
    student2_ID = 258399712
    student3_ID = 948140115
    
    student_lookup(student1_ID)
    student_lookup(student2_ID)
    student_lookup(student3_ID)

if __name__== "__main__":
    main()
