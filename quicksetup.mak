setup: 
	kubectl config use-context aws756
	kubectl create ns c756ns || true
	kubectl config set-context aws756 --namespace=c756ns
	istioctl install -y --set profile=demo --set hub=gcr.io/istio-release
	kubectl label namespace c756ns istio-injection=enabled || true
