# TestTaskPython
Test task implementation for STM Labs

## Quickstart
* **git clone https://github.com/murzinov01/TestTaskPython.git**
* **cd TestTaskPython**
* **py main.py file_to_data ip_type**  

Examples:
 *   **py main.py data/ipv4_data_set.txt ipv4**
 *   **py main.py data/ipv6_data_set.txt ipv6**

You can also check test coverage by the following instruction:  
In TestTaskPython directory:
* **cd test**
* **py input_tests.py**
* **py regression_tets.py**

## Time complexity of the algorithm
I believe that the complexity of my algorithm is estimated at worst as O(4*N + N) ~ O(N) in the case of ipv4 and as O(8*N + N) ~ O(N) in the case of ipv6 + small overhead for data preprocessing and transformations for correct output. I am not doing a complete search of all possible subnet masks and multiplying them by the ip addresses of the input data. My algorithm finds the first different part of the ip address (O(4N) for ipv4 or O(8N) for ipv6), and then finds the maximum value in this part among all the data addresses by a simple linear search (O(N)). I know that here it would be possible to use the binary search and simplify the complexity to O (log2*(N)). After that, I calculate the number of ones for the subnet mask and the subnet itself.
