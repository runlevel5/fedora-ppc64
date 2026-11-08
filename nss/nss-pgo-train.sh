#!/bin/bash
# PGO training workload for NSS: key generation and certificate creation in a
# softoken database, then TLS 1.2 and 1.3 full and resumed handshakes with RSA
# and ECDSA certificates over loopback, which run libssl, libnss, pk11wrap,
# certdb and libpkix. freebl and softoken are built without the profile, so
# their primitives are not trained here.
# Usage: nss-pgo-train.sh <bin dir> <lib path>
set -e
B=$1
export LD_LIBRARY_PATH=$2
export NSS_IGNORE_SYSTEM_POLICY=1
W=$(mktemp -d)
trap 'kill $SP 2>/dev/null || true; wait 2>/dev/null; rm -rf "$W"' EXIT
cd "$W"

mkdir db
head -c 1024 /dev/urandom > noise
$B/certutil -N -d db --empty-password
$B/certutil -S -x -d db -n rsa -m 1 -s "CN=localhost" -t "CTu,u,u" -k rsa -g 2048 -z noise -v 12 > /dev/null 2>&1
$B/certutil -S -x -d db -n ec -m 2 -s "CN=localhost" -t "CTu,u,u" -k ec -q nistp256 -z noise -v 12 > /dev/null 2>&1

P=$(( 20000 + RANDOM % 20000 ))
$B/selfserv -d db -p $P -n rsa -e ec -u -t 8 > selfserv.log 2>&1 &
SP=$!
for i in $(seq 50); do
  $B/tstclnt -h localhost -p $P -d db -o -q > /dev/null 2>&1 && break
  sleep 0.2
done

# strsclnt's exit status reflects its session-cache statistics, not whether
# the handshakes worked, so check the summary it prints instead: full
# handshakes report the certificates tested, resumptions the resumes.
C() {
  if $B/strsclnt -p $P -d db -o -q -t 4 "$@" localhost 2>&1 |
     grep -qE "server certificates tested|[1-9][0-9]* stateless resumes"; then
    echo 1 >> tested
  fi
}
C -N -c 300
C -N -c 300 -J ecdsa_secp256r1_sha256
C -c 600
C -N -c 200 -V tls1.2:tls1.2
C -N -c 200 -V tls1.2:tls1.2 -C :C02F
C -N -c 200 -C :1303
C -N -c 200 -C :1302

n=$(awk '{s+=$1} END {print s+0}' tested 2>/dev/null || echo 0)
echo "nss-pgo-train: $n of 7 strsclnt runs completed"
[ "$n" -eq 7 ]
