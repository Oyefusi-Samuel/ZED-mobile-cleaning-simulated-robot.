# generated from ament/cmake/core/templates/nameConfig.cmake.in

# prevent multiple inclusion
if(_visual_marker_CONFIG_INCLUDED)
  # ensure to keep the found flag the same
  if(NOT DEFINED visual_marker_FOUND)
    # explicitly set it to FALSE, otherwise CMake will set it to TRUE
    set(visual_marker_FOUND FALSE)
  elseif(NOT visual_marker_FOUND)
    # use separate condition to avoid uninitialized variable warning
    set(visual_marker_FOUND FALSE)
  endif()
  return()
endif()
set(_visual_marker_CONFIG_INCLUDED TRUE)

# output package information
if(NOT visual_marker_FIND_QUIETLY)
  message(STATUS "Found visual_marker: 0.0.0 (${visual_marker_DIR})")
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "Package 'visual_marker' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  # optionally quiet the deprecation message
  if(NOT ${visual_marker_DEPRECATED_QUIET})
    message(DEPRECATION "${_msg}")
  endif()
endif()

# flag package as ament-based to distinguish it after being find_package()-ed
set(visual_marker_FOUND_AMENT_PACKAGE TRUE)

# include all config extra files
set(_extras "")
foreach(_extra ${_extras})
  include("${visual_marker_DIR}/${_extra}")
endforeach()
