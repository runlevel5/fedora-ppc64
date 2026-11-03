#!/bin/sh
# Run by .copr/Makefile after the remote sources are downloaded, with the spec
# as $1: restore the NuGet packages the runner depends on into Source1, so the
# RPM builds offline.
#
# The restore has to see the same projects the build does, so the spec's
# patches are applied first. It runs on whichever architecture builds the
# SRPM, which need not be the one the RPM is built on; that is fine, because
# the only packages the runtime identifier chooses between are the .NET
# framework packs, and those come from the SDK rather than from here.
set -eu

spec=$1
specdir=$(cd "$(dirname "$spec")" && pwd)
version=$(rpmspec -q --srpm --qf '%{version}' "$spec")

dnf -y install dotnet-sdk-10.0 patch

work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
tar -xzf "$specdir/github-actions-runner-$version.tar.gz" -C "$work"
cd "$work/runner-$version"
for p in "$specdir"/*.patch; do patch -p1 -i "$p"; done

export DOTNET_CLI_TELEMETRY_OPTOUT=1
export DOTNET_NOLOGO=1

cd src
for proj in Sdk Runner.Common Runner.Listener Runner.Worker \
            Runner.PluginHost Runner.Sdk Runner.Plugins; do
    dotnet restore "$proj/$proj.csproj" \
        -r "$(rpm --eval '%{dotnet_runtime_id}')" \
        --packages "$work/packages" -v:quiet
done

mkdir "$work/nuget"
find "$work/packages" -name '*.nupkg' -exec cp -t "$work/nuget" {} +
tar -cJf "$specdir/github-actions-runner-$version-nuget.tar.xz" -C "$work" nuget
