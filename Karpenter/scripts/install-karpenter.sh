helm repo add karpenter https://charts.karpenter.sh
helm repo update

helm install karpenter karpenter/karpenter \
  --namespace karpenter --create-namespace \
  --set serviceAccount.annotations."eks\.amazonaws\.com/role-arn"=arn:aws:iam::<ACCOUNT_ID>:role/KarpenterControllerRole \
  --set settings.clusterName=my-cluster \
  --set settings.clusterEndpoint=<CLUSTER_ENDPOINT> \
  --set settings.aws.defaultInstanceProfile=KarpenterNodeInstanceProfile
