#include <sys/types.h>
#include <unistd.h>
#include <stdio.h>

int main() {
	pid_t pid_parent = getpid(); // Ran as first instruction -> will get process_id of the process which will later be the parent
	
	fork(); // syscall that will create a replica of this program running as a process
	
	if(getpid() == pid_parent) {
		printf("This is the parent process [PID = %d]\n", getpid());
	} else {
		printf("This is the child process [PID = %d]\n", getpid());
	}

	while(1) {
		sleep(1);
	}

	return 0;
}
