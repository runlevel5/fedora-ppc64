%global forgeurl https://github.com/actions/runner
# The runner is published framework-dependent against Fedora's .NET, so the
# only native code is the three apphosts, which come prebuilt from the SDK.
%global debug_package %{nil}
# Where the runner keeps its binaries, registration, work folder and logs. It
# finds all of them from the directory its binaries are in, so they share one
# directory; see README.fedora.
%global runnerdir %{_sharedstatedir}/%{name}

Name:           github-actions-runner
Version:        2.338.2
Release:        1%{?dist}
Summary:        Self-hosted runner for GitHub Actions

# runner:                MIT
# bundled .NET packages: MIT, except Apache.Arrow (Apache-2.0) and
#                        Microsoft.AspNet.WebApi.Client, which is under the
#                        Microsoft .NET Library license: redistributable, but
#                        not a free software license. It provides
#                        System.Net.Http.Formatting.dll, which the runner's
#                        HTTP clients are written against. See the Provides
#                        below for the full list.
SourceLicense:  MIT
License:        %{shrink:
    MIT AND
    Apache-2.0 AND
    LicenseRef-Microsoft-DotNet-Library
}
URL:            %{forgeurl}
Source0:        %{forgeurl}/archive/v%{version}/%{name}-%{version}.tar.gz
# The NuGet packages the runner depends on; sources.sh creates it when the
# SRPM is built.
Source1:        %{name}-%{version}-nuget.tar.xz
Source2:        %{name}.service
Source3:        %{name}.sysusers
Source4:        %{name}-config
Source5:        %{name}-service
Source6:        README.fedora

Patch:          0001-Add-ppc64le-and-s390x-to-the-runner-s-architectures.patch
Patch:          0002-Allow-building-from-a-source-tarball-and-for-a-distr.patch
Patch:          0003-Drop-the-bundled-runtime-dependency-check-from-confi.patch
Patch:          0004-Build-against-the-.NET-that-Fedora-ships.patch

# .NET runs on these four, and the runner has no other architecture-specific
# code; the binary release GitHub publishes covers only x86_64 and aarch64.
ExclusiveArch:  %{dotnet_arches}

BuildRequires:  dotnet-sdk-10.0
BuildRequires:  systemd-rpm-macros

Requires:       dotnet-runtime-10.0
# JavaScript actions run on the Node.js in externals/, which this package
# symlinks to Fedora's. Fedora has no Node.js 20, so node20 actions get 22.
Requires:       nodejs22
Requires:       nodejs24
# actions/checkout clones with git when it is there, and falls back to
# downloading a tarball over the API when it is not.
Recommends:     git-core
# Only needed by workflows that use containers or service containers.
Suggests:       podman-docker

Provides:       bundled(dotnet-package(Apache.Arrow)) = 22.1.0
Provides:       bundled(dotnet-package(Azure.Core)) = 1.60.0
Provides:       bundled(dotnet-package(Azure.Storage.Blobs)) = 12.30.0
Provides:       bundled(dotnet-package(Azure.Storage.Common)) = 12.29.0
Provides:       bundled(dotnet-package(Microsoft.AspNet.WebApi.Client)) = 6.0.0
Provides:       bundled(dotnet-package(Microsoft.AspNetCore.WebUtilities)) = 8.0.25
Provides:       bundled(dotnet-package(Microsoft.Bcl.AsyncInterfaces)) = 10.0.9
Provides:       bundled(dotnet-package(Microsoft.DevTunnels.Connections)) = 1.3.60
Provides:       bundled(dotnet-package(Microsoft.DevTunnels.Contracts)) = 1.3.60
Provides:       bundled(dotnet-package(Microsoft.DevTunnels.Management)) = 1.3.60
Provides:       bundled(dotnet-package(Microsoft.DevTunnels.Ssh)) = 3.12.42
Provides:       bundled(dotnet-package(Microsoft.DevTunnels.Ssh.Tcp)) = 3.12.42
Provides:       bundled(dotnet-package(Microsoft.Extensions.Configuration.Abstractions)) = 10.0.9
Provides:       bundled(dotnet-package(Microsoft.Extensions.DependencyInjection.Abstractions)) = 10.0.9
Provides:       bundled(dotnet-package(Microsoft.Extensions.Diagnostics.Abstractions)) = 10.0.9
Provides:       bundled(dotnet-package(Microsoft.Extensions.FileProviders.Abstractions)) = 10.0.9
Provides:       bundled(dotnet-package(Microsoft.Extensions.Hosting.Abstractions)) = 10.0.9
Provides:       bundled(dotnet-package(Microsoft.Extensions.Logging.Abstractions)) = 10.0.9
Provides:       bundled(dotnet-package(Microsoft.Extensions.Options)) = 10.0.9
Provides:       bundled(dotnet-package(Microsoft.Extensions.Primitives)) = 10.0.9
Provides:       bundled(dotnet-package(Microsoft.Identity.Client)) = 4.84.2
Provides:       bundled(dotnet-package(Microsoft.Identity.Client.Extensions.Msal)) = 4.84.2
Provides:       bundled(dotnet-package(Microsoft.IdentityModel.Abstractions)) = 8.14.0
Provides:       bundled(dotnet-package(Microsoft.Net.Http.Headers)) = 8.0.25
Provides:       bundled(dotnet-package(Microsoft.VisualStudio.Validation)) = 17.13.22
Provides:       bundled(dotnet-package(Minimatch)) = 2.0.0
Provides:       bundled(dotnet-package(Newtonsoft.Json)) = 13.0.3
Provides:       bundled(dotnet-package(Newtonsoft.Json.Bson)) = 1.0.2
Provides:       bundled(dotnet-package(System.ClientModel)) = 1.14.0
Provides:       bundled(dotnet-package(System.Diagnostics.EventLog)) = 10.0.9
Provides:       bundled(dotnet-package(System.IO.Hashing)) = 10.0.9
Provides:       bundled(dotnet-package(System.Memory.Data)) = 10.0.9
Provides:       bundled(dotnet-package(System.Security.Cryptography.Pkcs)) = 10.0.13
Provides:       bundled(dotnet-package(System.Security.Cryptography.ProtectedData)) = 10.0.13
Provides:       bundled(dotnet-package(System.ServiceProcess.ServiceController)) = 10.0.9
Provides:       bundled(dotnet-package(YamlDotNet.Signed)) = 5.3.0

