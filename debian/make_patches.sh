#!/bin/bash
#
# Replaces debian/patches/*.patch with patches generated by git-format-patch
#
# Copyright (C) 2011 Benoît Knecht <benoit.knecht@fsfe.org>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. Neither the name of the University nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# Usage: ./make_patches.sh ${upstream_branch} ${debian_branch}
#
#        This script should only be run if you cloned the git repository of the
#        minidlna debian package, and wish to generate the patches needed to
#        build the package. The patches are written to debian/patches/.
#
#        WARNING: Patches in debian/patches/ may be overwritten, if they happen
#        to have the same name as git-format-patch wants to use; patches that
#        do not follow git-format-patch's naming scheme are not deleted. The
#        debian/patches/series file is overwritten, and will contain the list
#        of generated patches.
#
#        If ${debian_branch} is not specified, it defaults to 'master', and if
#        ${upstream_branch} is also missing, it defaults to 'dfsg'.
#        make_patches.sh can be run from anywhere within the git repository.

upstream=${1:-dfsg}
debian=${2:-master}

cd $(git rev-parse --show-toplevel) || exit 1

paths=$(git ls-tree -r --name-only ${debian} | egrep -v '^debian')

git format-patch -o debian/patches -k --no-signature \
    ${upstream}..${debian} ${paths} |
    xargs debian/mbox2dep3.py |
    xargs -L1 basename > debian/patches/series
