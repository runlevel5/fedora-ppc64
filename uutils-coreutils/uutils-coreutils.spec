%bcond check 1
%bcond all_tests 0

%if 0%{?el9}
# systemd is too old
%bcond systemd_logind 0
%else
%bcond systemd_logind 1
%endif

%if %{with systemd_logind}
%global feature_flags feat_os_unix,feat_selinux,openssl,feat_systemd_logind,uudoc
%else
%global feature_flags feat_os_unix,feat_selinux,openssl,uudoc
%endif

# Peak memory usage is (on x86_64) roughly 4–5 GB in two parallel rustc
# processes, building the uudoc and coreutils crates. This is OK on the
# primary-architecture koji builders, but on more severely memory-constrained
# systems (like some in RISC-V koji) this may cause swapping or memory
# exhaustion. Setting a conservative memory limit per process helps.
%global _smp_tasksize_proc 8192

Name:           uutils-coreutils
Version:        0.13.0
Release:        1%{?dist}
Summary:        GNU coreutils reimplementation in Rust

SourceLicense:  MIT
# (MIT OR Apache-2.0) AND Unicode-3.0
# (MIT OR Apache-2.0) AND Unicode-DFS-2016
# (MIT OR Apache-2.0) AND Zlib
# Apache-2.0
# Apache-2.0 OR Apache-2.0 WITH LLVM-exception
# Apache-2.0 OR GPL-2.0-only
# Apache-2.0 OR MIT
# Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT
# BSD-2-Clause OR Apache-2.0 OR MIT
# CC0-1.0
# ISC
# MIT
# MIT OR Apache-2.0
# MIT-0 OR Apache-2.0
# Unicode-3.0
# Unlicense OR MIT
# Zlib
License:        %{shrink:
    MIT
    AND (MIT OR Apache-2.0)
    AND Unicode-DFS-2016
    AND Zlib
    AND Apache-2.0
    AND (Apache-2.0 OR Apache-2.0 WITH LLVM-exception)
    AND (Apache-2.0 OR GPL-2.0-only)
    AND (Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT)
    AND (BSD-2-Clause OR Apache-2.0 OR MIT)
    AND CC0-1.0
    AND ISC
    AND (MIT-0 OR Apache-2.0)
    AND Unicode-3.0
    AND (Unlicense OR MIT)
}
# LICENSE.dependencies contains a full license breakdown

URL:            https://uutils.github.io/coreutils/
Source:         https://github.com/uutils/coreutils/archive/%{version}/%{name}-%{version}.tar.gz
# disable benchmarks
# drop notify's macos_kqueue feature
# build the openssl feature against the system OpenSSL: drop the openssl
#   crate's vendored feature
Patch:          coreutils-fix-metadata.diff

# leaf package, SIGABRT on compile
ExcludeArch:    %{ix86}

BuildRequires:  cargo-rpm-macros
BuildRequires:  rust2rpm-helper
%if %{with systemd_logind}
BuildRequires:  systemd-devel
%endif

%description
uutils coreutils is a cross-platform reimplementation of the GNU coreutils in
Rust. While all programs have been implemented, some options might be missing or
different behavior might be experienced.


%prep
%autosetup -p1 -n coreutils-%{version}
%cargo_prep

# borrowed from ruff

# Patch out foreign (e.g. Windows-only) dependencies. Follow symbolic links so
# that we also patch the bundled crates we just finished setting up.
find -L . -type f -name Cargo.toml -print \
    -execdir rust2rpm-helper strip-foreign -o '{}' '{}' ';'

%generate_buildrequires
%cargo_generate_buildrequires -f %{feature_flags}


%build
%cargo_build -f %{feature_flags}
%{cargo_license_summary -f %{feature_flags}}
%{cargo_license -f %{feature_flags}} > LICENSE.dependencies
mkdir -p data/man/man1
mkdir -p data/completions/{bash,fish,zsh}

for utility in $(target/rpm/coreutils --list); do
  target/release/uudoc manpage $utility > data/man/man1/uu_${utility}.1
  for s in bash zsh; do
    target/release/uudoc completion $utility $s > data/completions/$s/uu_${utility}
  done
  target/release/uudoc completion $utility fish > data/completions/fish/uu_${utility}.fish
