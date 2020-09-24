#!/bin/bash
app_id="uam"
if [[ -f /data/src/official_saas/ ]];then
	template=$(ls /data/src/official_saas/uam* 2> /dev/null)
	[[ -n ${template} ]] && ls /data/src/official_saas/uam* | xargs rm -rf 
fi
if [[ -f /data/bkee/paas_agent/apps/projects/uam_saas/code/uam_saas/ ]];then
	rm -rf /data/bkee/paas_agent/apps/projects/uam_saas/code/uam_saas/*
fi
CONTAINER_ID=$(docker ps | grep uam | cut -d" " -f1 2> /dev/null)
if [[ -n ${CONTAINER_ID} ]];then
	docker exec -it ${CONTAINER_ID} /bin/bash && python -m compileall /data/app/code/home_application/ &> /dev/null
	if [[ $? -eq 0 ]];then
		cd /data/app/code/home_application/ && ls *.py | xargs rm -rf && exit
    fi
fi

