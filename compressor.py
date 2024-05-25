#Compressor 
# Anna Leitner, May/June 2024
import sys, os

#Todo: 
# 1. Build binary tree 
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


def build_binary_tree(character_map): 
   #TODO 
   return
# Call main on command line input 
main(sys)