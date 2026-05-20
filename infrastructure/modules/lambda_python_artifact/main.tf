locals {
  app_files = sort(fileset("${var.backend_path}/app", "**"))
}

resource "null_resource" "package" {
  triggers = {
    app_hash       = sha256(join("", [for file in local.app_files : filesha256("${var.backend_path}/app/${file}")]))
    pyproject_hash = filesha256("${var.backend_path}/pyproject.toml")
  }

  provisioner "local-exec" {
    interpreter = ["/bin/bash", "-c"]
    command     = <<-EOT
      rm -rf '${var.build_dir}'
      mkdir -p '${var.build_dir}'
      python3 -m pip install '${var.backend_path}' -t '${var.build_dir}'
      cp -R '${var.backend_path}/app' '${var.build_dir}/app'
    EOT
  }
}

data "archive_file" "package" {
  type        = "zip"
  source_dir  = var.build_dir
  output_path = var.output_path

  depends_on = [null_resource.package]
}
