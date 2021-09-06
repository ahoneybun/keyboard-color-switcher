#
# Regular cron jobs for the keyboard-color-switcher package
#
0 4	* * *	root	[ -x /usr/bin/keyboard-color-switcher_maintenance ] && /usr/bin/keyboard-color-switcher_maintenance
