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
      
         # now we have the map
         elif (not map): 
            #issue: Missing a zero at the end of lines 

            # This drops leading zeroes because its an integer
            # decoded = bin(line)
            decoded = bin(int.from_bytes(line, byteorder="big"))
            decoded = str(decoded)
            if (decoded[0:2] == "0b"): 
               decoded = decoded[2:]
            # print(len(decoded))
            # print(len(decoded) % 8)
            # Add back the leading 0 
            while ((len(decoded) % 8) != 0): 
               decoded = "0" + decoded
               # print(decoded)
               # print(len(decoded))
            while (prefix not in lookup_table_codes and len(decoded)): 
               prefix+=decoded[0]
               decoded = decoded[1:]
               if (prefix in lookup_table_codes): 
                  if (lookup_table_codes[prefix] == "newline"): 
                     j.write("\n")
                  elif (lookup_table_codes[prefix] == "colon"): 
                     j.write(":")
                  else: 
                     #print("prefix: " + prefix + " " + lookup_table_codes[prefix])
                     j.write(lookup_table_codes[prefix])
                  prefix = ""
            if (prefix in lookup_table_codes): 
                  if (lookup_table_codes[prefix] == "newline"): 
                     j.write("\n")
                  elif (lookup_table_codes[prefix] == "colon"): 
                     j.write(":")
                  else: 
                     #print("prefix: " + prefix + " " + lookup_table_codes[prefix])
                     j.write(lookup_table_codes[prefix])
                  prefix = ""
            

            #decoding will work because of prefix property!!! 
            

      f.close()
   else: 
      print("Second argument must be either: e, to compress the preceding file or d to decode the preceding file")




  

class letterNode: 
   def __init__(self, character, frequency, isLeaf, leftChild, rightChild):
      self.character = character
      self.frequency = frequency 
      self.isleaf = isLeaf
      self.leftChild = leftChild
      self.rightChild = rightChild

   def returnCharacter(self): 
      return self.character 

   def returnWeight(self): 
      return self.frequency

   def ifIsLeaf(self): 
      return self.isleaf

   def assignLeftChild(self, node): 
      self.leftChild = node
   
   def assignRightChild(self, node): 
      self.rightChild = node

   def returnLeftChild(self): 
      return self.leftChild
   
   def returnRightChild(self): 
      return self.rightChild

class letterTree(): 
   def __init__(self, element, weight, leaf, left, right): 
      self.root = letterNode(element, weight, leaf, left, right)
      self.weight = weight
      self.element = element
      self.leftChild = left
      self.rightChild = right
      self.isleaf = leaf

   def giveWeight(self): 
      return self.weight

   def compareTo(tree): 
      if self.root.weight < tree.weight: 
         return -1
      elif self.root.weight == tree.weight: 
         return 0
      return 1

class PriorityQueue(): 
   def __init__(self): 
      self.queue = []

   def __iter__(self): 
      yield len(self.queue)
      for x in self.queue: 
         yield x 

   def isEmpty(self): 
      if len(self.queue) != 0: 
         return False
      return True

   def insert(self, newLeaf): 
      self.queue.append(newLeaf)    

   def delete(self): 
      #index of max_val
      min_val = 0
      for i in range(len(self.queue)): 
         if self.queue[i].weight < self.queue[min_val].weight:
            min_val = i 
      item = self.queue[min_val]
      del self.queue[min_val]
      return item

   def size(self): 
      return len(self.queue)              

def build_tree_list(character_map): 
   tree_list = PriorityQueue()
   while (len(character_map) > 0): 
      pair = character_map.popitem()
      tree1 = letterTree(pair[0], pair[1], True, None, None)
      tree_list.insert(tree1)
   return tree_list

def build_binary_tree(tree_list): 
   tree3 = None
   while(tree_list.size() > 1): 
      tree1 = tree_list.delete()
      tree2 = tree_list.delete()
      tree3 = letterTree("", tree1.weight+tree2.weight, False, tree1, tree2)
      tree_list.insert(tree3)
   return tree3

def assign_codes(tree, file): 
   
   assign(tree.leftChild, "0")
   assign(tree.rightChild, "1")
   f = open(file, "w")
   # after assigning codes to the children, we should write out that info to a file
   for key in lookup_table_codes.keys(): 
      f.write(lookup_table_codes[key] + ":" + key+"\n")
   f.write ("******************************\n")
   f.close()


   

def assign(tree, val): 
   if (tree.isleaf is True): 
      if (not tree in lookup_table_codes): 
         #(tree.element + " : " + val)
         if (tree.element == "\n"): 
            tree.element = "newline"
         if (tree.element == ":"): 
            tree.element = "colon"
         lookup_table_codes[tree.element] = val
   else: 
      assign(tree.leftChild, val+"0")
      assign(tree.rightChild, val+"1")

def write_compressed_file(input_file, output_file): 
   f = open(input_file, "r")
   j = open(output_file, "ab")
   counter = 0
   byte = ""
   for line in f: 
      #I think the issue happens when we write things with long prefixes...
      for character in line: 
         if (character == "\n"): 
            character = "newline"
         if (character == ":"): 
            character = "colon"
         bits = lookup_table_codes[character]
         # if (character == "I" or character == "f" or character == " "): 
         #    print("checking this situation: " + character)
         #    print(counter)
         if ((counter + len(bits)) <= 8): 
            byte+= bits
            counter+= len(bits)
            # if (character == "I" or character == "f" or character == " "): 
            #    print(byte)
         else:    
            while (counter <= 8 and len(bits)): 
               byte+= bits[0]
               bits = bits[1:]
               counter+=1
               if (counter == 8): 
                  # if (character == "I" or character == "f" or character == " "): 
                  #    print(byte)
                  #    print(bytes([int(byte, 2)]))
                  #    print(bin(int.from_bytes(bytes([int(byte, 2)]), byteorder="big")))
                  arr = bytes([int(byte, 2)])
                  j.write(arr)
                  counter = 0
                  byte = ""
         if (counter == 8): 
            # byte_list = list(byte)
            # for i in range(len(byte_list)): 
            #    byte_list[i] = int(byte_list[i])
            # print(byte_list)
            # if (character == "I" or character == "f" or character == " "): 
            #    print(byte)
            #    print(bytes([int(byte, 2)]))
            #    print(bin(int.from_bytes(bytes([int(byte, 2)]), byteorder="big")))
            arr = bytes([int(byte, 2)])
            j.write(arr)
            counter = 0 
            byte = ""


   #This gives us the bitstring, which now must be broken into bytes 
   # bits = array.array('i', bits)
   # towrite = bits.to_bytes()
   # print(towrite) 
   # j.write(towrite)
   # f.close()
   # j.close()

      
main(sys)

lookup_table_codes.clear()

