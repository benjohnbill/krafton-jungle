#include <stdio.h>
#include <pthread.h>

int shared_counter = 0;  // 힙/데이터 영역 — 모든 쓰레드가 공유

void *worker(void *arg) {
    int id = *(int *)arg;          // 매개변수는 각자 스택에 따로 존재
    for (int i = 0; i < 100000; i++) {
        shared_counter++;          // 공유 변수를 각자 건드림
    }
    printf("쓰레드 %d 종료, counter = %d\n", id, shared_counter);
    return NULL;
}

int main() {
    pthread_t t1, t2;
    int id1 = 1, id2 = 2;

    pthread_create(&t1, NULL, worker, &id1);  // 쓰레드 1 생성
    pthread_create(&t2, NULL, worker, &id2);  // 쓰레드 2 생성

    pthread_join(t1, NULL);  // 두 쓰레드가 끝날 때까지 메인이 대기
    pthread_join(t2, NULL);

    printf("최종 counter = %d\n", shared_counter);
    return 0;
}
