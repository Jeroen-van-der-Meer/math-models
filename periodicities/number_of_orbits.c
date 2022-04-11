#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>

int f(int x) {
	int fx = x*x + 1;
	return fx;
}

void update_values(bool* arr, int* indices, int limit) {
	// Set arr[i] to true for the first i values in the indices array
	for (int i = 0; i < limit; i++) {
		arr[indices[i]] = true;
	}
}

int stable_orbits(int N) {
	// Given N, count the number of stable orbits mod N
	bool *found_in_orbit;
	found_in_orbit = (bool *) malloc(sizeof(bool) * N);
	for (int i = 0; i < N; i++) {
		found_in_orbit[i] = false;
	}
	int count = 0; // Number of stable orbits
	int x; // Variable when simulating dynamical system
	int step; // Keeps track of how long a simulated system has been running
	int *temp_values; // For keeping track of the values met while simulating
	temp_values = (int *) malloc(sizeof(int) * N);

	for (int start_value = 0; start_value < N; start_value++) {
		if (found_in_orbit[start_value] == false) {
			// Initiate some values
			x = start_value;
			step = 1;
			temp_values[0] = x;

			for (;;) { // Keep going with the simulation until we've either found a loop or a value that has already been considered
				step += 1;
				x = f(x) % N;
				if (found_in_orbit[x]) { // Already in an orbit that we've found before?
					// We must now register all temp_values into the found_in_orbit class since we don't need to consider them again
					update_values(found_in_orbit, temp_values, step);
					goto next_start_value; 
				}

				for (int j = 0; j < step; j++) { // Check if we've landed in a loop
					if (temp_values[j] == x) { 
						count += 1; // If we've encountered a loop then it must a new one, so increase the count by 1
						// We must now register all temp_values into the found_in_orbit class since we don't want to encounter them again
						update_values(found_in_orbit, temp_values, step);
						goto next_start_value;
					}
				}

				temp_values[step] = x; // If we keep going then we must add x to the temporary list
			}
		}
next_start_value:
	}
	return count;
}

int main() {    
	for (int n = 0; n < 2000; n++) {
		int out = stable_orbits(n);
		printf("%d ", out);
	}
	return 0;
}
