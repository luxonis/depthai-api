# Builds library at 'build/' and prepares sphinx configuration at 'build/docs/conf.py'
set(project_root "${CMAKE_CURRENT_LIST_DIR}/..")

# Get buildCommitHash for non release build
execute_process(COMMAND "git" "rev-parse" "HEAD" WORKING_DIRECTORY ${project_root} OUTPUT_VARIABLE buildCommitHash OUTPUT_STRIP_TRAILING_WHITESPACE)

execute_process(COMMAND ${CMAKE_COMMAND} -D DEPTHAI_PYTHON_COMMIT_HASH:STRING=${buildCommitHash} -D DEPTHAI_PYTHON_BUILD_DOCS:BOOL=YES -D DEPTHAI_BUILD_DOCS:BOOL=YES -S . -B build WORKING_DIRECTORY ${project_root} COMMAND_ECHO STDOUT)
execute_process(COMMAND ${CMAKE_COMMAND} --build build --parallel 8 WORKING_DIRECTORY ${project_root} COMMAND_ECHO STDOUT)