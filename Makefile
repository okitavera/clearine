ifeq ($(PREFIX),)
	PREFIX := /usr
endif

.PHONY: install
install:
	install -d $(DESTDIR)$(PREFIX)/bin
	install -d $(DESTDIR)/etc
	install -d $(DESTDIR)$(PREFIX)/share/themes/Clearine-Fallback/clearine
	install -m 644 data/clearine.conf $(DESTDIR)/etc/
	install -m 644 data/theme-default/*.svg $(DESTDIR)$(PREFIX)/share/themes/Clearine-Fallback/clearine/
	install -m 755 clearine.py $(DESTDIR)$(PREFIX)/bin/clearine

.PHONY: uninstall
uninstall:
	test -e $(DESTDIR)$(PREFIX)/bin/clearine && rm $(DESTDIR)$(PREFIX)/bin/clearine || exit 0
	test -d $(DESTDIR)$(PREFIX)/share/themes/Clearine-Fallback && rm -rf $(DESTDIR)$(PREFIX)/share/themes/Clearine-Fallback || exit 0
	test -d $(DESTDIR)/etc/clearine.conf && rm $(DESTDIR)/etc/clearine.conf || exit 0
