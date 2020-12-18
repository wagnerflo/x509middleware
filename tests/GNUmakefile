.PHONY: certs httpd

certs: ca.crt ca.key
certs: srv.key srv.crt
certs: client.key client.crt

%.key:
	openssl genrsa -out $@ 2048

ca.crt: ca.key
	openssl req -new \
	  -days 365 -nodes -x509 \
	  -subj "/O=CA" \
	  -key $< -out $@

%.csr: %.key %.conf
	openssl req -new \
	  -days 365 -nodes \
	  -config $(word 2,$^) \
	  -key $< -out $@

%.crt: %.csr %.conf ca.crt ca.key
	openssl x509 \
	  -req -extensions req_ext -extfile $(word 2,$^) \
	  -CA $(word 3,$^) -CAkey $(word 4,$^) -CAcreateserial \
	  -in $< -out $@

httpd.conf: httpd.conf.sh
	sh $< > $@

httpd: httpd.conf srv.crt srv.key
	$(shell apxs -q sbindir)/$(shell apxs -q progname) -X -f $(CURDIR)/$<
