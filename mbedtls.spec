#
# Conditional build:
%bcond_with	zlib	# zlib compression support (may reduce security, see CRIME)
#
Summary:	Light-weight cryptographic and SSL/TLS library
Summary(pl.UTF-8):	Lekka biblioteka kryptograficzna oraz SSL/TLS
Name:		mbedtls
Version:	3.1.0
Release:	2
License:	GPL v2+
Group:		Libraries
#Source0Download: https://github.com/ARMmbed/mbedtls/releases
Source0:	https://github.com/ARMmbed/mbedtls/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	a228170fbedd1202edcc1bf13d83b1a3
Patch0:		%{name}-config-dtls-srtp.patch
URL:		https://www.trustedfirmware.org/projects/mbed-tls/
BuildRequires:	cmake >= 2.8.12
BuildRequires:	doxygen
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.605
%{?with_zlib:BuildRequires:	zlib-devel}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# some false positives for format-truncation(?)
# for stringop-overflow see library/ssl_tls.c /stringop-overflow (workaround no longer works with gcc 11)
# maybe-uninitialized fails in tests/suites/test_suite_ssl.function only on i686 builder(???)
%define		specflags -Wno-error=format-truncation -Wno-error=stringop-overflow -Wno-error=maybe-uninitialized

%description
mbedTLS is a light-weight open source cryptographic and SSL/TLS
library written in C. mbedTLS makes it easy for developers to include
cryptographic and SSL/TLS capabilities in their (embedded)
applications with as little hassle as possible.

%description -l pl.UTF-8
mbedTLS to lekka, mająca otwarte źródła biblioteka kryptograficzna
oraz SSL/TLS napisana w C. mbedTLS ułatwia programistom dołączanie
funkcji kryptograficznych i SSL/TLS do swoich (wbudowanych) aplikacji
przy jak najmniejszym narzucie.

%package devel
Summary:	Development files for mbedTLS
Summary(pl.UTF-8):	Pliki programistyczne biblioteki mbedTLS
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the header files for developing applications
that use mbedTLS.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe do tworzenia aplikacji
wykorzystujących bibliotekę mbedTLS.

%package static
Summary:	Static mbedTLS library
Summary(pl.UTF-8):	Statyczna biblioteka mbedTLS
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static mbedTLS library.

%description static -l pl.UTF-8
Statyczna biblioteka mbedTLS.

%package apidocs
Summary:	API documentation for mbedTLS library
Summary(pl.UTF-8):	Dokumentacja API biblioteki mbedTLS
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for mbedTLS library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki mbedTLS.

%prep
%setup -q
%patch0 -p1

%build
install -d build
cd build
%cmake .. \
	-DLIB_INSTALL_DIR:PATH=%{_libdir} \
	%{?with_zlib:-DENABLE_ZLIB_SUPPORT=ON} \
	-DUSE_SHARED_MBEDTLS_LIBRARY=ON \
	-DGEN_FILES=OFF

%{__make}
%{__make} apidoc

%if %{with tests}
# Tests are not stable on 64-bit
ctest --output-on-failure
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	CMAKE_INSTALL_PREFIX=%{_libdir} \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_libdir}
%{__mv} $RPM_BUILD_ROOT%{_bindir} $RPM_BUILD_ROOT%{_libdir}/%{name}

