#include "stdio.h"
#include "stdlib.h"
#include "time.h"
#include "float.h"
#include <string.h>
#include <math.h>
#include <errno.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/ipc.h>
#include <sys/shm.h>
//#include <stdatomic.h>
#define mb()    asm volatile("mfence":::"memory")
#define rmb()   asm volatile("lfence":::"memory")
#define wmb()   asm volatile("sfence" ::: "memory")

#include "utils.c"
#include "core.c"

#define MAXCHANNELS 72

//========== SIMULATION PARAMETERS:
int n=50;
double D=1.0;
int dims=10;//25;//100;
int ddims=10;//25;//100;

//========== IPC DATAS:
long cores;
int* workspace;
int* parameterspace;
double* resultspace;
int child;
int parent;

//========== PARENT DATA:
int* work_program;
char output_file_name[80];

void output_data() {
	FILE *fp = fopen(output_file_name, "w");
	double v;
	fprintf(fp, "{\"config\":{\"n\":%i,\"D\":%f,\"dims\":%i,\"ddims\":%i},\"data\":{\n",n,D,dims,ddims);
	for (int s=0; s<dims+1; s++) {
		for (int y=0; y<dims+1; y++) {
			if (s>=y) {
				for (int dd=0; dd<=ddims; dd++) {
					v = resultspace[(s*(dims+1)+y)*(ddims+1)+dd];
					fprintf(fp, "\"(%f,%f,%f)\":%f", s*D*D/(4*dims),y*D*D/(4*dims),dd*D/(2*ddims),v);
					if (!((s==dims) && (y==dims) && (dd==ddims))) {
						fprintf(fp,",\n");
					}
				}
			}
		}
	}
	fprintf(fp, "\n}}");
	fclose(fp);
}

void debugprint() {
	for (int i = 0; i < cores+1; i++) {
		printf("%i ",workspace[i]);
	}
	printf("\n");
}

void loop() {
	int* command = &workspace[0];
	int* state = &workspace[child+1];
	int* s_int = &parameterspace[child*2];
	int* y_int = &parameterspace[child*2+1];
	double s, y;
	int ss_int, yy_int;
	int all_done,work_to_be_done,allocated,completed;
	completed=0;
	while (*command != -1) {
		if ((*state == 0) && (*command == 1) && (*s_int >= 0) && (*y_int >= 0)) {
			*state = 1;
			ss_int = *s_int;
			yy_int = *y_int;
			*s_int = -1;
			*y_int = -1;
			s = ss_int * D*D/(4*dims);
			y = yy_int * D*D/(4*dims);
			for (int dd=0; dd<=ddims; dd++)
				resultspace[(ss_int*(dims+1)+yy_int)*(ddims+1)+dd] = run_f(s,y,D,dd*D/(2*ddims),n);
			*state = 2;
			//printf("child %i finished: ", child);
			//debugprint();
		}
		if (parent) {
			all_done = 1;
			for (int i = 0; i < cores; i++) {
				if (workspace[i+1]!=2)
					all_done=0;
			}
			if (all_done==1) {
				//printf("parent detects all done: ");
				//debugprint();
				*command=0;
				work_to_be_done = 0;
				for (int i=0; i<cores; i++) {
					allocated = 0;
					for (int ss_int = 0; ((ss_int <= dims) && (allocated==0)); ss_int++) {
						for (int yy_int = 0; ((yy_int <= dims) && (allocated==0)); yy_int++) {
							if ((ss_int>=yy_int) && (work_program[ss_int*(dims+1)+yy_int]==0)) {
								parameterspace[2*i]   = ss_int;
								parameterspace[2*i+1] = yy_int;
								work_program[ss_int*(dims+1)+yy_int]=1;
								workspace[i+1] = 0;
								allocated=1;
								work_to_be_done+=1;
							}
						}
					}
				}
				completed += work_to_be_done;
				printf("%.2f%% complete\n",100*completed*2.0/((dims+1)*(dims+2)));
				if (work_to_be_done >0) {
					*command=1;
				} else {
					*command=-1;
				}
				//printf("parent commands issued: ");
				//debugprint();
			}
		}
	}
	if (parent) {
		output_data();
		while(wait(NULL)>0);
	}
}


void memory_allocate(char* key) {
	cores = sysconf(_SC_NPROCESSORS_ONLN);
	workspace = (int*)salloc(key,'z',sizeof(int)*(cores+1),0666|IPC_CREAT);
	parameterspace = (int*)salloc(key,'z',sizeof(int)*(2*cores),0666|IPC_CREAT);
	resultspace = (double*)salloc(key,'z',sizeof(double)*((dims+1)*(dims+1)*(ddims+1)),0666|IPC_CREAT);
	for (int i =1; i<cores+1; i++)
		workspace[i]=2;
}
void parent_memory_allocate() {
	work_program = (int*)calloc(sizeof(int),(dims+1)*(dims+1));
}
void memory_free() {
	sfree(workspace);
	sfree(parameterspace);
	sfree(resultspace);
}
void parent_memory_free() {
	free(work_program);
}

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
	memory_allocate(argv[0]);
	pid_t p = 999;
	child=0;
	while ((child < cores-1) && (p > 0)) {
		p = fork();
		if (p==-1) {
			perror("fork");
			exit(1);
		} else if (p>0) {
			child++;
		}
	}
	parent = (p==0) ? 0 : 1;
	clock_t t;
	if (parent) {
		t = clock();
		parent_memory_allocate();
	}
	loop();
	memory_free();
	if (parent) {
		parent_memory_free();
		printf("Execution time: %fs\n",(1.0*clock()-t)/CLOCKS_PER_SEC);
	}
	return 0;
}
