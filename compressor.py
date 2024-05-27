#Compressor 
# Anna Leitner, May/June 2024
import sys, os

#Todo: 
# 1. Build binary tree 
# -> Define leaf objects AND also a root that points to the first two leaves
#-> -> Each leaf object should contain a letter and its frequency, and right adn left children 
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
   build_binary_tree(character_map)

class leaf: 
   def __init__(self, character, frequency, isleaf, isroot):
      self.character = character
      self.frequency = frequency 
      self.isleaf = isleaf
      self.isroot = isroot

   def returnCharacter(self): 
      return self.character 

   def returnWeight(self): 
      return self.frequency

   def ifIsLeaf(self): 
      return self.isleaf

   def ifIsRoot(self): 
      return self.isroot

   def assignLeftChild(self, node): 
      self.leftChild = node
   
   def assignRightChild(self, node): 
      self.rightChild = node

   def returnLeftChild(self): 
      return self.leftChild
   
   def returnRightChild(self): 
      return self.rightChild



   
   



def build_binary_tree(character_map): 
   leaf1 = leaf("c", 12, False, True)
   leaf2 = leaf("a", 7, True, False)
   leaf3 = leaf("b", 22, True, False)
   print(leaf1.character)
   print(leaf1.frequency)
   print(leaf1.isroot)
   leaf1.assignLeftChild(leaf2)
   leaf1.assignRightChild(leaf3)
   print(leaf1.leftChild)
   print(leaf1.rightChild)
main(sys)