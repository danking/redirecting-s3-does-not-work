Trying to stand between boto3 and S3 does not work. Redirects
become errors. Certain kinds of redirects (301, 302, 307) trigger
S3 bucket wrong-region-redirect behavior which fails if the request
was not a Bucket-related request and also ignores the redirect
target. Other response codes just bubble up to the user.
