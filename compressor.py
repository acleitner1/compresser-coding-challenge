#Compressor 
# Anna Leitner, May/June 2024
# Provides options to compress and decompress files (Huffman Method)
# In order to compress a file, simply call "python3 compressor.py" followed by the 
# name of the file to be compressed and the letter "e," and, optionally, the name of a file 
# to which to write the compressed output. 
# TO Decompress a file, call "python3 compressor.py" folllowed by the name of the file to be 
# decompressed, the letter "d," and, optionally, the name of a file to which to write the decompressed 
# output. 

import sys, os, array

# Global prefix to character dictionary
lookup_table_codes = {}


# Defines a node within a binary tree
class letterNode: 
   # Initializes attributes 
   def __init__(self, character, frequency, isLeaf, leftChild, rightChild):
      self.character = character
      self.frequency = frequency 
      self.isleaf = isLeaf
      self.leftChild = leftChild
      self.rightChild = rightChild

   # Returns the character/string associated with a node 
   def returnCharacter(self): 
      return self.character 

   # Returns the weight of a node
   def returnWeight(self): 
      return self.frequency

   # Returns if a node is a leaf
   def ifIsLeaf(self): 
      return self.isleaf

   # Assigns the node the given left child 
   def assignLeftChild(self, node): 
      self.leftChild = node
   
   # Assigns the node the given right child 
   def assignRightChild(self, node): 
      self.rightChild = node

   # Returns the node's left child 
   def returnLeftChild(self): 
      return self.leftChild
   
   # Return the node's right child
   def returnRightChild(self): 
      return self.rightChild


# Defines a binary tree built of letter nodes 
class letterTree(): 
   # Initalizer 
   def __init__(self, element, weight, leaf, left, right): 
      self.root = letterNode(element, weight, leaf, left, right)
      self.weight = weight
      self.element = element
      self.leftChild = left
      self.rightChild = right
      self.isleaf = leaf

   # Returns the weight of the tree
   def giveWeight(self): 
      return self.weight

   # Provides functionality to compare two tree based on weight 
   def compareTo(tree): 
      if self.root.weight < tree.weight: 
         return -1
      elif self.root.weight == tree.weight: 
         return 0
      return 1


# Defines a Minimum Priority Queue
class PriorityQueue(): 
   # Innitializer
   def __init__(self): 
      self.queue = []

   # Allows Priority Queue Objects to be iterated through 
   def __iter__(self): 
      yield len(self.queue)
      for x in self.queue: 
         yield x 

   # Returns if the queue is empty 
   def isEmpty(self): 
      if len(self.queue) != 0: 
         return False
      return True

   # Adds an element to the queue
   def insert(self, newLeaf): 
      self.queue.append(newLeaf)    

   # Deletes and returns the minimum element in the queue 
   def delete(self): 
      min_val = 0

      for i in range(len(self.queue)): 
         if self.queue[i].weight < self.queue[min_val].weight:
            min_val = i 

      item = self.queue[min_val]
      del self.queue[min_val]
      return item

   # Returns the size of the priority queue
   def size(self): 
      return len(self.queue) 

def main(input): 
   if len(input.argv) < 3: 
      raise Exception("Must include at least a file to read and if file should be compressed or decompressed")
   file = input.argv[1] 

   # Option to Encode File
   if (input.argv[2] == "e"): 
      f = open(file, "r") 
      character_map = {}

      # Read file and note the occurence of each character 
      for line in f: 
         for character in line: 
            if character in character_map: 
               character_map[character] = character_map[character]+ 1 
            else: 
               character_map[character] = 1 
      f.close()

      # Build priority queue
      tree_list = build_tree_list(character_map)

      # Build binary tree 
      tree_tree = build_binary_tree(tree_list)

      # Create output file if one doesn't already exist 
      output_file = file + ".output.txt"
      if len(input.argv) > 3: 
         output_file = input.argv[3]
      
      # Assigns codes and writes them to the above output file
      assign_codes(tree_tree, output_file)

      #Write the compressed into the output file 
      write_compressed_file(file, output_file)

   # Option to decode a compressed/encoded file 
   elif input.argv[2] == "d": 
      f = open(file, "rb")
      character_map = {}
      map = 1
      printer = 0 
      prefix = ""
      output_file = file + "output.txt"

      if len(input.argv) > 3: 
         output_file = input.argv[3]
      j = open(output_file, "w")

      # Read header to build character lookup table, then unpack 
      # bytes into characters based on contents of the table
      for line in f: 
         check_line = str(line)
         if (check_line.find("******************************") != -1): 
            map = 0
            continue

          # Build lookup table by reading file header
         if (map): 
            decoded = line.decode('utf8')
            character_bool = 0
            key = ""
            val = ""
            splitter = decoded.split(':')
            val = splitter[1][:-1]
            lookup_table_codes[splitter[0]] = val
      
         # Read bytes and convert back into characters 
         elif (not map): 
            # This drops leading zeroes because its an integer
            decoded = bin(int.from_bytes(line, byteorder="big"))
            decoded = str(decoded)
            if (decoded[0:2] == "0b"): 
               decoded = decoded[2:]
            
            # Add back leading zeroes dropping by the conversion from bytes to ints
            while ((len(decoded) % 8) != 0): 
               decoded = "0" + decoded
            
            # Build a prefix until it matches a prefix read from the file's header
            while (prefix not in lookup_table_codes and len(decoded)): 
               prefix+=decoded[0]
               decoded = decoded[1:]
               if (prefix in lookup_table_codes): 
                  if (lookup_table_codes[prefix] == "newline"): 
                     j.write("\n")
                  elif (lookup_table_codes[prefix] == "colon"): 
                     j.write(":")
                  else: 
                     j.write(lookup_table_codes[prefix])
                  prefix = ""

            # Write characters to output file when prefix is found      
            if (prefix in lookup_table_codes): 
                  if (lookup_table_codes[prefix] == "newline"): 
                     j.write("\n")
                  elif (lookup_table_codes[prefix] == "colon"): 
                     j.write(":")
                  else: 
                     j.write(lookup_table_codes[prefix])
                  prefix = ""
      f.close()
   else: 
      print("Second argument must be either: e, to compress the preceding file or d to decode the preceding file")


