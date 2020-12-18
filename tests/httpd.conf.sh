#!/bin/sh

exp_libexecdir=$(apxs -q exp_libexecdir)
curdir=$(dirname "$(readlink -f "$0")")

[ -e "${exp_libexecdir}/mod_unixd.so" ] && cat <<EOF
LoadModule unixd_module "${exp_libexecdir}/mod_unixd.so"
EOF

[ -e "${exp_libexecdir}/mod_log_config.so" ] && cat <<EOF
LoadModule log_config_module "${exp_libexecdir}/mod_log_config.so"
EOF

cat <<EOF
LoadModule mpm_event_module "${exp_libexecdir}/mod_mpm_event.so"
LoadModule authz_core_module "${exp_libexecdir}/mod_authz_core.so"
LoadModule ssl_module "${exp_libexecdir}/mod_ssl.so"
LoadModule headers_module "${exp_libexecdir}/mod_headers.so"
LoadModule proxy_module "${exp_libexecdir}/mod_proxy.so"
LoadModule proxy_http_module "${exp_libexecdir}/mod_proxy_http.so"

ServerRoot "${curdir}"
DocumentRoot "${curdir}"

PidFile httpd.pid
ErrorLog /dev/stderr
TransferLog /dev/stderr
LogLevel trace3
Listen 127.0.0.1:8001

SSLEngine on
SSLCertificateFile "${curdir}/srv.crt"
SSLCertificateKeyFile "${curdir}/srv.key"
SSLCACertificateFile "${curdir}/ca.crt"
SSLVerifyClient optional
SSLVerifyDepth 2

ProxyPass / http://127.0.0.1:8000/
RequestHeader unset CLIENT-CERT-PLAIN
RequestHeader unset CLIENT-CERT-BASE64
RequestHeader unset CLIENT-CERT-ENCODE
RequestHeader set CLIENT-CERT-PLAIN  "%{SSL_CLIENT_CERT}s"
RequestHeader set CLIENT-CERT-BASE64 "expr=%{base64:%{SSL_CLIENT_CERT}s}"
RequestHeader set CLIENT-CERT-ENCODE "expr=%{escape:%{SSL_CLIENT_CERT}s}"
EOF
