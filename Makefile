all:
	docker build . -t tarasglek/roku-client
	docker push tarasglek/roku-client
	kubectl delete -f roku-client.yaml --force  --grace-period=0;  kubectl create -f roku-client.yaml 