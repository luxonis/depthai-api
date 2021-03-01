# Set PIC
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# Statically compile vcruntime library
add_compile_options(/MT)