%{__mv} $RPM_BUILD_ROOT{%{_prefix},%{_libdir}}/cmake

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog LICENSE README.md
%attr(755,root,root) %{_libdir}/libmbedcrypto.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmbedcrypto.so.11
%attr(755,root,root) %{_libdir}/libmbedtls.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmbedtls.so.17
%attr(755,root,root) %{_libdir}/libmbedx509.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmbedx509.so.4
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/benchmark
%attr(755,root,root) %{_libdir}/%{name}/cert_app
%attr(755,root,root) %{_libdir}/%{name}/cert_req
%attr(755,root,root) %{_libdir}/%{name}/cert_write
%attr(755,root,root) %{_libdir}/%{name}/crl_app
%attr(755,root,root) %{_libdir}/%{name}/crypt_and_hash
%attr(755,root,root) %{_libdir}/%{name}/crypto_examples
%attr(755,root,root) %{_libdir}/%{name}/dh_client
%attr(755,root,root) %{_libdir}/%{name}/dh_genprime
%attr(755,root,root) %{_libdir}/%{name}/dh_server
%attr(755,root,root) %{_libdir}/%{name}/dtls_client
%attr(755,root,root) %{_libdir}/%{name}/dtls_server
%attr(755,root,root) %{_libdir}/%{name}/ecdh_curve25519
%attr(755,root,root) %{_libdir}/%{name}/ecdsa
%attr(755,root,root) %{_libdir}/%{name}/gen_entropy
%attr(755,root,root) %{_libdir}/%{name}/gen_key
%attr(755,root,root) %{_libdir}/%{name}/gen_random_ctr_drbg
%attr(755,root,root) %{_libdir}/%{name}/generic_sum
%attr(755,root,root) %{_libdir}/%{name}/hello
%attr(755,root,root) %{_libdir}/%{name}/key_app
%attr(755,root,root) %{_libdir}/%{name}/key_app_writer
%attr(755,root,root) %{_libdir}/%{name}/key_ladder_demo
%attr(755,root,root) %{_libdir}/%{name}/key_ladder_demo.sh
%attr(755,root,root) %{_libdir}/%{name}/load_roots
%attr(755,root,root) %{_libdir}/%{name}/mini_client
%attr(755,root,root) %{_libdir}/%{name}/mpi_demo
%attr(755,root,root) %{_libdir}/%{name}/pem2der
%attr(755,root,root) %{_libdir}/%{name}/pk_decrypt
%attr(755,root,root) %{_libdir}/%{name}/pk_encrypt
%attr(755,root,root) %{_libdir}/%{name}/pk_sign
%attr(755,root,root) %{_libdir}/%{name}/pk_verify
%attr(755,root,root) %{_libdir}/%{name}/psa_constant_names
%attr(755,root,root) %{_libdir}/%{name}/query_compile_time_config
%attr(755,root,root) %{_libdir}/%{name}/req_app
%attr(755,root,root) %{_libdir}/%{name}/rsa_decrypt
%attr(755,root,root) %{_libdir}/%{name}/rsa_encrypt
%attr(755,root,root) %{_libdir}/%{name}/rsa_genkey
%attr(755,root,root) %{_libdir}/%{name}/rsa_sign
%attr(755,root,root) %{_libdir}/%{name}/rsa_sign_pss
%attr(755,root,root) %{_libdir}/%{name}/rsa_verify
%attr(755,root,root) %{_libdir}/%{name}/rsa_verify_pss
%attr(755,root,root) %{_libdir}/%{name}/selftest
%attr(755,root,root) %{_libdir}/%{name}/ssl_client1
%attr(755,root,root) %{_libdir}/%{name}/ssl_client2
%attr(755,root,root) %{_libdir}/%{name}/ssl_context_info
%attr(755,root,root) %{_libdir}/%{name}/ssl_fork_server
%attr(755,root,root) %{_libdir}/%{name}/ssl_mail_client
%attr(755,root,root) %{_libdir}/%{name}/ssl_pthread_server
%attr(755,root,root) %{_libdir}/%{name}/ssl_server
%attr(755,root,root) %{_libdir}/%{name}/ssl_server2
%attr(755,root,root) %{_libdir}/%{name}/strerror
%attr(755,root,root) %{_libdir}/%{name}/udp_proxy
%attr(755,root,root) %{_libdir}/%{name}/zeroize

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmbedcrypto.so
%attr(755,root,root) %{_libdir}/libmbedtls.so
%attr(755,root,root) %{_libdir}/libmbedx509.so
%{_includedir}/mbedtls
%{_includedir}/psa
%{_libdir}/cmake/MbedTLS*.cmake

%files static
%defattr(644,root,root,755)
%{_libdir}/libmbedcrypto.a
%{_libdir}/libmbedtls.a
%{_libdir}/libmbedx509.a

%files apidocs
%defattr(644,root,root,755)
%doc apidoc/*
