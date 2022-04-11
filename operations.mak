NREPLICAS=4

scale_all: scale_s1 scale_s2 scale_s3 scale_db

scale_s1:
	kubectl scale deploy/cmpt756s1 --replicas=$(NREPLICAS)

scale_s2:
	kubectl scale deploy/cmpt756s2-v1 --replicas=$(NREPLICAS)

scale_s3:
	kubectl scale deploy/cmpt756s3-v1 --replicas=$(NREPLICAS)

scale_db:
	kubectl scale deploy/cmpt756db --replicas=$(NREPLICAS)


breaker_all: breaker_s1 breaker_s2 breaker_s3

breaker_s1:
	kubectl apply -f cluster/s1_breaker_5.yaml

breaker_s2:
	kubectl apply -f cluster/s2_breaker_5.yaml

breaker_s3:
	kubectl apply -f cluster/s3_breaker_5.yaml