done
target/release/uudoc manpage coreutils > data/man/man1/uutils-coreutils.1
for s in bash zsh; do
  target/release/uudoc completion coreutils $s > data/completions/$s/uutils-coreutils
done
target/release/uudoc completion coreutils fish > data/completions/fish/uutils-coreutils.fish


%install
install -Dpm 0755 target/rpm/coreutils -T %{buildroot}%{_bindir}/uutils-coreutils
for utility in $(target/rpm/coreutils --list); do
  ln -sr %{buildroot}%{_bindir}/uutils-coreutils  %{buildroot}%{_bindir}/uu_$utility
done
mkdir -p %{buildroot}%{_mandir}/man1
cp -p data/man/man1/* %{buildroot}%{_mandir}/man1/
mkdir -p %{buildroot}%{bash_completions_dir}
mkdir -p %{buildroot}%{fish_completions_dir}
mkdir -p %{buildroot}%{zsh_completions_dir}
cp -p data/completions/bash/* %{buildroot}%{bash_completions_dir}/
cp -p data/completions/fish/* %{buildroot}%{fish_completions_dir}/
cp -p data/completions/zsh/* %{buildroot}%{zsh_completions_dir}/


%if %{with check}
%check
# test_cksum::test_openssl_link expects this when OpenSSL is linked dynamically
export OPENSSL_NO_VENDOR=1
%if %{with all_tests}
%{cargo_test -f %{feature_flags}}
%else
# * --test-threads 1: tests fail with permission denied error if run with too
#   many threads (currently not needed)
# * test_cp: operation not supported
# * test_df: needs an actual filesystem to test
# * test_du: expected sublink/symlink in output
# * test_ls: need block/char device
# * test_od: s390x failures, see
#   https://github.com/uutils/coreutils/issues/9017#issuecomment-4148721220
# * various color and localization tests: the translations embedded in the
#   binary are English and $LANG's (C.UTF-8 in the build root), so the French
#   ones are missing
# * SELinux tests: SELinux is not enabled in the build root
# * test_cp sparse/reflink, test_du dereference: depend on the build root's
#   filesystem
# * test_hostname::test_hostname_ip: no network
# * test_logname: no login session
# * test_tee pipe and /dev/full errors: fail in the build root
# %%ifarch is not processed inside %%{shrink:...}, so the s390x skips are kept
# in a macro defined here
%ifarch s390x
%global arch_skips %{shrink:
    --skip test_od::test_od_options_after_filename
    --skip test_od::test_suppress_duplicates
}
%endif
%{cargo_test -f %{feature_flags} -- -- %{shrink:
    --skip test_cat::test_write_fast_read_error
    --skip test_chcon::role_change
    --skip test_chmod::test_chmod_colored_output
    --skip test_cp::test_copy_dir_preserve_permissions_inaccessible_file
    --skip test_cp::test_cp_debug_sparse_source::case_09_sparse_always_zeros_then_data
    --skip test_cp::test_cp_dest_no_permissions
    --skip test_cp::test_cp_preserve_selinux
    --skip test_cp::test_cp_preserve_selinux_admin_context
    --skip test_cp::test_cp_readonly_dest_with_existing_file
    --skip test_cp::test_cp_readonly_dest_with_reflink
    --skip test_cp::test_cp_readonly_source_and_dest
    --skip test_cp::test_cp_reflink_insufficient_permission
    --skip test_cp::test_cp_reflink_never
    --skip test_cp::test_cp_selinux
    --skip test_cp::test_cp_selinux_context_priority
    --skip test_cp::test_cp_selinux_empty_context
    --skip test_cp::test_cp_selinux_invalid
    --skip test_cp::test_cp_selinux_recursive
    --skip test_cp::test_cp_sparse_always_empty
    --skip test_cp::test_cp_sparse_always_non_empty
    --skip test_date::test_date_for_no_permission_file
    --skip test_date::test_date_set_valid
    --skip test_date::test_date_set_valid_2
    --skip test_date::test_date_set_valid_3
    --skip test_date::test_date_set_valid_4
    --skip test_df::test_column_width_if_header_contains_unicode_chars
    --skip test_df::test_file_column_width_if_filename_contains_unicode_chars
    --skip test_df::test_nonexistent_file
    --skip test_df::test_output_file_specific_files
    --skip test_df::test_output_mp_repeat
    --skip test_df::test_output_option_without_equals_sign
    --skip test_df::test_total_label_in_correct_column
    --skip test_df::test_type_option_with_file
    --skip test_du::test_du_dereference_args
    --skip test_du::test_du_inaccessible_directory
    --skip test_env::test_env_french
    --skip test_error_messages_french_translation
    --skip test_french_colored_error_messages
    --skip test_help_messages_french_translation
    --skip test_hostname::test_hostname_ip
    --skip test_logname::test_normal
    --skip test_logname::test_output_format
    --skip test_ls::test_device_number
    --skip test_ls::test_localized_possible_values
    --skip test_ls::test_ls_allocation_size
    --skip test_ls::test_ls_capabilities
    --skip test_md5sum::test_continue_after_directory_error
    --skip test_mkdir::test_selinux
    --skip test_mkdir::test_selinux_invalid
    --skip test_mkfifo::test_mkfifo_selinux
    --skip test_mkfifo::test_mkfifo_selinux_invalid
    --skip test_more::test_invalid_file_perms
    --skip test_mv::inter_partition_copying::test_mv_unlinks_dest_symlink_error_message
    --skip test_mv::test_move_should_not_fallback_to_copy
    --skip test_mv::test_mv_cross_device_permission_denied
    --skip test_mv::test_mv_permission_error
    --skip test_mv::test_mv_selinux_context
    --skip test_rm::test_only_first_error_recursive
    --skip test_rm::test_recursive_remove_unreadable_subdir
    --skip test_rm::test_unreadable_and_nonempty_dir
    --skip test_runcon::custom_context
    --skip test_runcon::plain_context
    --skip test_shred::test_shred_force
    --skip test_sort::test_argument_suggestion
    --skip test_sort::test_clap_localization_help_message
    --skip test_sort::test_clap_localization_invalid_value
    --skip test_sort::test_clap_localization_unknown_argument
    --skip test_sort::test_error_colors_disabled
    --skip test_sort::test_error_colors_enabled
    --skip test_sort::test_french_translations
    --skip test_sort::test_help_colors_disabled
    --skip test_sort::test_help_colors_enabled
    --skip test_stat::test_stat_selinux
    --skip test_tail::test_permission_denied
    --skip test_tail::test_permission_denied_multiple
    --skip test_tail::test_retry9
    --skip test_tee::linux_only::test_pipe_error_exit
    --skip test_tee::linux_only::test_space_error_exit
    --skip test_tee::linux_only::test_space_error_exit_nopipe
    --skip test_tee::test_readonly
    --skip test_test::test_file_not_owned_by_egid
    --skip test_test::test_file_not_owned_by_euid
    --skip test_touch::test_touch_permission_denied_error_msg
    --skip test_touch::test_touch_system_fails
    %{?arch_skips}
}}
%endif
%endif


%files
%license LICENSE
%license LICENSE.dependencies
%doc CODE_OF_CONDUCT.md
%doc CONTRIBUTING.md
%doc DEVELOPMENT.md
%doc README.md
%doc README.package.md
%doc SECURITY.md
%{_bindir}/uutils-coreutils
%{_bindir}/uu_*
%{_mandir}/man1/*
%{bash_completions_dir}/*
%{fish_completions_dir}/*
%{zsh_completions_dir}/*


%changelog
* Sat Nov 21 2026 Trung Lê <8@tle.id.au> - 0.13.0-1
- Update to 0.13.0
- Build the openssl feature, for the checksum utilities, against the system
  OpenSSL
- Drop feat_acl, gone upstream; drop the ctor patch, upstream now
- Run the test suite: %%ifarch inside %%{shrink:} passed its lines as test
  filters, which filtered out every test; skip the tests that fail in the
  build root
