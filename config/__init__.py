class Config:
    DNS_USER_ID = "SERVICE_ACCOUNT_NAME@YOUR_PROJECT.iam.gserviceaccount.com" # The GCP Service Account ID
    DNS_KEY = "config/google.json" 		# The path to the JSON-key file (relative to the project's root)
    DNS_PROJECT_NAME = "YOUR_PROJECT" 	# Your Google Cloud Platform project name

# Example settings for creating an test.mydomain.com A record that points to your current IP
    A_RECORD_TTL_SECONDS = 3600 	# The desired TTL for your DNS record
    A_RECORD_NAME = "test" 		# The record name
    A_RECORD_ZONE_NAME = "mydomain.com." # The domain zone name (usually the domain with an ending `.`)
