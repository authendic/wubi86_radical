
wubi86.pyz:
	python -m zipapp . -m 'wubi86:main' -o $@ -p "/usr/bin/env python"
	chmod +x $@
	python $@ 字

check:
	python -m wubi86 字

clean:
	rm -f *.pyz
