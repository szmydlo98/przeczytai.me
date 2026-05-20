output "filename" {
  value = data.archive_file.package.output_path
}

output "output_base64sha256" {
  value = data.archive_file.package.output_base64sha256
}
