import sys

dump_file = sys.argv[-1]

with open(dump_file, "w") as f:
	for path in sys.path:
		f.write( path + "," )

exit()