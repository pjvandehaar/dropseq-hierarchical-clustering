#!/bin/bash
set -euo pipefail

/users/pjvh/binf527-proj/writable/STAR-2.5.2b/bin/Linux_x86_64_static/STAR \
    --genomeDir /users/pjvh/binf527-proj/writable/mouseref/index \
    --genomeLoad LoadAndExit
