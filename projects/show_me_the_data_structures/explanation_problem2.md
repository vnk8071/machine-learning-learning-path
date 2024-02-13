# Finds all files with a given suffix in a specified directory and its subdirectories.

Time Complexity: The time complexity of the function is O(n), where n is the total number of files and directories in the specified path. This is because the function uses os.walk(), which generates the file names in a directory tree by walking the tree either top-down or bottom-up. For each directory in the tree rooted at directory top (including top itself), it produces a 3-tuple (dirpath, dirnames, filenames). The function then checks each file name to see if it ends with the specified suffix.

Space Complexity: The space complexity of the function is also O(n), where n is the total number of files and directories in the specified path. This is because os.walk() generates a list of 3-tuples, and the function creates a list of file paths. In the worst-case scenario (every file has the specified suffix), the list of file paths will have as many elements as there are files.
