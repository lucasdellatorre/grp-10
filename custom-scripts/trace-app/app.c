#include <stdio.h>
#include <pthread.h>
#include <semaphore.h>
#include <string.h>

#define THREADS 5

char buffer[2048];

pthread_barrier_t barrier;

void *task(void *arg)
{
	pthread_barrier_wait(&barrier);

	int tid;
	int cont = 5;
	tid = (int)(long int)arg;

	char id = 'A' + tid;

	char id_str[2];
	id_str[0] = id;
	id_str[1] = '\0';

	for (int i = 0; i < cont; i++) {
		strncat(buffer, id_str, 1);
	}
}

int main(void)
{
	long int i;
	pthread_t threads[THREADS];

	pthread_barrier_init(&barrier, NULL, THREADS);

	for (i = 0; i < THREADS; i++)
		pthread_create(&threads[i], NULL, task, (void *)i);

	pthread_barrier_wait(&barrier);

	for (i = 0; i < THREADS; i++) {
		pthread_join(threads[i], NULL);
	}

	// Clean up the barrier
	pthread_barrier_destroy(&barrier);

	printf("%s\n", buffer);

	return 0;
}

//gcc app.c -O2 -o appGcc
//usar semaforo