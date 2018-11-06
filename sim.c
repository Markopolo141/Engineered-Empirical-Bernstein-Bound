#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

//========== COMMAND LINE INPUT PARAMETERS
int n;
int dims;
int ddims;

//========== SIMULATION PARAMETERS:
double D=1.0;
double phi_iterator=0.0009999;

//========== CORE PROCEDURES
#include "core.c"

//========== DATAS:
char output_file_name[80];


// the main loop - computes all the data and interatively outputs it to a JSON formatted file
void run() {
	// open the file and print the JSON header
	FILE *fp = fopen(output_file_name, "w");
	fprintf(fp, "{\"config\":{\"n\":%i,\"D\":%f,\"dims\":%i,\"ddims\":%i},\"data\":{\n",n,D,dims,ddims);
	
	double s, y, d, v;
	for (int s_int = 0; s_int <= dims; s_int++) { // for all indices of variances s
		printf("%.2f%% complete\n",s_int*100.0/dims);
		for (int y_int = 0; y_int <= dims; y_int++) { // for all indices of offsets y
			
			if (s_int>=y_int) { // if the variance is greater than the offset
				s = s_int * D*D/(4*dims); // calculate the variance
				y = y_int * D*D/(4*dims); // calculate the offset
				for (int dd=0; dd<=ddims; dd++) { // for all indicies of bound offsets d
					d = dd*D/(2*ddims); // calculate the bound offset d
					if (s<=D*D*d*(1-d)) { // if the variance and data offset are possible
						v = run_f(s,y,D,d,n); // calculate the EBB
						fprintf(fp, "\"(%f,%f,%f)\":%f", s,y,d,v); // print it to the JSON file
						if (!((s_int==dims) && (y_int==dims) && (dd==ddims))) {
							fprintf(fp,",\n"); // print JSON commas where necessary
						}
					}
				}
			}
		}
	}
	// print JSON closing braces and close file
	fprintf(fp, "\n}}");
	fclose(fp);
}


// the main method - parses command line arguments, computes results, and outputs.
int main(int argc, char *argv[]) {
	if (argc!=4) {
		printf("needs three arguments\n");
		return 0;
	}
	n = atoi(argv[1]);
	dims = atoi(argv[2]);
	ddims = atoi(argv[3]);
	if ((n==0)||(dims==0)||(ddims==0)) {
		printf("arguments must be numbers\n");
		return 0;
	}
	printf("Compiling variance bound -- n=%i,dims=%i,ddims=%i \n",n,dims,ddims);
	sprintf(output_file_name,"data%i_%i_%i.json",n,dims,ddims);
	clock_t t;
	t = clock();
	run();
	printf("Execution time: %fs\n",(1.0*clock()-t)/CLOCKS_PER_SEC);
	return 0;
}
