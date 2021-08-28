from sys import argv
import urllib.request as urq
import os

# Collect only image files. If set to False forces script to collect all files
ONLY_IMAGES = True

# @argv[1]: input filename with URLs passed as argument to the script
# This parameter is mandatory
if len(argv) > 1:
    # Input file
    in_file = argv[1]

    # @argv[2]: path to the folder for collected files to be placed
    # if omited or folder does not exist, the current folder is used by default
    if len(argv) > 2 and os.path.exists(argv[2]):
        out_dir = os.path.abspath(argv[2])
    else:
        out_dir = os.path.abspath('.')

    # Is the input file exist?
    if(os.path.isfile(in_file)):
        with open(in_file, 'r', encoding='utf-8') as f:
            i = 1

            # @url: line from the input file containing URL
            for url in f:
                u = url.strip() # URL without ending newline character

                # URL to the file may contain no file extension or it may point to the script generating an image
                # Thus, the type of the file can not be determined properly only by URL. To collect only images it is needed to know
                # the MIME type of the retrieved file
                try:
                    # @temp_fn: retrieved file stores in the temporary folder by default
                    # @info: file information variable
                    temp_fn, info = urq.urlretrieve(u)

                    # Is it the type of file is an image or not? Or other files is also allowed
                    if info.get_content_maintype() == 'image' or not ONLY_IMAGES:
                        # Output filename with proper image file extension
                        out_fn = os.path.abspath(out_dir + '/' + str(i) + '.' + info.get_content_subtype())

                        # Rename and move file to the output folder
                        os.rename(temp_fn, out_fn)

                        i += 1

                        # Logging information: source URL and new filename
                        print(u + '\t', out_fn)

                    # Removing temporary non-image file
                    else:
                        os.remove(temp_fn)
                        print(u + '\t\tNot an image!')

                except urq.URLError:
                    print(u + '\t\tError retriving!')

    else:
        print('Cannot open file "' + in_file + '". File not found or it is not a file.')

# Help information
else:
    print('Usage: python', argv[0], '<input_file> <output_folder>')
    print('<input_file> is a plaintext file containing URLs, one per line.')
    print('[output_folder] path to the folder for storing downloaded content.')
    print('If omitted or folder is not exist, the current folder is used.')
