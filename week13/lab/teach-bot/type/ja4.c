#include "ja4.h"
#include "client_hello.h"

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <openssl/sha.h>

/* Source: FoxIO JA4 rules, technical_details/JA4.md. */

#define COUNT_MAX 99 /* a count is two digits */
#define HASH_LEN 12  /* the first 12 hex characters of SHA-256 */
#define HASH_TEXT_MAX 2048
#define EXTENSION_SNI 0x0000
#define EXTENSION_ALPN 0x0010

static size_t list_copy_without_grease(uint16_t *list, const uint16_t *values,
                                       size_t count);
static bool value_is_grease(uint16_t value);
static void alpn_format(const struct client_hello *hello, char *alpn);
static void cipher_hash_format(uint16_t *ciphers, size_t count, char *hash);
static int value_compare(const void *left, const void *right);
static void list_append_text(char *text, const uint16_t *values, size_t count);
static void text_hash_format(const char *text, char *hash);
static void extension_hash_format(const struct client_hello *hello,
                                  const uint16_t *extensions, size_t count,
                                  char *hash);
static bool extensions_has(const uint16_t *extensions, size_t count,
                           uint16_t value);
static const char *version_get_text(const struct client_hello *hello);
static size_t count_get_capped(size_t count);

/* ======================== Main Function ================================= */

void ja4_format(const struct client_hello *hello, char *ja4)
{
    uint16_t ciphers[CLIENT_HELLO_CIPHER_MAX];
    size_t cipher_count =
        list_copy_without_grease(ciphers, hello->ciphers, hello->cipher_count);
    uint16_t extensions[CLIENT_HELLO_EXTENSION_MAX];
    size_t extension_count = list_copy_without_grease(
        extensions, hello->extensions, hello->extension_count);

    char alpn[3];
    alpn_format(hello, alpn);
    char cipher_hash[HASH_LEN + 1];
    cipher_hash_format(ciphers, cipher_count, cipher_hash);
    char extension_hash[HASH_LEN + 1];
    extension_hash_format(hello, extensions, extension_count, extension_hash);

    char sni =
        extensions_has(extensions, extension_count, EXTENSION_SNI) ? 'd' : 'i';
    snprintf(ja4, JA4_LEN + 1, "t%s%c%02zu%02zu%s_%s_%s",
             version_get_text(hello), sni, count_get_capped(cipher_count),
             count_get_capped(extension_count), alpn, cipher_hash,
             extension_hash);
}

/* ======================== Helper Function ================================= */

static size_t list_copy_without_grease(uint16_t *list, const uint16_t *values,
                                       size_t count)
{
    size_t kept = 0;
    for (size_t i = 0; i < count; i++) {
        if (!value_is_grease(values[i])) {
            list[kept++] = values[i];
        }
    }

    return kept;
}

/* GREASE (RFC 8701): 0x0a0a, 0x1a1a, ... 0xfafa. */
static bool value_is_grease(uint16_t value)
{
    return (value & 0x0f0f) == 0x0a0a && (value >> 8) == (value & 0xff);
}

/* The first and last character of the first ALPN value. If one of them is
   not alphanumeric, the first and last hex digit of the two bytes. */
static void alpn_format(const struct client_hello *hello, char *alpn)
{
    if (hello->alpn_len == 0) {
        strcpy(alpn, "00");
        return;
    }
    unsigned char first = hello->alpn[0];
    unsigned char last = hello->alpn[hello->alpn_len - 1];
    if (isalnum(first) && isalnum(last)) {
        alpn[0] = (char)first;
        alpn[1] = (char)last;
        alpn[2] = '\0';
        return;
    }
    char first_hex[3];
    char last_hex[3];
    snprintf(first_hex, sizeof(first_hex), "%02x", first);
    snprintf(last_hex, sizeof(last_hex), "%02x", last);
    alpn[0] = first_hex[0];
    alpn[1] = last_hex[1];
    alpn[2] = '\0';
}

