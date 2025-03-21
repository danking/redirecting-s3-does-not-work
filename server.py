from flask import Flask, request, redirect
from urllib.parse import quote

app = Flask(__name__)

# Configure this dictionary to map from the user-provided bucket name
# to the *actual* bucket name you want to redirect to on S3.
BUCKET_MAP = {
    "test-bucket-alias": "your-real-s3-bucket-name",
}


@app.route("/", methods=["GET", "HEAD", "PUT", "POST", "DELETE"])
def wtf_flask():
    return foo("")


@app.route("/<path:s3_path>", methods=["GET", "HEAD", "PUT", "POST", "DELETE"])
def s3_redirect(s3_path):
    return foo(s3_path)

def foo(s3_path):
    headers = request.headers

    # Option 1: Log headers to the console (or any preferred logging system)
    for header, value in headers.items():
        print(f"{header}: {value}")

    # Split the first path segment as the bucket name, and the rest as the object key.
    parts = s3_path.split("/", 1)
    if len(parts) == 1:
        if parts[0] == '':
            print('redirecting to "https://s3.amazonaws.com/"')
            return redirect("https://s3.amazonaws.com/", code=303)
        # If there's no slash, we treat the entire string as the bucket name,
        # and assume an empty key
        user_bucket = parts[0]
        object_key = ""
    else:
        user_bucket, object_key = parts[0], parts[1]

    # Determine the real bucket name from the BUCKET_MAP (default to the same if not found)
    real_bucket = BUCKET_MAP.get(user_bucket, user_bucket)
    print(real_bucket)

    # Construct the redirect URL.
    # We URL-encode the object_key in case it has special characters, then
    # tack on any existing query string from the user.
    base_url = f"https://{real_bucket}.s3.amazonaws.com"
    encoded_key = quote(object_key, safe="/")
    query = request.query_string.decode("utf-8")
    if query:
        redirect_url = f"{base_url}/{encoded_key}?{query}"
    else:
        redirect_url = f"{base_url}/{encoded_key}"

    # Return a 307 (Temporary Redirect) so that the client preserves its HTTP method
    # on the next request.
    print(f'redirecting to {redirect_url}')
    return redirect(redirect_url, code=307)


if __name__ == "__main__":
    # Run on localhost for testing
    app.run(host="127.0.0.1", port=5001, debug=True)
