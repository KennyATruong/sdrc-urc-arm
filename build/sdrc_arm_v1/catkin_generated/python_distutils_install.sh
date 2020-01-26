#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
    DESTDIR_ARG="--root=$DESTDIR"
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/kenny/sdrc-urc-arm/src/sdrc_arm_v1"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/kenny/sdrc-urc-arm/install/lib/python2.7/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/kenny/sdrc-urc-arm/install/lib/python2.7/dist-packages:/home/kenny/sdrc-urc-arm/build/sdrc_arm_v1/lib/python2.7/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/kenny/sdrc-urc-arm/build/sdrc_arm_v1" \
    "/usr/bin/python2" \
    "/home/kenny/sdrc-urc-arm/src/sdrc_arm_v1/setup.py" \
    build --build-base "/home/kenny/sdrc-urc-arm/build/sdrc_arm_v1" \
    install \
    $DESTDIR_ARG \
    --install-layout=deb --prefix="/home/kenny/sdrc-urc-arm/install" --install-scripts="/home/kenny/sdrc-urc-arm/install/bin"
