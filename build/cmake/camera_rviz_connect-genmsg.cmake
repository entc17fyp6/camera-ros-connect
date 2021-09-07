# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "camera_rviz_connect: 4 messages, 0 services")

set(MSG_I_FLAGS "-Icamera_rviz_connect:/home/samare/catkin_ws/src/camera_rviz_connect/msg;-Isensor_msgs:/opt/ros/noetic/share/sensor_msgs/cmake/../msg;-Istd_msgs:/opt/ros/noetic/share/std_msgs/cmake/../msg;-Igeometry_msgs:/opt/ros/noetic/share/geometry_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(gennodejs REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(camera_rviz_connect_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/samare/catkin_ws/src/camera_rviz_connect/msg/Lanes.msg" NAME_WE)
add_custom_target(_camera_rviz_connect_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "camera_rviz_connect" "/home/samare/catkin_ws/src/camera_rviz_connect/msg/Lanes.msg" "std_msgs/Header"
)

get_filename_component(_filename "/home/samare/catkin_ws/src/camera_rviz_connect/msg/Road_markings.msg" NAME_WE)
add_custom_target(_camera_rviz_connect_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "camera_rviz_connect" "/home/samare/catkin_ws/src/camera_rviz_connect/msg/Road_markings.msg" "std_msgs/Header"
)

get_filename_component(_filename "/home/samare/catkin_ws/src/camera_rviz_connect/msg/Traffic_signs.msg" NAME_WE)
add_custom_target(_camera_rviz_connect_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "camera_rviz_connect" "/home/samare/catkin_ws/src/camera_rviz_connect/msg/Traffic_signs.msg" "std_msgs/Header"
)

get_filename_component(_filename "/home/samare/catkin_ws/src/camera_rviz_connect/msg/Traffic_lights.msg" NAME_WE)
add_custom_target(_camera_rviz_connect_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "camera_rviz_connect" "/home/samare/catkin_ws/src/camera_rviz_connect/msg/Traffic_lights.msg" "std_msgs/Header"
)

#
#  langs = gencpp;geneus;genlisp;gennodejs;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(camera_rviz_connect
  "/home/samare/catkin_ws/src/camera_rviz_connect/msg/Lanes.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/camera_rviz_connect
)
_generate_msg_cpp(camera_rviz_connect
  "/home/samare/catkin_ws/src/camera_rviz_connect/msg/Road_markings.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/camera_rviz_connect
)
_generate_msg_cpp(camera_rviz_connect
  "/home/samare/catkin_ws/src/camera_rviz_connect/msg/Traffic_signs.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/camera_rviz_connect
)
_generate_msg_cpp(camera_rviz_connect
  "/home/samare/catkin_ws/src/camera_rviz_connect/msg/Traffic_lights.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/camera_rviz_connect
)

### Generating Services

