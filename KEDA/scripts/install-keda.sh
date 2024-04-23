# helm installation scripts 

helm repo add kedacore https://kedacore.github.io/charts
helm repo update

kubectl create namespace keda
helm install keda kedacore/keda --namespace keda --version 2.17.1