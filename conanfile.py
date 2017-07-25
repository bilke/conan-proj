import os
from conans import ConanFile, CMake
from conans.tools import download, unzip, patch

class ProjConan(ConanFile):
    name = "proj"
    description = """proj.4 is a library which converts geographic longitude and
                     latitude coordinates into cartesian coordinates."""
    version = "4.9.2"
    generators = "cmake"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    exports = ["CMakeLists.txt", "FindPROJ4.cmake"]
    url="http://github.com/bilke/conan-proj"
    license="https://github.com/OSGeo/proj.4"

    ZIP_FOLDER_NAME = "proj.4-%s" % version

    def source(self):
        zip_name = self.version + ".zip"
        download("https://github.com/OSGeo/proj.4/archive/%s" % zip_name , zip_name)
        unzip(zip_name)
        os.unlink(zip_name)

    def build(self):
        # produced with `diff -U 1 -p Proj4Config.cmake tmp.cmake`
        patch_content1 = '''--- cmake/Proj4Config.cmake	2016-04-25 09:27:06.000000000 +0200
+++ cmake/Proj4Config.cmake	2016-04-25 09:27:02.000000000 +0200
@@ -38,2 +38,2 @@ set(PACKAGE_VERSION "${${PROJECT_INTERN_

-configure_file(cmake/proj_config.cmake.in src/proj_config.h)
+configure_file(${PROJ4_SOURCE_DIR}/cmake/proj_config.cmake.in ${CMAKE_SOURCE_DIR}/build/%s/src/proj_config.h)
''' % self.ZIP_FOLDER_NAME
        patch(patch_string=patch_content1, base_path=self.ZIP_FOLDER_NAME)
        patch_content2 = '''--- cmake/Proj4InstallPath.cmake	2016-04-25 09:27:06.000000000 +0200
+++ cmake/Proj4InstallPath.cmake	2016-04-25 09:28:02.000000000 +0200
@@ -24,3 +24,3 @@ ENDIF(CMAKE_INSTALL_PREFIX_INITIALIZED_T

-if(WIN32)
+if(FALSE)
   set(DEFAULT_BIN_SUBDIR bin)
'''
        patch(patch_string=patch_content2, base_path=self.ZIP_FOLDER_NAME)

        cmake = CMake(self)
        if self.settings.os != "Windows":
            cmake.definitions["BUILD_CS2CS"] = "OFF"
            cmake.definitions["BUILD_PROJ"] = "OFF"
            cmake.definitions["BUILD_GEOD"] = "OFF"
            cmake.definitions["BUILD_NAD2BIN"] = "OFF"
        cmake.definitions["PROJ4_TESTS"] = "OFF"
        if self.options.shared == False:
            cmake.definitions["BUILD_LIBPROJ_SHARED"] = "OFF"
        else:
            cmake.definitions["BUILD_LIBPROJ_SHARED"] = "ON"
        cmake.configure(build_dir="build")
        cmake.build(target="install")

    def package_info(self):
        if self.settings.os == "Windows":
            if self.settings.build_type == "Debug":
                self.cpp_info.libs = ["proj_4_9_d"]
            else:
                self.cpp_info.libs = ["proj_4_9"]
        else:
            self.cpp_info.libs = ["proj"]
