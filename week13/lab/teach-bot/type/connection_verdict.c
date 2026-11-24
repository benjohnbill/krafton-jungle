#include "connection_verdict.h"

#include <stddef.h>

struct connection_rule {
    bool (*matches)(const struct connection_signals *signals);
    enum connection_verdict verdict;
};

static bool ip_is_listed(const struct connection_signals *signals);
static bool key_is_blocked(const struct connection_signals *signals);

static const struct connection_rule connection_rules[] = {
    {ip_is_listed, CONN_DROP},
    {key_is_blocked, CONN_DROP},
};

enum connection_verdict
connection_decide(const struct connection_signals *signals)
{
    size_t count = sizeof(connection_rules) / sizeof(connection_rules[0]);
    for (size_t i = 0; i < count; i++) {
        if (connection_rules[i].matches(signals)) {
            return connection_rules[i].verdict;
        }
    }

    return CONN_PASS;
}

static bool ip_is_listed(const struct connection_signals *signals)
{
    return signals->is_listed;
}

static bool key_is_blocked(const struct connection_signals *signals)
{
    return signals->is_blocked;
}