# Puts items in a character frequency map into a priority queue
# Returns the priority queue
def build_tree_list(character_map): 
   tree_list = PriorityQueue()

   # Creates tree objects for each character and puts them into the priority queue
   while (len(character_map) > 0): 
      pair = character_map.popitem()
      tree1 = letterTree(pair[0], pair[1], True, None, None)
      tree_list.insert(tree1)
   return tree_list


# Builds a binary tree out of a priority queue and returns its root 
def build_binary_tree(tree_list): 
   tree3 = None

   # Iterates through priority queue and builds binary tree
   while(tree_list.size() > 1): 
      tree1 = tree_list.delete()
      tree2 = tree_list.delete()
      tree3 = letterTree("", tree1.weight+tree2.weight, False, tree1, tree2)
      tree_list.insert(tree3)
   return tree3


# Traverses a binary tree, assigns weight based codes to its leaves 
# and writes those codes to a given file 
def assign_codes(tree, file): 
   # Recursively assign codes to children of root node
   assign(tree.leftChild, "0")
   assign(tree.rightChild, "1")
   f = open(file, "w")

   # After assigning codes to the children, write out that info to a file
   for key in lookup_table_codes.keys(): 
      f.write(lookup_table_codes[key] + ":" + key+"\n")
   f.write ("******************************\n")
   f.close()
  

# Recursively assign codes to the children of a node 
# If node has no children, assign it a code
# Each left child adds a 0 to the code, each right child adds a 1
# Each leaf will have a unique code that is not a prefix of another 
# code because all prefix-codes are internal tree nodes not associated with 
# a character 
def assign(tree, val): 

   # Only assign codes to leaf nodes 
   # Base case 
   if (tree.isleaf is True): 
      if (not tree in lookup_table_codes): 
         if (tree.element == "\n"): 
            tree.element = "newline"
         if (tree.element == ":"): 
            tree.element = "colon"
         lookup_table_codes[tree.element] = val
   else: 
      assign(tree.leftChild, val+"0")
      assign(tree.rightChild, val+"1")


# Packs characters from input file into bytes built out of their 
# binary prefix codes. More frequently used characters are associated with 
# shorter codes of less than 8 bits, resulting in compression when codes are 
# packed into bytes 
def write_compressed_file(input_file, output_file): 
   f = open(input_file, "r")
   j = open(output_file, "ab")
   counter = 0
   byte = ""

   # Read input file 
   for line in f: 
      for character in line: 
         if (character == "\n"): 
            character = "newline"
         if (character == ":"): 
            character = "colon"
         bits = lookup_table_codes[character]

         # Pack bits into a byte before writing it to the output file 
         if ((counter + len(bits)) <= 8): 
            byte+= bits
            counter+= len(bits)
         else:    
            while (counter <= 8 and len(bits)): 
               if (counter == 8): 
                  arr = bytes([int(byte, 2)])
                  j.write(arr)
                  counter = 0
                  byte = ""
               byte+= bits[0]
               bits = bits[1:]
               counter+=1

# Calls main function and clears lookup table codes after running  
main(sys)
lookup_table_codes.clear()

