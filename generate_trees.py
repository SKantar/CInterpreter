import os
path = '/home/skantar/Documents/Learning/CInterpreter/examples'

print("PROCESSING...")
for dir_name in sorted(os.listdir(path)):
    print(dir_name)
    dir_path = os.path.join(path, dir_name)
    input_filename = "{}.c".format(os.path.join(dir_path, dir_name))
    dot_filename = "{}.dot".format(os.path.join(dir_path, dir_name))
    png_filename = "{}.png".format(os.path.join(dir_path, dir_name))

    os.system('python genastdot.py {} > {} && dot -Tpng -o {} {}'.format(
        input_filename,
        dot_filename,
        png_filename,
        dot_filename,
    ))
    # break
print("FINISHED")