/* The ciphers sorted. No ciphers give twelve zeros. */
static void cipher_hash_format(uint16_t *ciphers, size_t count, char *hash)
{
    if (count == 0) {
        strcpy(hash, "000000000000");
        return;
    }
    qsort(ciphers, count, sizeof(ciphers[0]), value_compare);
    char text[HASH_TEXT_MAX] = "";
    list_append_text(text, ciphers, count);
    text_hash_format(text, hash);
}

static int value_compare(const void *left, const void *right)
{
    uint16_t left_value = *(const uint16_t *)left;
    uint16_t right_value = *(const uint16_t *)right;

    return (left_value > right_value) - (left_value < right_value);
}

/* Appends "1301,1302,..." (4 lowercase hex digits each) to text. */
static void list_append_text(char *text, const uint16_t *values, size_t count)
{
    size_t len = strlen(text);
    for (size_t i = 0; i < count; i++) {
        len += (size_t)snprintf(text + len, HASH_TEXT_MAX - len, "%s%04x",
                                i == 0 ? "" : ",", values[i]);
    }
}

/* The first 12 hex characters of SHA-256 of text. */
static void text_hash_format(const char *text, char *hash)
{
    unsigned char digest[SHA256_DIGEST_LENGTH];
    SHA256((const unsigned char *)text, strlen(text), digest);
    for (size_t i = 0; i < HASH_LEN / 2; i++) {
        snprintf(hash + 2 * i, 3, "%02x", digest[i]);
    }
}

/* The extensions sorted, without SNI and ALPN, then "_" and the signature
   algorithms in the order of the wire. No signature algorithms: no "_".
   No extensions left: twelve zeros. */
static void extension_hash_format(const struct client_hello *hello,
                                  const uint16_t *extensions, size_t count,
                                  char *hash)
{
    uint16_t hashed[CLIENT_HELLO_EXTENSION_MAX];
    size_t hashed_count = 0;
    for (size_t i = 0; i < count; i++) {
        if (extensions[i] != EXTENSION_SNI && extensions[i] != EXTENSION_ALPN) {
            hashed[hashed_count++] = extensions[i];
        }
    }
    if (hashed_count == 0) {
        strcpy(hash, "000000000000");
        return;
    }
    qsort(hashed, hashed_count, sizeof(hashed[0]), value_compare);
    char text[HASH_TEXT_MAX] = "";
    list_append_text(text, hashed, hashed_count);

    uint16_t signatures[CLIENT_HELLO_SIGNATURE_MAX];
    size_t signature_count = list_copy_without_grease(
        signatures, hello->signatures, hello->signature_count);
    if (signature_count > 0) {
        strcat(text, "_");
        list_append_text(text, signatures, signature_count);
    }
    text_hash_format(text, hash);
}

static bool extensions_has(const uint16_t *extensions, size_t count,
                           uint16_t value)
{
    for (size_t i = 0; i < count; i++) {
        if (extensions[i] == value) {
            return true;
        }
    }

    return false;
}

/* The highest value of supported_versions, else the legacy version. */
static const char *version_get_text(const struct client_hello *hello)
{
    uint16_t version = 0;
    for (size_t i = 0; i < hello->version_count; i++) {
        uint16_t value = hello->versions[i];
        if (!value_is_grease(value) && value > version) {
            version = value;
        }
    }
    if (version == 0) {
        version = hello->legacy_version;
    }
    switch (version) {
    case 0x0304:
        return "13";
    case 0x0303:
        return "12";
    case 0x0302:
        return "11";
    case 0x0301:
        return "10";
    case 0x0300:
        return "s3";
    case 0x0002:
        return "s2";
    case 0xfeff:
        return "d1";
    case 0xfefd:
        return "d2";
    case 0xfefc:
        return "d3";
    default:
        return "00";
    }
}

static size_t count_get_capped(size_t count)
{
    return count > COUNT_MAX ? COUNT_MAX : count;
}
