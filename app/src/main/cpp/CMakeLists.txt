cmake_minimum_required(VERSION 3.18.1)

project("aegis")

add_library(
        aegis
        SHARED
        aegis_native.cpp
)

find_library(
        log-lib
        log
)

target_link_libraries(
        aegis
        ${log-lib}
)
