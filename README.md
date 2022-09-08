# Checkpoints:

1. Customer Satisifaction and Public safety
2. Time Complexity 
3. Space Complexity

# Assumptions:

Based on our human experience I have considered below factors inorder to satisfy customer :

1. Seating Arrangement based on First Come - First Serve
2. Normal consideration of distance to screen 
3. Group splitting - (Suppose if a person is booking >1 ticket and based on the seat availability the algorithm tries to assign both the seats side by side)
4. Public safety (covid rules in consideration)(three seats buffer)


# Instructions:

1. To develop an algorithm that assign seats based on reservation requests
2. To start with, I created a function for groups ( One single reservation)
3. Order in which reservation requests are received(first come first serve)
4. Each line in the file will be comprised of a reservation identifier
5. Code and Seat reservations should be followed by a space
6. Number of seats requested
7. The reservation identifier will have the format: R####.
8. Each row in the file should include the reservation number followed by a space, and then a comma-delimited list of the assigned seats for the output file
9. The command for executing the program should accept the complete path to the input file as an argument and should return the full path to the output file.




# Testcases:

I have created a separate input file i.e input_file-testing.txt with random seat reservations and checked with the multiple use cases.