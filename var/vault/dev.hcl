#
# Hashicorp Vault configuration to demonstrate the use a configuration class

ui = true
cluster_addr = "http://127.0.0.1:8201"
api_addr = "http://127.0.0.1:8200"
cluster_name = "mrmat-hello-python"

storage "file" {
  path = "/tmp/vault/data"
}
