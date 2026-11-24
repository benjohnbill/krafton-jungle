#include "rate_limit.h"

#include <math.h>
#include <pthread.h>
#include <stdlib.h>
#include <string.h>

/* Source: token bucket, as in nginx limit_req and Envoy local_ratelimit. */

#define KEY_LEN_MAX 64 /* a longer key is cut; an IPv6 text is 45 bytes */

struct bucket {
    char key[KEY_LEN_MAX];
    double tokens;
    double last; /* the time of the last take: the refill and the forgetting
                    both start from it */
};

struct rate_limit {
    struct rate_limit_options options;
    pthread_mutex_t lock;
    struct bucket *buckets; /* options.key_max slots */
    size_t count;           /* slots in use: buckets[0] to buckets[count - 1] */
};

static struct bucket *bucket_find(struct rate_limit *limit, const char *key);
static struct bucket *bucket_claim(struct rate_limit *limit, const char *key,
                                   double now);
static void bucket_refill(struct bucket *bucket,
                          const struct rate_limit_options *options, double now);
static int bucket_get_wait(const struct bucket *bucket, double rate);

struct rate_limit *rate_limit_create(const struct rate_limit_options *options)
{
    struct rate_limit *limit = calloc(1, sizeof(*limit));
    if (limit == NULL) {
        return NULL;
    }
    limit->options = *options;
    limit->buckets = calloc(options->key_max, sizeof(limit->buckets[0]));
    if (limit->buckets == NULL || pthread_mutex_init(&limit->lock, NULL) != 0) {
        free(limit->buckets);
        free(limit);
        return NULL;
    }

    return limit;
}

void rate_limit_destroy(struct rate_limit *limit)
{
    if (limit == NULL) {
        return;
    }
    pthread_mutex_destroy(&limit->lock);
    free(limit->buckets);
    free(limit);
}

int rate_limit_take(struct rate_limit *limit, const char *key, double now)
{
    /* L3: type mini-webserver/src/rproxy/rate_limit.c:60-77 here. */
    (void)limit;
    (void)key;
    (void)now;

    return 0;
}

static struct bucket *bucket_find(struct rate_limit *limit, const char *key)
{
    for (size_t i = 0; i < limit->count; i++) {
        if (strncmp(limit->buckets[i].key, key, KEY_LEN_MAX - 1) == 0) {
            return &limit->buckets[i];
        }
    }

    return NULL;
}

/* A free slot, or else the slot of the key used longest ago. A new key
   starts with a full bucket. */
static struct bucket *bucket_claim(struct rate_limit *limit, const char *key,
                                   double now)
{
    struct bucket *bucket = &limit->buckets[0];
    if (limit->count < limit->options.key_max) {
        bucket = &limit->buckets[limit->count++];
    } else {
        for (size_t i = 1; i < limit->count; i++) {
            if (limit->buckets[i].last < bucket->last) {
                bucket = &limit->buckets[i];
            }
        }
    }
    strncpy(bucket->key, key, KEY_LEN_MAX - 1);
    bucket->key[KEY_LEN_MAX - 1] = '\0';
    bucket->tokens = limit->options.burst;
    bucket->last = now;

    return bucket;
}

/* rate tokens come back each second, up to burst. */
static void bucket_refill(struct bucket *bucket,
                          const struct rate_limit_options *options, double now)
{
    double tokens = bucket->tokens + (now - bucket->last) * options->rate;
    bucket->tokens = tokens > options->burst ? options->burst : tokens;
    bucket->last = now;
}

/* Whole seconds until the bucket holds one token, at least 1. */
static int bucket_get_wait(const struct bucket *bucket, double rate)
{
    int wait = (int)ceil((1 - bucket->tokens) / rate);

    return wait < 1 ? 1 : wait;
}
