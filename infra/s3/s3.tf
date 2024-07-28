provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "bucket" {
  bucket = "arquivosgeraispaulo"
  tags = {
    Name = "arquivosgeraispaulo"
    Environment = "Production"
  }
}

resource "aws_s3_bucket_versioning" "bucket_versioning" {
  depends_on = [aws_s3_bucket.bucket]
  bucket = aws_s3_bucket.bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

#Object Lock works only in buckets that have S3 Versioning enabled. When you lock an object version, Amazon S3 stores the lock information in the metadata for that object version. Placing a retention period or a 
#legal hold on an object protects only the version that's specified in the request. Retention periods and legal holds don't prevent new versions of the object from being created, or delete markers to be added on top of the object. 
#For information about S3 Versioning, see Using versioning in S3 buckets.

resource "aws_s3_bucket_object_lock_configuration" "bucket_object_lock" {
  depends_on = [aws_s3_bucket_versioning.bucket_versioning]
  bucket = aws_s3_bucket.bucket.id
 #rule {
 #  default_retention {
 #    mode = "COMPLIANCE"
 #    days = 1
 #  }
 #}
}

resource "aws_s3_bucket_public_access_block" "arquivosgeraispaulo" {
  depends_on = [aws_s3_bucket.bucket]
  bucket = aws_s3_bucket.bucket.id
  block_public_acls   = true
  block_public_policy = true
  ignore_public_acls  = true
  restrict_public_buckets = true
}
