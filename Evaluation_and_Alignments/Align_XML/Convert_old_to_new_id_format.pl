## convert the ids in the old Text+Berg XML files
## into ids in the new format

## Example: 
## --> OLD
##     <s lang="de" n="1-3">
##        <w lemma="du" n="1-3-1" pos="PPER">Du</w>

## --> NEW
##     <s lang="de" n="a1-s3">
##        <w lemma="du" n="a1-s3-w1" pos="PPER">Du</w>

while (<>) {
	if (/<article /) {
		s/ n="(\d+)"/ n="a$1"/;
	}
	elsif (/<s /) {
		s/ n="(\d+)-(\d+)"/ n="a$1-s$2"/;
	}
	elsif (/<w /) {
		s/ n="(\d+)-(\d+)-(\d+)"/ n="a$1-s$2-w$3"/;
	}
	
	print $_;
}