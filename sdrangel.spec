# Don't build with LTO since it breaks sdrangel
%define _disable_lto 1

%ifarch %{ix86} %{arm}
%bcond_with    fec
%else
%bcond_without fec
%endif
%bcond_without freedv

Name:		sdrangel
Version:	6.19.1
Release:	1
Summary:	SDR/Analyzer frontend for Airspy, BladeRF, HackRF, RTL-SDR and FunCube
License:	GPL-3.0-or-later
Group:		Productivity/Hamradio/Other
URL:		https://github.com/f4exb/sdrangel
Source0:	https://github.com/f4exb/sdrangel/archive/v%{version}.tar.gz
Patch0:		sdrangel-6.18.0-fix-build.patch
#Patch1:		sdrangel-6.18.0-ffmpeg-5.0.patch
BuildRequires:	cmake
BuildRequires:	dsdcc-devel
BuildRequires:	hicolor-icon-theme
BuildRequires:	boost-devel
BuildRequires:	LimeSuite-devel
BuildRequires:	serialDV-devel
BuildRequires:	airspyone_host-devel
BuildRequires:	ffmpeg-devel
BuildRequires:	qmake5
BuildRequires:	pkgconfig(libxtrxll)
BuildRequires:	pkgconfig(libperseus-sdr)
BuildRequires:	pkgconfig(Qt5QuickWidgets)
BuildRequires:	pkgconfig(Qt5MultimediaWidgets)
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5Multimedia)
BuildRequires:	pkgconfig(Qt5OpenGL)
BuildRequires:	pkgconfig(Qt5Widgets)
BuildRequires:	pkgconfig(Qt5WebSockets)
BuildRequires:	pkgconfig(Qt5Location)
BuildRequires:	pkgconfig(Qt5Charts)
BuildRequires:	pkgconfig(Qt5SerialPort)
BuildRequires:	pkgconfig(Qt5TextToSpeech)
BuildRequires:	pkgconfig(Qt5WebEngine)
BuildRequires:	pkgconfig(Qt5WebEngineWidgets)
BuildRequires:	pkgconfig(SoapySDR)
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(codec2)
BuildRequires:	pkgconfig(fftw3f)
BuildRequires:	pkgconfig(libairspyhf)
BuildRequires:	pkgconfig(libavcodec)
BuildRequires:	pkgconfig(libavformat)
BuildRequires:	pkgconfig(libavutil)
BuildRequires:	pkgconfig(libbladeRF)
BuildRequires:	pkgconfig(libhackrf)
BuildRequires:	pkgconfig(libiio)
BuildRequires:	pkgconfig(liblz4)
BuildRequires:	pkgconfig(librtlsdr)
BuildRequires:	pkgconfig(libpostproc)
# It does not build with libmirisdr from upstream
# https://github.com/f4exb/libmirisdr-4 is needed
BuildRequires:	pkgconfig(libmirisdr)
BuildRequires:	pkgconfig(libusb-1.0)
BuildRequires:	pkgconfig(libxtrxll)
BuildRequires:	pkgconfig(opus)
BuildRequires:	pkgconfig(opencv4)
BuildRequires:	pkgconfig(libswscale)
Requires:	python-requests
%if %{with fec}
BuildRequires:	pkgconfig(libcm256cc)
BuildRequires:	pkgconfig(nanomsg)
%endif
%if %{with freedv}
BuildRequires:	pkgconfig(codec2)
%endif

%description
SDRangel is an Open Source Qt5/OpenGL SDR and signal analyzer frontend
to various hardware.

%package doc
Summary:	Documentation for SDRangel

%description doc
Documentation for SDRangel.

%prep
%autosetup -p1
sed -i 's/\r$//' Readme.md
sed -i 's|#!%{_bindir}/env python|#!%{__python}|g' swagger/sdrangel/examples/*.py

%build
%cmake \
  -DCMAKE_SHARED_LINKER_FLAGS="" \
  -DCMAKE_SKIP_RPATH:BOOL=OFF \
  -DCMAKE_BUILD_TYPE=Release \
  -DENABLE_DISTRIBUTION=ON \
  -DINSTALL_LIB_DIR=%{_libdir}/%{name} \
%ifarch %{aarch64}
  -DARCH_OPT="" \
%endif
%ifarch %{ix86}
  -DFORCE_SSE41=ON \
%endif
  -DRX_SAMPLE_24BIT=ON

%make_build

%install
%make_install -C build
rm -f %{buildroot}%{_datadir}/sdrangel/Readme.md

%files
%license LICENSE
%{_bindir}/sdrangel
%{_bindir}/ldpctool
%{_bindir}/sdrangelbench
%{_bindir}/sdrangelsrv
%dir %{_libdir}/sdrangel
%{_libdir}/sdrangel/lib*
%{_libdir}/sdrangel/plugins*/
%{_datadir}/applications/sdrangel.desktop
%{_datadir}/icons/hicolor/scalable/apps/sdrangel_icon.svg

%files doc
%doc Readme.md
%doc swagger/sdrangel/examples/