%description
The GitHub Actions runner runs the jobs of a GitHub Actions workflow on a
machine you provide, instead of on GitHub's hosted runners. Register it with
a repository, an organisation or an enterprise and jobs that ask for a
self-hosted runner with matching labels are sent to it.

This build comes from source and uses the .NET runtime and the Node.js that
Fedora ships rather than bundling its own, so it also runs on the
architectures GitHub publishes no runner for. Read README.fedora before
registering it; jobs run on this machine with the runner user's privileges.

%prep
%autosetup -n runner-%{version} -N -a1
%autopatch -p1

# Package auditing asks nuget.org about advisories, and the build has no
# network; the package versions are those upstream pinned either way.
sed -i 's|<NuGetAudit>true</NuGetAudit>|<NuGetAudit>false</NuGetAudit>|' \
    src/Directory.Build.props

# Restore from the NuGet packages in Source1 and nowhere else.
cat > src/NuGet.config <<'EOF'
<?xml version="1.0" encoding="utf-8"?>
<configuration>
  <packageSources>
    <clear />
    <add key="local" value="../nuget" />
  </packageSources>
</configuration>
EOF

%build
export DOTNET_CLI_TELEMETRY_OPTOUT=1
export DOTNET_NOLOGO=1
export NUGET_PACKAGES=$PWD/.nuget-packages

cd src
# PackageRuntime names the platform the way upstream does, which is what the
# build constants and the architecture defines key off; PackageRid is the
# runtime identifier of the .NET doing the build, which Fedora names after
# the distribution.
dotnet msbuild -t:Layout ./dir.proj \
    -p:PackageRuntime=linux-%{dotnet_runtime_arch} \
    -p:PackageRid=%{dotnet_runtime_id} \
    -p:BUILDCONFIG=Release \
    -p:RunnerVersion=%{version} \
    -p:RunnerCommitHash=v%{version} \
    -v:minimal

%install
install -d %{buildroot}%{runnerdir}

# The binaries, and the scripts that belong beside them.
cp -a _layout/bin %{buildroot}%{runnerdir}/
# Dependencies come from RPM, the macOS and Windows pieces are of no use here,
# and the release tarball GitHub publishes ships no symbol files either.
rm %{buildroot}%{runnerdir}/bin/installdependencies.sh
rm %{buildroot}%{runnerdir}/bin/actions.runner.plist.template
rm %{buildroot}%{runnerdir}/bin/darwin.svc.sh.template
rm %{buildroot}%{runnerdir}/bin/macos-run-invoker.js
rm %{buildroot}%{runnerdir}/bin/update.cmd.template
rm %{buildroot}%{runnerdir}/bin/*.pdb
# The assemblies come out of their NuGet packages executable.
find %{buildroot}%{runnerdir}/bin -name '*.dll' -exec chmod 0644 {} +

# The scripts that run from the runner's own directory: config.sh and run.sh
# are the commands, and env.sh, run-helper.sh.template and safe_sleep.sh are
# run by them.
install -pm 0755 -t %{buildroot}%{runnerdir} \
    _layout/config.sh _layout/env.sh _layout/run.sh \
    _layout/run-helper.sh.template _layout/safe_sleep.sh

# JavaScript actions run on these. Fedora has no Node.js 20; node20 actions
# get Node.js 22, which is the closest it ships.
install -d %{buildroot}%{runnerdir}/externals/node20/bin
ln -s %{_bindir}/node-22 %{buildroot}%{runnerdir}/externals/node20/bin/node
install -d %{buildroot}%{runnerdir}/externals/node24/bin
ln -s %{_bindir}/node-24 %{buildroot}%{runnerdir}/externals/node24/bin/node

install -Dpm 0755 %{SOURCE4} %{buildroot}%{_bindir}/%{name}-config
install -Dpm 0755 %{SOURCE5} %{buildroot}%{_libexecdir}/%{name}-service
install -Dpm 0644 %{SOURCE2} %{buildroot}%{_unitdir}/%{name}.service
install -Dpm 0644 %{SOURCE3} %{buildroot}%{_sysusersdir}/%{name}.conf
install -pm 0644 %{SOURCE6} .

%check
test "$(_layout/bin/Runner.Listener --version)" = "%{version}"

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
# Deliberately not %%systemd_postun_with_restart: restarting mid-job would
# abandon it. The runner picks the new binaries up when it is next started.
%systemd_postun %{name}.service

%files
%license LICENSE
%doc README.md README.fedora
%{_bindir}/%{name}-config
%{_libexecdir}/%{name}-service
%{_unitdir}/%{name}.service
%{_sysusersdir}/%{name}.conf
# The runner writes its registration, work folder and logs here, so the
# directory belongs to its user; what RPM puts in it belongs to root, so a job
# cannot rewrite the runner it runs under.
%dir %attr(0750,github-actions-runner,github-actions-runner) %{runnerdir}
%{runnerdir}/bin
%{runnerdir}/externals
%{runnerdir}/*.sh
%{runnerdir}/run-helper.sh.template

%changelog
* Tue Nov 03 2026 Trung Lê <8@tle.id.au> - 2.338.2-1
- Initial package
