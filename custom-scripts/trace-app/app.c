#include <stdio.h>
#include <pthread.h>
#include <semaphore.h>
#include <string.h>

#define THREADS 3
#define BUFFER_SIZE 1000

char buffer[BUFFER_SIZE];
int size = 0;

pthread_barrier_t barrier;
pthread_mutex_t mutex;
pthread_mutexattr_t attr;

void *task(void *arg)
{
	pthread_barrier_wait(&barrier);

	int tid;
	tid = (int)(long int)arg;

	char id = 'A' + tid;

	char id_str[2];
	id_str[0] = id;
	id_str[1] = '\0';

	while (1)
	{
		pthread_mutex_lock(&mutex);
		if (size >= BUFFER_SIZE - 1) {
			pthread_mutex_unlock(&mutex);
			break;
		}
		strncat(buffer, id_str, 1);
		size++;
		pthread_mutex_unlock(&mutex);
	}
}

int main(void)
{
	long int i;
	pthread_t threads[THREADS];

	pthread_mutex_init(&mutex, &attr);
	pthread_barrier_init(&barrier, NULL, THREADS);

	for (i = 0; i < THREADS; i++) {
		pthread_create(&threads[i], NULL, task, (void *)i);
	}

	for (i = 0; i < THREADS; i++) {
		pthread_join(threads[i], NULL);
	}

	pthread_barrier_destroy(&barrier);

	printf("%s\n", buffer);

	return 0;
}

//gcc app.c -O2 -o appGcc -lpthread
//taskset -c 0 ./appGcc