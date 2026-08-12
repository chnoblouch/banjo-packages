#include <curl/curl.h>

#undef CURL_GLOBAL_SSL
#undef CURL_GLOBAL_WIN32
#undef CURL_GLOBAL_ALL
#undef CURL_GLOBAL_ACK_EINTR

#define CURL_GLOBAL_SSL 0x00000001
#define CURL_GLOBAL_WIN32 0x00000002
#define CURL_GLOBAL_ACK_EINTR 0x00000004
#define CURL_GLOBAL_ALL 0x00000003

CURLcode curl_easy_setopt_l(CURL *handle, CURLoption option, long long parameter);
CURLcode curl_easy_setopt_p(CURL *handle, CURLoption option, void *parameter);
CURLcode curl_easy_setopt_s(CURL *handle, CURLoption option, const char *parameter);
