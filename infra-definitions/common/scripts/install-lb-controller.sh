# Create IAM policy
#curl -o iam-policy.json https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/main/docs/install/iam_policy.json

aws iam create-policy \
    --policy-name AWSLoadBalancerControllerIAMPolicy \
    --policy-document file://iam-policy.json

# Create IAM service account
eksctl create iamserviceaccount \
  --cluster stress-app-cluster \
  --namespace kube-system \
  --name aws-load-balancer-controller-9 \
  --attach-policy-arn arn:aws:iam::533267453751:policy/AWSLoadBalancerControllerIAMPolicy \
  --approve

# Install Helm chart
helm repo add eks https://aws.github.io/eks-charts
helm repo update

helm upgrade -i aws-load-balancer-controller eks/aws-load-balancer-controller \
  -n kube-system \
  --set clusterName=stress-app-cluster \
  --set serviceAccount.create=false \
  --set serviceAccount.name=aws-load-balancer-controller-9 \
  --set region=us-east-1 \
  --set vpcId=vpc-01514225692262158