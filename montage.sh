#!/bin/sh

TMPDIR=`mktemp -d`

GENERATORS=`python2.5 <<EOF
from model.generator_factory import GeneratorFactory
gf = GeneratorFactory()
gf.rated_list()
for n in map(lambda g: g.get_name(), gf.rated_list()): print n
EOF`

PNG_FILE="static/images/generators.png"
CSS_FILE="static/css/generators.css"

make_png() {
    echo "creating $PNG_FILE"
    COUNT=0
    for G in $GENERATORS; do
	NAME=`printf "%0.3d.$G" $COUNT`
	./generators/process_interface.py print generators/$G.py | sed 's/xlink:href=\"\/images\//xlink:href=\"static\/images\//g' > $TMPDIR/$NAME.svg
	inkscape $TMPDIR/$NAME.svg -z -a 0:-20:300:220 -h 80 -e $TMPDIR/$NAME.png > /dev/null 2>&1
	COUNT=`expr $COUNT + 1`
    done
    montage $TMPDIR/*.png -geometry 100x80+0+0 -tile $COUNT $TMPDIR/montage.png

    mv $TMPDIR/montage.png $PNG_FILE
}

make_css() {
    echo "creating $CSS_FILE"
    echo "
 #carousel-arrow {
     vertical-align      : middle;
     padding             : 2px 2px 2px 2px;
 }

 #carousel-wrapper {
     width               : 760px;
     height              : 80px;
     overflow            : hidden;
 }

 .thumb {
     width               : 100px;
     height              : 80px;
     display             : block;
     background-image    : url('/images/generators.png');
     background-repeat   : no-repeat;
 }

 .slide {
     width               : 100px;
     height              : 80px;
 }

 .list_image {
     border-style        : outset;
     border-color        : black;
     border-width        : 1px;
 }" > $TMPDIR/list.css
    POS=0
    SIZE=0
    for G in $GENERATORS; do
	echo "
 .gen_$G {
     background-position : -${POS}px 0px;
 }" >> $TMPDIR/list.css
	POS=`expr $POS + 100`
	SIZE=`expr $SIZE + 110`
    done
    echo "
 #carousel-content {
     width               : ${SIZE}px;
 }" >> $TMPDIR/list.css

    mv $TMPDIR/list.css $CSS_FILE
}

if [ "x$1" = "xforce" ]; then
    make_png
    make_css
    exit 0
fi

if ! [ -e $PNG_FILE ]; then
    make_png
fi

if ! [ -e $CSS_FILE ]; then    
    make_css
fi

exit 0
