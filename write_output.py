# write output file

def dump(output_file_name, time, number_of_atoms, dimensions, configurations):

    output_file = open(output_file_name, 'a')

    output_file.write("ITEM: TIMESTEP\n")
    output_file.write(str(time) + "\n")
    output_file.write("ITEM: NUMBER OF ATOMS\n")
    output_file.write(str(number_of_atoms) + "\n")
    output_file.write("ITEM: BOX BOUNDS pp pp pp\n")
    output_file.write(str(dimensions[0, 0]) + " " + str(dimensions[0, 1]) + "\n")
    output_file.write(str(dimensions[1, 0]) + " " + str(dimensions[1, 1]) + "\n")
    output_file.write(str(dimensions[2, 0]) + " " + str(dimensions[2, 1]) + "\n") 
    output_file.write("ITEM: ATOMS id type x y z\n")
    
    for row in range(len(configurations)):
        for column in range(4):
            output_file.write(str(configurations[row, column]) +" ")
        output_file.write(str(configurations[row, -1]) +"\n")

    output_file.close()

    return None
