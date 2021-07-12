# Simple test
execute_process(
    COMMAND "/usr/bin/git"  clone --no-checkout "https://github.com/Maratyszcza/psimd.git" "psimd-source"
    WORKING_DIRECTORY ${CMAKE_CURRENT_LIST_DIR}
    RESULT_VARIABLE error_code
)

execute_process(
  COMMAND "/usr/bin/git"  checkout origin/master --
  WORKING_DIRECTORY ${CMAKE_CURRENT_LIST_DIR}/psimd-source
  RESULT_VARIABLE error_code
)

execute_process(
    COMMAND "/usr/bin/git"  submodule update --recursive --init
  WORKING_DIRECTORY ${CMAKE_CURRENT_LIST_DIR}/psimd-source
    RESULT_VARIABLE error_code
    )

execute_process(COMMAND ls ${CMAKE_CURRENT_LIST_DIR}/psimd-source)


# Builds library at 'build/' and prepares sphinx configuration at 'build/docs/conf.py'
set(project_root "${CMAKE_CURRENT_LIST_DIR}/..")

# Get buildCommitHash for non release build
execute_process(COMMAND "git" "rev-parse" "HEAD" WORKING_DIRECTORY ${project_root} OUTPUT_VARIABLE buildCommitHash OUTPUT_STRIP_TRAILING_WHITESPACE)

# Configure
execute_process(COMMAND ${CMAKE_COMMAND}
    -D DEPTHAI_PYTHON_COMMIT_HASH:STRING=${buildCommitHash}
    -D DEPTHAI_PYTHON_BUILD_DOCS:BOOL=YES
    -D DEPTHAI_BUILD_DOCS:BOOL=YES
    -D DEPTHAI_PYTHON_BUILD_DOCSTRINGS:BOOL=YES
    -D DEPTHAI_PYTHON_FORCE_DOCSTRINGS:BOOL=YES
    -S . -B build
    WORKING_DIRECTORY ${project_root} COMMAND_ECHO STDOUT
)

# Build
execute_process(COMMAND ${CMAKE_COMMAND} --build build --parallel 4 WORKING_DIRECTORY ${project_root} COMMAND_ECHO STDOUT)