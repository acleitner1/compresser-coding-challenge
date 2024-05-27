#Compressor 
# Anna Leitner, May/June 2024
import sys, os

#Todo: 
# 1. Build binary tree 
#->-> Put the leaf objects into a PQ organized by frequency 
#->-> remove the two trees with the lowest weights 
#->-> create a new tree (weight sum of children) with those two trees as children and continue until all trees have been combined into one 
# 2. Generate prefix codes based on binary tree 
# 3. Header section for output file
# 4. Encode text using code table and write it to output file 
#     -> Be sure to translate prefixes into bit string and pack into bytes to achieve compression 
# 5. Read header and rebuild prefix table 
# 6. Decode the text and write it to specified output file.
#     -> If this works, should be able to take a file, encode it, check that the new file is smaller 
#        than the original, then decode that file into a file identical to the original. 
def main(input): 
   # Main function: It has been a long time since I did anything in python....
   if len(input.argv) != 2: 
      raise Exception("Must include 1 and only 1 file")
   file = input.argv[1] 
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
   #build priority queue
   tree_list = build_tree_list(character_map)
   build_binary_tree(tree_list)

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

   def giveWeight(self): 
      return self.weight

   def compareTo(tree): 
      if self.root.weight < tree.weight: 
         return -1
      elif self.root.weight == tree.weight: 
         return 0
      return 1

class PrioirityQueue(): 
   def __init__(self): 
      self.queue = []

   def isEmpty(self): 
      if len(self.queue) != 0: 
         return False
      return True

   def insert(self, newLeaf): 
      self.queue.append(newLeaf)    

   def delete(self): 
      #index of max_val
      max_val = 0
      for i in range(len(self.queue)): 
         if self.queue[i] > self.queue[max_val].frequency: 
            max_val = i 
      item = self.queue[max_val]
      del self.queue[max_val]
      return item

   def size(self): 
      return len(self.queue)              

def build_tree_list(character_map): 
   tree_list = PrioirityQueue()
   while (len(character_map) > 0): 
      pair = character_map.popitem()
      tree1 = letterTree(pair[0], pair[1], True, None, None)
      tree_list.insert(tree1)
   return tree_list

def build_binary_tree(leaf_list): 
   return
   # root = leaf("", 0, True, False)
   # while(leaf_list.size() > 1): 
   #    leaf1 = leaf_list.delete()
   #    leaf2 = leaf_list.delete()
   #    leaf3 = leaf()
      
main(sys)