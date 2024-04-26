# Configure the MongoDB Atlas Provider 
provider "mongodbatlas" {
  public_key = "xxx"
  private_key  = "xxx"
}


resource "mongodbatlas_project" "project" {
  name   = var.project_name
  org_id = var.mongodb_atlas_org_id
}


resource "mongodbatlas_cluster" "cluster" {
  project_id   = mongodbatlas_project.project.id
  name         = "stress-app"
  cluster_type = "REPLICASET"

  provider_name                = "TENANT"         # Required for M0/M2/M5
  backing_provider_name        = "AWS"
  provider_region_name         = "US_EAST_1"
  provider_instance_size_name  = "M0"             
  auto_scaling_disk_gb_enabled = true
}