### Generating Module File
_generate_module_cpp(camera_rviz_connect
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/camera_rviz_connect
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(camera_rviz_connect_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(camera_rviz_connect_generate_messages camera_rviz_connect_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/samare/catkin_ws/src/camera_rviz_connect/msg/Lanes.msg" NAME_WE)
add_dependencies(camera_rviz_connect_generate_messages_cpp _camera_rviz_connect_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/samare/catkin_ws/src/camera_rviz_connect/msg/Road_markings.msg" NAME_WE)
add_dependencies(camera_rviz_connect_generate_messages_cpp _camera_rviz_connect_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/samare/catkin_ws/src/camera_rviz_connect/msg/Traffic_signs.msg" NAME_WE)
add_dependencies(camera_rviz_connect_generate_messages_cpp _camera_rviz_connect_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/samare/catkin_ws/src/camera_rviz_connect/msg/Traffic_lights.msg" NAME_WE)
add_dependencies(camera_rviz_connect_generate_messages_cpp _camera_rviz_connect_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(camera_rviz_connect_gencpp)
add_dependencies(camera_rviz_connect_gencpp camera_rviz_connect_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS camera_rviz_connect_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages
_generate_msg_eus(camera_rviz_connect
  "/home/samare/catkin_ws/src/camera_rviz_connect/msg/Lanes.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/camera_rviz_connect
)
_generate_msg_eus(camera_rviz_connect
  "/home/samare/catkin_ws/src/camera_rviz_connect/msg/Road_markings.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/camera_rviz_connect
)
_generate_msg_eus(camera_rviz_connect
  "/home/samare/catkin_ws/src/camera_rviz_connect/msg/Traffic_signs.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/camera_rviz_connect
)
_generate_msg_eus(camera_rviz_connect
  "/home/samare/catkin_ws/src/camera_rviz_connect/msg/Traffic_lights.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/camera_rviz_connect
)

### Generating Services

### Generating Module File
_generate_module_eus(camera_rviz_connect
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/camera_rviz_connect
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(camera_rviz_connect_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(camera_rviz_connect_generate_messages camera_rviz_connect_generate_messages_eus)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/samare/catkin_ws/src/camera_rviz_connect/msg/Lanes.msg" NAME_WE)
add_dependencies(camera_rviz_connect_generate_messages_eus _camera_rviz_connect_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/samare/catkin_ws/src/camera_rviz_connect/msg/Road_markings.msg" NAME_WE)
add_dependencies(camera_rviz_connect_generate_messages_eus _camera_rviz_connect_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/samare/catkin_ws/src/camera_rviz_connect/msg/Traffic_signs.msg" NAME_WE)
add_dependencies(camera_rviz_connect_generate_messages_eus _camera_rviz_connect_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/samare/catkin_ws/src/camera_rviz_connect/msg/Traffic_lights.msg" NAME_WE)
add_dependencies(camera_rviz_connect_generate_messages_eus _camera_rviz_connect_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(camera_rviz_connect_geneus)
add_dependencies(camera_rviz_connect_geneus camera_rviz_connect_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS camera_rviz_connect_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(camera_rviz_connect
  "/home/samare/catkin_ws/src/camera_rviz_connect/msg/Lanes.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/camera_rviz_connect
)
_generate_msg_lisp(camera_rviz_connect
  "/home/samare/catkin_ws/src/camera_rviz_connect/msg/Road_markings.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/camera_rviz_connect
)
_generate_msg_lisp(camera_rviz_connect
  "/home/samare/catkin_ws/src/camera_rviz_connect/msg/Traffic_signs.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/camera_rviz_connect
)
_generate_msg_lisp(camera_rviz_connect
  "/home/samare/catkin_ws/src/camera_rviz_connect/msg/Traffic_lights.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/camera_rviz_connect
)

### Generating Services

### Generating Module File
_generate_module_lisp(camera_rviz_connect
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/camera_rviz_connect
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(camera_rviz_connect_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(camera_rviz_connect_generate_messages camera_rviz_connect_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/samare/catkin_ws/src/camera_rviz_connect/msg/Lanes.msg" NAME_WE)
add_dependencies(camera_rviz_connect_generate_messages_lisp _camera_rviz_connect_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/samare/catkin_ws/src/camera_rviz_connect/msg/Road_markings.msg" NAME_WE)
add_dependencies(camera_rviz_connect_generate_messages_lisp _camera_rviz_connect_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/samare/catkin_ws/src/camera_rviz_connect/msg/Traffic_signs.msg" NAME_WE)
add_dependencies(camera_rviz_connect_generate_messages_lisp _camera_rviz_connect_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/samare/catkin_ws/src/camera_rviz_connect/msg/Traffic_lights.msg" NAME_WE)
add_dependencies(camera_rviz_connect_generate_messages_lisp _camera_rviz_connect_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(camera_rviz_connect_genlisp)
add_dependencies(camera_rviz_connect_genlisp camera_rviz_connect_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS camera_rviz_connect_generate_messages_lisp)

### Section generating for lang: gennodejs
### Generating Messages
_generate_msg_nodejs(camera_rviz_connect
  "/home/samare/catkin_ws/src/camera_rviz_connect/msg/Lanes.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/camera_rviz_connect
)
_generate_msg_nodejs(camera_rviz_connect
  "/home/samare/catkin_ws/src/camera_rviz_connect/msg/Road_markings.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/camera_rviz_connect
)
_generate_msg_nodejs(camera_rviz_connect
  "/home/samare/catkin_ws/src/camera_rviz_connect/msg/Traffic_signs.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/camera_rviz_connect
)
_generate_msg_nodejs(camera_rviz_connect
  "/home/samare/catkin_ws/src/camera_rviz_connect/msg/Traffic_lights.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/camera_rviz_connect
)

### Generating Services

### Generating Module File
_generate_module_nodejs(camera_rviz_connect
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/camera_rviz_connect
  "${ALL_GEN_OUTPUT_FILES_nodejs}"
)

add_custom_target(camera_rviz_connect_generate_messages_nodejs
  DEPENDS ${ALL_GEN_OUTPUT_FILES_nodejs}
)
add_dependencies(camera_rviz_connect_generate_messages camera_rviz_connect_generate_messages_nodejs)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/samare/catkin_ws/src/camera_rviz_connect/msg/Lanes.msg" NAME_WE)
add_dependencies(camera_rviz_connect_generate_messages_nodejs _camera_rviz_connect_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/samare/catkin_ws/src/camera_rviz_connect/msg/Road_markings.msg" NAME_WE)
add_dependencies(camera_rviz_connect_generate_messages_nodejs _camera_rviz_connect_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/samare/catkin_ws/src/camera_rviz_connect/msg/Traffic_signs.msg" NAME_WE)
add_dependencies(camera_rviz_connect_generate_messages_nodejs _camera_rviz_connect_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/samare/catkin_ws/src/camera_rviz_connect/msg/Traffic_lights.msg" NAME_WE)
add_dependencies(camera_rviz_connect_generate_messages_nodejs _camera_rviz_connect_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(camera_rviz_connect_gennodejs)
add_dependencies(camera_rviz_connect_gennodejs camera_rviz_connect_generate_messages_nodejs)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS camera_rviz_connect_generate_messages_nodejs)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(camera_rviz_connect
  "/home/samare/catkin_ws/src/camera_rviz_connect/msg/Lanes.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/camera_rviz_connect
)
_generate_msg_py(camera_rviz_connect
  "/home/samare/catkin_ws/src/camera_rviz_connect/msg/Road_markings.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/camera_rviz_connect
)
_generate_msg_py(camera_rviz_connect
  "/home/samare/catkin_ws/src/camera_rviz_connect/msg/Traffic_signs.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/camera_rviz_connect
)
_generate_msg_py(camera_rviz_connect
  "/home/samare/catkin_ws/src/camera_rviz_connect/msg/Traffic_lights.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/noetic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/camera_rviz_connect
)

### Generating Services

### Generating Module File
_generate_module_py(camera_rviz_connect
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/camera_rviz_connect
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(camera_rviz_connect_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(camera_rviz_connect_generate_messages camera_rviz_connect_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/samare/catkin_ws/src/camera_rviz_connect/msg/Lanes.msg" NAME_WE)
add_dependencies(camera_rviz_connect_generate_messages_py _camera_rviz_connect_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/samare/catkin_ws/src/camera_rviz_connect/msg/Road_markings.msg" NAME_WE)
add_dependencies(camera_rviz_connect_generate_messages_py _camera_rviz_connect_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/samare/catkin_ws/src/camera_rviz_connect/msg/Traffic_signs.msg" NAME_WE)
add_dependencies(camera_rviz_connect_generate_messages_py _camera_rviz_connect_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/samare/catkin_ws/src/camera_rviz_connect/msg/Traffic_lights.msg" NAME_WE)
add_dependencies(camera_rviz_connect_generate_messages_py _camera_rviz_connect_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(camera_rviz_connect_genpy)
add_dependencies(camera_rviz_connect_genpy camera_rviz_connect_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS camera_rviz_connect_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/camera_rviz_connect)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/camera_rviz_connect
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
if(TARGET sensor_msgs_generate_messages_cpp)
  add_dependencies(camera_rviz_connect_generate_messages_cpp sensor_msgs_generate_messages_cpp)
endif()
if(TARGET std_msgs_generate_messages_cpp)
  add_dependencies(camera_rviz_connect_generate_messages_cpp std_msgs_generate_messages_cpp)
endif()

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/camera_rviz_connect)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/camera_rviz_connect
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()
if(TARGET sensor_msgs_generate_messages_eus)
  add_dependencies(camera_rviz_connect_generate_messages_eus sensor_msgs_generate_messages_eus)
endif()
if(TARGET std_msgs_generate_messages_eus)
  add_dependencies(camera_rviz_connect_generate_messages_eus std_msgs_generate_messages_eus)
endif()

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/camera_rviz_connect)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/camera_rviz_connect
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
if(TARGET sensor_msgs_generate_messages_lisp)
  add_dependencies(camera_rviz_connect_generate_messages_lisp sensor_msgs_generate_messages_lisp)
endif()
if(TARGET std_msgs_generate_messages_lisp)
  add_dependencies(camera_rviz_connect_generate_messages_lisp std_msgs_generate_messages_lisp)
endif()

if(gennodejs_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/camera_rviz_connect)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/camera_rviz_connect
    DESTINATION ${gennodejs_INSTALL_DIR}
  )
endif()
if(TARGET sensor_msgs_generate_messages_nodejs)
  add_dependencies(camera_rviz_connect_generate_messages_nodejs sensor_msgs_generate_messages_nodejs)
endif()
if(TARGET std_msgs_generate_messages_nodejs)
  add_dependencies(camera_rviz_connect_generate_messages_nodejs std_msgs_generate_messages_nodejs)
endif()

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/camera_rviz_connect)
  install(CODE "execute_process(COMMAND \"/usr/bin/python3\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/camera_rviz_connect\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/camera_rviz_connect
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
if(TARGET sensor_msgs_generate_messages_py)
  add_dependencies(camera_rviz_connect_generate_messages_py sensor_msgs_generate_messages_py)
endif()
if(TARGET std_msgs_generate_messages_py)
  add_dependencies(camera_rviz_connect_generate_messages_py std_msgs_generate_messages_py)
endif()
