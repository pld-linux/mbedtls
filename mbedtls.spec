#
# Conditional build:
%bcond_with	x86aes	# x86-32 pclmul+sse2+aes instruction sets

%ifnarch %{ix86}
%undefine	with_x86aes
%endif
Summary:	Light-weight cryptographic and SSL/TLS library
Summary(pl.UTF-8):	Lekka biblioteka kryptograficzna oraz SSL/TLS
Name:		mbedtls
Version:	3.6.3.1
Release:	1
License:	GPL v2+
Group:		Libraries
#Source0Download: https://github.com/Mbed-TLS/mbedtls/releases
Source0:	https://github.com/Mbed-TLS/mbedtls/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	ca72e14669a8fddc7d1bf154947ebd4c
Patch0:		%{name}-config-dtls-srtp.patch
URL:		https://www.trustedfirmware.org/projects/mbed-tls/
BuildRequires:	cmake >= 3.5.1
BuildRequires:	doxygen
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.605
%if %{with x86aes}
Requires:	cpuinfo(aes)
Requires:	cpuinfo(pclmulqdq)
Requires:	cpuinfo(sse2)
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
%patch -P0 -p1

%build
%if %{with x86aes}
# in mbedtls 3.5/3.6 on 32-bit x86, hardware AESNI requires aes.c and aesni.c
# built with AES+SSE2 options
# but aes.c code is executed regardless of CPU features detection
CFLAGS="%{rpmcflags} -mpclmul -msse2 -maes"
%endif

install -d build
cd build
%cmake .. \
	-DLIB_INSTALL_DIR:PATH=%{_libdir} \
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

