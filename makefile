#################### PACKAGE ACTIONS ###################
run_api: # make -j 2 run_api
	uvicorn api.fast:app
