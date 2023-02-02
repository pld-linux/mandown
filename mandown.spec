%define		crates_ver	0.1.3

Summary:	Convert Markdown to man pages
Name:		mandown
Version:	0.1.3
Release:	1
License:	Apache v2.0
Group:		Development/Tools
Source0:	https://gitlab.com/kornelski/mandown/-/archive/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	7d756131eff24c8044234bb9bce3711a
Source1:	%{name}-crates-%{version}.tar.xz
# Source1-md5:	ac722b794ec5cc275a3abfbf17684078
URL:		https://gitlab.com/kornelski/mandown
BuildRequires:	cargo
BuildRequires:	rpmbuild(macros) >= 2.004
BuildRequires:	rust >= 1.42
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
ExclusiveArch:	%{rust_arches}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Convert Markdown to man pages.

%prep
%setup -q -a1

%{__mv} %{name}-%{crates_ver}/* .
sed -i -e 's/@@VERSION@@/%{version}/' Cargo.lock

# use our offline registry
export CARGO_HOME="$(pwd)/.cargo"

mkdir -p "$CARGO_HOME"
cat >.cargo/config <<EOF
[source.crates-io]
registry = 'https://github.com/rust-lang/crates.io-index'
replace-with = 'vendored-sources'

[source.vendored-sources]
directory = '$PWD/vendor'
EOF

%build
export CARGO_HOME="$(pwd)/.cargo"

%cargo_build --frozen

%install
rm -rf $RPM_BUILD_ROOT
export CARGO_HOME="$(pwd)/.cargo"

%cargo_install --frozen --root $RPM_BUILD_ROOT%{_prefix} --path $PWD
%{__rm} $RPM_BUILD_ROOT%{_prefix}/.crates*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/mandown