install -d $RPM_BUILD_ROOT%{_libexecdir}
%{__mv} $RPM_BUILD_ROOT%{_bindir} $RPM_BUILD_ROOT%{_libexecdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog LICENSE README.md
%attr(755,root,root) %{_libdir}/libmbedcrypto.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmbedcrypto.so.16
%attr(755,root,root) %{_libdir}/libmbedtls.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmbedtls.so.21
%attr(755,root,root) %{_libdir}/libmbedx509.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmbedx509.so.7
%attr(755,root,root) %{_libdir}/libeverest.so
%attr(755,root,root) %{_libdir}/libp256m.so
%dir %{_libexecdir}/%{name}
%attr(755,root,root) %{_libexecdir}/%{name}/aead_demo
%attr(755,root,root) %{_libexecdir}/%{name}/benchmark
%attr(755,root,root) %{_libexecdir}/%{name}/cert_app
%attr(755,root,root) %{_libexecdir}/%{name}/cert_req
%attr(755,root,root) %{_libexecdir}/%{name}/cert_write
%attr(755,root,root) %{_libexecdir}/%{name}/cipher_aead_demo
%attr(755,root,root) %{_libexecdir}/%{name}/crl_app
%attr(755,root,root) %{_libexecdir}/%{name}/crypt_and_hash
%attr(755,root,root) %{_libexecdir}/%{name}/crypto_examples
%attr(755,root,root) %{_libexecdir}/%{name}/dh_client
%attr(755,root,root) %{_libexecdir}/%{name}/dh_genprime
%attr(755,root,root) %{_libexecdir}/%{name}/dh_server
%attr(755,root,root) %{_libexecdir}/%{name}/dtls_client
%attr(755,root,root) %{_libexecdir}/%{name}/dtls_server
%attr(755,root,root) %{_libexecdir}/%{name}/ecdh_curve25519
%attr(755,root,root) %{_libexecdir}/%{name}/ecdsa
%attr(755,root,root) %{_libexecdir}/%{name}/gen_entropy
%attr(755,root,root) %{_libexecdir}/%{name}/gen_key
%attr(755,root,root) %{_libexecdir}/%{name}/gen_random_ctr_drbg
%attr(755,root,root) %{_libexecdir}/%{name}/generic_sum
%attr(755,root,root) %{_libexecdir}/%{name}/hello
%attr(755,root,root) %{_libexecdir}/%{name}/hmac_demo
%attr(755,root,root) %{_libexecdir}/%{name}/key_app
%attr(755,root,root) %{_libexecdir}/%{name}/key_app_writer
%attr(755,root,root) %{_libexecdir}/%{name}/key_ladder_demo
%attr(755,root,root) %{_libexecdir}/%{name}/key_ladder_demo.sh
%attr(755,root,root) %{_libexecdir}/%{name}/load_roots
%attr(755,root,root) %{_libexecdir}/%{name}/md_hmac_demo
%attr(755,root,root) %{_libexecdir}/%{name}/metatest
%attr(755,root,root) %{_libexecdir}/%{name}/mini_client
%attr(755,root,root) %{_libexecdir}/%{name}/mpi_demo
%attr(755,root,root) %{_libexecdir}/%{name}/pem2der
%attr(755,root,root) %{_libexecdir}/%{name}/pk_decrypt
%attr(755,root,root) %{_libexecdir}/%{name}/pk_encrypt
%attr(755,root,root) %{_libexecdir}/%{name}/pk_sign
%attr(755,root,root) %{_libexecdir}/%{name}/pk_verify
%attr(755,root,root) %{_libexecdir}/%{name}/psa_constant_names
%attr(755,root,root) %{_libexecdir}/%{name}/psa_hash
%attr(755,root,root) %{_libexecdir}/%{name}/query_compile_time_config
%attr(755,root,root) %{_libexecdir}/%{name}/query_included_headers
%attr(755,root,root) %{_libexecdir}/%{name}/req_app
%attr(755,root,root) %{_libexecdir}/%{name}/rsa_decrypt
%attr(755,root,root) %{_libexecdir}/%{name}/rsa_encrypt
%attr(755,root,root) %{_libexecdir}/%{name}/rsa_genkey
%attr(755,root,root) %{_libexecdir}/%{name}/rsa_sign
%attr(755,root,root) %{_libexecdir}/%{name}/rsa_sign_pss
%attr(755,root,root) %{_libexecdir}/%{name}/rsa_verify
%attr(755,root,root) %{_libexecdir}/%{name}/rsa_verify_pss
%attr(755,root,root) %{_libexecdir}/%{name}/selftest
%attr(755,root,root) %{_libexecdir}/%{name}/ssl_client1
%attr(755,root,root) %{_libexecdir}/%{name}/ssl_client2
%attr(755,root,root) %{_libexecdir}/%{name}/ssl_context_info
%attr(755,root,root) %{_libexecdir}/%{name}/ssl_fork_server
%attr(755,root,root) %{_libexecdir}/%{name}/ssl_mail_client
%attr(755,root,root) %{_libexecdir}/%{name}/ssl_pthread_server
%attr(755,root,root) %{_libexecdir}/%{name}/ssl_server
%attr(755,root,root) %{_libexecdir}/%{name}/ssl_server2
%attr(755,root,root) %{_libexecdir}/%{name}/strerror
%attr(755,root,root) %{_libexecdir}/%{name}/udp_proxy
%attr(755,root,root) %{_libexecdir}/%{name}/zeroize

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmbedcrypto.so
%attr(755,root,root) %{_libdir}/libmbedtls.so
%attr(755,root,root) %{_libdir}/libmbedx509.so
%{_includedir}/everest
%{_includedir}/mbedtls
%{_includedir}/psa
%{_libdir}/cmake/MbedTLS
%{_pkgconfigdir}/mbedcrypto.pc
%{_pkgconfigdir}/mbedtls.pc
%{_pkgconfigdir}/mbedx509.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libmbedcrypto.a
%{_libdir}/libmbedtls.a
%{_libdir}/libmbedx509.a

%files apidocs
%defattr(644,root,root,755)
%doc apidoc/{search,*.css,*.html,*.js,*.png}
