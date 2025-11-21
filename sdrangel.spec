# Don't build with LTO since it breaks sdrangel
%define _disable_lto 1

%ifarch %{ix86} %{arm}
%bcond_with    fec
%else
%bcond_without fec
%endif
%bcond_without freedv

Name:		sdrangel
Version:	7.22.9
Release:	1
Summary:	SDR/Analyzer frontend for Airspy, BladeRF, HackRF, RTL-SDR and FunCube
License:	GPL-3.0-or-later
Group:		Productivity/Hamradio/Other
URL:		https://github.com/f4exb/sdrangel
Source0:	https://github.com/f4exb/sdrangel/archive/v%{version}.tar.gz
# Fix CMakeLists & FindXX.cmake issues
Patch0:		sdrangel-7.22.9-cmakelist-fixes.patch

#BuildRequires:	airspyone_host-devel
BuildRequires:	cmake
BuildRequires:	boost-devel
BuildRequires:	doxygen
BuildRequires:	dsdcc-devel
BuildRequires:	ffmpeg-devel
BuildRequires:	gcc
BuildRequires:	glibc-devel
BuildRequires:	graphviz
BuildRequires:	hicolor-icon-theme
BuildRequires:	LimeSuite-devel
BuildRequires:	qmake-qt6
BuildRequires:	qt6-qtbase-theme-gtk3
BuildRequires:	qt6-qtmultimedia-gstreamer
BuildRequires:	serialDV-devel
BuildRequires:	stdc++-devel
BuildRequires:	vulkan-headers
BuildRequires:	cmake(KF6Declarative)
BuildRequires:	cmake(lz4)
BuildRequires:	cmake(Qt6Charts)
BuildRequires:	cmake(Qt6Core)
BuildRequires:	cmake(Qt6Core5Compat)
BuildRequires:	cmake(Qt6ExamplesAssetDownloaderPrivate)
BuildRequires:	cmake(Qt6Gui)
BuildRequires:	cmake(Qt6LabsSynchronizer)
BuildRequires:	cmake(Qt6Location)
BuildRequires:	cmake(Qt6Multimedia)
BuildRequires:	cmake(Qt6MultimediaWidgets)
BuildRequires:	cmake(Qt6Network)
BuildRequires:	cmake(Qt6OpenGL)
BuildRequires:	cmake(Qt6OpenGLWidgets)
BuildRequires:	cmake(Qt6Positioning)
BuildRequires:	cmake(Qt6QmlAssetDownloader)
BuildRequires:	cmake(Qt6Qml)
BuildRequires:	cmake(Qt6QmlCore)
BuildRequires:	cmake(Qt6QmlNetwork)
BuildRequires:	cmake(Qt6QmlMeta)
BuildRequires:	cmake(Qt6Quick)
BuildRequires:	cmake(Qt6QuickControls2)
BuildRequires:	cmake(Qt6QuickDialogs2)
BuildRequires:	cmake(Qt6QuickLayouts)
BuildRequires:	cmake(Qt6QuickWidgets)
BuildRequires:	cmake(Qt6SerialPort)
BuildRequires:	cmake(Qt6StateMachine)
BuildRequires:	cmake(Qt6Svg)
BuildRequires:	cmake(Qt6SvgWidgets)
BuildRequires:	cmake(Qt6TextToSpeech)
BuildRequires:	cmake(Qt6WebEngineCore)
BuildRequires:	cmake(Qt6WebEngineQuick)
BuildRequires:	cmake(Qt6WebEngineWidgets)
BuildRequires:	cmake(Qt6WebSockets)
BuildRequires:	cmake(Qt6Widgets)
# The cmake(XKB) parameter pulls in lib64KF5KDELibs4Support-devel as
# a dependency and a whole bunch of KF5/qt5 packages with it,
# we dont want this in a Qt6 package
#BuildRequires:	cmake(XKB)
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(codec2)
BuildRequires:	pkgconfig(fftw3f)
BuildRequires:	pkgconfig(flac)
BuildRequires:	pkgconfig(hamlib)
BuildRequires:	pkgconfig(libairspyhf)
BuildRequires:	pkgconfig(libavcodec)
BuildRequires:	pkgconfig(libavformat)
BuildRequires:	pkgconfig(libavutil)
BuildRequires:	pkgconfig(libbladeRF)
BuildRequires:	pkgconfig(libhackrf)
BuildRequires:	pkgconfig(libiio)
BuildRequires:	pkgconfig(liblz4)
#BuildRequires:	pkgconfig(libpostproc)
# It does not build with libmirisdr from upstream
# https://github.com/f4exb/libmirisdr-4 is needed
BuildRequires:	pkgconfig(libmirisdr)
BuildRequires:	pkgconfig(libperseus-sdr)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(librtlsdr)
BuildRequires:	pkgconfig(libswscale)
BuildRequires:	pkgconfig(libusb-1.0)
BuildRequires:	pkgconfig(libxtrxll)
BuildRequires:	pkgconfig(nanomsg)
BuildRequires:	pkgconfig(opencv4)
BuildRequires:	pkgconfig(opus)
BuildRequires:	pkgconfig(SoapySDR)
BuildRequires:	pkgconfig(uhd)
BuildRequires:	pkgconfig(xkbcommon)
BuildRequires:	pkgconfig(zlib)
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
  -DENABLE_QT6:BOOL=ON \
  -DINSTALL_LIB_DIR=%{_libdir}/%{name} \
%ifarch %{aarch64}
  -DARCH_OPT="" \
%endif
%ifarch %{ix86}
  -DFORCE_SSE41=ON \
%endif
  -DRX_SAMPLE_24BIT=ON \
  -G Ninja

%ninja_build

%install
%ninja_install -C build
rm -f %{buildroot}%{_datadir}/sdrangel/Readme.md

%files
%license LICENSE
%{_bindir}/sdrangel
#%%{_bindir}/ldpctool
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
