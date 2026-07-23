resource "aws_s3_bucket" "conversation_store" {
  bucket = "acme-copilot-conversations"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "conversation_store" {
  bucket = aws_s3_bucket.conversation_store.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "aws:kms"
    }
  }
}
